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
    NthWeekdayInput,
)

from utils.error_handler import handle_tool_errors

# ==================================================
# MCP INITIALIZATION
# ==================================================

mcp = FastMCP("Date-Time MCP")

DEFAULT_TIMEZONE = settings.default_timezone


# ==================================================
# SERVICE INITIALIZATION
# ==================================================

current_datetime_service = CurrentDateTimeService()
timezone_service = TimezoneService()
relative_date_service = RelativeDateService()
relative_datetime_service = RelativeDateTimeService()
date_range_service = DateRangeService()
date_parser_service = DateParserService()
month_service = MonthService()
date_difference_service = DateDifferenceService()
time_difference_service = TimeDifferenceService()


# ==================================================
# 1. CURRENT DATE AND TIME TOOLS
# ==================================================


@mcp.tool()
@handle_tool_errors
def get_current_datetime(
    timezone: Annotated[
        str,
        Field(
            description=(
                "IANA timezone used to retrieve the current datetime. "
                "Examples: Asia/Kolkata, Europe/Berlin, America/New_York, UTC. "
                f"Defaults to the configured timezone: {DEFAULT_TIMEZONE}."
            ),
        ),
    ] = DEFAULT_TIMEZONE,
) -> dict:
    """
    Get the current date and time in a specified IANA timezone.

    WHEN TO USE:
    - "What is the current time in Tokyo?"
    - When another MCP needs the current date and time.
    - When multiple relative date calculations need the same reference time.

    INPUT:
    - timezone: Optional IANA timezone. Defaults to configured timezone.

    WORKING:
    - Gets the current time.
    - Converts it to the requested timezone.
    - Calculates the corresponding UTC time and offset.

    OUTPUT:
    - Local date and time.
    - Weekday.
    - ISO datetime.
    - Timezone and UTC offset.
    - Corresponding UTC datetime.

    IMPORTANT:
    - Use get_current_date when only the date is needed.
    - Use get_current_time when only the time is needed.
    - Never assume the server timezone is the user's timezone.
    """

    data = TimezoneInput.model_validate({"timezone": timezone})

    return current_datetime_service.get_current_datetime(data.timezone)


@mcp.tool()
@handle_tool_errors
def get_current_date(
    timezone: Annotated[
        str,
        Field(
            description=(
                "IANA timezone used to determine today's local date. "
                "Examples: Asia/Kolkata, Europe/Berlin or UTC. "
                f"Defaults to {DEFAULT_TIMEZONE}."
            ),
        ),
    ] = DEFAULT_TIMEZONE,
) -> dict:
    """
    Retrieve today's calendar date and weekday in a specified timezone.

    WHEN TO USE:
    - "What's today's date in Berlin?"
    - When another MCP needs today's date for a search.
    - When the current weekday is required.

    INPUT:
    - timezone: Optional IANA timezone. Defaults to configured timezone.

    WORKING:
    - Determines today's date in the selected timezone.
    - Identifies the corresponding weekday.

    OUTPUT:
    - Current date.
    - Weekday.
    - Selected timezone.

    IMPORTANT:
    - Returns a calendar date, not a timestamp.
    - Use get_current_datetime when time information is required.
    """

    data = TimezoneInput.model_validate({"timezone": timezone})

    return current_datetime_service.get_current_date(data.timezone)


@mcp.tool()
@handle_tool_errors
def get_current_time(
    timezone: Annotated[
        str,
        Field(
            description=(
                "IANA timezone used to retrieve the current local time. "
                "Examples: Asia/Kolkata, Europe/Berlin or UTC. "
                f"Defaults to {DEFAULT_TIMEZONE}."
            ),
        ),
    ] = DEFAULT_TIMEZONE,
) -> dict:
    """
    Retrieve the current local time in a specified IANA timezone.

    WHEN TO USE:
    - "What time is it in Tokyo?"
    - When another MCP needs the current local time.
    - When comparing current times across locations.

    INPUT:
    - timezone: Optional IANA timezone. Defaults to configured timezone.

    WORKING:
    - Gets the current instant.
    - Converts it into the selected timezone.
    - Determines the local UTC offset.

    OUTPUT:
    - Local time.
    - Timezone abbreviation.
    - UTC offset.
    - ISO datetime.

    IMPORTANT:
    - Returns current time, not a future or historical time.
    - Use get_current_datetime when date information is also needed.
    """

    data = TimezoneInput.model_validate({"timezone": timezone})

    return current_datetime_service.get_current_time(data.timezone)


