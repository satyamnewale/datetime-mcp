from datetime import datetime, timedelta, timezone as utc_timezone
from zoneinfo import ZoneInfo


class RelativeDateTimeService:

    def calculate_relative_datetime(
        self,
        amount: int,
        unit: str,
        direction: str,
        timezone: str = "Asia/Kolkata"
    ) -> dict:

        if amount < 0:
            raise ValueError("Amount must be non-negative")

        if direction not in ("past", "future"):
            raise ValueError("Direction must be past or future")

        units = {
            "seconds": "seconds",
            "minutes": "minutes",
            "hours": "hours",
            "days": "days",
            "weeks": "weeks"
        }

        if unit not in units:
            raise ValueError("Unsupported time unit")

        now = datetime.now(ZoneInfo(timezone))

        delta = timedelta(**{units[unit]: amount})

        result = now - delta if direction == "past" else now + delta

        return {
            "original_datetime": now.isoformat(),
            "result_datetime": result.isoformat(),
            "result_date": result.date().isoformat(),
            "result_time": result.strftime("%H:%M:%S"),
            "day": result.strftime("%A"),
            "timezone": timezone,
            "utc_datetime": result.astimezone(utc_timezone.utc).isoformat(),
            "amount": amount,
            "unit": unit,
            "direction": direction
        }