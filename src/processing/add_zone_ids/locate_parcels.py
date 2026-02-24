"""Add zone IDs to households, persons, and linked trips based on geographic locations."""

import logging

import geopandas as gpd
import polars as pl

from pipeline.decoration import step

logger = logging.getLogger(__name__)


# Helper function to add zone ID to a dataframe based on lon/lat
def add_parcel_to_dataframe(
    df: pl.DataFrame,
    parcel_gdf: gpd.GeoDataFrame,
    df_index: str,
    lon_col: str,
    lat_col: str,
    parcel_col_name: str,
    parcel_id_field: str,
    crs: str
) -> pl.DataFrame:
    """Add zone ID to dataframe based on lon/lat coordinates."""
    # Convert to GeoDataFrame
    # Keep just index to avoid corrupting original polars DataFrame with pandas nonsense
    gdf = gpd.GeoDataFrame(
        index=df[df_index].to_list(),
        geometry=gpd.points_from_xy(df[lon_col].to_list(), df[lat_col].to_list()),
        crs="EPSG:4326",
    )
    gdf.index.name = df_index
    gdf = gdf.to_crs(crs) 

    # Prepare parcel gdf for spatial join and ensure zone ID is string to handle nulls in pandas land
    parcel_prepared = parcel_gdf.loc[:, [parcel_id_field, "geometry"]].copy()
    parcel_prepared[parcel_id_field] = parcel_prepared[parcel_id_field].astype(str)
    parcel_prepared = parcel_prepared.set_index(parcel_id_field)

    # Spatial join to find zone containing each point
    gdf_joined = gpd.sjoin_nearest(gdf, parcel_prepared, how="left")
    gdf_joined = gdf_joined.rename(columns={parcel_id_field: parcel_col_name})
    gdf_joined = gdf_joined.drop(columns="geometry")

    # If all zone IDs are integers, convert to Int64 to allow nulls
    # else keep as string
    casttype = pl.Utf8
    if gdf_joined[parcel_col_name].dropna().apply(lambda x: x.isdigit()).all():
        casttype = pl.Int64

    # Join back to original polars DataFrame on index
    df_joined = df.join(
        pl.from_pandas(gdf_joined.reset_index()),
        on=df_index,
        how="left",
    ).with_columns(pl.col(parcel_col_name).cast(casttype))

    return df_joined


