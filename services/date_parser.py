
import dateparser
from datetime import datetime

from utils.timezone_utils import get_timezone
from utils.formatters import format_datetime_response


class DateParserService:

    def parse_natural_datetime(
        self,
        expression: str,
        timezone: str = "Asia/Kolkata"
    ) -> dict:

        try:
            tz = get_timezone(timezone)

        except ValueError as exc:
            return {
                "success": False,
                "error": str(exc)
            }

        reference = datetime.now(tz)

        parsed = dateparser.parse(
            expression,
            settings={
                "TIMEZONE": timezone,
                "TO_TIMEZONE": timezone,
                "RETURN_AS_TIMEZONE_AWARE": True,
                "RELATIVE_BASE": reference,
                "PREFER_DATES_FROM": "future"
            }
        )

        if parsed is None:
            return {
                "success": False,
                "error": "Could not understand the date-time expression."
            }

        if parsed.tzinfo is None:
            parsed = parsed.replace(tzinfo=tz)
        else:
            parsed = parsed.astimezone(tz)

        return {
            "success": True,
            "original_expression": expression,
            **format_datetime_response(parsed)
        }
