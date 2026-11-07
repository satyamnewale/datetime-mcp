
import pytest

from services.month_service import MonthService


@pytest.fixture
def service():
    return MonthService()


def test_november_dates(service):
    result = service.get_month_dates(2026, 11)

    assert result["month_name"] == "November"
    assert result["total_days"] == 30
    assert len(result["dates"]) == 30


def test_february_leap_year(service):
    result = service.get_month_dates(2028, 2)

    assert result["total_days"] == 29


def test_february_non_leap_year(service):
    result = service.get_month_dates(2027, 2)

    assert result["total_days"] == 28


def test_first_and_last_dates(service):
    result = service.get_month_dates(2026, 11)

    assert result["dates"][0]["date"] == "2026-11-01"
    assert result["dates"][-1]["date"] == "2026-11-30"


def test_invalid_month(service):
    with pytest.raises(ValueError):
        service.get_month_dates(2026, 13)


def test_invalid_year(service):
    with pytest.raises(ValueError):
        service.get_month_dates(0, 11)
