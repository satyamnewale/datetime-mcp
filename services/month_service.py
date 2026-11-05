import calendar
from datetime import datetime
from zoneinfo import ZoneInfo


class MonthService:

    def get_month_dates(
        self,
        year: int | None = None,
        month: int | None = None,
        timezone: str = "Asia/Kolkata"
    ) -> dict:

        now = datetime.now(ZoneInfo(timezone))

        year = year if year is not None else now.year
        month = month if month is not None else now.month

        if not 1 <= month <= 12:
            raise ValueError("Month must be between 1 and 12")

        _, total_days = calendar.monthrange(year, month)

        dates = [
            {
                "date": f"{year:04d}-{month:02d}-{day:02d}",
                "day": calendar.day_name[
                    calendar.weekday(year, month, day)
                ]
            }
            for day in range(1, total_days + 1)
        ]

        return {
            "year": year,
            "month": month,
            "month_name": calendar.month_name[month],
            "total_days": total_days,
            "dates": dates,
            "timezone": timezone
        }