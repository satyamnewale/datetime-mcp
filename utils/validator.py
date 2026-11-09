import re

from datetime import date, datetime, time
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

SUPPORTED_DATE_UNITS = {
    "days",
    "weeks",
    "months",
    "years",
}

SUPPORTED_TIME_UNITS = {
    "seconds",
    "minutes",
    "hours",
    "days",
    "weeks",
}


DATE_PATTERN = re.compile(r"^\d{4}-\d{2}-\d{2}$")

TIME_PATTERN = re.compile(r"^(?:[01]\d|2[0-3]):[0-5]\d" r"(?::[0-5]\d(?:\.\d{1,6})?)?$")

DATETIME_PATTERN = re.compile(
    r"^\d{4}-\d{2}-\d{2}"
    r"T"
    r"(?:[01]\d|2[0-3]):[0-5]\d"
    r"(?::[0-5]\d(?:\.\d{1,6})?)?"
    r"(?:Z|[+-](?:0\d|1\d|2[0-3]):?[0-5]\d)?$"
)


# --------------------------------------------------
# DATE VALIDATION
# --------------------------------------------------


def validate_date(value: str) -> date:

    if not isinstance(value, str):
        raise ValueError("Date must be a string in YYYY-MM-DD format.")

    if not DATE_PATTERN.fullmatch(value):
        raise ValueError("Invalid date format. Expected YYYY-MM-DD.")

    try:
        return date.fromisoformat(value)

    except ValueError as exc:
        raise ValueError("Invalid calendar date.") from exc


# --------------------------------------------------
# TIME VALIDATION
# --------------------------------------------------


def validate_time(value: str) -> time:

    if not isinstance(value, str):
        raise ValueError("Time must be a string.")

    if not TIME_PATTERN.fullmatch(value):
        raise ValueError("Invalid time format. Expected HH:MM or HH:MM:SS.")

    try:
        return time.fromisoformat(value)

    except ValueError as exc:
        raise ValueError("Invalid time.") from exc


# --------------------------------------------------
# DATETIME VALIDATION
# --------------------------------------------------


def validate_datetime(value: str) -> datetime:

    if not isinstance(value, str):
        raise ValueError("Datetime must be a string.")

    if not DATETIME_PATTERN.fullmatch(value):
        raise ValueError(
            "Invalid datetime format. Expected ISO 8601 datetime "
            "such as 2026-11-05T15:30:00 or "
            "2026-11-05T15:30:00+05:30."
        )

    try:
        normalized = value[:-1] + "+00:00" if value.endswith("Z") else value

        return datetime.fromisoformat(normalized)

    except ValueError as exc:
        raise ValueError("Invalid ISO 8601 datetime.") from exc


# --------------------------------------------------
# TIMEZONE VALIDATION
# --------------------------------------------------


def validate_timezone(value: str) -> str:

    if not isinstance(value, str) or not value.strip():
        raise ValueError("Timezone must be a non-empty IANA timezone name.")

    value = value.strip()

    try:
        ZoneInfo(value)
        return value

    except (ZoneInfoNotFoundError, ValueError, TypeError) as exc:
        raise ValueError(f"Invalid timezone: {value}") from exc


# --------------------------------------------------
# AMOUNT VALIDATION
# --------------------------------------------------


def validate_amount(
    amount: int,
    minimum: int = 0,
    maximum: int | None = None,
) -> int:

    if isinstance(amount, bool) or not isinstance(amount, int):
        raise ValueError("Amount must be an integer.")

    if amount < minimum:
        raise ValueError(f"Amount must be at least {minimum}.")

    if maximum is not None and amount > maximum:
        raise ValueError(f"Amount cannot exceed {maximum}.")

    return amount


# --------------------------------------------------
# UNIT VALIDATION
# --------------------------------------------------


def validate_unit(
    unit: str,
    supported_units: set,
) -> str:

    if not isinstance(unit, str):
        raise ValueError("Unit must be a string.")

    normalized = unit.lower().strip()

    if normalized not in supported_units:
        raise ValueError(
            f"Unsupported unit: {unit}. " f"Supported units: {sorted(supported_units)}"
        )

    return normalized


# --------------------------------------------------
# DATE RANGE VALIDATION
# --------------------------------------------------


def validate_date_range(
    start_date: str,
    end_date: str,
    max_days: int = 366,
) -> tuple[date, date]:

    start = validate_date(start_date)
    end = validate_date(end_date)

    if end < start:
        raise ValueError("End date cannot be before start date.")

    total_days = (end - start).days + 1

    if total_days > max_days:
        raise ValueError(f"Date range cannot exceed {max_days} days.")

    return start, end


# --------------------------------------------------
# WEEK START VALIDATION
# --------------------------------------------------


def validate_week_start(value: int) -> int:

    if isinstance(value, bool) or not isinstance(value, int):
        raise ValueError("Week start must be an integer.")

    if not 0 <= value <= 6:
        raise ValueError("Week start must be between 0 and 6.")

    return value
