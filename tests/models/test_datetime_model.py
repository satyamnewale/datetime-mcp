import pytest

from pydantic import ValidationError

from models.datetime_model import (
    TimezoneInput,
    RelativeDateInput,
    DateListInput,
    DateRangeInput,
    WeekDatesInput,
    DateParserInput,
    MonthDatesInput,
    TimeDifferenceInput,
)


@pytest.mark.model
def test_valid_timezone():
    result = TimezoneInput(timezone="Asia/Kolkata")
    assert result.timezone == "Asia/Kolkata"


@pytest.mark.model
def test_invalid_timezone():
    with pytest.raises(ValidationError):
        TimezoneInput(timezone="Invalid/Zone")


@pytest.mark.model
def test_valid_relative_date():
    result = RelativeDateInput(
        amount=15,
        unit="days",
        direction="future"
    )

    assert result.amount == 15


@pytest.mark.model
@pytest.mark.parametrize("amount", [-1, True, 1.5])
def test_invalid_relative_date_amount(amount):
    with pytest.raises(ValidationError):
        RelativeDateInput(
            amount=amount,
            unit="days",
            direction="future"
        )


@pytest.mark.model
def test_invalid_relative_date_unit():
    with pytest.raises(ValidationError):
        RelativeDateInput(
            amount=10,
            unit="centuries",
            direction="future"
        )


@pytest.mark.model
def test_invalid_date_range():
    with pytest.raises(ValidationError):
        DateRangeInput(
            start_date="2026-11-10",
            end_date="2026-11-01"
        )


@pytest.mark.model
def test_invalid_date_format():
    with pytest.raises(ValidationError):
        DateRangeInput(
            start_date="10-11-2026",
            end_date="2026-11-20"
        )


@pytest.mark.model
@pytest.mark.parametrize("n", [-1, 0, 500])
def test_invalid_date_list_limit(n):
    with pytest.raises(ValidationError):
        DateListInput(n=n)


@pytest.mark.model
@pytest.mark.parametrize("day", [-1, 7, 8])
def test_invalid_week_start(day):
    with pytest.raises(ValidationError):
        WeekDatesInput(week_starts_on=day)


@pytest.mark.model
def test_empty_expression():
    with pytest.raises(ValidationError):
        DateParserInput(expression="   ")


@pytest.mark.model
@pytest.mark.parametrize("month", [0, 13, -1])
def test_invalid_month(month):
    with pytest.raises(ValidationError):
        MonthDatesInput(month=month)


@pytest.mark.model
def test_invalid_datetime():
    with pytest.raises(ValidationError):
        TimeDifferenceInput(
            start_datetime="invalid",
            end_datetime="2026-11-06T12:00:00"
        )


@pytest.mark.model
def test_default_month_values():
    result = MonthDatesInput()

    assert result.year is None
    assert result.month is None
    assert result.timezone == "Asia/Kolkata"