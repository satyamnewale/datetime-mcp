
from utils.timezone_utils import get_timezone, convert_to_utc
from utils.datetime_utils import get_elapsed_time_difference
from utils.formatters import format_duration
from utils.validator import validate_datetime


class TimeDifferenceService:

    def calculate_time_difference(
        self,
        start_datetime: str,
        end_datetime: str,
        timezone: str = "Asia/Kolkata"
    ) -> dict:

        # 1. Validate and retrieve timezone
        tz = get_timezone(timezone)

        # 2. Validate and parse datetime strings
        start = validate_datetime(start_datetime)
        end = validate_datetime(end_datetime)

        # 3. Attach the supplied timezone only to naive datetimes
        if start.tzinfo is None:
            start = start.replace(tzinfo=tz)

        if end.tzinfo is None:
            end = end.replace(tzinfo=tz)

        # 4. Convert both timestamps to UTC
        start_utc = convert_to_utc(start)
        end_utc = convert_to_utc(end)

        # 5. Calculate signed elapsed difference
        difference = get_elapsed_time_difference(
            start_utc,
            end_utc
        )

        signed_seconds = int(difference.total_seconds())
        total_seconds = abs(signed_seconds)

        # 6. Format duration
        duration = format_duration(total_seconds)

        # 7. Determine direction
        if signed_seconds > 0:
            direction = "future"

        elif signed_seconds < 0:
            direction = "past"

        else:
            direction = "same_time"

        # 8. Return structured result
        return {
            "start_datetime": start.isoformat(),
            "end_datetime": end.isoformat(),
            "difference_seconds": total_seconds,
            "difference_minutes": total_seconds // 60,
            "difference_hours": round(total_seconds / 3600, 2),
            "difference_days": round(total_seconds / 86400, 2),
            "direction": direction,
            "duration": duration,
            "timezone": timezone
        }
