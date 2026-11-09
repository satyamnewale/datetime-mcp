from utils.datetime_utils import (
    get_current_datetime,
    get_current_date,
)

from utils.timezone_utils import convert_to_utc

from utils.formatters import (
    format_datetime_response,
    format_date,
    format_time,
)


class CurrentDateTimeService:

    def get_current_datetime(
        self,
        timezone: str = "Asia/Kolkata",
    ) -> dict:

        now = get_current_datetime(timezone)

        result = format_datetime_response(now)

        result["utc_offset"] = now.strftime("%z")
        result["utc_datetime"] = convert_to_utc(now).isoformat()

        return result

    def get_current_date(
        self,
        timezone: str = "Asia/Kolkata",
    ) -> dict:

        today = get_current_date(timezone)

        return {
            "date": format_date(today),
            "day": today.strftime("%A"),
            "timezone": timezone,
        }

    def get_current_time(
        self,
        timezone: str = "Asia/Kolkata",
    ) -> dict:

        # Take one snapshot instead of calling now() twice.
        now = get_current_datetime(timezone)

        return {
            "time": format_time(now.time()),
            "timezone": timezone,
            "utc_offset": now.strftime("%z"),
            "datetime_iso": now.isoformat(),
        }