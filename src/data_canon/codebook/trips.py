"""Codebook enumerations for trip table."""

from typing import ClassVar

from data_canon.core.labeled_enum import LabeledEnum
from enum import StrEnum


class Purpose(StrEnum):
    """Base class for purpose value labels."""

    HOME = "Went home"

    PRIMARY_WORKPLACE = "Went to primary workplace"
    WORK_ACTIVITY = "Went to work-related activity (e.g., meeting, delivery, worksite)"
    OTHER_WORK = "Went to other work-related activity"
    VOLUNTEERING = "Volunteering"

    K12_SCHOOL = "Attend K-12 school"
    DAYCARE = "Attend daycare or preschool"
    SCHOOL = "Went to school/daycare (e.g., daycare, K-12, college)"
    COLLEGE = "Attend college/university"
    VOCATIONAL = "Attend vocational education class"
    OTHER_EDUCATION = "Attend other education-related activity (e.g., field trip)"
    OTHER_CLASS = "Attend other type of class (e.g., cooking class)"

    DROP_OFF = "Drop someone off"
    PICK_UP = "Pick someone up"
    PICK_UP_AND_DROP_OFF = "BOTH pick up AND drop off"
    ACCOMPANY = "Accompany someone only (e.g., go along for the ride)"
    ESCORT = "Dropped off, picked up, or accompanied another person"

    GROCERY = "Grocery shopping"
    OTHER_SHOPPING = "Other shopping (e.g., mall, pet store)"

    DINING = "Went to restaurant to eat/get take-out"

    EXERCISE = "Exercise or recreation (e.g., gym, jog, bike, walk dog)"
    SOCIAL = "Social event (e.g., visit friends, family, co-workers)"
    OTHER_SOCIAL = "Other social/leisure"
    FAMILY_ACTIVITY = "Went to a family activity (e.g., child's softball game)"
    TRAVEL = "Vacation/Traveling (rMove only)"
    RECREATION = "Recreational event (e.g., movies, sporting event)"
    RELIGIOUS_CIVIC = "Religious/civic/volunteer activity"

    MEDICAL = "Medical appointment (e.g., doctor, dentist)"
    SHOPPING_ERRANDS = "Appointment, shopping, or errands (e.g., gas)"
    OTHER_ERRAND = "Other appointment/errands"
    PERSONAL_BUSINESS = "Personal business (e.g., bank, post office)"
    GAS = "Got gas"

    MODE_CHANGE = "Changed or transferred mode (e.g., change from ferry to bus)"
    OTHER_RESIDENCE = "Went to another residence (e.g., someone else's home, second home)"
    TEMP_LODGING = "Went to temporary lodging (e.g., hotel, vacation rental)"
    OTHER = "Other reason"


class PurposeCategory(StrEnum):
    """d_purpose_category value labels."""

    HOME = "Home"
    WORK = "Work"
    WORK_RELATED = "Work-related"
    SCHOOL = "School"
    SCHOOL_RELATED = "School-related"
    ESCORT = "Escort"
    SHOP = "Shopping"
    MEAL = "Meal"
    SOCIALREC = "Social/Recreation"
    ERRAND = "Personal Business/Errand/Appointment"
    CHANGE_MODE = "Change mode"
    OVERNIGHT = "Overnight"
    OTHER = "Other"
    MISSING = "Missing Response"
    PNTA = "Prefer not to answer"
    NOT_IMPUTABLE = "Not imputable"


