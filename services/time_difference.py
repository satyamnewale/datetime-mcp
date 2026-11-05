from datetime import datetime
from zoneinfo import ZoneInfo


class TimeDifferenceService:

    def calculate_time_difference(
        self,
        start_datetime: str,
        end_datetime: str,
        timezone: str = "Asia/Kolkata"
    ) -> dict:

        tz = ZoneInfo(timezone)

        start = datetime.fromisoformat(start_datetime)
        end = datetime.fromisoformat(end_datetime)

        if start.tzinfo is None:
            start = start.replace(tzinfo=tz)

        if end.tzinfo is None:
            end = end.replace(tzinfo=tz)

        # Compare actual instants rather than local wall-clock values.
        difference = (
            end.astimezone(ZoneInfo("UTC"))
            - start.astimezone(ZoneInfo("UTC"))
        )

        total_seconds = int(abs(difference.total_seconds()))

        return {
            "start_datetime": start.isoformat(),
            "end_datetime": end.isoformat(),
            "difference_seconds": total_seconds,
            "difference_minutes": total_seconds // 60,
            "difference_hours": round(total_seconds / 3600, 2),
            "difference_days": round(total_seconds / 86400, 2),
            "direction": (
                "future" if difference.total_seconds() > 0
                else "past" if difference.total_seconds() < 0
                else "same_time"
            ),
            "timezone": timezone
        }