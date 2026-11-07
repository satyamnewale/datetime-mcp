import pytest

from services.current_datetime import CurrentDateTimeService


@pytest.fixture
def service():
    return CurrentDateTimeService()


@pytest.mark.service
def test_get_current_datetime(service, frozen_time):
    result = service.get_current_datetime("Asia/Kolkata")

    assert result["date"] == "2026-11-05"
    assert result["time"] == "15:30:00"
    assert result["day"] == "Thursday"
    assert result["timezone"] == "Asia/Kolkata"
    assert result["utc_offset"] == "+0530"


@pytest.mark.service
def test_get_current_date(service, frozen_time):
    result = service.get_current_date("Asia/Kolkata")

    assert result["date"] == "2026-11-05"
    assert result["day"] == "Thursday"


@pytest.mark.service
def test_get_current_time(service, frozen_time):
    result = service.get_current_time("Asia/Kolkata")

    assert result["time"] == "15:30:00"
    assert result["timezone"] == "Asia/Kolkata"


@pytest.mark.service
def test_utc_datetime(service, frozen_time):
    result = service.get_current_datetime("UTC")

    assert result["time"] == "10:00:00"
    assert result["utc_offset"] == "+0000"


@pytest.mark.service
def test_invalid_timezone(service):
    with pytest.raises(ValueError):
        service.get_current_datetime("Invalid/Timezone")