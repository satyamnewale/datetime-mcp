
from datetime import date, datetime, time
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError


SUPPORTED_DATE_UNITS = {
    "days", "weeks", "months", "years"
}

SUPPORTED_TIME_UNITS = {
    "seconds", "minutes", "hours", "days", "weeks"
}


def validate_date(value: str) -> date:
    try:
        return date.fromisoformat(value)
    except (ValueError, TypeError):
        raise ValueError("Invalid date. Expected YYYY-MM-DD")


def validate_time(value: str) -> time:
    try:
        return time.fromisoformat(value)
    except (ValueError, TypeError):
        raise ValueError("Invalid time format")


def validate_datetime(value: str) -> datetime:
    try:
        return datetime.fromisoformat(value)
    except (ValueError, TypeError):
        raise ValueError("Invalid ISO datetime format")


def validate_timezone(value: str) -> str:
    try:
        ZoneInfo(value)
        return value
    except (ZoneInfoNotFoundError, ValueError):
        raise ValueError(f"Invalid timezone: {value}")


def validate_amount(amount: int, minimum: int = 0) -> int:
    if isinstance(amount, bool) or not isinstance(amount, int):
        raise ValueError("Amount must be an integer")

    if amount < minimum:
        raise ValueError(f"Amount must be at least {minimum}")

    return amount


def validate_unit(unit: str, supported_units: set) -> str:
    normalized = unit.lower().strip()

    if normalized not in supported_units:
        raise ValueError(
            f"Unsupported unit: {unit}. "
            f"Supported units: {sorted(supported_units)}"
        )

    return normalized


def validate_date_range(
    start_date: str,
    end_date: str,
    max_days: int = 366
) -> tuple[date, date]:

    start = validate_date(start_date)
    end = validate_date(end_date)

    if end < start:
        raise ValueError("End date cannot be before start date")

    total_days = (end - start).days + 1

    if total_days > max_days:
        raise ValueError(
            f"Date range cannot exceed {max_days} days"
        )

    return start, end


def validate_week_start(value: int) -> int:
    if isinstance(value, bool) or not isinstance(value, int):
        raise ValueError("Week start must be an integer")

    if not 0 <= value <= 6:
        raise ValueError("Week start must be between 0 and 6")

    return value
