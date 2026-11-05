from datetime import datetime, timezone
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError


class TimezoneService:

    def get_timezone_info(self, timezone_name: str) -> dict:

        try:
            tz = ZoneInfo(timezone_name)
            now = datetime.now(tz)

            return {
                "timezone": timezone_name,
                "utc_offset": now.strftime("%z"),
                "utc_offset_name": now.strftime("%Z"),
                "is_dst": bool(now.dst()),
                "current_datetime": now.isoformat(),
                "utc_datetime": datetime.now(timezone.utc).isoformat()
            }

        except ZoneInfoNotFoundError:
            return {
                "success": False,
                "error": f"Invalid or unavailable timezone: {timezone_name}"
            }