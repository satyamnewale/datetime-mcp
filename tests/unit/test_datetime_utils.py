import pytest

from utils.timezone_utils import (
    get_timezone,
    validate_timezone,
    get_timezone_details,
    convert_to_utc,
)


@pytest.mark.unit
def test_timezone_validation():
    assert validate_timezone("Asia/Kolkata") is True


@pytest.mark.unit
def test_invalid_timezone_validation():
    assert validate_timezone("Invalid/Timezone") is False


@pytest.mark.unit
def test_get_timezone():
    timezone = get_timezone("Asia/Kolkata")
    assert str(timezone) == "Asia/Kolkata"


@pytest.mark.unit
def test_get_timezone_invalid():
    with pytest.raises(ValueError):
        get_timezone("Invalid/Timezone")


@pytest.mark.unit
def test_timezone_details():
    result = get_timezone_details("Asia/Kolkata")

    assert result["timezone"] == "Asia/Kolkata"
    assert result["utc_offset"] == "+05:30"
    assert result["is_dst"] is False


@pytest.mark.unit
def test_convert_to_utc(fixed_datetime):
    result = convert_to_utc(fixed_datetime)

    assert result.utcoffset().total_seconds() == 0
    assert result.hour == 10