# ==================================================
# 2. TIMEZONE INFORMATION
# ==================================================


@mcp.tool()
@handle_tool_errors
def get_timezone_info(
    timezone_name: Annotated[
        str,
        Field(
            description=(
                "Valid IANA timezone name to inspect. "
                "Examples: Asia/Kolkata, Europe/Berlin, "
                "America/New_York or UTC. "
                f"Defaults to {DEFAULT_TIMEZONE}."
            ),
        ),
    ] = DEFAULT_TIMEZONE,
) -> dict:
    """
    Retrieve timezone properties for a specified IANA timezone.

    WHEN TO USE:
    - "What is the UTC offset in Tokyo?"
    - When comparing timezone differences.
    - When checking daylight-saving information.

    INPUT:
    - timezone: Required IANA timezone identifier.

    WORKING:
    - Validates the timezone.
    - Retrieves its current local time and UTC offset.
    - Checks daylight-saving status where applicable.

    OUTPUT:
    - Timezone identifier.
    - Local datetime.
    - UTC offset.
    - Timezone abbreviation.
    - Daylight-saving status.

    IMPORTANT:
    - UTC offsets can change depending on the date.
    - Use the requested event date when evaluating historical or future timezone differences.
    """

    data = TimezoneInfoInput.model_validate({"timezone_name": timezone_name})

    return timezone_service.get_timezone_info(data.timezone_name)


# ==================================================
# 3. RELATIVE CALENDAR DATE CALCULATION
# ==================================================


@mcp.tool()
@handle_tool_errors
def calculate_relative_date(
    amount: Annotated[
        int,
        Field(
            strict=True,
            ge=0,
            le=settings.max_relative_date_amount,
            description=(
                "Number of calendar units to move from today's date. "
                "Must be a non-negative integer. "
                f"Maximum: {settings.max_relative_date_amount}."
            ),
        ),
    ],
    unit: Annotated[
        Literal["days", "weeks", "months", "years"],
        Field(
            description=(
                "Calendar unit for the calculation: days, weeks, "
                "months or years. Months and years use calendar-aware "
                "arithmetic rather than fixed day durations."
            ),
        ),
    ],
    direction: Annotated[
        Literal["past", "future"],
        Field(
            description=(
                "Calculation direction: 'past' subtracts from today's "
                "date; 'future' adds to today's date."
            ),
        ),
    ],
    timezone: Annotated[
        str,
        Field(
            description=(
                "IANA timezone used to determine today's reference date. "
                f"Defaults to {DEFAULT_TIMEZONE}."
            ),
        ),
    ] = DEFAULT_TIMEZONE,
) -> dict:
    """
    Calculate a calendar date before or after a reference date.

    WHEN TO USE:
    - "What date was 15 days ago?"
    - "What date is 3 months from now?"
    - When another MCP needs a calculated date.

    INPUT:
    - amount: Number of units.
    - unit: Days, weeks, months, or years.
    - direction: Before or after.
    - timezone: Optional timezone for determining today's date.

    WORKING:
    - Determines the reference date.
    - Applies calendar-based arithmetic.
    - Calculates the resulting date.

    OUTPUT:
    - Original date.
    - Calculated date.
    - Weekday.
    - Calculation details.

    IMPORTANT:
    - Calendar months and years are not fixed-duration periods.
    - Use calculate_relative_datetime for exact elapsed-time calculations.
    """

    data = RelativeDateInput.model_validate(
        {
            "amount": amount,
            "unit": unit,
            "direction": direction,
            "timezone": timezone,
        }
    )

    return relative_date_service.calculate_relative_date(
        data.amount,
        data.unit,
        data.direction,
        data.timezone,
    )


