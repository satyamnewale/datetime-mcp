import pytest

from utils.validator import (
    validate_date,
    validate_time,
    validate_datetime,
    validate_timezone,
    validate_amount,
    validate_unit,
    validate_date_range,
    validate_week_start,
    SUPPORTED_DATE_UNITS,
)


@pytest.mark.unit
@pytest.mark.parametrize(
    "value",
    ["2026-11-05", "2024-02-29", "2000-01-01"]
)
def test_valid_date(value):
    assert validate_date(value).isoformat() == value


@pytest.mark.unit
@pytest.mark.parametrize(
    "value",
    [
        "2026-02-30",
        "2026-13-01",
        "05-11-2026",
        "",
        "invalid",
    ]
)
def test_invalid_date(value):
    with pytest.raises(ValueError):
        validate_date(value)


@pytest.mark.unit
@pytest.mark.parametrize(
    "value",
    ["15:30:00", "00:00:00", "23:59:59"]
)
def test_valid_time(value):
    assert validate_time(value) is not None


@pytest.mark.unit
@pytest.mark.parametrize(
    "value",
    ["25:00:00", "12:60:00", "invalid", ""]
)
def test_invalid_time(value):
    with pytest.raises(ValueError):
        validate_time(value)


@pytest.mark.unit
def test_valid_datetime():
    result = validate_datetime("2026-11-05T15:30:00")
    assert result.year == 2026


@pytest.mark.unit
def test_invalid_datetime():
    with pytest.raises(ValueError):
        validate_datetime("invalid")


@pytest.mark.unit
def test_valid_timezone():
    assert validate_timezone("Asia/Kolkata") == "Asia/Kolkata"


@pytest.mark.unit
def test_invalid_timezone():
    with pytest.raises(ValueError):
        validate_timezone("Invalid/Timezone")


@pytest.mark.unit
@pytest.mark.parametrize("amount", [0, 1, 15, 365])
def test_valid_amount(amount):
    assert validate_amount(amount) == amount


@pytest.mark.unit
@pytest.mark.parametrize("amount", [-1, -100, True, 1.5])
def test_invalid_amount(amount):
    with pytest.raises(ValueError):
        validate_amount(amount)


@pytest.mark.unit
def test_valid_unit():
    assert validate_unit("days", SUPPORTED_DATE_UNITS) == "days"


@pytest.mark.unit
def test_invalid_unit():
    with pytest.raises(ValueError):
        validate_unit("centuries", SUPPORTED_DATE_UNITS)


@pytest.mark.unit
def test_valid_date_range(valid_date_range):
    start, end = validate_date_range(*valid_date_range)
    assert (end - start).days == 6


@pytest.mark.unit
def test_invalid_date_range(invalid_date_range):
    with pytest.raises(ValueError):
        validate_date_range(*invalid_date_range)


@pytest.mark.unit
@pytest.mark.parametrize("day", range(7))
def test_valid_week_start(day):
    assert validate_week_start(day) == day


@pytest.mark.unit
@pytest.mark.parametrize("day", [-1, 7, 8])
def test_invalid_week_start(day):
    with pytest.raises(ValueError):
        validate_week_start(day)