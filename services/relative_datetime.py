from datetime import datetime, timedelta, timezone as utc_timezone

from config.settings import settings

from utils.datetime_utils import get_current_datetime
from utils.timezone_utils import (
    convert_to_utc,
    get_timezone,
    localize_naive_datetime,
)

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
        reference_datetime: str | None = None,
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

        # --------------------------------------------------
        # 1. Resolve the calculation reference
        # --------------------------------------------------

        if reference_datetime is None:

            now = get_current_datetime(timezone)

        else:

            try:

                normalized = reference_datetime.replace(
                    "Z",
                    "+00:00",
                )

                parsed_reference = datetime.fromisoformat(
                    normalized
                )

            except (AttributeError, TypeError, ValueError) as exc:

                raise ValueError(
                    "reference_datetime must be a valid ISO 8601 datetime."
                ) from exc

            now = localize_naive_datetime(
                parsed_reference,
                timezone,
            )

            now = now.astimezone(
                get_timezone(timezone)
            )

        # --------------------------------------------------
        # 2. Perform elapsed-time calculation in UTC
        # --------------------------------------------------

        delta = timedelta(
            **{unit: amount}
        )

        now_utc = now.astimezone(
            utc_timezone.utc
        )

        if direction == "past":

            result_utc = now_utc - delta

        else:

            result_utc = now_utc + delta

        result = result_utc.astimezone(
            get_timezone(timezone)
        )

        # --------------------------------------------------
        # 3. Build response
        # --------------------------------------------------

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
                "reference_supplied": reference_datetime is not None,
            }
        )

        return response
