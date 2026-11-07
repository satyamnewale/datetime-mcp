
import pytest

from services.timezone_service import TimezoneService
from utils.timezone_utils import (
    get_timezone,
    validate_timezone,
    get_timezone_details
)


def test_valid_timezone():
    assert validate_timezone("Asia/Kolkata") is True


def test_invalid_timezone():
    assert validate_timezone("Invalid/Timezone") is False


def test_get_timezone():
    timezone = get_timezone("Asia/Kolkata")

    assert str(timezone) == "Asia/Kolkata"


def test_get_timezone_invalid():
    with pytest.raises(ValueError):
        get_timezone("Invalid/Timezone")


def test_timezone_details():
    result = get_timezone_details("Asia/Kolkata")

    assert result["timezone"] == "Asia/Kolkata"
    assert result["utc_offset"] == "+05:30"
    assert result["is_dst"] is False


def test_timezone_service():
    service = TimezoneService()

    result = service.get_timezone_info("Asia/Kolkata")

    assert result["timezone"] == "Asia/Kolkata"
    assert result["utc_offset"] == "+0530"
    assert result["is_dst"] is False


def test_timezone_service_invalid():
    service = TimezoneService()

    result = service.get_timezone_info("Invalid/Timezone")

    assert result["success"] is False
    assert "error" in result
