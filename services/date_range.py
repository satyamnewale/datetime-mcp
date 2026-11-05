from datetime import date

class DateRangeService:

    def get_date_range(
        self,
        start_date: str,
        end_date: str,
        timezone: str = "Asia/Kolkata"
    ) -> dict:

        start = date.fromisoformat(start_date)
        end = date.fromisoformat(end_date)

        if end < start:
            raise ValueError("End date cannot be before start date")

        total_days = (end - start).days + 1

        return {
            "start_date": start.isoformat(),
            "end_date": end.isoformat(),
            "total_days": total_days,
            "start_day": start.strftime("%A"),
            "end_day": end.strftime("%A"),
            "timezone": timezone
        }