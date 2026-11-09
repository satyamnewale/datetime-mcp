from datetime import timedelta, timezone as utc_timezone
from config.settings import settings

from utils.datetime_utils import get_current_datetime
from utils.timezone_utils import convert_to_utc
from utils.formatters import format_datetime_response
from utils.validator import validate_amount, validate_unit


SUPPORTED_TIME_UNITS = {
    "seconds",
    "minutes",
    "hours",
    "days",
    "weeks",
}


SECONDS_PER_UNIT = {
    "seconds": 1,
    "minutes": 60,
    "hours": 3600,
    "days": 86400,
    "weeks": 604800,
}


class RelativeDateTimeService:

    def calculate_relative_datetime(
        self,
        amount: int,
        unit: str,
        direction: str,
        timezone: str = "Asia/Kolkata",
    ) -> dict:

        unit = validate_unit(
            unit,
            SUPPORTED_TIME_UNITS,
        )

        maximum_amount = (
            settings.max_relative_datetime_seconds
            // SECONDS_PER_UNIT[unit]
        )

        amount = validate_amount(
            amount,
            minimum=0,
            maximum=maximum_amount,
        )

        if direction not in ("past", "future"):
            raise ValueError(
                "Direction must be past or future."
            )

        now = get_current_datetime(timezone)

        delta = timedelta(
            **{unit: amount}
        )

        # Perform elapsed arithmetic in UTC.
        # Convert the result back to the requested timezone.
        now_utc = now.astimezone(
            utc_timezone.utc
        )

        if direction == "past":
            result_utc = now_utc - delta
        else:
            result_utc = now_utc + delta

        result = result_utc.astimezone(
            now.tzinfo
        )

        response = format_datetime_response(result)

        response.update(
            {
                "original_datetime": now.isoformat(),
                "result_datetime": result.isoformat(),
                "result_date": result.date().isoformat(),
                "result_time": result.strftime("%H:%M:%S"),
                "timezone": timezone,
                "utc_datetime": convert_to_utc(result).isoformat(),
                "amount": amount,
                "unit": unit,
                "direction": direction,
                "calculation_type": "elapsed_duration",
            }
        )

        return response