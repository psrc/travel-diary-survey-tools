"""Custom cleaning steps for the DaySim pipeline."""

import logging

import polars as pl

from data_canon.codebook.households import ResidenceRentOwn, ResidenceType
from data_canon.codebook.days import TravelDow
from data_canon.models.survey import PersonDayModel
from pipeline.decoration import step
from utils.helpers import add_time_columns, expr_haversine

logger = logging.getLogger(__name__)


@step()
def clean_2023_psrc_hts(
    households: pl.DataFrame,
    persons: pl.DataFrame,
    days: pl.DataFrame,
    unlinked_trips: pl.DataFrame,
) -> dict[str, pl.DataFrame]:
    """Custom cleaning steps go here, not in the main pipeline."""
    # CLEANUP UNLINKED TRIPS =================================
    # Much wow...
    logger.info("Cleaning 2023 trip data")

    unlinked_trips = unlinked_trips.rename(
        {
        "depart_time_hour": "depart_hour",
        "depart_time_minute": "depart_minute",
        "depart_time_second": "depart_seconds",
        "arrival_time_hour": "arrive_hour",
        "arrival_time_minute": "arrive_minute",
        "arrival_time_second": "arrive_seconds",
        "dest_lng": "d_lon",
        "dest_lat": "d_lat",
        "origin_lng": "o_lon",
        "origin_lat": "o_lat",
        "dest_purpose_cat": "d_purpose_category",
        "mode_class": "mode_type"
        }
    )

    # Add time columns if missing
    unlinked_trips = add_time_columns(unlinked_trips)

    # "Correct" trips when depart_time > arrive_time, flip them
    # including the separate hours, minutes, seconds columns
    # Create a swap condition to reuse
    swap_condition = pl.col("depart_time") > pl.col("arrive_time")
    # Swap depart/arrive columns when depart_time > arrive_time
    swap_cols = [
        ("depart_time", "arrive_time"),
        ("depart_hour", "arrive_hour"),
        ("depart_minute", "arrive_minute"),
        ("depart_seconds", "arrive_seconds"),
    ]

    unlinked_trips = unlinked_trips.with_columns(
        [
            pl.when(swap_condition).then(pl.col(b)).otherwise(pl.col(a)).alias(a)
            for a, b in swap_cols
        ]
        + [
            pl.when(swap_condition).then(pl.col(a)).otherwise(pl.col(b)).alias(b)
            for a, b in swap_cols
        ]
    )

    # Replace any -1 value in *_purpose columns with missing code
    # unlinked_trips = unlinked_trips.with_columns(
    #     [
    #         pl.when(pl.col(col_name) == -1).then(996).otherwise(pl.col(col_name)).alias(col_name)
    #         for col_name in [
    #             "o_purpose",
    #             "d_purpose",
    #             "o_purpose_category",
    #             "d_purpose_category",
    #         ]
    #     ]
    # )

    # If distance is null, recalculate it from lat/lon
    unlinked_trips = unlinked_trips.with_columns(
        (
            expr_haversine(
                pl.col("o_lon"),
                pl.col("o_lat"),
                pl.col("d_lon"),
                pl.col("d_lat"),
            )
        )
        .alias("distance_meters")
    )

    # If duration_minutes is null, recalculate it from depart/arrive times
    unlinked_trips = unlinked_trips.with_columns(
        (
            (pl.col("arrive_time") - pl.col("depart_time")).dt.total_minutes()
        )
        .alias("duration_minutes")
    )

    # ADD DAYS FOR PERSONS WITHOUT DAYS =================================
    # Find persons without days
    persons_without_days = persons.filter(
        ~pl.col("person_id").is_in(days["person_id"].unique().implode())
    )

    # Get travel_dow from other household members' days
    days_for_dow = (
        days.select(["hh_id", "travel_dow"])
        .filter(pl.col("hh_id").is_in(persons_without_days["hh_id"].unique().implode()))
        .unique()
    )

    days_for_dow = days_for_dow.with_columns(
        pl.col("travel_dow").replace_strict({value: key for key, value in TravelDow.to_dict().items()}, default=None).alias("travel_dow_value")
    )

    # Create a default day for each person without days
    dummy_days = (
        persons_without_days.join(days_for_dow, on="hh_id", how="left")
        .with_columns(
            # Construct default day_id (person_id * 100 + travel_dow)
            (pl.col("person_id") * 100 + pl.col("travel_dow_value")).alias("day_id")
        )
        .select(PersonDayModel.model_json_schema().get("properties").keys())
    )
    # Add dummy days to days dataframe
    days = pl.concat([days, dummy_days], how="diagonal")

    # Move residence type and residence rent/own from persons to households
    # Extract household-level attributes from persons table
    # Only one person reports residence_rent_own and residence_type
    # hh_attributes = persons.group_by("hh_id").agg(
    #     pl.col("residence_rent_own")
    #     .filter(
    #         ~pl.col("residence_rent_own").is_in(
    #             [ResidenceRentOwn.MISSING.value, ResidenceRentOwn.PNTA.value]
    #         )
    #     )
    #     .mode()
    #     .first()
    #     .fill_null(995),
    #     pl.col("residence_type")
    #     .filter(pl.col("residence_type") != ResidenceType.MISSING.value)
    #     .mode()
    #     .first()
    #     .fill_null(995),
    # )
    # # Join to households
    # households = households.join(hh_attributes, on="hh_id", how="left")

    return {
        "households": households,
        "persons": persons,
        "unlinked_trips": unlinked_trips,
        "days": days,
    }
