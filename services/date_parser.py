import re
import dateparser
from datetime import datetime

from utils.timezone_utils import get_timezone
from utils.formatters import format_datetime_response


_COARSE_TIME = re.compile(
    r"\b(?:morning|afternoon|evening|night)\b",
    re.IGNORECASE,
)

_EXPLICIT_TIME = re.compile(
    r"\b(?:"
    r"\d{1,2}:\d{2}\s*(?:am|pm)?"
    r"|"
    r"(?:1[0-2]|0?[1-9])\s*(?:am|pm)"
    r"|"
    r"noon|midnight"
    r")\b",
    re.IGNORECASE,
)

_AMBIGUOUS_CLOCK = re.compile(
    r"\b(?:at|around|about)\s+\d{1,2}(?!\s*(?:am|pm|:))\b",
    re.IGNORECASE,
)


class DateParserService:
    def parse_natural_datetime(
        self,
        expression: str,
        timezone: str = "Asia/Kolkata",
    ) -> dict:
        try:
            tz = get_timezone(timezone)
        except ValueError as exc:
            return {
                "success": False,
                "error": str(exc),
            }

        has_explicit_time = bool(_EXPLICIT_TIME.search(expression))

        if (
            (_COARSE_TIME.search(expression) and not has_explicit_time)
            or _AMBIGUOUS_CLOCK.search(expression)
        ):
            return {
                "success": False,
                "needs_clarification": True,
                "error": (
                    "The request does not specify an exact, unambiguous "
                    "clock time. Ask the user for one."
                ),
            }

        reference = datetime.now(tz)

        parsed = dateparser.parse(
            expression,
            settings={
                "TIMEZONE": timezone,
                "TO_TIMEZONE": timezone,
                "RETURN_AS_TIMEZONE_AWARE": True,
                "RELATIVE_BASE": reference,
                "PREFER_DATES_FROM": "future",
            },
        )

        if parsed is None:
            return {
                "success": False,
                "error": "Could not understand the date-time expression.",
            }

        if parsed.tzinfo is None:
            parsed = parsed.replace(tzinfo=tz)
        else:
            parsed = parsed.astimezone(tz)

        return {
            "success": True,
            "time_specified": has_explicit_time,
            "original_expression": expression,
            **format_datetime_response(parsed),
        }