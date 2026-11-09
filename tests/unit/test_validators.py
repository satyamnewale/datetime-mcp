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
    [
        "2026-11-05",
        "2024-02-29",
        "2000-01-01",
    ],
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
        "20261105",
        "2026-1-05",
        "",
        "invalid",
    ],
)
def test_invalid_date(value):
    with pytest.raises(ValueError):
        validate_date(value)


@pytest.mark.unit
@pytest.mark.parametrize(
    "value",
    [
        "15:30",
        "15:30:00",
        "00:00:00",
        "23:59:59",
        "12:30:15.123456",
    ],
)
def test_valid_time(value):
    assert validate_time(value) is not None


@pytest.mark.unit
@pytest.mark.parametrize(
    "value",
    [
        "25:00:00",
        "12:60:00",
        "15:30:60",
        "invalid",
        "",
        "153000",
    ],
)
def test_invalid_time(value):
    with pytest.raises(ValueError):
        validate_time(value)


@pytest.mark.unit
@pytest.mark.parametrize(
    "value",
    [
        "2026-11-05T15:30:00",
        "2026-11-05T15:30:00+05:30",
        "2026-11-05T10:00:00Z",
        "2026-11-05T10:00+00:00",
    ],
)
def test_valid_datetime(value):
    result = validate_datetime(value)
    assert result.year == 2026


@pytest.mark.unit
@pytest.mark.parametrize(
    "value",
    [
        "invalid",
        "2026-11-05",
        "20261105T153000",
        "2026-11-05 15:30:00",
        "2026-11-05T25:30:00",
        "2026-11-05T15:30:00+25:00",
    ],
)
def test_invalid_datetime(value):
    with pytest.raises(ValueError):
        validate_datetime(value)


@pytest.mark.unit
def test_valid_timezone():
    assert validate_timezone("Asia/Kolkata") == "Asia/Kolkata"


@pytest.mark.unit
def test_invalid_timezone():
    with pytest.raises(ValueError):
        validate_timezone("Invalid/Timezone")


@pytest.mark.unit
@pytest.mark.parametrize(
    "amount",
    [0, 1, 15, 365],
)
def test_valid_amount(amount):
    assert validate_amount(amount) == amount


@pytest.mark.unit
@pytest.mark.parametrize(
    "amount",
    [-1, -100, True, 1.5],
)
def test_invalid_amount(amount):
    with pytest.raises(ValueError):
        validate_amount(amount)


@pytest.mark.unit
def test_amount_maximum():
    assert validate_amount(
        50,
        maximum=100,
    ) == 50


@pytest.mark.unit
def test_amount_above_maximum():
    with pytest.raises(ValueError):
        validate_amount(
            101,
            maximum=100,
        )


@pytest.mark.unit
def test_valid_unit():
    assert validate_unit(
        "days",
        SUPPORTED_DATE_UNITS,
    ) == "days"


@pytest.mark.unit
def test_invalid_unit():
    with pytest.raises(ValueError):
        validate_unit(
            "centuries",
            SUPPORTED_DATE_UNITS,
        )


@pytest.mark.unit
def test_valid_date_range(valid_date_range):
    start, end = validate_date_range(*valid_date_range)

    assert (end - start).days == 6


@pytest.mark.unit
def test_invalid_date_range(invalid_date_range):
    with pytest.raises(ValueError):
        validate_date_range(*invalid_date_range)


@pytest.mark.unit
def test_date_range_maximum():

    with pytest.raises(
        ValueError,
        match="Date range cannot exceed 366 days",
    ):
        validate_date_range(
            "2026-01-01",
            "2027-01-02",
            max_days=366,
        )

@pytest.mark.unit
def test_date_range_at_maximum():

    start, end = validate_date_range(
        "2026-01-01",
        "2027-01-01",
        max_days=366,
    )

    assert (end - start).days + 1 == 366

    
@pytest.mark.unit
@pytest.mark.parametrize(
    "day",
    range(7),
)
def test_valid_week_start(day):
    assert validate_week_start(day) == day


@pytest.mark.unit
@pytest.mark.parametrize(
    "day",
    [-1, 7, 8, True],
)
def test_invalid_week_start(day):
    with pytest.raises(ValueError):
        validate_week_start(day)