@mcp.tool()
@handle_tool_errors
def get_previous_n_days(
    n: Annotated[
        int,
        Field(
            strict=True,
            ge=1,
            le=settings.max_list_days,
            description=(
                "Number of previous calendar dates to retrieve. "
                "Must be between 1 and "
                f"{settings.max_list_days}. Today is excluded."
            ),
        ),
    ],
    timezone: Annotated[
        str,
        Field(
            description=(
                "IANA timezone used to determine today's date. "
                f"Defaults to {DEFAULT_TIMEZONE}."
            ),
        ),
    ] = DEFAULT_TIMEZONE,
) -> dict:
    """
    Retrieve a list of the previous N calendar dates, excluding today.

    WHEN TO USE:
    - "Show me the previous 7 dates."
    - "Get the last 30 calendar days."
    - When another MCP needs explicit date values for a historical date-based search.

    INPUT:
    - n: Number of previous dates to retrieve.
    - timezone: Timezone used to determine today's date.

    WORKING:
    - Determines today's date in the selected timezone.
    - Generates the N dates immediately preceding today.
    - Does not include today's date.
    - Returns each date with its weekday.

    OUTPUT:
    - dates: List of date and weekday objects.
    - count: Number of dates returned.
    - timezone: Selected timezone.

    IMPORTANT:
    - Returned values are calendar dates, not timestamps.
    - Dates are ordered from oldest to most recent.
    - Use get_next_n_days for upcoming dates.
    """

    data = DateListInput.model_validate({"n": n, "timezone": timezone})

    return relative_date_service.get_previous_n_days_and_dates(
        data.n,
        data.timezone,
    )


@mcp.tool()
@handle_tool_errors
def get_next_n_days(
    n: Annotated[
        int,
        Field(
            strict=True,
            ge=1,
            le=settings.max_list_days,
            description=(
                "Number of upcoming calendar dates to retrieve. "
                "Must be between 1 and "
                f"{settings.max_list_days}. Today is excluded."
            ),
        ),
    ],
    timezone: Annotated[
        str,
        Field(
            description=(
                "IANA timezone used to determine today's date. "
                f"Defaults to {DEFAULT_TIMEZONE}."
            ),
        ),
    ] = DEFAULT_TIMEZONE,
) -> dict:
    """
    Retrieve the next N calendar dates, excluding today.

    WHEN TO USE:
    - "Show me the next 7 days."
    - "Get the upcoming 30 calendar dates."
    - When another MCP needs future dates for scheduling or searches.

    INPUT:
    - n: Number of upcoming dates.
    - timezone: Timezone used to determine today's date.

    WORKING:
    - Determines today's date in the selected timezone.
    - Generates the N immediately following calendar dates.
    - Excludes today and identifies each weekday.

    OUTPUT:
    - dates: List of date and weekday objects.
    - count: Number of dates returned.
    - timezone: Selected timezone.

    IMPORTANT:
    - Returns calendar dates, not timestamps.
    - Dates are ordered from nearest to farthest.
    - Use get_previous_n_days for historical dates.
    """

    data = DateListInput.model_validate({"n": n, "timezone": timezone})

    return relative_date_service.get_next_n_days_and_dates(
        data.n,
        data.timezone,
    )