class PurposeToCategoryMap:
    """Mapping from detailed purpose codes to purpose categories."""

    PURPOSE_TO_CATEGORY: ClassVar[dict] = {
        Purpose.HOME: PurposeCategory.HOME,
        Purpose.PRIMARY_WORKPLACE: PurposeCategory.WORK,
        Purpose.WORK_ACTIVITY: PurposeCategory.WORK_RELATED,
        Purpose.OTHER_WORK: PurposeCategory.WORK_RELATED,
        Purpose.VOLUNTEERING: PurposeCategory.WORK_RELATED,
        Purpose.K12_SCHOOL: PurposeCategory.SCHOOL,
        Purpose.DAYCARE: PurposeCategory.SCHOOL,
        Purpose.SCHOOL: PurposeCategory.SCHOOL,
        Purpose.COLLEGE: PurposeCategory.SCHOOL,
        Purpose.VOCATIONAL: PurposeCategory.SCHOOL,
        Purpose.OTHER_EDUCATION: PurposeCategory.SCHOOL_RELATED,
        Purpose.OTHER_CLASS: PurposeCategory.SCHOOL_RELATED,
        Purpose.DROP_OFF: PurposeCategory.ESCORT,
        Purpose.PICK_UP: PurposeCategory.ESCORT,
        Purpose.PICK_UP_AND_DROP_OFF: PurposeCategory.ESCORT,
        Purpose.ACCOMPANY: PurposeCategory.ESCORT,
        Purpose.ESCORT: PurposeCategory.ESCORT,
        Purpose.GROCERY: PurposeCategory.SHOP,
        Purpose.OTHER_SHOPPING: PurposeCategory.SHOP,
        Purpose.DINING: PurposeCategory.MEAL,
        Purpose.EXERCISE: PurposeCategory.SOCIALREC,
        Purpose.SOCIAL: PurposeCategory.SOCIALREC,
        Purpose.OTHER_SOCIAL: PurposeCategory.SOCIALREC,
        Purpose.FAMILY_ACTIVITY: PurposeCategory.SOCIALREC,
        Purpose.TRAVEL: PurposeCategory.SOCIALREC,
        Purpose.RECREATION: PurposeCategory.SOCIALREC,
        Purpose.RELIGIOUS_CIVIC: PurposeCategory.SOCIALREC,
        Purpose.MEDICAL: PurposeCategory.ERRAND,
        Purpose.SHOPPING_ERRANDS: PurposeCategory.ERRAND,
        Purpose.OTHER_ERRAND: PurposeCategory.ERRAND,
        Purpose.PERSONAL_BUSINESS: PurposeCategory.ERRAND,
        Purpose.GAS: PurposeCategory.ERRAND,
        Purpose.MODE_CHANGE: PurposeCategory.CHANGE_MODE,
        Purpose.OTHER_RESIDENCE: PurposeCategory.OVERNIGHT,
        Purpose.TEMP_LODGING: PurposeCategory.OVERNIGHT,
        Purpose.OTHER: PurposeCategory.OTHER
    }

    @classmethod
    def get_category(cls, purpose: Purpose) -> PurposeCategory:
        """Get the category for a given purpose code."""
        return cls.PURPOSE_TO_CATEGORY.get(purpose, PurposeCategory.OTHER)

class Driver(StrEnum):
    """driver value labels."""

    DRIVER = "Driver"
    PASSENGER = "Passenger"
    BOTH = "Both (switched drivers during trip)"
    MISSING = "Missing: Skip Logic"


