
import pytest

from services.date_range import DateRangeService


@pytest.fixture
def service():
    return DateRangeService()


def test_valid_date_range(service):
    result = service.get_date_range(
        "2026-11-01",
        "2026-11-07"
    )

    assert result["total_days"] == 7
    assert result["start_day"] == "Sunday"
    assert result["end_day"] == "Saturday"


def test_same_date_range(service):
    result = service.get_date_range(
        "2026-11-05",
        "2026-11-05"
    )

    assert result["total_days"] == 1


def test_invalid_start_date(service):
    with pytest.raises(ValueError):
        service.get_date_range(
            "2026-02-30",
            "2026-03-01"
        )


def test_end_before_start(service):
    with pytest.raises(ValueError):
        service.get_date_range(
            "2026-11-10",
            "2026-11-01"
        )
