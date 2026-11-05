
from datetime import date, datetime, time

from utils.timezone_utils import get_utc_offset


def format_date(value: date, date_format: str = "%Y-%m-%d") -> str:
    return value.strftime(date_format)


def format_time(value: time, time_format: str = "%H:%M:%S") -> str:
    return value.strftime(time_format)


def format_datetime(
    value: datetime,
    datetime_format: str = "%Y-%m-%dT%H:%M:%S%z"
) -> str:
    return value.strftime(datetime_format)


def format_datetime_response(value: datetime) -> dict:
    if value.tzinfo is None:
        raise ValueError("Datetime must be timezone-aware")

    return {
        "date": value.date().isoformat(),
        "time": value.strftime("%H:%M:%S"),
        "day": value.strftime("%A"),
        "datetime_iso": value.isoformat(),
        "timezone": str(value.tzinfo),
        "utc_offset": get_utc_offset(value)
    }


def format_date_list(dates: list[date]) -> list[dict]:
    return [
        {
            "date": item.isoformat(),
            "day": item.strftime("%A")
        }
        for item in dates
    ]


def format_duration(total_seconds: int) -> dict:
    seconds = abs(total_seconds)

    days, remaining = divmod(seconds, 86400)
    hours, remaining = divmod(remaining, 3600)
    minutes, seconds = divmod(remaining, 60)

    return {
        "days": days,
        "hours": hours,
        "minutes": minutes,
        "seconds": seconds,
        "total_seconds": total_seconds
    }