@mcp.tool()
@handle_tool_errors
def get_week_dates(
    reference_date: Annotated[
        str | None,
        Field(
            description=(
                "Reference date in YYYY-MM-DD format. "
                "The returned week contains this date. "
                "Defaults to today's date in the selected timezone."
            ),
        ),
    ] = None,
    week_starts_on: Annotated[
        int,
        Field(
            strict=True,
            ge=0,
            le=6,
            description=(
                "First weekday of the week. "
                "0 = Monday, 1 = Tuesday, ..., 6 = Sunday. "
                f"Configured default: {settings.week_starts_on}."
            ),
        ),
    ] = settings.week_starts_on,
    timezone: Annotated[
        str,
        Field(
            description=(
                "IANA timezone used when reference_date is omitted. "
                f"Defaults to {DEFAULT_TIMEZONE}."
            ),
        ),
    ] = DEFAULT_TIMEZONE,
) -> dict:
    """
    Retrieve all seven calendar dates belonging to a specified week.

    WHEN TO USE:
    - "Show me this week's dates."
    - "Get the dates for the week containing November 20."
    - When another MCP needs explicit weekly date boundaries.

    INPUT:
    - reference_date: Optional date used to identify the week.
    - week_start: Optional first weekday of the week.
    - timezone: Optional IANA timezone.

    WORKING:
    - Determines the week containing the reference date.
    - Calculates its start and end dates.
    - Generates all seven dates with weekdays.

    OUTPUT:
    - Week start and end.
    - Seven calendar dates.
    - Weekday information.
    - Selected timezone.

    IMPORTANT:
    - The reference date is included in the week.
    - Week boundaries depend on the configured week-start setting.
    """

    data = WeekDatesInput.model_validate(
        {
            "reference_date": reference_date,
            "week_starts_on": week_starts_on,
            "timezone": timezone,
        }
    )

    return relative_date_service.get_week_dates(
        data.reference_date or None,
        data.week_starts_on,
        data.timezone,
    )


@mcp.tool()
@handle_tool_errors
def get_nth_weekday(
    weekday: Annotated[
        Literal[
            "Monday",
            "Tuesday",
            "Wednesday",
            "Thursday",
            "Friday",
            "Saturday",
            "Sunday",
        ],
        Field(
            description=(
                "Full weekday name to locate. "
                "Must be one of Monday, Tuesday, Wednesday, Thursday, "
                "Friday, Saturday or Sunday."
            ),
        ),
    ],
    occurrence: Annotated[
        int,
        Field(
            strict=True,
            ge=1,
            le=53,
            description=(
                "Which matching weekday occurrence to return, "
                "counting strictly after reference_date. "
                "1 means the first upcoming occurrence; "
                "2 means the second upcoming occurrence."
            ),
        ),
    ],
    reference_date: Annotated[
        str | None,
        Field(
            default=None,
            description=(
                "Reference date in YYYY-MM-DD format. "
                "Defaults to today's date in the selected timezone."
            ),
        ),
    ] = None,
    timezone: Annotated[
        str,
        Field(
            description=(
                "IANA timezone used when reference_date is omitted. "
                f"Defaults to {DEFAULT_TIMEZONE}."
            ),
        ),
    ] = DEFAULT_TIMEZONE,
) -> dict:
    """
    Find the Nth occurrence of a specified weekday after a reference date.

    WHEN TO USE:
    - "Find the second Friday from now."
    - "What date is the third Monday after November 10?"
    - When scheduling requires a particular weekday occurrence.

    INPUT:
    - weekday: Target weekday.
    - occurrence: Required occurrence number.
    - reference_date: Optional starting date.
    - timezone: Optional IANA timezone.

    WORKING:
    - Identifies the reference date.
    - Searches subsequent calendar dates.
    - Finds the requested weekday occurrence.

    OUTPUT:
    - Calculated date.
    - Weekday.
    - Reference date.
    - Occurrence information.

    IMPORTANT:
    - The reference date itself is excluded.
    - This calculates occurrences after a reference date, not within a specified calendar month.
    """

    data = NthWeekdayInput.model_validate(
        {
            "weekday": weekday,
            "occurrence": occurrence,
            "reference_date": reference_date,
            "timezone": timezone,
        }
    )

    return relative_date_service.get_nth_weekday(
        data.weekday,
        data.occurrence,
        data.reference_date,
        data.timezone,
    )


# ==================================================
# 4. RELATIVE ELAPSED DATETIME CALCULATION
# ==================================================


