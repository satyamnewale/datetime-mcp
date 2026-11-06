from typing import Literal
from pydantic import BaseModel, Field, ConfigDict, field_validator, model_validator

from datetime import datetime, date
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

DEFAULT_TIMEZONE = "Asia/Kolkata"

# -------------------------------
# Base Models
# -------------------------------


class DateTimeBaseModel(BaseModel):
    """
    Common configuration and validation
    shared by all datetime input models.
    """

    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    @field_validator("timezone", check_fields=False)
    @classmethod
    def validate_timezone(cls, value: str) -> str:
        try:
            ZoneInfo(value)
        except (ZoneInfoNotFoundError, ValueError):
            raise ValueError(f"Invalid or unavailable IANA timezone: {value}")

        return value


# -------------------------------
# Common Input Models
# -------------------------------


class TimezoneInput(DateTimeBaseModel):

    timezone: str = Field(
        default=DEFAULT_TIMEZONE,
        description="IANA timezone, eg. Asia/Kolkata, Europe/London or UTC.",
    )


class DateInput(DateTimeBaseModel):

    date: str = Field(description="Date in ISO 8601 format: YYYY-MM-DD.")

    @field_validator("date")
    @classmethod
    def validate_date_format(cls, value: str) -> str:

        try:
            date.fromisoformat(value)

        except ValueError:
            raise ValueError("Invalid date. Expected YYYY-MM-DD.")

        return value


class DateRangeInput(DateTimeBaseModel):
    start_date: str = Field(
        description="Inclusive starting date in format: YYYY-MM-DD."
    )
    end_date: str = Field(description="Inclusive ending date in format: YYYY-MM-DD.")
    timezone: str = Field(
        default=DEFAULT_TIMEZONE,
        description="IANA timezone used for date range, eg. Asia/Kolkata, Europe/London or UTC.",
    )

    @field_validator("start_date", "end_date")
    @classmethod
    def validate_date_format(cls, value: str) -> str:

        try:
            date.fromisoformat(value)

        except ValueError:
            raise ValueError("Invalid date. Expected YYYY-MM-DD.")

        return value

    @model_validator(mode="after")
    def valide_date_order(self):

        start = date.fromisoformat(self.start_date)
        end = date.fromisoformat(self.end_date)

        if end < start:
            raise ValueError("End date cannot be before start date")

        return self


# -------------------------------
# Relative Date Models
# -------------------------------


class RelativeDateInput(TimezoneInput):
    amount: int = Field(strict=True, ge=0, description="number of date units to move")
    unit: Literal["days", "weeks", "months", "years"] = Field(
        description="unit od date calculations"
    )
    direction: Literal["past", "future"] = Field(
        description="Direction of calculation: past or future."
    )


class DateListInput(TimezoneInput):
    n: int = Field(
        ge=1,
        le=366,
        strict=True,
        description="Number of previous or upcoming days to retrieve.",
    )


class WeekDatesInput(TimezoneInput):

    reference_date: str | None = Field(
        default=None,
        description="Reference date in YYYY-MM-DD format. Defaults to today.",
    )

    week_starts_on: int = Field(
        default=0,
        strict=True,
        ge=0,
        le=6,
        description="First weekday: 0 = Monday, 6 = Sunday.",
    )

    @field_validator("reference_date")
    @classmethod
    def validate_reference_date(cls, value):
        if value is None:
            return value

        try :
            date.fromisoformat(value)

        except ValueError:
            raise ValueError("Invalid date. Expected YYYY-MM-DD.")

        return value


# -------------------------------
# Relative Datetime Models
# -------------------------------


class RelativeDateTimeInput(TimezoneInput):
    amount: int = Field(
        strict=True,
        ge=0,
        description="Number of time units to move."
    )

    unit: Literal[
        "seconds",
        "minutes",
        "hours",
        "days",
        "weeks"
    ] = Field(
        description="Unit of datetime calculation."
    )

    direction: Literal[
        "past",
        "future"
    ] = Field(
        description="Direction of calculation: past or future."
    )


# -------------------------------
# Natural Language Parser
# -------------------------------


class DateParserInput(TimezoneInput):
    expression: str = Field(
        min_length=1,
        max_length=500,
        description="Natural language date-time expression, e.g. tomorrow at 5 PM."
    )

    @field_validator("expression")
    @classmethod
    def validate_expression(cls, value : str) -> str :

        if not value.strip():
            raise ValueError("date-time expression cannot be empty.")

        return value.strip()

# -------------------------------
# Month Dates
# -------------------------------


class MonthDatesInput(TimezoneInput):
    year: int | None = Field(
        default=None,
        strict=True,
        ge=1,
        le=9999,
        description="Year to retrieve. Defaults to the current year."
    )

    month: int | None = Field(
        default=None,
        strict=True,
        ge=1,
        le=12,
        description="Month number from 1 to 12. Defaults to the current month."
    )


# -------------------------------
# Difference Calculations
# -------------------------------


class DateDifferenceInput(DateTimeBaseModel):
    start_date: str = Field(
        description="Starting date in YYYY-MM-DD format."
    )

    end_date: str = Field(
        description="Ending date in YYYY-MM-DD format."
    )

    @field_validator("start_date", "end_date")
    @classmethod
    def validate_date_format(cls, value : str) -> str:

        try :
            date.fromisoformat(value)

        except ValueError:
            raise ValueError("Invalid date. Expected YYYY-MM-DD.")

        return value

# ==========================================
# TIME DIFFERENCE MODEL
# ==========================================

class TimeDifferenceInput(TimezoneInput):
    start_datetime: str = Field(
        description="Starting ISO 8601 datetime."
    )

    end_datetime: str = Field(
        description="Ending ISO 8601 datetime."
    )

    @field_validator("start_datetime", "end_datetime")
    @classmethod
    def validate_datetime_format(cls, value: str) -> str:

        try:
            datetime.fromisoformat(value)

        except ValueError:
            raise ValueError(
                "Invalid datetime. Expected ISO 8601 format."
            )

        return value
