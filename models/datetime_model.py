from datetime import date
from typing import Literal

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    field_validator,
    model_validator,
)

from config.settings import settings

from utils.validator import (
    validate_date,
    validate_datetime,
    validate_timezone,
)


DEFAULT_TIMEZONE = settings.default_timezone


# ==========================================
# BASE MODEL
# ==========================================

class DateTimeBaseModel(BaseModel):

    model_config = ConfigDict(
        extra="forbid",
        str_strip_whitespace=True,
    )


# ==========================================
# TIMEZONE INPUT
# ==========================================

class TimezoneInput(DateTimeBaseModel):

    timezone: str = Field(
        default=DEFAULT_TIMEZONE,
        description=(
            "IANA timezone, e.g. Asia/Kolkata, Europe/Berlin or UTC."
        ),
    )

    @field_validator("timezone")
    @classmethod
    def validate_timezone_field(cls, value: str) -> str:

        return validate_timezone(value)


# ==========================================
# DATE INPUT
# ==========================================

class DateInput(DateTimeBaseModel):

    date: str = Field(
        description="Date in YYYY-MM-DD format."
    )

    @field_validator("date")
    @classmethod
    def validate_date_field(cls, value: str) -> str:

        return validate_date(value).isoformat()


# ==========================================
# DATE RANGE INPUT
# ==========================================

class DateRangeInput(TimezoneInput):

    start_date: str = Field(
        description="Inclusive starting date in YYYY-MM-DD format."
    )

    end_date: str = Field(
        description="Inclusive ending date in YYYY-MM-DD format."
    )

    @field_validator("start_date", "end_date")
    @classmethod
    def validate_dates(cls, value: str) -> str:

        return validate_date(value).isoformat()

    @model_validator(mode="after")
    def validate_date_range(self):

        start = date.fromisoformat(self.start_date)
        end = date.fromisoformat(self.end_date)

        if end < start:
            raise ValueError(
                "End date cannot be before start date."
            )

        total_days = (end - start).days + 1

        if total_days > settings.max_date_range_days:
            raise ValueError(
                f"Date range cannot exceed "
                f"{settings.max_date_range_days} days."
            )

        return self


# ==========================================
# RELATIVE DATE MODEL
# ==========================================

class RelativeDateInput(TimezoneInput):

    amount: int = Field(
        strict=True,
        ge=0,
        le=settings.max_relative_date_amount,
        description=(
            "Number of calendar date units to move. "
            f"Maximum: {settings.max_relative_date_amount}."
        ),
    )

    unit: Literal[
        "days",
        "weeks",
        "months",
        "years",
    ] = Field(
        description="Unit of date calculation."
    )

    direction: Literal[
        "past",
        "future",
    ] = Field(
        description="Direction of calculation."
    )


# ==========================================
# DATE LIST MODEL
# ==========================================

class DateListInput(TimezoneInput):

    n: int = Field(
        strict=True,
        ge=1,
        le=settings.max_list_days,
        description=(
            "Number of previous or upcoming dates to retrieve. "
            f"Maximum: {settings.max_list_days}."
        ),
    )


# ==========================================
# WEEK DATES MODEL
# ==========================================

class WeekDatesInput(TimezoneInput):

    reference_date: str | None = Field(
        default=None,
        description=(
            "Reference date in YYYY-MM-DD format. Defaults to today."
        ),
    )

    week_starts_on: int = Field(
        default=settings.week_starts_on,
        strict=True,
        ge=0,
        le=6,
        description="First weekday: 0 = Monday, 6 = Sunday.",
    )

    @field_validator("reference_date")
    @classmethod
    def validate_reference_date(cls, value):

        if value is None:
            return None

        return validate_date(value).isoformat()


# ==========================================
# RELATIVE DATETIME MODEL
# ==========================================

class RelativeDateTimeInput(TimezoneInput):

    amount: int = Field(
        strict=True,
        ge=0,
        le=settings.max_relative_datetime_seconds,
        description=(
            "Number of time units to move. "
            "The actual maximum depends on the selected unit."
        ),
    )

    unit: Literal[
        "seconds",
        "minutes",
        "hours",
        "days",
        "weeks",
    ] = Field(
        description="Unit of elapsed-time calculation."
    )

    direction: Literal[
        "past",
        "future",
    ] = Field(
        description="Direction of calculation."
    )

    @model_validator(mode="after")
    def validate_elapsed_duration(self):

        seconds_per_unit = {
            "seconds": 1,
            "minutes": 60,
            "hours": 3600,
            "days": 86400,
            "weeks": 604800,
        }

        total_seconds = (
            self.amount * seconds_per_unit[self.unit]
        )

        if total_seconds > settings.max_relative_datetime_seconds:
            raise ValueError(
                "Requested relative datetime duration exceeds "
                f"the configured maximum of "
                f"{settings.max_relative_datetime_seconds} seconds."
            )

        return self


# ==========================================
# NATURAL LANGUAGE PARSER MODEL
# ==========================================

class DateParserInput(TimezoneInput):

    expression: str = Field(
        min_length=1,
        max_length=500,
        description=(
            "Natural language date-time expression, "
            "e.g. tomorrow at 5 PM."
        ),
    )

    @field_validator("expression")
    @classmethod
    def validate_expression(cls, value: str) -> str:

        value = value.strip()

        if not value:
            raise ValueError(
                "Date-time expression cannot be empty."
            )

        if any(ord(char) < 32 and char not in "\t" for char in value):
            raise ValueError(
                "Date-time expression cannot contain control characters."
            )

        return value


# ==========================================
# MONTH DATES MODEL
# ==========================================

class MonthDatesInput(TimezoneInput):

    year: int | None = Field(
        default=None,
        strict=True,
        ge=1,
        le=9999,
        description="Year to retrieve. Defaults to current year.",
    )

    month: int | None = Field(
        default=None,
        strict=True,
        ge=1,
        le=12,
        description="Month number from 1 to 12.",
    )


# ==========================================
# DATE DIFFERENCE MODEL
# ==========================================

class DateDifferenceInput(DateTimeBaseModel):

    start_date: str = Field(
        description="Starting date in YYYY-MM-DD format."
    )

    end_date: str = Field(
        description="Ending date in YYYY-MM-DD format."
    )

    @field_validator("start_date", "end_date")
    @classmethod
    def validate_dates(cls, value: str) -> str:

        return validate_date(value).isoformat()


# ==========================================
# TIME DIFFERENCE MODEL
# ==========================================

class TimeDifferenceInput(TimezoneInput):

    start_datetime: str = Field(
        description=(
            "Starting ISO 8601 datetime. "
            "May include an explicit UTC offset."
        ),
    )

    end_datetime: str = Field(
        description=(
            "Ending ISO 8601 datetime. "
            "May include an explicit UTC offset."
        ),
    )

    @field_validator("start_datetime", "end_datetime")
    @classmethod
    def validate_datetime_format(cls, value: str) -> str:

        validate_datetime(value)

        return value


# ==========================================
# TIMEZONE INFO MODEL
# ==========================================

class TimezoneInfoInput(DateTimeBaseModel):

    timezone_name: str = Field(
        default=DEFAULT_TIMEZONE,
        description="IANA timezone name, e.g. Asia/Kolkata.",
    )

    @field_validator("timezone_name")
    @classmethod
    def validate_timezone_name(cls, value: str) -> str:

        return validate_timezone(value)