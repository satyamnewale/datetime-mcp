
from datetime import datetime

from utils.timezone_utils import (
    get_timezone_details,
    convert_to_utc,
)


class TimezoneService:

    def get_timezone_info(self, timezone_name: str) -> dict:

        try:
            details = get_timezone_details(timezone_name)

            current = datetime.fromisoformat(
                details["current_datetime"]
            )

            return {
                "timezone": details["timezone"],
                "utc_offset": details["utc_offset"].replace(":", ""),
                "utc_offset_name": details["timezone_abbreviation"],
                "is_dst": details["is_dst"],
                "current_datetime": details["current_datetime"],
                "utc_datetime": convert_to_utc(current).isoformat()
            }

        except ValueError as exc:
            return {
                "success": False,
                "error": str(exc)
            }
