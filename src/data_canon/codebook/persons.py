"""Codebook enumerations for person table."""

from data_canon.core.labeled_enum import LabeledEnum
from enum import StrEnum


class AgeCategory(StrEnum):
    """age value labels."""

    canonical_field_name = "age"

    AGE_UNDER_5 = "Under 5 years old"
    AGE_5_TO_15 = "5-15 years"
    AGE_16_TO_17 = "16-17 years"
    AGE_18_TO_24 = "18-24 years"
    AGE_25_TO_34 = "25-34 years"
    AGE_35_TO_44 = "35-44 years"
    AGE_45_TO_54 = "45-54 years"
    AGE_55_TO_64 = "55-64 years"
    AGE_65_TO_74 = "65-74 years"
    AGE_75_TO_84 = "75-84 years"
    AGE_85_AND_UP = "85 years or older"


class Education(StrEnum):
    """education value labels."""

    canonical_field_name = "education"

    LESS_HIGH_SCHOOL = "Less than high school"
    HIGHSCHOOL = "High school graduate"
    SOME_COLLEGE = "Some college"
    VOCATIONAL = "Vocational/technical training"
    ASSOCIATE = "Associates degree"
    BACHELORS = "Bachelor degree"
    GRAD = "Graduate/post-graduate degree"
    MISSING = "Missing: Skip Logic"
    PNTA = "Prefer not to answer"


class Employment(StrEnum):
    """employment value labels."""

    canonical_field_name = "employment"

    EMPLOYED_FULLTIME = "Employed full time (35+ hours/week, paid)"
    EMPLOYED_PARTTIME = "Employed part time (fewer than 35 hours/week, paid)"
    EMPLOYED_SELF = "Self-employed"
    UNEMPLOYED_NOT_LOOKING = "Not employed and not looking for work (e.g., retired, stay-at-home parent, student)"
    UNEMPLOYED_LOOKING = "Unemployed and looking for work"
    EMPLOYED_UNPAID = "Unpaid volunteer or intern"
    # NOTE This should include some number of hours per week
    EMPLOYED_FURLOUGHED = "Employed but not currently working (e.g., on leave, furloughed 100%)"
    MISSING = "Missing: Skip Logic"
    # NOTE: This should be broken out into multiple categories if possible
    # UNEMPLOYED_PARENT = (6, "Not employed and not looking, full-time parent")
    # UNEMPLOYED_STUDENT = (7, "Not employed and not looking, enrolled as full-time student")  # noqa: E501
    # UNEMPLOYED_RETIRED = (8, "Not employed and not working, retired")


class Ethnicity(LabeledEnum):
    """ethnicity value labels."""

    canonical_field_name = "ethnicity"

    NOT_HISPANIC = (1, "Not Hispanic or Latino")
    MEXICAN = (2, "Mexican, Mexican American, Chicano")
    PUERTO_RICAN = (3, "Puerto Rican")
    CUBAN = (4, "Cuban")
    OTHER = (5, "Other Hispanic or Latino")
    MISSING = (995, "Missing Response")
    PNTA = (999, "Prefer not to answer")


class Gender(LabeledEnum):
    """gender value labels."""

    canonical_field_name = "gender"

    FEMALE = (1, "Female")
    MALE = (2, "Male")
    NON_BINARY = (4, "Non-binary")
    MISSING = (995, "Missing Response")
    OTHER = (997, "Other/prefer to self-describe")
    PNTA = (999, "Prefer not to answer")


class Industry(LabeledEnum):
    """industry value labels."""

    canonical_field_name = "industry"

    AGRICULTURE = (1, "Agriculture, Forestry, Fishing, and Hunting")
    MINING = (2, "Mining, Quarrying, and Oil and Gas Extraction")
    UTILITIES = (3, "Utilities")
    CONSTRUCTION = (4, "Construction")
    MANUFACTURING = (5, "Manufacturing")
    WHOLESALE_TRADE = (6, "Wholesale Trade")
    RETAIL_TRADE = (7, "Retail Trade")
    TRANSPORTATION = (8, "Transportation and Warehousing")
    INFORMATION = (9, "Information")
    FINANCE_AND_INSURANCE = (10, "Finance and Insurance")
    REALESTATE = (11, "Real Estate and Rental and Leasing")
    PROFESSIONAL = (12, "Professional, Scientific, and Technical Services")
    MANAGEMENT = (13, "Management of Companies and Enteprises")
    ADMINISTRATIVE = (
        14,
        "Administrative and Support and Waste Management and Remediation Services",
    )
    EDUCATIONAL = (15, "Educational Services")
    HEALTH_AND_SOCIAL = (16, "Health Care and Social Assistance")
    ARTS_AND_RECREATION = (17, "Arts, Entertainment, and Recreation")
    ACCOMMODATION = (18, "Accommodation and Food Services")
    OTHER = (19, "Other Services (except Public Administration)")
    PUBLIC_ADMINISTRATION = (20, "Public Administration")
    MISSING = (995, "Missing Response")
    OTHER_SPECIFY = (997, "Other, please specify")


