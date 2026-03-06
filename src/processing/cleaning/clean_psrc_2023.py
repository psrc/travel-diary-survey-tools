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
    linked_trips: pl.DataFrame,
) -> dict[str, pl.DataFrame]:
    """Custom cleaning steps go here, not in the main pipeline."""
    # CLEANUP UNLINKED TRIPS =================================
    # Much wow...
    logger.info("Cleaning 2023 trip data")

    households = households.rename(
        {
            "home_lng": "home_lon",
            "vehicle_count": "num_vehicles",
            "numworkers": "num_workers",
            "hhincome_detailed": "income_detailed",
            "hhincome_followup": "income_followup",
            "rent_own": "residence_rent_own",
            "res_type": "residence_type",
        }
    )

    persons = persons.rename(
        {
            "pernum": "person_num",
            "adult_student": "student",
            "schooltype": "school_type",
            "workplace": "job_type",
            "work_lng": "work_lon",
            "school_loc_lat": "school_lat",
            "school_loc_lng": "school_lon",
            "commute_subsidy_1": "transit_pass",
            "commute_subsidy_3": "work_park",
            # "person_weight": "psexpfac"
        }
    )

    days = days.rename(
        {
            "day_iscomplete": "is_complete",
        }
    )

    # change data types
    persons = persons.with_columns(
        [
            pl.col(col).cast(pl.Float32, strict=False).alias(col)
            for col in ["school_lat", "school_lon", "work_lat", "work_lon"]
        ]
    )

    # combine 5-15 years old
    persons = persons.with_columns(
        pl.when(pl.col("age").is_in(["5-11 years", "12-15 years"]))
        .then(pl.lit("5-15 years"))
        .otherwise(pl.col("age"))
        .alias("age")
    )

    # refactor part-time student
    persons = persons.with_columns(
        pl.when(pl.col("student")=="Part-time student")
        .then(pl.lit("Part-time student, currently attending some or all classes in-person"))
        .otherwise(pl.col("student"))
        .alias("student")
    )

    # rename variables in trip table
    linked_trips = linked_trips.rename(
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
            "origin_purpose": "o_purpose",
            "dest_purpose": "d_purpose",
            "origin_purpose_cat": "o_purpose_category",
            "dest_purpose_cat": "d_purpose_category",
            "mode_class": "mode_type",
            "mode_acc": "access_mode",
            "mode_egr": "egress_mode",
            "trip_id": "linked_trip_id"
        }
    )

    # number of travelers with int
    linked_trips = linked_trips.with_columns(
        pl.col("travelers_total").str
        .head(1)
        .cast(pl.Int64, strict=False)
        .alias("num_travelers")
    )

    # Add time columns if missing
    linked_trips = add_time_columns(linked_trips)

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

    linked_trips = linked_trips.with_columns(
        [
            pl.when(swap_condition).then(pl.col(b)).otherwise(pl.col(a)).alias(a)
            for a, b in swap_cols
        ]
        + [
            pl.when(swap_condition).then(pl.col(a)).otherwise(pl.col(b)).alias(b)
            for a, b in swap_cols
        ]
    )

    linked_trips = linked_trips.with_columns(
        
        pl.when(pl.col("access_mode") == "Drove and parked my own household's vehicle (or motorcycle)")
        .then(pl.lit("Drove and parked a car (e.g., a vehicle in my household)"))
        .when(pl.col("access_mode").is_in(["NA"]))
        .then(pl.lit("Missing: Skip Logic"))
        .otherwise(pl.col("access_mode")).alias("access_mode")
        
    )

    linked_trips = linked_trips.with_columns(
        [
            pl.when(pl.col(col) == "NA")
            .then(pl.lit("Missing Response"))
            .otherwise(pl.col(col)).alias(col)
            for col in ["o_purpose_category", "d_purpose_category", "o_purpose", "d_purpose"]

        ]
        
    )

    # If distance is null, recalculate it from lat/lon
    linked_trips = linked_trips.with_columns(
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
    linked_trips = linked_trips.with_columns(
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

    dow_dict = {
        "Monday": 1,
        "Tuesday": 2,
        "Wednesday": 3,
        "Thursday": 4,
        "Friday": 5,
        "Saturday": 6,
        "Sunday": 7
    }

    days_for_dow = days_for_dow.with_columns(
        pl.col("travel_dow").replace_strict(dow_dict, default=None).alias("travel_dow_value")
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


    return {
        "households": households,
        "persons": persons,
        "linked_trips": linked_trips,
        "days": days,
    }
