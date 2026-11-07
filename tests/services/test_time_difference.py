
import pytest

from services.time_difference import TimeDifferenceService


@pytest.fixture
def service():
    return TimeDifferenceService()


def test_time_difference(service):
    result = service.calculate_time_difference(
        "2026-11-05T10:00:00+05:30",
        "2026-11-05T15:00:00+05:30"
    )

    assert result["difference_seconds"] == 18000
    assert result["difference_hours"] == 5
    assert result["direction"] == "future"


def test_reverse_time_difference(service):
    result = service.calculate_time_difference(
        "2026-11-05T15:00:00+05:30",
        "2026-11-05T10:00:00+05:30"
    )

    assert result["difference_hours"] == 5
    assert result["direction"] == "past"


def test_timezone_conversion(service):
    result = service.calculate_time_difference(
        "2026-11-05T10:00:00+05:30",
        "2026-11-05T04:30:00+00:00"
    )

    assert result["difference_seconds"] == 0
    assert result["difference_hours"] == 0
    assert result["direction"] == "same_time"


def test_naive_datetime_uses_default_timezone(service):
    result = service.calculate_time_difference(
        "2026-11-05T10:00:00",
        "2026-11-05T12:00:00",
        "Asia/Kolkata"
    )

    assert result["difference_hours"] == 2


def test_invalid_datetime(service):
    with pytest.raises(ValueError):
        service.calculate_time_difference(
            "invalid",
            "2026-11-05T12:00:00"
        )
