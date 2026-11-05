
from typing import Literal
from pydantic import BaseModel, Field, ConfigDict


# -------------------------------
# Common Models
# -------------------------------

class TimezoneInput(BaseModel):
    timezone: str = Field(
        default="Asia/Kolkata",
        description="IANA timezone, e.g. Asia/Kolkata"
    )


class DateInput(BaseModel):
    date: str = Field(
        description="Date in YYYY-MM-DD format"
    )


class DateRangeInput(BaseModel):
    start_date: str
    end_date: str
    timezone: str = "Asia/Kolkata"


# -------------------------------
# Relative Date Models
# -------------------------------

class RelativeDateInput(BaseModel):
    amount: int = Field(ge=0)
    unit: Literal["days", "weeks", "months", "years"]
    direction: Literal["past", "future"]
    timezone: str = "Asia/Kolkata"


class DateListInput(BaseModel):
    n: int = Field(ge=1, le=366)
    timezone: str = "Asia/Kolkata"


class WeekDatesInput(BaseModel):
    reference_date: str | None = None
    week_starts_on: int = Field(default=0, ge=0, le=6)
    timezone: str = "Asia/Kolkata"


# -------------------------------
# Relative Datetime Models
# -------------------------------

class RelativeDateTimeInput(BaseModel):
    amount: int = Field(ge=0)
    unit: Literal[
        "seconds",
        "minutes",
        "hours",
        "days",
        "weeks"
    ]
    direction: Literal["past", "future"]
    timezone: str = "Asia/Kolkata"


# -------------------------------
# Natural Language Parser
# -------------------------------

class DateParserInput(BaseModel):
    expression: str = Field(min_length=1)
    timezone: str = "Asia/Kolkata"


# -------------------------------
# Month Dates
# -------------------------------

class MonthDatesInput(BaseModel):
    year: int | None = Field(default=None, ge=1, le=9999)
    month: int | None = Field(default=None, ge=1, le=12)
    timezone: str = "Asia/Kolkata"


# -------------------------------
# Difference Calculations
# -------------------------------

class DateDifferenceInput(BaseModel):
    start_date: str
    end_date: str


class TimeDifferenceInput(BaseModel):
    start_datetime: str
    end_datetime: str
    timezone: str = "Asia/Kolkata"
