import calendar
from datetime import date

from utils.datetime_utils import get_current_datetime
from utils.formatters import format_date_list

class MonthService:

    def get_month_dates(
        self,
        year: int | None = None,
        month: int | None = None,
        timezone: str = "Asia/Kolkata"
    ) -> dict:

        now = get_current_datetime(timezone)

        year = year if year is not None else now.year
        month = month if month is not None else now.month

        if not 1 <= year <= 9999:
            raise ValueError("Year must be between 1 and 9999")

        if not 1 <= month <= 12:
            raise ValueError("Month must be between 1 and 12")

        _, total_days = calendar.monthrange(year, month)

        dates = [
            date(year, month, day)
            for day in range(1, total_days + 1)
        ]

        return {
            "year": year,
            "month": month,
            "month_name": calendar.month_name[month],
            "total_days": total_days,
            "dates": format_date_list(dates),
            "timezone": timezone
        }
