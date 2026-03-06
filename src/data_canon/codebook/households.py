"""Codebook enumerations for hh table."""

from data_canon.core.labeled_enum import LabeledEnum
from enum import StrEnum


class BicycleType(LabeledEnum):
    """bicycle_type value labels."""

    canonical_field_name = "bicycle_type"

    STANDARD = (1, "Standard")
    ELECTRIC = (2, "Electric")
    OTHER = (3, "Other")
    MISSING = (995, "Missing Response")


class HomeInRegion(LabeledEnum):
    """home_in_region value labels."""

    canonical_field_name = "home_in_region"

    NO = (0, "No")
    YES = (1, "Yes")


class IncomeDetailed(StrEnum):
    """income_detailed value labels."""

    canonical_field_name = "income_detailed"

    INCOME_UNDER10 = "Under $10,000"
    INCOME_10TO25 = "$10,000-$24,999"
    INCOME_25TO35 = "$25,000-$34,999"
    INCOME_35TO50 = "$35,000-$49,999"
    INCOME_50TO75 = "$50,000-$74,999"
    INCOME_75TO100 = "$75,000-$99,999"
    INCOME_100TO150 = "$100,000-$149,999"
    INCOME_150TO200 = "$150,000-$199,999"
    INCOME_200TO250 = "$200,000-$249,999"
    INCOME_250_OR_MORE = "$250,000 or more"
    PNTA = "Prefer not to answer"


class IncomeFollowup(StrEnum):
    """income_followup value labels."""

    canonical_field_name = "income_followup"

    INCOME_UNDER25 = "Under $25,000"
    INCOME_25TO50 = "$25,000-$49,999"
    INCOME_50TO75 = "$50,000-$74,999"
    INCOME_75TO100 = "$75,000-$99,999"
    INCOME_100TO200 = "$100,000-$199,999"
    INCOME_200_OR_MORE = "$200,000 or more"
    MISSING = "Missing: Skip Logic"
    PNTA = "Prefer not to answer"


class IncomeBroad(StrEnum):
    """income_broad value labels."""

    canonical_field_name = "income_broad"

    INCOME_UNDER25 = "Under $25,000"
    INCOME_25TO50 = "$25,000-$49,999"
    INCOME_50TO75 = "$50,000-$74,999"
    INCOME_75TO100 = "$75,000-$99,999"
    INCOME_100TO200 = "$100,000-$199,999"
    INCOME_200_OR_MORE = "$200,000 or more"
    PNTA = "Prefer not to answer"


class ParticipationGroup(LabeledEnum):
    """participation_group value labels."""

    canonical_field_name = "participation_group"
    field_description = "Indicates the survey mode used for signup and diary completion"

    SIGNUP_BMOVE_DIARY_BMOVE = (
        1,
        "Signup via browserMove, Diary via browserMove",
    )
    SIGNUP_BMOVE_DIARY_CALL_CENTER = (
        2,
        "Signup via browserMove, Diary via call center",
    )
    SIGNUP_BMOVE_DIARY_RMOVE = (3, "Signup via browserMove, Diary via rMove")
    SIGNUP_CALL_DIARY_BMOVE = (
        4,
        "Signup via call center, Diary via browserMove",
    )
    SIGNUP_CALL_DIARY_CALL_CENTER = (
        5,
        "Signup via call center, Diary via call center",
    )
    SIGNUP_CALL_DIARY_RMOVE = (6, "Signup via call center, Diary via rMove")
    SIGNUP_RMOVE_DIARY_BMOVE = (7, "Signup via rMove, Diary via browserMove")
    SIGNUP_RMOVE_DIARY_CALL_CENTER = (
        8,
        "Signup via rMove, Diary via call center",
    )
    SIGNUP_RMOVE_DIARY_RMOVE = (9, "Signup via rMove, Diary via rMove")


class ResidenceRentOwn(StrEnum):
    """residence_rent_own value labels."""

    canonical_field_name = "residence_rent_own"

    OWN = "Own/paying mortgage" 
    RENT = "Rent"
    NOPAYMENT_EMPLOYER = "Provided by job or military"
    NOPAYMENT_OTHER = "Provided by family, relative, or friend without payment or rent"
    MISSING = "Missing Response"
    OTHER = "Other"
    PNTA = "Prefer not to answer"


class ResidenceType(StrEnum):
    """residence_type value labels."""

    canonical_field_name = "residence_type"

    SFH = "Single-family house (detached house)"
    TOWNHOUSE = "Townhouse (attached house)"
    APART_CONDO_3FEWER = "Building with 3 or fewer apartments/condos"
    APART_CONDO_4MORE = "Building with 4 or more apartments/condos"
    MOBILE = "Mobile home/trailer"
    GROUP_QUARTERS = "Dorm or institutional housing" 
    MISSING = "Missing Response"
    BOAT_RV = "Other (including boat, RV, van, etc.)"