@mcp.tool()
@handle_tool_errors
def calculate_relative_datetime(
    amount: Annotated[
        int,
        Field(
            strict=True,
            ge=0,
            le=settings.max_relative_datetime_seconds,
            description=(
                "Number of elapsed-time units to add or subtract. "
                "Must be a non-negative integer. "
                "The effective maximum depends on unit. "
                f"Configured maximum duration: "
                f"{settings.max_relative_datetime_seconds} seconds."
            ),
        ),
    ],
    unit: Annotated[
        Literal["seconds", "minutes", "hours", "days", "weeks"],
        Field(
            description=(
                "Elapsed-time unit: seconds, minutes, hours, days or weeks. "
                "Days represent 24-hour durations and weeks represent "
                "7-day durations, not calendar-day or calendar-week boundaries."
            ),
        ),
    ],
    direction: Annotated[
        Literal["past", "future"],
        Field(
            description=(
                "'past' subtracts the elapsed duration; "
                "'future' adds the elapsed duration."
            ),
        ),
    ],
    timezone: Annotated[
        str,
        Field(
            description=(
                "IANA timezone used for the reference and returned datetime. "
                f"Defaults to {DEFAULT_TIMEZONE}."
            ),
        ),
    ] = DEFAULT_TIMEZONE,
    reference_datetime: Annotated[
        str | None,
        Field(
            default=None,
            description=(
                "Optional ISO 8601 reference datetime. "
                "If omitted, the current datetime is used. "
                "If supplied, the calculation starts from this exact instant. "
                "For consistent multi-step calculations, pass datetime_iso "
                "from get_current_datetime."
            ),
        ),
    ] = None,
) -> dict:
    """
    Calculate a datetime before or after a reference instant.

    WHEN TO USE:
    - "What time will it be 5 hours from now?"
    - "Calculate the time 34 hours ago."
    - When another MCP needs an exact future or historical timestamp.

    INPUT:
    - amount: Number of units.
    - unit: Seconds, minutes, hours, days, or weeks.
    - direction: Before or after.
    - timezone: Optional IANA timezone.
    - reference_datetime: Optional ISO datetime.

    WORKING:
    - Determines the reference instant.
    - Applies elapsed-time arithmetic.
    - Converts the result into the requested timezone.

    OUTPUT:
    - Original datetime.
    - Calculated datetime.
    - Timezone.
    - Calculation details.

    IMPORTANT:
    - A day represents exactly 24 elapsed hours.
    - Use calculate_relative_date for calendar-based month or year calculations.
    """

    data = RelativeDateTimeInput.model_validate(
        {
            "amount": amount,
            "unit": unit,
            "direction": direction,
            "timezone": timezone,
            "reference_datetime": reference_datetime,
        }
    )

    return relative_datetime_service.calculate_relative_datetime(
        data.amount,
        data.unit,
        data.direction,
        data.timezone,
        data.reference_datetime,
    )


# ==================================================
# 5. DATE RANGE INFORMATION
# ==================================================


@mcp.tool()
@handle_tool_errors
def get_date_range(
    start_date: Annotated[
        str,
        Field(
            description=(
                "Inclusive beginning date in YYYY-MM-DD format. "
                "This date is included in the calculated range."
            ),
        ),
    ],
    end_date: Annotated[
        str,
        Field(
            description=(
                "Inclusive ending date in YYYY-MM-DD format. "
                "Must be the same as or later than start_date. "
                "The maximum allowed range is controlled by server settings."
            ),
        ),
    ],
    timezone: Annotated[
        str,
        Field(
            description=(
                "Valid IANA timezone used for the date-range operation. "
                f"Defaults to {DEFAULT_TIMEZONE}."
            ),
        ),
    ] = DEFAULT_TIMEZONE,
) -> dict:
    """
    Calculate the metadata for a date range between two calendar dates.

    WHEN TO USE:
    - "How many days are between November 1 and November 15?"
    - When another MCP needs the number of dates in a range.
    - When validating historical search boundaries.

    INPUT:
    - start_date: Range beginning in YYYY-MM-DD format.
    - end_date: Range ending in YYYY-MM-DD format.
    - timezone: Optional timezone.

    WORKING:
    - Validates the supplied dates.
    - Calculates the inclusive date count.
    - Identifies weekday information for both boundaries.

    OUTPUT:
    - Start and end dates.
    - Total inclusive days.
    - Weekdays.
    - Timezone.

    IMPORTANT:
    - Both boundary dates are included.
    - Returns range metadata, not a list of every date.
    """

    data = DateRangeInput.model_validate(
        {
            "start_date": start_date,
            "end_date": end_date,
            "timezone": timezone,
        }
    )

    return date_range_service.get_date_range(
        data.start_date,
        data.end_date,
        data.timezone,
    )