@step()
def locate_parcels(
    parcel_geography: str,
    parcel_to_zones: list[dict],
    parcel_id: str,
    x_coord: str,
    y_coord: str,
    crs: str,
    households: pl.DataFrame | None = None,
    persons: pl.DataFrame | None = None,
    unlinked_trips: pl.DataFrame | None = None,
    linked_trips: pl.DataFrame | None = None,
    tours: pl.DataFrame | None = None,
    joint_trips: pl.DataFrame | None = None,
) -> dict:
    """Add parcel IDs and multiple geographic levels based on locations.

    Automatically applies each zone geography to standard locations:
    - households: home_lon/lat → home_{zone_name}
    - persons: work_lon/lat → work_{zone_name},
                school_lon/lat → school_{zone_name}
    - linked_trips: o_lon/lat → o_{zone_name}, d_lon/lat → d_{zone_name}

    Args:
        households: Households dataframe
        persons: Persons dataframe
        unlinked_trips: Unlinked trips dataframe
        linked_trips: Linked trips dataframe
        tours: Tours dataframe
        joint_trips: Joint trips dataframe
        parcel_geography: Path to file with parcel centroids (str)
        parcel_to_zones: List of dicts, each containing:
            - zone_name: Short name for zone type (e.g., 'taz', 'maz', 'county')
            - lookup_file: Path to file mapping parcel IDs to zone IDs (str)
            - match_parcel_id: Parcel ID field in lookup file to match parcel (str)
            - zone_id_field: Zone ID field in lookup file (str)
        parcel_id: Parcel ID field in parcel_geography file (str),
        x_coord: x coordinate field in parcel_geography file (str),
        y_coord: y coordinate field in parcel_geography file (str),
        crs: Coordinate reference system for parcel geometry (str),

    Returns:
        Dictionary with updated dataframes
    """
    # Initialize results dictionary in outer scope to update in loop, allow accumulation of zone IDs
    results = {
        "households": households,
        "persons": persons,
        "unlinked_trips": unlinked_trips,
        "linked_trips": linked_trips,
        "tours": tours,
        "joint_trips": joint_trips,
    }

    # Load parcel data
    parcel_df = pl.read_csv(parcel_geography, separator=" ").select([parcel_id, x_coord, y_coord])
    parcel_gdf = gpd.GeoDataFrame(
        parcel_df.to_pandas(),
        geometry=gpd.points_from_xy(parcel_df[x_coord].to_list(), parcel_df[y_coord].to_list()),
        crs=crs
    )

    # create zone lookup for parcels
    parcel_zone_lookup = parcel_df.select([parcel_id])

    for zone_config in parcel_to_zones:
        zone_name = zone_config["zone_name"]
        lookup_path = zone_config["lookup_file"]
        zone_id_field = zone_config["zone_id_field"]
        match_parcel_id = zone_config["match_parcel_id"]

        # Load the lookup file
        lookup = pl.read_csv(lookup_path).select([match_parcel_id, zone_id_field]).rename({match_parcel_id: parcel_id,
                                                                                           zone_id_field: zone_name})

        # Merge parcel_df with lookup to get zone IDs
        parcel_zone_lookup = parcel_zone_lookup.join(lookup, how="left", on=parcel_id)
    

    # Standard location mappings: (table, table_index, lon_col, lat_col, location_prefix)
    standard_locations = [
        ("households", "hh_id", "home_lon", "home_lat", "home"),
        ("persons", "person_id", "work_lon", "work_lat", "work"),
        ("persons", "person_id", "school_lon", "school_lat", "school"),
        ("unlinked_trips", "trip_id", "o_lon", "o_lat", "o"),
        ("unlinked_trips", "trip_id", "d_lon", "d_lat", "d"),
        ("linked_trips", "linked_trip_id", "o_lon", "o_lat", "o"),
        ("linked_trips", "linked_trip_id", "d_lon", "d_lat", "d"),
        ("tours", "tour_id", "o_lon", "o_lat", "o"),
        ("tours", "tour_id", "d_lon", "d_lat", "d"),
        ("joint_trips", "joint_trip_id", "o_lon_mean", "o_lat_mean", "o"),
        ("joint_trips", "joint_trip_id", "d_lon_mean", "d_lat_mean", "d"),
    ]
    # Apply this zone geography to all standard locations
    for table, idx, lon_col, lat_col, location_prefix in standard_locations:
        output_col = f"{location_prefix}_parcel"

        df = results.get(table)

        if df is None:
            # Make sure its not in results
            results.pop(table, None)
            continue  # Skip if no table specified

        logger.info(
            "Adding parcel IDs to %s location on table %s",
            location_prefix,
            table
        )

        if output_col in df.columns:
            logger.warning(
                "Column %s already exists in %s; replacing it.",
                output_col,
                table,
            )
            df = df.drop(output_col)

        df_result = add_parcel_to_dataframe(
            df,
            parcel_gdf,
            df_index=idx,
            lon_col=lon_col,
            lat_col=lat_col,
            parcel_col_name=output_col,
            parcel_id_field=parcel_id,
            crs=crs
        )

        # join wth parcel_zone_lookup to get zone IDs for this location
        all_zones = {zone: f"{location_prefix}_{zone}" for zone in parcel_zone_lookup.columns[1:]}
        results[table] = df_result.join(parcel_zone_lookup.rename(all_zones), how="left", left_on=output_col, right_on=parcel_id)

    return results