class Mode(StrEnum):
    """mode value labels."""

    WALK = "Walk (or jog/wheelchair)"
    HOUSEHOLD_VEHICLE_1 = "Household vehicle 1"
    HOUSEHOLD_VEHICLE_2 = "Household vehicle 2"
    HOUSEHOLD_VEHICLE_3 = "Household vehicle 3"
    HOUSEHOLD_VEHICLE_4 = "Household vehicle 4"
    HOUSEHOLD_VEHICLE_5 = "Household vehicle 5"
    HOUSEHOLD_VEHICLE_6 = "Household vehicle 6"
    HOUSEHOLD_VEHICLE_7 = "Household vehicle 7"
    HOUSEHOLD_VEHICLE_8 = "Household vehicle 8"
    HOUSEHOLD_VEHICLE_OTHER = "Other vehicle in household"
    OTHER_VEHICLE = "Other non-household vehicle"
    CAR_WORK = "Car from work"
    CAR_FRIEND = "Friend/colleague's car"
    CAR_RENTAL = "Rental car"
    CAR_SHARE = "Carshare service (e.g., Turo, Zipcar, Getaround, GIG)"
    VANPOOL = "Vanpool"
    SCHOOL_BUS = "School bus"
    BUS = "Bus (public transit)"
    BUS_PRIVATE = "Private bus or shuttle"
    BUS_OTHER = "Other bus (rMove only)"
    PARATRANSIT = "Paratransit"
    RAIL_URBAN = "Urban Rail (e.g., Link light rail, monorail, streetcar)"
    RAIL_COMMUTER = "Commuter rail (Sounder, Amtrak)"
    RAIL_OTHER = "Other rail"
    AIR = "Airplane or helicopter"
    TNC = "Other hired service (Uber, Lyft, or other smartphone-app car service)"
    TAXI = "Taxi (e.g., Yellow Cab)"
    TNC_OTHER = "Other hired car service (e.g., black car, limo)" 
    MOTORCYCLE_HOUSEHOLD = "Other motorcycle in household"
    MOTORCYCLE_OTHER = "Other motorcycle (not my household's)"  
    BIKE = "Standard bicycle (my household's)"
    BIKE_GENERAL = "Bicycle or e-bike (rSurvey only)"
    BIKE_ELECTRIC = "Electric bicycle (my household's)"
    BIKE_BORROWED = "Borrowed bicycle (e.g., a friend's)"
    BIKE_RENTED = "Other rented bicycle"
    BIKE_SHARE = "Bike-share - standard bicycle"
    BIKE_SHARE_ELECTRIC = "Bike-share - electric bicycle"
    SKATE = "Skateboard or rollerblade"
    SEGWAY = "Segway or Onewheel/electric unicycle"
    SCOOTER_MOPED = "Personal scooter or moped (not shared)"
    FERRY = "Ferry or water taxi"
    VEHICLE_FERRY = "Vehicle ferry (took vehicle on board)"
    OTHER_SCOOTER_MOPED = "Other scooter, moped, skateboard" 
    OTHER_LONG = "Other mode (e.g., skateboard, kayak, motorhome, etc.)" 
    MISSING = "Missing Response"

    # from work_mode
    MICROMOBILITY_WORK = "Scooter, moped, skateboard"
    OTHER = "Other"
    TNC_WORK = "Uber/Lyft, taxi, or car service"
    BUS_WORK = "Bus, shuttle, or vanpool (public transit, private service, or shuttles for older adults and people with disabilities)"
    RAIL_WORK = "Rail (e.g., train, subway)"
    HOUSEHOLD_VEHICLE_WORK = "Household vehicle (or motorcycle)"
    OTHER_VEHICLE_WORK = "Other vehicle (e.g., friend's car, rental, carshare, work car)"
    BIKE_WORK = "Bicycle or e-bicycle"
    