# ==================================================
# 6. NATURAL-LANGUAGE DATE AND TIME PARSER
# ==================================================


@mcp.tool()
@handle_tool_errors
def parse_natural_datetime(
    expression: Annotated[
        str,
        Field(
            min_length=1,
            max_length=500,
            description=(
                "Natural-language date or datetime expression to interpret. "
                "Examples: 'tomorrow at 7 AM', 'next Monday at 10:30 AM', "
                "'3 days from now', 'yesterday at noon'. "
                "Provide the complete expression rather than splitting "
                "its date and time into separate arguments."
            ),
        ),
    ],
    timezone: Annotated[
        str,
        Field(
            description=(
                "IANA timezone in which the expression must be interpreted. "
                "Examples: Asia/Kolkata, Europe/Berlin or UTC. "
                f"Defaults to {DEFAULT_TIMEZONE}."
            ),
        ),
    ] = DEFAULT_TIMEZONE,
) -> dict:
    """
    Convert a natural-language date or datetime expression into structured datetime values.

    WHEN TO USE:
    - "Tomorrow at 7 AM."
    - "Next Monday at 10:30."
    - "November 27 at 5 PM Tokyo time."
    - When another MCP needs a normalized datetime.

    INPUT:
    - expression: Natural-language date or datetime.
    - timezone: IANA timezone used to interpret the expression.

    WORKING:
    - Parses the supplied expression.
    - Resolves relative date and time components.
    - Applies the selected timezone.
    - Produces structured datetime information.

    OUTPUT:
    - Success status.
    - Resolved date and time.
    - Weekday.
    - ISO datetime.
    - Timezone and UTC offset.

    IMPORTANT:
    - Check success before using the result.
    - Clarify ambiguous or incomplete expressions.
    - Never silently assume a different event timezone.
    """

    data = DateParserInput.model_validate(
        {
            "expression": expression,
            "timezone": timezone,
        }
    )

    return date_parser_service.parse_natural_datetime(
        data.expression,
        data.timezone,
    )


# ==================================================
# 7. MONTH CALENDAR DATES
# ==================================================


@mcp.tool()
@handle_tool_errors
def get_month_dates(
    year: Annotated[
        int | None,
        Field(
            ge=1,
            le=9999,
            description=(
                "Calendar year to retrieve. "
                "Must be between 1 and 9999. "
                "Defaults to the current year in the selected timezone."
            ),
        ),
    ] = None,
    month: Annotated[
        int | None,
        Field(
            ge=1,
            le=12,
            description=(
                "Calendar month number: 1 = January, ..., 12 = December. "
                "Defaults to the current month in the selected timezone."
            ),
        ),
    ] = None,
    timezone: Annotated[
        str,
        Field(
            description=(
                "IANA timezone used when year or month is omitted. "
                f"Defaults to {DEFAULT_TIMEZONE}."
            ),
        ),
    ] = DEFAULT_TIMEZONE,
) -> dict:
    """
    Retrieve every calendar date and weekday belonging to a specified month.

    WHEN TO USE:
    - "Show all dates in November 2026."
    - "Get the dates in February."
    - When another MCP needs monthly date values.

    INPUT:
    - year: Optional calendar year.
    - month: Optional month number.
    - timezone: Optional IANA timezone.

    WORKING:
    - Determines the requested year and month.
    - Calculates the number of days in that month.
    - Generates every date with its weekday.

    OUTPUT:
    - Year and month.
    - Total days.
    - List of dates and weekdays.
    - Timezone.

    IMPORTANT:
    - Includes the first and last dates of the month.
    - Defaults to the current year and month when omitted.
    - Returns dates, not timestamps.
    """

    data = MonthDatesInput.model_validate(
        {
            "year": year,
            "month": month,
            "timezone": timezone,
        }
    )

    return month_service.get_month_dates(
        data.year,
        data.month,
        data.timezone,
    )


