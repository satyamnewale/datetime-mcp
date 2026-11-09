from utils.timezone_utils import (
    get_timezone,
    convert_to_utc,
    localize_naive_datetime,
)

from utils.datetime_utils import get_elapsed_time_difference

from utils.formatters import format_duration
from utils.validator import validate_datetime


class TimeDifferenceService:

    def calculate_time_difference(
        self,
        start_datetime: str,
        end_datetime: str,
        timezone: str = "Asia/Kolkata",
    ) -> dict:

        tz = get_timezone(timezone)

        # Parse ISO datetime strings.
        start = validate_datetime(start_datetime)
        end = validate_datetime(end_datetime)

        # Attach the selected timezone only when no offset is supplied.
        if start.tzinfo is None:
            start = localize_naive_datetime(
                start,
                timezone,
            )

        if end.tzinfo is None:
            end = localize_naive_datetime(
                end,
                timezone,
            )

        # Explicit offsets are preserved.
        start_utc = convert_to_utc(start)
        end_utc = convert_to_utc(end)

        difference = get_elapsed_time_difference(
            start_utc,
            end_utc,
        )

        signed_seconds = int(
            difference.total_seconds()
        )

        total_seconds = abs(signed_seconds)

        duration = format_duration(total_seconds)

        if signed_seconds > 0:
            direction = "future"

        elif signed_seconds < 0:
            direction = "past"

        else:
            direction = "same_time"

        return {
            "start_datetime": start.isoformat(),
            "end_datetime": end.isoformat(),
            "start_utc": start_utc.isoformat(),
            "end_utc": end_utc.isoformat(),
            "difference_seconds": total_seconds,
            "difference_minutes": total_seconds // 60,
            "difference_hours": round(total_seconds / 3600, 2),
            "difference_days": round(total_seconds / 86400, 2),
            "direction": direction,
            "duration": duration,
            "timezone": timezone,
        }