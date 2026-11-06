from fastmcp import FastMCP

from config.settings import settings

from typing import Annotated, Literal
from pydantic import Field

from services.current_datetime import CurrentDateTimeService
from services.timezone_service import TimezoneService
from services.relative_date import RelativeDateService
from services.relative_datetime import RelativeDateTimeService
from services.date_range import DateRangeService
from services.date_parser import DateParserService
from services.month_service import MonthService
from services.date_difference import DateDifferenceService
from services.time_difference import TimeDifferenceService

from models.datetime_model import (
    TimezoneInput,
    TimezoneInfoInput,
    RelativeDateInput,
    DateListInput,
    WeekDatesInput,
    RelativeDateTimeInput,
    DateRangeInput,
    DateParserInput,
    MonthDatesInput,
    DateDifferenceInput,
    TimeDifferenceInput,
)

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
#  current_datetime.py from services
@mcp.tool()  # checked -> date, day, time
def get_current_datetime(
    timezone: Annotated[
        str, Field(description="IANA timezone, e.g. Asia/Kolkata or Europe/Berlin.")
    ] = DEFAULT_TIMEZONE,
) -> dict:
    """
    Get the current date, time, weekday and UTC information
    for a specified timezone.
    """

    data = TimezoneInput.model_validate({"timezone": timezone})
    return current_datetime_service.get_current_datetime(data.timezone)


@mcp.tool()  # checked -> return date day
def get_current_date(
    timezone: Annotated[
        str, Field(description="IANA timezone, e.g. Asia/Kolkata or Europe/Berlin.")
    ] = DEFAULT_TIMEZONE,
) -> dict:
    """
    Get today's date and weekday in a specified timezone.
    """

    data = TimezoneInput.model_validate({"timezone": timezone})
    return current_datetime_service.get_current_date(data.timezone)


@mcp.tool()  # checked -> time timezone
def get_current_time(
    timezone: Annotated[
        str, Field(description="IANA timezone, e.g. Asia/Kolkata or Europe/Berlin.")
    ] = DEFAULT_TIMEZONE,
) -> dict:
    """
    Get the current local time and UTC offset.
    """

    data = TimezoneInput.model_validate({"timezone": timezone})
    return current_datetime_service.get_current_time(data.timezone)


# ==============================================
# 2. TIMEZONE TOOL
# ==============================================
# timezome_service.py
@mcp.tool()  # checked -> timezon name, utc offset, utc offset name
def get_timezone_info(
    timezone_name: Annotated[
        str, Field(description="IANA timezone name to inspect, e.g. Asia/Kolkata.")
    ] = DEFAULT_TIMEZONE,
) -> dict:
    """
    Get timezone information including UTC offset,
    abbreviation and daylight-saving status.
    """

    data = TimezoneInfoInput.model_validate({"timezone_name": timezone_name})
    return timezone_service.get_timezone_info(data.timezone_name)


# ==============================================
# 3. RELATIVE DATE TOOLS
# ==============================================


@mcp.tool()
def calculate_relative_date(
    amount: Annotated[
        int, Field(strict=True, ge=0, description="Number of date units.")
    ],
    unit: Annotated[
        Literal["days", "weeks", "months", "years"],
        Field(description="Unit of calculation."),
    ],
    direction: Annotated[
        Literal["past", "future"],
        Field(description="Whether to calculate into the past or future."),
    ],
    timezone: Annotated[
        str, Field(description="IANA timezone used for the calculation.")
    ] = DEFAULT_TIMEZONE,
) -> dict:
    """
    Calculate a date in the past or future.

    Examples:
    - 15 days ago
    - 40 days later
    - 2 months ago
    """

    data = RelativeDateInput.model_validate(
        {"amount": amount, "unit": unit, "direction": direction, "timezone": timezone}
    )
    return relative_date_service.calculate_relative_date(
        data.amount, data.unit, data.direction, data.timezone
    )


@mcp.tool()
def get_previous_n_days(
    n: Annotated[
        int,
        Field(
            strict=True,
            ge=1,
            le=366,
            description="Number of previous days to retrieve. Range: 1-366.",
        ),
    ],
    timezone: Annotated[str, Field(description="IANA timezone.")] = DEFAULT_TIMEZONE,
) -> dict:
    """
    Get the dates of the previous N days, excluding today.
    """

    data = DateListInput.model_validate({"n": n, "timezone": timezone})
    return relative_date_service.get_previous_n_days_and_dates(data.n, data.timezone)


@mcp.tool()
def get_next_n_days(
    n: Annotated[
        int,
        Field(
            strict=True,
            ge=1,
            le=366,
            description="Number of upcoming days to retrieve. Range: 1-366.",
        ),
    ],
    timezone: Annotated[str, Field(description="IANA timezone.")] = DEFAULT_TIMEZONE,
) -> dict:
    """
    Get the dates of the next N days, excluding today.
    """

    data = DateListInput.model_validate({"n": n, "timezone": timezone})
    return relative_date_service.get_next_n_days_and_dates(data.n, data.timezone)


@mcp.tool()
def get_week_dates(
    reference_date: Annotated[
        str | None,
        Field(description="Reference date in YYYY-MM-DD format. Defaults to today."),
    ] = None,
    week_starts_on: Annotated[
        int,
        Field(
            strict=True,
            ge=0,
            le=6,
            description="Week starting day: 0 = Monday, 6 = Sunday.",
        ),
    ] = 0,
    timezone: Annotated[str, Field(description="IANA timezone.")] = DEFAULT_TIMEZONE,
) -> dict:
    """
    Get all seven dates of the week containing the reference date.

    If reference_date is omitted, use the current date.
    week_starts_on: 0 for Monday, 6 for Sunday.
    """

    data = WeekDatesInput.model_validate(
        {
            "reference_date": reference_date,
            "week_starts_on": week_starts_on,
            "timezone": timezone,
        }
    )

    return relative_date_service.get_week_dates(
        data.reference_date or None, data.week_starts_on, data.timezone
    )


