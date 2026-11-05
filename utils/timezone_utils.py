
from datetime import datetime, timezone as utc_timezone
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError


def get_timezone(timezone_name: str) -> ZoneInfo:
    """Return a validated IANA timezone object."""

    try:
        return ZoneInfo(timezone_name)
    except (ZoneInfoNotFoundError, ValueError):
        raise ValueError(f"Invalid timezone: {timezone_name}")


def validate_timezone(timezone_name: str) -> bool:
    """Check whether a timezone exists."""

    try:
        get_timezone(timezone_name)
        return True
    except ValueError:
        return False


def get_local_datetime(timezone_name: str) -> datetime:
    """Get current datetime in a specified timezone."""

    return datetime.now(get_timezone(timezone_name))


def convert_timezone(
    dt: datetime,
    target_timezone: str
) -> datetime:
    """Convert an aware datetime into another timezone."""

    if dt.tzinfo is None:
        raise ValueError("Datetime must be timezone-aware")

    return dt.astimezone(get_timezone(target_timezone))


def convert_to_utc(dt: datetime) -> datetime:
    """Convert an aware datetime to UTC."""

    if dt.tzinfo is None:
        raise ValueError("Datetime must be timezone-aware")

    return dt.astimezone(utc_timezone.utc)


def get_utc_offset(dt: datetime) -> str:
    """Return UTC offset in +05:30 format."""

    if dt.tzinfo is None:
        raise ValueError("Datetime must be timezone-aware")

    offset = dt.strftime("%z")

    return f"{offset[:3]}:{offset[3:]}" if offset else ""


def get_timezone_details(timezone_name: str) -> dict:
    """Get timezone information for the current instant."""

    tz = get_timezone(timezone_name)
    now = datetime.now(tz)

    return {
        "timezone": timezone_name,
        "utc_offset": get_utc_offset(now),
        "timezone_abbreviation": now.strftime("%Z"),
        "is_dst": bool(now.dst()),
        "current_datetime": now.isoformat()
    }
