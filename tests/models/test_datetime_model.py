import pytest

from pydantic import ValidationError

from config.settings import settings

from models.datetime_model import (
    TimezoneInput,
    RelativeDateInput,
    DateListInput,
    DateRangeInput,
    WeekDatesInput,
    DateParserInput,
    MonthDatesInput,
    TimeDifferenceInput,
    RelativeDateTimeInput,
    DateDifferenceInput,
)


@pytest.mark.model
def test_valid_timezone():

    result = TimezoneInput(
        timezone="Asia/Kolkata"
    )

    assert result.timezone == "Asia/Kolkata"


@pytest.mark.model
def test_invalid_timezone():

    with pytest.raises(ValidationError):
        TimezoneInput(
            timezone="Invalid/Zone"
        )


@pytest.mark.model
def test_valid_relative_date():

    result = RelativeDateInput(
        amount=15,
        unit="days",
        direction="future",
    )

    assert result.amount == 15


@pytest.mark.model
@pytest.mark.parametrize(
    "amount",
    [-1, True, 1.5, settings.max_relative_date_amount + 1],
)
def test_invalid_relative_date_amount(amount):

    with pytest.raises(ValidationError):
        RelativeDateInput(
            amount=amount,
            unit="days",
            direction="future",
        )


@pytest.mark.model
def test_invalid_relative_date_unit():

    with pytest.raises(ValidationError):
        RelativeDateInput(
            amount=10,
            unit="centuries",
            direction="future",
        )


@pytest.mark.model
def test_valid_date_range():

    result = DateRangeInput(
        start_date="2026-11-01",
        end_date="2026-11-10",
        timezone="Asia/Kolkata",
    )

    assert result.start_date == "2026-11-01"


@pytest.mark.model
def test_invalid_date_range():

    with pytest.raises(ValidationError):
        DateRangeInput(
            start_date="2026-11-10",
            end_date="2026-11-01",
        )


@pytest.mark.model
@pytest.mark.parametrize(
    "value",
    [
        "10-11-2026",
        "20261110",
        "2026-1-10",
        "2026-02-30",
    ],
)
def test_invalid_date_format(value):

    with pytest.raises(ValidationError):
        DateRangeInput(
            start_date=value,
            end_date="2026-11-20",
        )


@pytest.mark.model
def test_date_range_rejects_invalid_timezone():

    with pytest.raises(ValidationError):
        DateRangeInput(
            start_date="2026-11-01",
            end_date="2026-11-10",
            timezone="Invalid/Timezone",
        )


@pytest.mark.model
def test_date_range_enforces_configured_limit():

    from datetime import date, timedelta

    start = date(2026, 1, 1)

    end = start + timedelta(
        days=settings.max_date_range_days
    )

    with pytest.raises(ValidationError):
        DateRangeInput(
            start_date=start.isoformat(),
            end_date=end.isoformat(),
        )


@pytest.mark.model
@pytest.mark.parametrize(
    "n",
    [
        -1,
        0,
        settings.max_list_days + 1,
    ],
)
def test_invalid_date_list_limit(n):

    with pytest.raises(ValidationError):
        DateListInput(n=n)


@pytest.mark.model
def test_valid_date_list_limit():

    result = DateListInput(
        n=settings.max_list_days
    )

    assert result.n == settings.max_list_days


@pytest.mark.model
@pytest.mark.parametrize(
    "day",
    [-1, 7, 8],
)
def test_invalid_week_start(day):

    with pytest.raises(ValidationError):
        WeekDatesInput(
            week_starts_on=day
        )


@pytest.mark.model
def test_week_start_uses_settings_default():

    result = WeekDatesInput()

    assert result.week_starts_on == settings.week_starts_on


@pytest.mark.model
def test_empty_expression():

    with pytest.raises(ValidationError):
        DateParserInput(
            expression="   "
        )


@pytest.mark.model
@pytest.mark.parametrize(
    "month",
    [0, 13, -1],
)
def test_invalid_month(month):

    with pytest.raises(ValidationError):
        MonthDatesInput(
            month=month
        )


@pytest.mark.model
def test_invalid_datetime():

    with pytest.raises(ValidationError):
        TimeDifferenceInput(
            start_datetime="invalid",
            end_datetime="2026-11-06T12:00:00",
        )


@pytest.mark.model
def test_date_only_is_not_valid_datetime():

    with pytest.raises(ValidationError):
        TimeDifferenceInput(
            start_datetime="2026-11-05",
            end_datetime="2026-11-06T12:00:00",
        )


@pytest.mark.model
def test_explicit_offset_datetime_is_valid():

    result = TimeDifferenceInput(
        start_datetime="2026-11-05T10:00:00+05:30",
        end_datetime="2026-11-05T12:00:00+05:30",
        timezone="Asia/Kolkata",
    )

    assert result.start_datetime.endswith("+05:30")


@pytest.mark.model
def test_relative_datetime_duration_limit():

    with pytest.raises(ValidationError):
        RelativeDateTimeInput(
            amount=settings.max_relative_datetime_seconds,
            unit="weeks",
            direction="future",
        )


@pytest.mark.model
def test_relative_datetime_valid():

    result = RelativeDateTimeInput(
        amount=34,
        unit="hours",
        direction="future",
    )

    assert result.amount == 34


@pytest.mark.model
def test_date_difference_rejects_compact_date():

    with pytest.raises(ValidationError):
        DateDifferenceInput(
            start_date="20261105",
            end_date="2026-11-10",
        )


@pytest.mark.model
def test_default_month_values():

    result = MonthDatesInput()

    assert result.year is None
    assert result.month is None
    assert result.timezone == settings.default_timezone