# ==============================================
# 4. RELATIVE DATETIME TOOL
# ==============================================


@mcp.tool()
def calculate_relative_datetime(
    amount: Annotated[
        int, Field(strict=True, ge=0, description="Number of time units.")
    ],
    unit: Annotated[
        Literal["seconds", "minutes", "hours", "days", "weeks"],
        Field(description="Unit of datetime calculation."),
    ],
    direction: Annotated[
        Literal["past", "future"],
        Field(description="Whether to calculate into the past or future."),
    ],
    timezone: Annotated[str, Field(description="IANA timezone.")] = DEFAULT_TIMEZONE,
) -> dict:
    """
    Calculate a datetime before or after now.

    Examples:
    - 5 hours ago
    - 34 hours from now
    - 90 minutes later
    """

    data = RelativeDateTimeInput.model_validate(
        {"amount": amount, "unit": unit, "direction": direction, "timezone": timezone}
    )

    return relative_datetime_service.calculate_relative_datetime(
        data.amount, data.unit, data.direction, data.timezone
    )


# ==============================================
# 5. DATE RANGE TOOL
# ==============================================


@mcp.tool()
def get_date_range(
    start_date: Annotated[
        str, Field(description="Inclusive start date in YYYY-MM-DD format.")
    ],
    end_date: Annotated[
        str,
        Field(
            description="Inclusive end date in YYYY-MM-DD format. Must not precede start date."
        ),
    ],
    timezone: Annotated[str, Field(description="IANA timezone.")] = DEFAULT_TIMEZONE,
) -> dict:
    """
    Get information about a date range including
    its total number of calendar days.
    """

    data = DateRangeInput.model_validate(
        {"start_date": start_date, "end_date": end_date, "timezone": timezone}
    )

    return date_range_service.get_date_range(
        data.start_date, data.end_date, data.timezone
    )


# ==============================================
# 6. NATURAL LANGUAGE DATE PARSER
# ==============================================


@mcp.tool()
def parse_natural_datetime(
    expression: Annotated[
        str,
        Field(
            min_length=1,
            max_length=500,
            description="Natural-language date/time expression, e.g. tomorrow at 5 PM.",
        ),
    ],
    timezone: Annotated[
        str, Field(description="IANA timezone used to interpret the expression.")
    ] = DEFAULT_TIMEZONE,
) -> dict:
    """
    Parse natural-language date and time expressions.

    Examples:
    - Tomorrow at 5 PM
    - Next Monday
    - 15 days ago
    """
    data = DateParserInput.model_validate(
        {"expression": expression, "timezone": timezone}
    )

    return date_parser_service.parse_natural_datetime(data.expression, data.timezone)


# ==============================================
# 7. MONTH DATES TOOL
# ==============================================


@mcp.tool()
def get_month_dates(
    year: Annotated[
        int | None,
        Field(ge=1, le=9999, description="Year to retrieve. Defaults to current year."),
    ] = None,
    month: Annotated[
        int | None,
        Field(
            ge=1,
            le=12,
            description="Month number from 1 to 12. Defaults to current month.",
        ),
    ] = None,
    timezone: Annotated[str, Field(description="IANA timezone.")] = DEFAULT_TIMEZONE,
) -> dict:
    """
    Get every date and weekday in a particular month.

    If year or month is omitted, use the current year or month.
    """
    data = MonthDatesInput.model_validate(
        {"year": year, "month": month, "timezone": timezone}
    )

    return month_service.get_month_dates(data.year, data.month, data.timezone)


# ==============================================
# 8. DATE DIFFERENCE TOOL
# ==============================================


@mcp.tool()
def calculate_date_difference(
    start_date: Annotated[
        str, Field(description="Starting date in YYYY-MM-DD format.")
    ],
    end_date: Annotated[str, Field(description="Ending date in YYYY-MM-DD format.")],
) -> dict:
    """
    Calculate the number of calendar days between two dates.
    """
    data = DateDifferenceInput.model_validate(
        {"start_date": start_date, "end_date": end_date}
    )

    return date_difference_service.calculate_date_difference(
        data.start_date, data.end_date
    )


# ==============================================
# 9. TIME DIFFERENCE TOOL
# ==============================================


@mcp.tool()
def calculate_time_difference(
    start_datetime: Annotated[str, Field(description="Starting ISO 8601 datetime.")],
    end_datetime: Annotated[str, Field(description="Ending ISO 8601 datetime.")],
    timezone: Annotated[
        str, Field(description="Timezone used when datetime inputs have no UTC offset.")
    ] = DEFAULT_TIMEZONE,
) -> dict:
    """
    Calculate the elapsed time between two datetimes.
    """
    data = TimeDifferenceInput.model_validate(
        {
            "start_datetime": start_datetime,
            "end_datetime": end_datetime,
            "timezone": timezone,
        }
    )

    return time_difference_service.calculate_time_difference(
        data.start_datetime, data.end_datetime, data.timezone
    )


# ==============================================
# SERVER ENTRY POINT
# ==============================================

if __name__ == "__main__":
    mcp.run()
