from datetime import datetime, timezone as utc_timezone
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError


# --------------------------------------------------
# GET TIMEZONE
# --------------------------------------------------

def get_timezone(timezone_name: str) -> ZoneInfo:

    if not isinstance(timezone_name, str) or not timezone_name.strip():
        raise ValueError("Timezone must be a non-empty IANA timezone name.")

    try:
        return ZoneInfo(timezone_name.strip())

    except (ZoneInfoNotFoundError, ValueError, TypeError) as exc:
        raise ValueError(
            f"Invalid timezone: {timezone_name}"
        ) from exc


# --------------------------------------------------
# VALIDATE TIMEZONE
# --------------------------------------------------

def validate_timezone(timezone_name: str) -> bool:

    try:
        get_timezone(timezone_name)
        return True

    except ValueError:
        return False


# --------------------------------------------------
# LOCALIZE NAIVE DATETIME SAFELY
# --------------------------------------------------

def localize_naive_datetime(
    value: datetime,
    timezone_name: str,
) -> datetime:
    """
    Attach an IANA timezone to a naive datetime safely.

    DST behavior:

    1. Normal local time:
       Accepted.

    2. Nonexistent local time:
       Rejected.

    3. Ambiguous local time:
       Rejected. Caller must supply an explicit UTC offset.

    4. Already timezone-aware:
       Returned unchanged.
    """

    if not isinstance(value, datetime):
        raise ValueError("Value must be a datetime instance.")

    # An explicitly supplied timezone/offset already resolves local ambiguity.
    if value.tzinfo is not None and value.utcoffset() is not None:
        return value

    tz = get_timezone(timezone_name)

    candidate_0 = value.replace(
        tzinfo=tz,
        fold=0,
    )

    candidate_1 = value.replace(
        tzinfo=tz,
        fold=1,
    )

    utc_candidate_0 = (
        candidate_0
        .astimezone(utc_timezone.utc)
        .astimezone(tz)
        .replace(tzinfo=None)
    )

    utc_candidate_1 = (
        candidate_1
        .astimezone(utc_timezone.utc)
        .astimezone(tz)
        .replace(tzinfo=None)
    )

    valid_0 = utc_candidate_0 == value
    valid_1 = utc_candidate_1 == value

    # The local time does not exist due to a DST forward transition.
    if not valid_0 and not valid_1:
        raise ValueError(
            f"The local datetime {value.isoformat()} does not exist "
            f"in timezone {timezone_name} because of a daylight-saving "
            "transition."
        )

    # Both folds are valid but correspond to different UTC offsets.
    if (
        valid_0
        and valid_1
        and candidate_0.utcoffset() != candidate_1.utcoffset()
    ):
        raise ValueError(
            f"The local datetime {value.isoformat()} is ambiguous "
            f"in timezone {timezone_name}. "
            "Provide an explicit UTC offset to identify the intended time."
        )

    if valid_0:
        return candidate_0

    return candidate_1


# --------------------------------------------------
# CURRENT LOCAL DATETIME
# --------------------------------------------------

def get_local_datetime(timezone_name: str) -> datetime:

    return datetime.now(
        get_timezone(timezone_name)
    )


# --------------------------------------------------
# TIMEZONE CONVERSION
# --------------------------------------------------

def convert_timezone(
    dt: datetime,
    target_timezone: str,
) -> datetime:

    if dt.tzinfo is None or dt.utcoffset() is None:
        raise ValueError(
            "Datetime must be timezone-aware."
        )

    return dt.astimezone(
        get_timezone(target_timezone)
    )


# --------------------------------------------------
# UTC CONVERSION
# --------------------------------------------------

def convert_to_utc(dt: datetime) -> datetime:

    if dt.tzinfo is None or dt.utcoffset() is None:
        raise ValueError(
            "Datetime must be timezone-aware."
        )

    return dt.astimezone(
        utc_timezone.utc
    )


# --------------------------------------------------
# UTC OFFSET
# --------------------------------------------------

def get_utc_offset(dt: datetime) -> str:

    if dt.tzinfo is None or dt.utcoffset() is None:
        raise ValueError(
            "Datetime must be timezone-aware."
        )

    offset = dt.strftime("%z")

    if not offset:
        return ""

    return f"{offset[:3]}:{offset[3:]}"


# --------------------------------------------------
# TIMEZONE DETAILS
# --------------------------------------------------

def get_timezone_details(timezone_name: str) -> dict:

    tz = get_timezone(timezone_name)
    now = datetime.now(tz)

    return {
        "timezone": timezone_name,
        "utc_offset": get_utc_offset(now),
        "timezone_abbreviation": now.strftime("%Z"),
        "is_dst": bool(now.dst()),
        "current_datetime": now.isoformat(),
    }