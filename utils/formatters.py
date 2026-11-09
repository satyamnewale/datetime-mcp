from datetime import date, datetime, time

from config.settings import settings
from utils.timezone_utils import get_utc_offset


def format_date(
    value: date,
    date_format: str | None = None,
) -> str:

    selected_format = (
        date_format or settings.default_date_format
    )

    return value.strftime(selected_format)


def format_time(
    value: time,
    time_format: str | None = None,
) -> str:

    selected_format = (
        time_format or settings.default_time_format
    )

    return value.strftime(selected_format)


def format_datetime(
    value: datetime,
    datetime_format: str = "%Y-%m-%dT%H:%M:%S%z",
) -> str:

    return value.strftime(datetime_format)


def format_datetime_response(value: datetime) -> dict:

    if value.tzinfo is None or value.utcoffset() is None:
        raise ValueError(
            "Datetime must be timezone-aware."
        )

    return {
        "date": format_date(value.date()),
        "time": format_time(value.time()),
        "day": value.strftime("%A"),
        "datetime_iso": value.isoformat(),
        "timezone": str(value.tzinfo),
        "utc_offset": get_utc_offset(value),
    }


def format_date_list(dates: list[date]) -> list[dict]:

    return [
        {
            "date": format_date(item),
            "day": item.strftime("%A"),
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
        "total_seconds": total_seconds,
    }