from utils.datetime_utils import get_date_difference
from utils.formatters import format_date
from utils.validator import validate_date
class DateRangeService:

    def get_date_range(
        self,
        start_date: str,
        end_date: str,
        timezone: str = "Asia/Kolkata"
    ) -> dict:

        start = validate_date(start_date)
        end = validate_date(end_date)

        if end < start:
            raise ValueError("End date cannot be before start date")

        total_days = get_date_difference(start, end) + 1

        return {
            "start_date": format_date(start),
            "end_date": format_date(end),
            "total_days": total_days,
            "start_day": start.strftime("%A"),
            "end_day": end.strftime("%A"),
            "timezone": timezone
        }