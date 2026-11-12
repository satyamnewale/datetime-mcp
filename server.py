
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
    Retrieve the current date and time as a timezone-aware datetime.

    WHEN TO USE:
    - When both the current date and current time are required.
    - Before performing multiple relative calculations that should share
      one consistent reference instant.
    - When another MCP workflow needs the current datetime as an input.

    INPUT:
    - timezone: IANA timezone name. Defaults to the server configuration.

    WORKING:
    - Retrieves the current instant.
    - Interprets and formats it in the requested timezone.
    - Also calculates its corresponding UTC datetime.

    OUTPUT:
    Returns date, time, weekday, datetime_iso, timezone, utc_offset,
    and utc_datetime.

    IMPORTANT:
    - datetime_iso is the timezone-aware ISO 8601 representation.
    - Reuse datetime_iso as a reference when subsequent calculations
      must use exactly the same starting instant.
    - Do not use this tool to interpret expressions such as
      "tomorrow at 7 AM"; use parse_natural_datetime instead.
    """ 

    data = TimezoneInput.model_validate({"timezone": timezone})

    return current_datetime_service.get_current_datetime(
        data.timezone
    )


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
    - When only today's date or weekday is required.
    - As a reference for calendar-date calculations.
    - When the current time of day is not relevant.

    INPUT:
    - timezone: IANA timezone used to determine the local date.
      Defaults to the server's configured timezone.

    WORKING:
    - Retrieves the current date in the selected timezone.
    - Determines its weekday.
    - Does not return the current time.

    OUTPUT:
    Returns:
    - date: Date formatted using the configured date format.
    - day: Full weekday name.
    - timezone: Selected IANA timezone.

    IMPORTANT:
    - Use get_current_datetime when both date and time are required.
    - Use parse_natural_datetime when interpreting a natural-language
      date expression.
    """ 

    data = TimezoneInput.model_validate({"timezone": timezone})

    return current_datetime_service.get_current_date(
        data.timezone
    )


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
    Retrieve the current local time and its timezone information.

    WHEN TO USE:
    - When the user asks for the current time in a location.
    - When only the time and UTC offset are needed.
    - When a current timestamp is needed without separately requesting
      the formatted date.

    INPUT:
    - timezone: IANA timezone name. Defaults to the server configuration.

    WORKING:
    - Retrieves one current timezone-aware datetime snapshot.
    - Extracts the local time, UTC offset and ISO datetime.

    OUTPUT:
    Returns:
    - time: Local time in the configured time format.
    - timezone: Selected timezone.
    - utc_offset: Current UTC offset.
    - datetime_iso: Complete timezone-aware ISO 8601 datetime.

    IMPORTANT:
    - Use get_current_datetime when the formatted date and weekday
      are also required.
    - This tool does not parse a requested future or past time.
    """ 

    data = TimezoneInput.model_validate({"timezone": timezone})

    return current_datetime_service.get_current_time(
        data.timezone
    )


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
    Retrieve timezone properties and current timezone information.

    WHEN TO USE:
    - When the user asks about a timezone's UTC offset.
    - When comparing timezone information between locations.
    - When checking whether daylight-saving time is active.
    - When timezone abbreviation or current UTC conversion is required.

    INPUT:
    - timezone_name: Valid IANA timezone identifier.

    WORKING:
    - Resolves the supplied timezone.
    - Retrieves its current local datetime.
    - Determines its UTC offset, timezone abbreviation and DST status.
    - Calculates the corresponding UTC datetime.

    OUTPUT:
    Returns:
    - timezone: Resolved timezone name.
    - utc_offset: Current UTC offset without the colon.
    - utc_offset_name: Current timezone abbreviation.
    - is_dst: Whether daylight-saving time is active.
    - current_datetime: Current local ISO datetime.
    - utc_datetime: Corresponding UTC datetime.

    IMPORTANT:
    - UTC offsets and DST status can change depending on the date.
    - This tool reports current timezone properties, not a complete
      historical or future timezone transition schedule.
    """ 

    data = TimezoneInfoInput.model_validate(
        {"timezone_name": timezone_name}
    )

    return timezone_service.get_timezone_info(
        data.timezone_name
    )


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
    Calculate a calendar date before or after today's date.

    WHEN TO USE:
    - "15 days ago"
    - "2 weeks from today"
    - "3 months from now"
    - "1 year from today"

    INPUT:
    - amount: Number of calendar units.
    - unit: days, weeks, months or years.
    - direction: past or future.
    - timezone: Timezone used to determine today's date.

    WORKING:
    - Uses today's date in the selected timezone as the reference.
    - Applies calendar-aware date arithmetic.
    - Month and year calculations account for calendar boundaries.

    OUTPUT:
    Returns original_date, result_date, day, amount, unit, direction,
    timezone and calculation_type.

    IMPORTANT:
    - This calculates a calendar date, not an exact elapsed duration.
    - Use calculate_relative_datetime for expressions involving
      hours, minutes, seconds or exact elapsed durations.
    - Use parse_natural_datetime for complete natural-language
      expressions containing a date and time.
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
    - When another MCP needs explicit date values for a historical
      date-based search.

    INPUT:
    - n: Number of previous dates to retrieve.
    - timezone: Timezone used to determine today's date.

    WORKING:
    - Determines today's date in the selected timezone.
    - Generates the N dates immediately preceding today.
    - Does not include today's date.
    - Returns each date with its weekday.

    OUTPUT:
    Returns:
    - dates: List of date and weekday objects.
    - count: Number of dates returned.
    - timezone: Selected timezone.

    IMPORTANT:
    - The returned dates are calendar dates, not timestamps.
    - The list is ordered from oldest to most recent.
    - Use get_next_n_days for upcoming dates.
    """ 

    data = DateListInput.model_validate(
        {"n": n, "timezone": timezone}
    )

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
    Retrieve a list of the next N calendar dates, excluding today.

    WHEN TO USE:
    - "Show me the next 7 dates."
    - "List the upcoming 30 calendar days."
    - When another MCP needs explicit upcoming dates for searches
      or scheduling workflows.

    INPUT:
    - n: Number of upcoming dates to retrieve.
    - timezone: Timezone used to determine today's date.

    WORKING:
    - Determines today's date in the selected timezone.
    - Generates the N calendar dates immediately following today.
    - Does not include today's date.
    - Returns each date with its weekday.

    OUTPUT:
    Returns:
    - dates: List of date and weekday objects.
    - count: Number of dates returned.
    - timezone: Selected timezone.

    IMPORTANT:
    - The returned dates are ordered from nearest to farthest.
    - Use calculate_relative_date when only one calculated date
      is required.
    - Use get_previous_n_days for historical dates.
    """ 

    data = DateListInput.model_validate(
        {"n": n, "timezone": timezone}
    )

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
    Retrieve all seven calendar dates in the week containing a reference date.

    WHEN TO USE:
    - "Show me this week's dates."
    - "Get the dates for the week containing November 6."
    - When a weekly email or calendar search needs explicit date boundaries.

    INPUT:
    - reference_date: Optional YYYY-MM-DD reference date.
    - week_starts_on: Week-start index from 0 (Monday) to 6 (Sunday).
    - timezone: Timezone used when the reference date is omitted.

    WORKING:
    - Uses the supplied reference date or today's date.
    - Finds the beginning of the week according to week_starts_on.
    - Generates seven consecutive dates, including the reference date.

    OUTPUT:
    Returns:
    - week_start: First date of the week.
    - week_end: Last date of the week.
    - dates: Seven date and weekday objects.
    - week_starts_on: Selected week-start index.
    - timezone: Selected timezone.

    IMPORTANT:
    - The reference date is included in the returned week.
    - This tool returns the week containing a date; it does not
      calculate the next occurrence of a particular weekday.
    - Use get_nth_weekday for requests such as "second Friday from now".
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
    Find the Nth occurrence of a weekday strictly after a reference date.

    WHEN TO USE:
    - "The second Friday from now."
    - "The third Monday after November 10."
    - "Find the next upcoming Wednesday."
    - When a weekday occurrence must be calculated precisely.

    INPUT:
    - weekday: Full weekday name.
    - occurrence: Positive occurrence number from 1 to 53.
    - reference_date: Optional YYYY-MM-DD starting date.
    - timezone: Timezone used when reference_date is omitted.

    WORKING:
    - Uses the supplied reference date or today's date.
    - Finds the first matching weekday strictly after that date.
    - Advances by seven-day intervals to locate the requested occurrence.

    OUTPUT:
    Returns:
    - reference_date: Date used as the calculation reference.
    - requested_weekday: Requested weekday.
    - occurrence: Requested occurrence number.
    - result_date: Calculated date.
    - day: Weekday of the result.
    - timezone: Selected timezone.
    - calculation_type: nth_weekday.

    IMPORTANT:
    - The reference date itself is always excluded.
    - Occurrence 1 means the first matching weekday AFTER the reference.
    - This is not the Nth weekday within a calendar month.
    - For example, "second Friday of November" requires a monthly
      calendar interpretation, not simply occurrence=2 from today.
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
    Calculate a datetime before or after a reference instant using elapsed time.

    WHEN TO USE:
    - "3 hours from now."
    - "30 minutes ago."
    - "72 hours after this timestamp."
    - When an exact elapsed duration is required.

    INPUT:
    - amount: Number of units.
    - unit: seconds, minutes, hours, days or weeks.
    - direction: past or future.
    - timezone: IANA timezone for the result.
    - reference_datetime: Optional ISO 8601 reference instant.

    WORKING:
    - Uses the current datetime when no reference is supplied.
    - Otherwise uses the supplied reference datetime.
    - Performs elapsed-time arithmetic using UTC internally.
    - Converts the result back to the requested timezone.

    OUTPUT:
    Returns formatted datetime fields, original_datetime,
    result_datetime, result_date, result_time, timezone,
    utc_datetime, amount, unit, direction, calculation_type
    and reference_supplied.

    IMPORTANT:
    - A day means exactly 24 elapsed hours.
    - A week means exactly 168 elapsed hours.
    - Use calculate_relative_date for calendar-based months,
      years, weeks or days.
    - Use parse_natural_datetime for natural-language expressions
      such as "tomorrow at 7 AM".
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
    Retrieve information about an inclusive calendar date range.

    WHEN TO USE:
    - "How many days are there between November 1 and November 30?"
    - "Get the weekdays at the beginning and end of this date range."
    - When another MCP workflow needs date-range metadata.

    INPUT:
    - start_date: Inclusive start date in YYYY-MM-DD format.
    - end_date: Inclusive end date in YYYY-MM-DD format.
    - timezone: Valid IANA timezone.

    WORKING:
    - Validates both dates and the selected timezone.
    - Ensures the ending date does not precede the starting date.
    - Calculates the total number of calendar dates, including
      both boundaries.
    - Enforces the configured maximum date-range length.

    OUTPUT:
    Returns:
    - start_date and end_date.
    - total_days: Inclusive number of dates.
    - start_day and end_day: Weekday names.
    - timezone: Selected timezone.

    IMPORTANT:
    - Both boundary dates are included in total_days.
    - This tool does not return every date in the range.
    - Use get_week_dates or get_month_dates when a complete
      list of dates is required.
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
    Convert a natural-language date or datetime expression into structured values.

    WHEN TO USE:
    - This is the primary tool for interpreting human-readable date/time input.
    - "Tomorrow at 7 AM."
    - "Next Monday at 10:30 AM."
    - "3 days from now."
    - "Yesterday at noon."
    - When a downstream MCP requires an exact date or datetime.

    INPUT:
    - expression: Complete natural-language date/time expression.
    - timezone: IANA timezone used for interpretation.

    WORKING:
    - Interprets the expression using the selected timezone.
    - Uses the current timezone-aware datetime as its relative reference.
    - Converts a successfully interpreted expression into structured
      date and time information.
    - Does not perform calendar event creation or email searching.

    OUTPUT ON SUCCESS:
    Returns:
    - success: True.
    - original_expression: Original supplied expression.
    - date: Resolved calendar date.
    - time: Resolved local time.
    - day: Weekday name.
    - datetime_iso: Timezone-aware ISO 8601 datetime.
    - timezone: Selected timezone.
    - utc_offset: UTC offset of the resolved datetime.

    OUTPUT ON PARSE FAILURE:
    Returns success=False and an error message explaining that the
    expression could not be interpreted.

    IMPORTANT:
    - Always inspect success before using the result.
    - For downstream scheduling, use datetime_iso rather than
      reconstructing the date and time manually.
    - If interpretation is unsuccessful or ambiguous, ask the user
      for clarification rather than inventing a date or time.
    - Use calculate_relative_date or calculate_relative_datetime
      for explicit arithmetic operations instead.
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
    Retrieve every calendar date and weekday in a specified month.

    WHEN TO USE:
    - "Show me all dates in November 2026."
    - "List the dates in the current month."
    - When a monthly calendar needs to be generated or inspected.

    INPUT:
    - year: Optional four-digit calendar year.
    - month: Optional month number from 1 to 12.
    - timezone: Timezone used to determine the current year/month
      when either is omitted.

    WORKING:
    - Uses supplied year and month values.
    - Defaults omitted values independently to the current year
      and current month.
    - Determines the number of days in the selected month.
    - Generates every date and its weekday.

    OUTPUT:
    Returns:
    - year: Selected year.
    - month: Selected month number.
    - month_name: Full month name.
    - total_days: Number of dates in the month.
    - dates: Complete list of date and weekday objects.
    - timezone: Selected timezone.

    IMPORTANT:
    - Supplying only a year uses the current month.
    - Supplying only a month uses the current year.
    - Use get_week_dates for a seven-day week rather than a full month.
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
    - "How far away is December 31 from today?"
    - When a signed calendar-day difference is needed.

    INPUT:
    - start_date: Starting date in YYYY-MM-DD format.
    - end_date: Ending date in YYYY-MM-DD format.

    WORKING:
    - Validates both calendar dates.
    - Calculates end_date minus start_date.
    - Calculates the absolute difference and its week/day breakdown.
    - Does not use time-of-day or timezone information.

    OUTPUT:
    Returns:
    - start_date and end_date.
    - difference_days: Absolute calendar-day difference.
    - signed_difference_days: Signed difference from start to end.
    - difference_weeks: Complete weeks in the absolute difference.
    - remaining_days: Remaining days after complete weeks.
    - direction: future, past or same_date.

    IMPORTANT:
    - A result of zero means both dates are the same.
    - signed_difference_days is positive when end_date is later
      and negative when end_date is earlier.
    - Use calculate_time_difference for timestamp comparisons.
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
    Calculate the elapsed time between two ISO 8601 datetime values.

    WHEN TO USE:
    - "How many hours are between these two timestamps?"
    - "Calculate the duration between 10 AM and 12:30 PM."
    - When comparing timestamps with timezone offsets.
    - When a duration in seconds, minutes, hours or days is required.

    INPUT:
    - start_datetime: Starting ISO 8601 datetime.
    - end_datetime: Ending ISO 8601 datetime.
    - timezone: Timezone used for datetime values without offsets.

    WORKING:
    - Parses and validates both datetime values.
    - Applies the selected timezone to naive datetime values.
    - Preserves explicit timezone offsets.
    - Converts both instants to UTC for elapsed-time calculation.
    - Calculates the absolute duration and its direction.

    OUTPUT:
    Returns:
    - start_datetime and end_datetime.
    - start_utc and end_utc.
    - difference_seconds.
    - difference_minutes.
    - difference_hours.
    - difference_days.
    - direction: future, past or same_time.
    - duration: Structured days, hours, minutes and seconds.
    - timezone: Selected timezone.

    IMPORTANT:
    - The direction describes the relationship of end_datetime
      to start_datetime.
    - Duration values are absolute; use direction to understand
      which timestamp is later.
    - Explicit UTC offsets are not replaced by the selected timezone.
    - Use calculate_date_difference for date-only comparisons.
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