class ModeType(StrEnum):
    """mode_type value labels."""
    
    CAR = "Drive"
    TRANSIT = "Transit"
    FERRY = "Ferry"
    WALK = "Walk"
    BIKE = "Bike"
    TNC = "Ride Hail"
    SCHOOL_BUS = "School bus"
    LONG_DISTANCE = "Airplane or helicopter"
    OTHER = "Other"
    MISSING = "Missing Response"
    # not applicable, but included for mode hierarchy and mapping
    BIKESHARE = "Bike Share"
    SCOOTERSHARE = "Scooter Share"
    CARSHARE = "Carshare"
    TAXI = "Taxi"
    SHUTTLE = "Shuttle"

    @classmethod
    def from_mode(cls) -> dict["Mode", "ModeType"]:
        """Get mapping from detailed Mode to ModeType.

        Returns:
            Dictionary mapping Mode enum values to ModeType enum values
        """
        return {
            # Walk
            Mode.WALK: cls.WALK,
            # Drive
            Mode.HOUSEHOLD_VEHICLE_1: cls.CAR,
            Mode.HOUSEHOLD_VEHICLE_2: cls.CAR,
            Mode.HOUSEHOLD_VEHICLE_3: cls.CAR,
            Mode.HOUSEHOLD_VEHICLE_4: cls.CAR,
            Mode.HOUSEHOLD_VEHICLE_5: cls.CAR,
            Mode.HOUSEHOLD_VEHICLE_6: cls.CAR,
            Mode.HOUSEHOLD_VEHICLE_7: cls.CAR,
            Mode.HOUSEHOLD_VEHICLE_8: cls.CAR,
            Mode.HOUSEHOLD_VEHICLE_OTHER: cls.CAR,
            Mode.OTHER_VEHICLE: cls.CAR,
            Mode.CAR_WORK: cls.CAR,
            Mode.CAR_FRIEND: cls.CAR,
            Mode.CAR_RENTAL: cls.CAR,
            Mode.CAR_SHARE: cls.CAR,
            Mode.VANPOOL: cls.CAR,
            Mode.MOTORCYCLE_HOUSEHOLD: cls.CAR,
            Mode.MOTORCYCLE_OTHER: cls.CAR,
            Mode.HOUSEHOLD_VEHICLE_WORK: cls.CAR,
            Mode.OTHER_VEHICLE_WORK: cls.CAR,
            # School bus
            Mode.SCHOOL_BUS: cls.SCHOOL_BUS,
            # Transit
            Mode.BUS: cls.TRANSIT,
            Mode.RAIL_URBAN: cls.TRANSIT,
            Mode.RAIL_COMMUTER: cls.TRANSIT,
            Mode.RAIL_OTHER: cls.TRANSIT,
            Mode.BUS_WORK: cls.TRANSIT,
            Mode.RAIL_WORK: cls.TRANSIT,
            # Ferry
            Mode.FERRY: cls.FERRY,
            Mode.VEHICLE_FERRY: cls.FERRY,
            # Airplane or helicopter
            Mode.AIR: cls.LONG_DISTANCE,
            # TNC
            Mode.TNC: cls.TNC,
            Mode.TAXI: cls.TNC,
            Mode.TNC_OTHER: cls.TNC,
            Mode.TNC_WORK: cls.TNC,
            # Bike
            Mode.BIKE: cls.BIKE,
            Mode.BIKE_GENERAL:cls.BIKE,
            Mode.BIKE_ELECTRIC:cls.BIKE,
            Mode.BIKE_BORROWED: cls.BIKE,
            Mode.BIKE_RENTED: cls.BIKE,
            Mode.BIKE_SHARE: cls.BIKE,
            Mode.BIKE_SHARE_ELECTRIC: cls.BIKE,
            Mode.BIKE_WORK: cls.BIKE,
            # Micromobility
            Mode.SKATE: cls.OTHER,
            Mode.SEGWAY: cls.OTHER,
            Mode.SCOOTER_MOPED: cls.OTHER,
            Mode.MICROMOBILITY_WORK: cls.OTHER,
            # Other
            Mode.BUS_PRIVATE: cls.OTHER,
            Mode.BUS_OTHER: cls.OTHER,
            Mode.PARATRANSIT: cls.OTHER,
            Mode.OTHER_SCOOTER_MOPED: cls.OTHER,
            Mode.OTHER_LONG: cls.OTHER,
            Mode.OTHER: cls.OTHER,
            # Missing response
            Mode.MISSING: cls.MISSING
        }


class AccessEgressMode(StrEnum):
    """transit_access value labels."""

    # NOTE: Why is this not just inherited from Mode???

    WALK = "Walked or jogged"
    BICYCLE = "Bicycle or e-bicycle"
    TRANSFER_BUS = "Transferred from another bus, shuttle, or vanpool"
    MICROMOBILITY = "Scooter, moped, skateboard"
    TRANSFER_OTHER = "Transferred from other transit (e.g., ferry, air)"
    TNC = "Uber/Lyft, taxi, or car service"
    CAR_HOUSEHOLD = "Drove and parked a car (e.g., a vehicle in my household)"
    CAR_OTHER = "Drove and parked a carshare vehicle (e.g., ZipCar, Car2Go)"
    DROPOFF_HOUSEHOLD = "Got dropped off in my own household's vehicle (or motorcycle)"
    DROPOFF_OTHER = "Got dropped off in another vehicle (or motorcycle)"
    MISSING = "Missing: Skip Logic"
    OTHER = "Other"