# ==================================================
# 8. CALENDAR DATE DIFFERENCE
# ==================================================


@mcp.tool()
@handle_tool_errors
def calculate_date_difference(
    start_date: Annotated[
        str,
        Field(
            description=(
                "Starting calendar date in YYYY-MM-DD format. "
                "Used as the first date in the comparison."
            ),
        ),
    ],
    end_date: Annotated[
        str,
        Field(
            description=(
                "Ending calendar date in YYYY-MM-DD format. "
                "The result's direction is determined relative to start_date."
            ),
        ),
    ],
) -> dict:
    """
    Calculate the calendar-day difference between two dates.

    WHEN TO USE:
    - "How many days are between November 1 and November 10?"
    - "How many days have passed since October 15?"
    - When calculating calendar-day intervals.

    INPUT:
    - start_date: First date in YYYY-MM-DD format.
    - end_date: Second date in YYYY-MM-DD format.

    WORKING:
    - Validates both dates.
    - Calculates the signed and absolute difference.
    - Determines complete weeks and remaining days.

    OUTPUT:
    - Start and end dates.
    - Signed difference.
    - Absolute difference.
    - Complete weeks and remaining days.
    - Direction.

    IMPORTANT:
    - Measures calendar-day differences.
    - Does not consider time-of-day or timezone offsets.
    """

    data = DateDifferenceInput.model_validate(
        {
            "start_date": start_date,
            "end_date": end_date,
        }
    )

    return date_difference_service.calculate_date_difference(
        data.start_date,
        data.end_date,
    )


# ==================================================
# 9. ELAPSED TIME DIFFERENCE
# ==================================================


@mcp.tool()
@handle_tool_errors
def calculate_time_difference(
    start_datetime: Annotated[
        str,
        Field(
            description=(
                "Starting ISO 8601 datetime. "
                "May include an explicit UTC offset, for example "
                "2026-11-06T10:00:00+05:30. "
                "If no offset is supplied, the selected timezone is used."
            ),
        ),
    ],
    end_datetime: Annotated[
        str,
        Field(
            description=(
                "Ending ISO 8601 datetime. "
                "May include an explicit UTC offset. "
                "If no offset is supplied, the selected timezone is used."
            ),
        ),
    ],
    timezone: Annotated[
        str,
        Field(
            description=(
                "IANA timezone used to interpret naive datetime inputs. "
                "Explicit offsets in the supplied datetime strings are preserved. "
                f"Defaults to {DEFAULT_TIMEZONE}."
            ),
        ),
    ] = DEFAULT_TIMEZONE,
) -> dict:
    """
    Calculate the elapsed time between two datetime values.

    WHEN TO USE:
    - "How many hours are between these two meetings?"
    - "Calculate the duration between 9 AM and 5 PM."
    - When another MCP needs an exact elapsed-time calculation.

    INPUT:
    - start_datetime: Starting ISO datetime.
    - end_datetime: Ending ISO datetime.
    - timezone: Optional timezone for naive datetime values.

    WORKING:
    - Parses both datetime values.
    - Resolves timezone information.
    - Compares instants using UTC.
    - Calculates elapsed duration.

    OUTPUT:
    - Duration in seconds.
    - Duration in minutes, hours, and days.
    - Direction and comparison result.

    IMPORTANT:
    - Explicit UTC offsets are preserved.
    - Naive datetimes require an interpretation timezone.
    - Does not calculate calendar-month differences.
    """

    data = TimeDifferenceInput.model_validate(
        {
            "start_datetime": start_datetime,
            "end_datetime": end_datetime,
            "timezone": timezone,
        }
    )

    return time_difference_service.calculate_time_difference(
        data.start_datetime,
        data.end_datetime,
        data.timezone,
    )


# ==================================================
# SERVER ENTRY POINT
# ==================================================

if __name__ == "__main__":
    mcp.run()