class JobType(LabeledEnum):
    """job_type value labels."""

    canonical_field_name = "job_type"

    # NONWORKER = (0, "Non-worker")
    FIXED = (1, "Go to one work location ONLY (outside of home)")
    VARIES = (2, "Work location regularly varies (different offices/jobsites)")
    WFH = (3, "Work ONLY from home or remotely (telework, self-employed)")
    DELIVERY = (4, "Drive/bike/travel for work (driver, sales, deliveries)")
    HYBRID = (
        5,
        "Work remotely some days and travel to a work location some days",
    )
    MISSING = (995, "Missing Response")


class Occupation(LabeledEnum):
    """occupation value labels."""

    canonical_field_name = "occupation"

    MANAGEMENT = (1, "Management")
    BUSINESS_FINANCE = (2, "Business and Financial Operations")
    COMPUTER_MATH = (3, "Computer and Mathematical")
    ARCH_ENG = (4, "Architecture and Engineering")
    SCIENCE = (5, "Life, Physical, and Social Science")
    COMMUNITY_SOCIAL = (6, "Community and Social Service")
    LEGAL = (7, "Legal")
    EDUCATION = (8, "Educational Instruction and Library")
    ARTS_MEDIA = (9, "Arts, Design, Entertainment, Sports, and Media")
    HEALTHCARE_PROFESSIONAL = (10, "Healthcare Practitioners and Technical")
    HEALTHCARE_SUPPORT = (11, "Healthcare Support")
    PROTECTIVE = (12, "Protective Service")
    FOOD_SERVICE = (13, "Food Preparation and Serving Related")
    CLEANING_MAINTENANCE = (14, "Building and Grounds Cleaning and Maintenance")
    PERSONAL_CARE = (15, "Personal Care and Service")
    SALES = (16, "Sales and Related")
    OFFICE_ADMIN = (17, "Office and Administrative Support")
    FARMING_FISHING = (18, "Farming, Fishing, and Forestry")
    CONSTRUCTION = (19, "Construction and Extraction")
    INSTALLATION_REPAIR = (20, "Installation, Maintenance, and Repair")
    PRODUCTION = (21, "Production")
    TRANSPORTATION = (22, "Transportation and Material Moving")
    MILITARY = (23, "Military Specific")
    MISSING = (995, "Missing Response")
    OTHER_PLEASE_SPECIFY = (997, "Other, please specify")


class Race(LabeledEnum):
    """race value labels."""

    canonical_field_name = "race"
    field_description = "Grouped race for the respondent"

    AFAM = (1, "African American or Black")
    NATIVE = (2, "American Indian or Alaska Native")
    ASIAN = (3, "Asian")
    PACIFIC = (4, "Native Hawaiian or Other Pacific Islander")
    WHITE = (5, "White")
    OTHER = (6, "Some other race")
    MULTI = (7, "Multiple races")
    MISSING = (995, "Missing Response")
    PNTA = (999, "Prefer not to answer")


class Relationship(LabeledEnum):
    """relationship value labels."""

    canonical_field_name = "relationship"
    field_description = "Indicates the relationship of the person to the primary respondent"

    SELF = (0, "Self")
    SPOUSE_PARTNER = (1, "Spouse, partner")
    CHILD = (2, "Child or child-in-law")
    PARENT = (3, "Parent or parent-in-law")
    SIBLING = (4, "Sibling or sibling-in-law")
    OTHER_RELATIVE = (5, "Other relative (grandchild, cousin)")
    NONRELATIVE = (6, "Nonrelative (friend, roommate, household help)")


class RemoteClassFreq(LabeledEnum):
    """remote_class_freq value labels."""

    canonical_field_name = "remote_class_freq"

    REMOTESCHOOL_6_7_DAYS = (1, "6-7 days a week")
    REMOTESCHOOL_5_DAYS = (2, "5 days a week")
    REMOTESCHOOL_4_DAYS = (3, "4 days a week")
    REMOTESCHOOL_3_DAYS = (4, "3 days a week")
    REMOTESCHOOL_2_DAYS = (5, "2 days a week")
    REMOTESCHOOL_1_DAY = (6, "1 day a week")
    REMOTESCHOOL_1_3_PER_MONTH = (7, "1-3 days a month")
    LESS_THAN_MONTHLY = (8, "Less than monthly")
    MISSING = (995, "Missing Response")
    NEVER = (996, "Never")


