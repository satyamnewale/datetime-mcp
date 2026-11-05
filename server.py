
from fastmcp import FastMCP

from config.settings import settings

from services.current_datetime import CurrentDateTimeService
from services.timezone_service import TimezoneService
from services.relative_date import RelativeDateService
from services.relative_datetime import RelativeDateTimeService
from services.date_range import DateRangeService
from services.date_parser import DateParserService
from services.month_service import MonthService
from services.date_difference import DateDifferenceService
from services.time_difference import TimeDifferenceService


# --------------------------------
# MCP Initialization
# --------------------------------

mcp = FastMCP("Date-Time MCP")


# --------------------------------
# Service Initialization
# --------------------------------

current_datetime_service = CurrentDateTimeService()
timezone_service = TimezoneService()
relative_date_service = RelativeDateService()
relative_datetime_service = RelativeDateTimeService()
date_range_service = DateRangeService()
date_parser_service = DateParserService()
month_service = MonthService()
date_difference_service = DateDifferenceService()
time_difference_service = TimeDifferenceService()


DEFAULT_TIMEZONE = settings.default_timezone


# ==============================================
# 1. CURRENT DATE AND TIME TOOLS
# ==============================================

@mcp.tool()
def get_current_datetime(timezone: str = DEFAULT_TIMEZONE) -> dict:
    """
    Get the current date, time, weekday and UTC information
    for a specified timezone.
    """
    return current_datetime_service.get_current_datetime(timezone)


@mcp.tool()
def get_current_date(timezone: str = DEFAULT_TIMEZONE) -> dict:
    """
    Get today's date and weekday in a specified timezone.
    """
    return current_datetime_service.get_current_date(timezone)


@mcp.tool()
def get_current_time(timezone: str = DEFAULT_TIMEZONE) -> dict:
    """
    Get the current local time and UTC offset.
    """
    return current_datetime_service.get_current_time(timezone)


# ==============================================
# 2. TIMEZONE TOOL
# ==============================================

@mcp.tool()
def get_timezone_info(timezone_name: str = DEFAULT_TIMEZONE) -> dict:
    """
    Get timezone information including UTC offset,
    abbreviation and daylight-saving status.
    """
    return timezone_service.get_timezone_info(timezone_name)


# ==============================================
# 3. RELATIVE DATE TOOLS
# ==============================================

@mcp.tool()
def calculate_relative_date(
    amount: int,
    unit: str,
    direction: str,
    timezone: str = DEFAULT_TIMEZONE
) -> dict:
    """
    Calculate a date in the past or future.

    Examples:
    - 15 days ago
    - 40 days later
    - 2 months ago
    """
    return relative_date_service.calculate_relative_date(
        amount, unit, direction, timezone
    )


@mcp.tool()
def get_previous_n_days(
    n: int,
    timezone: str = DEFAULT_TIMEZONE
) -> dict:
    """
    Get the dates of the previous N days, excluding today.
    """
    return relative_date_service.get_previous_n_days(n, timezone)


@mcp.tool()
def get_next_n_days(
    n: int,
    timezone: str = DEFAULT_TIMEZONE
) -> dict:
    """
    Get the dates of the next N days, excluding today.
    """
    return relative_date_service.get_next_n_days(n, timezone)


@mcp.tool()
def get_week_dates(
    reference_date: str = "",
    week_starts_on: int = 0,
    timezone: str = DEFAULT_TIMEZONE
) -> dict:
    """
    Get all seven dates of the week containing the reference date.

    If reference_date is omitted, use the current date.
    week_starts_on: 0 for Monday, 6 for Sunday.
    """
    return relative_date_service.get_week_dates(
        reference_date or None,
        week_starts_on,
        timezone
    )


# ==============================================
# 4. RELATIVE DATETIME TOOL
# ==============================================

@mcp.tool()
def calculate_relative_datetime(
    amount: int,
    unit: str,
    direction: str,
    timezone: str = DEFAULT_TIMEZONE
) -> dict:
    """
    Calculate a datetime before or after now.

    Examples:
    - 5 hours ago
    - 34 hours from now
    - 90 minutes later
    """
    return relative_datetime_service.calculate_relative_datetime(
        amount, unit, direction, timezone
    )


# ==============================================
# 5. DATE RANGE TOOL
# ==============================================

@mcp.tool()
def get_date_range(
    start_date: str,
    end_date: str,
    timezone: str = DEFAULT_TIMEZONE
) -> dict:
    """
    Get information about a date range including
    its total number of calendar days.
    """
    return date_range_service.get_date_range(
        start_date, end_date, timezone
    )


# ==============================================
# 6. NATURAL LANGUAGE DATE PARSER
# ==============================================

@mcp.tool()
def parse_natural_datetime(
    expression: str,
    timezone: str = DEFAULT_TIMEZONE
) -> dict:
    """
    Parse natural-language date and time expressions.

    Examples:
    - Tomorrow at 5 PM
    - Next Monday
    - 15 days ago
    """
    return date_parser_service.parse_natural_datetime(
        expression, timezone
    )


# ==============================================
# 7. MONTH DATES TOOL
# ==============================================

@mcp.tool()
def get_month_dates(
    year: int = 0,
    month: int = 0,
    timezone: str = DEFAULT_TIMEZONE
) -> dict:
    """
    Get every date and weekday in a particular month.

    If year or month is omitted, use the current year or month.
    """
    return month_service.get_month_dates(
        year or None,
        month or None,
        timezone
    )


# ==============================================
# 8. DATE DIFFERENCE TOOL
# ==============================================

@mcp.tool()
def calculate_date_difference(
    start_date: str,
    end_date: str
) -> dict:
    """
    Calculate the number of calendar days between two dates.
    """
    return date_difference_service.calculate_date_difference(
        start_date, end_date
    )


# ==============================================
# 9. TIME DIFFERENCE TOOL
# ==============================================

@mcp.tool()
def calculate_time_difference(
    start_datetime: str,
    end_datetime: str,
    timezone: str = DEFAULT_TIMEZONE
) -> dict:
    """
    Calculate the elapsed time between two datetimes.
    """
    return time_difference_service.calculate_time_difference(
        start_datetime, end_datetime, timezone
    )


# ==============================================
# SERVER ENTRY POINT
# ==============================================

if __name__ == "__main__":
    mcp.run()
