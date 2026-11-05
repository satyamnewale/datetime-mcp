
from datetime import (
    date,
    datetime,
    timedelta,
    time,
    timezone as utc_timezone
)

from dateutil.relativedelta import relativedelta

from utils.timezone_utils import get_timezone


def get_current_datetime(timezone_name: str) -> datetime:
    return datetime.now(get_timezone(timezone_name))


def get_current_date(timezone_name: str) -> date:
    return get_current_datetime(timezone_name).date()


def get_current_time(timezone_name: str) -> time:
    return get_current_datetime(timezone_name).time()


def add_days(value: date, days: int) -> date:
    return value + timedelta(days=days)


def add_weeks(value: date, weeks: int) -> date:
    return value + timedelta(weeks=weeks)


def add_months(value: date, months: int) -> date:
    return value + relativedelta(months=months)


def add_years(value: date, years: int) -> date:
    return value + relativedelta(years=years)


def get_week_start(value: date, week_starts_on: int = 0) -> date:
    if not 0 <= week_starts_on <= 6:
        raise ValueError("Week start must be between 0 and 6")

    offset = (value.weekday() - week_starts_on) % 7

    return value - timedelta(days=offset)


def get_week_end(value: date, week_starts_on: int = 0) -> date:
    return get_week_start(value, week_starts_on) + timedelta(days=6)


def get_start_of_day(value: date, timezone_name: str) -> datetime:
    tz = get_timezone(timezone_name)

    return datetime.combine(value, time.min, tzinfo=tz)


def get_start_of_next_day(value: date, timezone_name: str) -> datetime:
    tz = get_timezone(timezone_name)
    next_day = value + timedelta(days=1)

    return datetime.combine(next_day, time.min, tzinfo=tz)


def get_date_difference(start: date, end: date) -> int:
    return (end - start).days


def get_elapsed_time_difference(
    start: datetime,
    end: datetime
) -> timedelta:

    if start.tzinfo is None or end.tzinfo is None:
        raise ValueError("Both datetimes must be timezone-aware")

    return (
        end.astimezone(utc_timezone.utc)
        - start.astimezone(utc_timezone.utc)
    )