class SchoolFreq(LabeledEnum):
    """school_freq value labels."""

    canonical_field_name = "school_freq"

    SCHOOL_6_7_DAYS = (1, "6-7 days a week")
    SCHOOL_5_DAYS = (2, "5 days a week")
    SCHOOL_4_DAYS = (3, "4 days a week")
    SCHOOL_3_DAYS = (4, "3 days a week")
    SCHOOL_2_DAYS = (5, "2 days a week")
    SCHOOL_1_DAY = (6, "1 day a week")
    SCHOOL_1_3_PER_MONTH = (7, "1-3 days a month")
    LESS_THAN_MONTHLY = (8, "Less than monthly")
    MISSING = (995, "Missing Response")
    NEVER = (996, "Never")


class SchoolType(StrEnum):
    """school_type value labels."""

    canonical_field_name = "school_type"

    ATHOME = "Cared for at home"
    DAYCARE = "Daycare"
    PRESCHOOL = "Preschool"
    HOME_SCHOOL = "Home school"
    ELEMENTARY = "Elementary school (public, private, charter)"
    MIDDLE_SCHOOL = "Middle school (public, private, charter)"
    HIGH_SCHOOL = "High school (public, private, charter)"
    VOCATIONAL = "Vocational/technical school"
    COLLEGE_2YEAR = "2-year college"
    COLLEGE_4YEAR = "4-year college"
    GRADUATE_SCHOOL = "Graduate or professional school"
    MISSING = "Missing: Skip Logic"
    PNTA = "Prefer not to answer"
    OTHER = "Other"


class Student(StrEnum):
    """student value labels."""

    canonical_field_name = "student"

    FULLTIME_INPERSON = "Full-time student, currently attending some or all classes in-person"
    PARTTIME_INPERSON = "Part-time student, currently attending some or all classes in-person"
    NONSTUDENT = "No, not a student"
    PARTTIME_ONLINE = "Part-time student, ONLY online classes"
    FULLTIME_ONLINE = "Full-time student, ONLY online classes"
    MISSING = "Missing Response"


class CommuteFreq(LabeledEnum):
    """commute and telework frequency value labels."""

    DAYS_6_7 = (1, "6-7 days a week")
    DAYS_5 = (2, "5 days a week")
    DAYS_4 = (3, "4 days a week")
    DAYS_3 = (4, "3 days a week")
    DAYS_2 = (5, "2 days a week")
    DAY_1 = (6, "1 day a week")
    DAYS_1_3_PER_MONTH = (7, "1-3 days a month")
    LESS_THAN_MONTHLY = (8, "Less than monthly")
    MISSING = (995, "Missing Response")
    NEVER = (996, "Never")


class Vehicle(LabeledEnum):
    """vehicle value labels."""

    canonical_field_name = "vehicle"
    field_description = "Indicates the vehicle the person primarily drives"

    HOUSEHOLD_VEHICLE_1 = (6, "Household vehicle 1")
    HOUSEHOLD_VEHICLE_2 = (7, "Household vehicle 2")
    HOUSEHOLD_VEHICLE_3 = (8, "Household vehicle 3")
    HOUSEHOLD_VEHICLE_4 = (9, "Household vehicle 4")
    HOUSEHOLD_VEHICLE_5 = (10, "Household vehicle 5")
    HOUSEHOLD_VEHICLE_6 = (11, "Household vehicle 6")
    HOUSEHOLD_VEHICLE_7 = (12, "Household vehicle 7")
    CARSHARE = (18, "A carshare vehicle (e.g., ZipCar)")
    MISSING = (995, "Missing Response")
    NONE = (996, "None (I do not drive a vehicle)")
    OTHER_VEHICLE = (997, "Other vehicle")


class PersonType(LabeledEnum):
    """Derived person type from employment status, student status, and age."""

    canonical_field_name = "person_type"
    field_description = "Person type derived from employment, student status, and age"

    FULL_TIME_WORKER = (1, "Full-time worker")
    PART_TIME_WORKER = (2, "Part-time worker")
    RETIRED = (3, "Non-working adult 65+")
    NON_WORKER = (4, "Non-working adult < 65")
    UNIVERSITY_STUDENT = (5, "University student")
    CHILD_DRIVING_AGE = (6, "High school student 16+")
    CHILD_NON_DRIVING_AGE = (7, "Child 5-15")
    CHILD_UNDER_5 = (8, "Child 0-4")


class WorkParking(LabeledEnum):
    """work_park value labels."""

    canonical_field_name = "work_park"

    FREE = (1, "Parking is always free at/near work, at park & ride, etc.")
    EMPLOYER_PAYS_ALL = (2, "Employer pays ALL parking costs (for me)")
    EMPLOYER_DISCOUNT = (3, "Employer offers discounted parking (I pay some)")
    PERSONAL_PAY = (
        4,
        "I personally pay some or all parking costs (employer pays none)",
    )
    MISSING = (995, "Missing Response")
    NOT_APPLICABLE = (996, "Not applicable (I never drive to work)")
    DONT_KNOW = (998, "Don't know")
