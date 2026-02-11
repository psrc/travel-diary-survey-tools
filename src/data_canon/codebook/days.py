"""Codebook enumerations for day table."""

from enum import StrEnum


class TravelDow(StrEnum):
    """travel_dow value labels."""

    field_description = "Day of the week enumeration"

    MONDAY = "Monday"
    TUESDAY = "Tuesday"
    WEDNESDAY = "Wednesday"
    THURSDAY = "Thursday"
    FRIDAY = "Friday"
    SATURDAY = "Saturday"
    SUNDAY = "Sunday"