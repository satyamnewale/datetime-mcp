from datetime import datetime
from zoneinfo import ZoneInfo


class CurrentDateTimeService:

    def get_current_datetime(self, timezone: str = "Asia/Kolkata") -> dict:
        now = datetime.now(ZoneInfo(timezone))

        return {
            "date": now.date().isoformat(),
            "time": now.strftime("%H:%M:%S"),
            "day": now.strftime("%A"),
            "timezone": timezone,
            "utc_offset": now.strftime("%z"),
            "datetime_iso": now.isoformat(),
            "utc_datetime": now.astimezone(ZoneInfo("UTC")).isoformat()
        }

    def get_current_date(self, timezone: str = "Asia/Kolkata") -> dict:
        now = datetime.now(ZoneInfo(timezone))

        return {
            "date": now.date().isoformat(),
            "day": now.strftime("%A"),
            "timezone": timezone
        }

    def get_current_time(self, timezone: str = "Asia/Kolkata") -> dict:
        now = datetime.now(ZoneInfo(timezone))

        return {
            "time": now.strftime("%H:%M:%S"),
            "timezone": timezone,
            "utc_offset": now.strftime("%z")
        }