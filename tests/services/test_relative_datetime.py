import pytest

from services.relative_datetime import RelativeDateTimeService


@pytest.fixture
def service():
    return RelativeDateTimeService()


@pytest.mark.service
def test_hours_in_past(service, frozen_time):
    result = service.calculate_relative_datetime(
        5, "hours", "past", "Asia/Kolkata"
    )

    assert result["result_date"] == "2026-11-05"
    assert result["result_time"] == "10:30:00"


@pytest.mark.service
def test_hours_in_future(service, frozen_time):
    result = service.calculate_relative_datetime(
        34, "hours", "future", "Asia/Kolkata"
    )

    assert result["result_date"] == "2026-11-07"
    assert result["result_time"] == "01:30:00"


@pytest.mark.service
def test_minutes_in_future(service, frozen_time):
    result = service.calculate_relative_datetime(
        90, "minutes", "future", "Asia/Kolkata"
    )

    assert result["result_time"] == "17:00:00"


@pytest.mark.service
def test_days_in_future(service, frozen_time):
    result = service.calculate_relative_datetime(
        2, "days", "future", "Asia/Kolkata"
    )

    assert result["result_date"] == "2026-11-07"


@pytest.mark.service
def test_seconds_in_future(service, frozen_time):
    result = service.calculate_relative_datetime(
        30, "seconds", "future", "Asia/Kolkata"
    )

    assert result["result_time"] == "15:30:30"


@pytest.mark.service
@pytest.mark.parametrize(
    "amount, unit, direction",
    [
        (-1, "hours", "past"),
        (5, "invalid", "future"),
        (5, "hours", "invalid"),
        (1.5, "hours", "future"),
    ]
)
def test_invalid_input(service, amount, unit, direction):
    with pytest.raises(ValueError):
        service.calculate_relative_datetime(
            amount, unit, direction
        )


@pytest.mark.service
def test_zero_amount(service, frozen_time):
    result = service.calculate_relative_datetime(
        0, "hours", "future", "Asia/Kolkata"
    )

    assert result["result_date"] == "2026-11-05"
    assert result["result_time"] == "15:30:00"