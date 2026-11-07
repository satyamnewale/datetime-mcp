
from datetime import timedelta

from utils.datetime_utils import get_current_datetime
from utils.timezone_utils import convert_to_utc
from utils.formatters import format_datetime_response
from utils.validator import validate_amount, validate_unit

SUPPORTED_TIME_UNITS = {
    "seconds",
    "minutes",
    "hours",
    "days",
    "weeks"
}

class RelativeDateTimeService:

    def calculate_relative_datetime(
        self,
        amount: int,
        unit: str,
        direction: str,
        timezone: str = "Asia/Kolkata"
    ) -> dict:

        amount = validate_amount(amount)
        unit = validate_unit(unit, SUPPORTED_TIME_UNITS)

        if direction not in ("past", "future"):
            raise ValueError("Direction must be past or future")

        now = get_current_datetime(timezone)

        delta = timedelta(**{unit: amount})

        result = (
            now - delta
            if direction == "past"
            else now + delta
        )

        response = format_datetime_response(result)

        response.update({
            "original_datetime": now.isoformat(),
            "result_datetime": result.isoformat(),
            "result_date": result.date().isoformat(),
            "result_time": result.strftime("%H:%M:%S"),
            "timezone": timezone,
            "utc_datetime": convert_to_utc(result).isoformat(),
            "amount": amount,
            "unit": unit,
            "direction": direction
        })

        return response