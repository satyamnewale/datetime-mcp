from config.settings import settings

from utils.datetime_utils import get_date_difference
from utils.formatters import format_date
from utils.timezone_utils import get_timezone
from utils.validator import validate_date_range


class DateRangeService:

    def get_date_range(
        self,
        start_date: str,
        end_date: str,
        timezone: str = "Asia/Kolkata",
    ) -> dict:

        # Validate timezone even though date-only arithmetic
        # does not require a time conversion.
        get_timezone(timezone)

        start, end = validate_date_range(
            start_date,
            end_date,
            max_days=settings.max_date_range_days,
        )

        total_days = get_date_difference(
            start,
            end,
        ) + 1

        return {
            "start_date": format_date(start),
            "end_date": format_date(end),
            "total_days": total_days,
            "start_day": start.strftime("%A"),
            "end_day": end.strftime("%A"),
            "timezone": timezone,
        }