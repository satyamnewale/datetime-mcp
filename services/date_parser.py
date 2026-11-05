import dateparser
from datetime import datetime
from zoneinfo import ZoneInfo


class DateParserService:

    def parse_natural_datetime(
        self,
        expression: str,
        timezone: str = "Asia/Kolkata"
    ) -> dict:

        try:
            tz = ZoneInfo(timezone)

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

            return {
                "success": True,
                "original_expression": expression,
                "date": parsed.date().isoformat(),
                "time": parsed.strftime("%H:%M:%S"),
                "day": parsed.strftime("%A"),
                "datetime_iso": parsed.isoformat(),
                "timezone": timezone
            }

        except Exception as exc:
            return {
                "success": False,
                "error": str(exc)
            }