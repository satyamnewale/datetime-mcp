from datetime import datetime
from zoneinfo import ZoneInfo

import pytest

from services.relative_datetime import RelativeDateTimeService


@pytest.fixture
def service():
    return RelativeDateTimeService()


@pytest.mark.service
def test_hours_in_past(service, frozen_time):

    result = service.calculate_relative_datetime(
        5,
        "hours",
        "past",
        "Asia/Kolkata",
    )

    assert result["result_date"] == "2026-11-05"
    assert result["result_time"] == "10:30:00"


@pytest.mark.service
def test_hours_in_future(service, frozen_time):

    result = service.calculate_relative_datetime(
        34,
        "hours",
        "future",
        "Asia/Kolkata",
    )

    assert result["result_date"] == "2026-11-07"
    assert result["result_time"] == "01:30:00"


@pytest.mark.service
def test_minutes_in_future(service, frozen_time):

    result = service.calculate_relative_datetime(
        90,
        "minutes",
        "future",
        "Asia/Kolkata",
    )

    assert result["result_time"] == "17:00:00"


@pytest.mark.service
def test_days_in_future(service, frozen_time):

    result = service.calculate_relative_datetime(
        2,
        "days",
        "future",
        "Asia/Kolkata",
    )

    assert result["result_date"] == "2026-11-07"


@pytest.mark.service
def test_seconds_in_future(service, frozen_time):

    result = service.calculate_relative_datetime(
        30,
        "seconds",
        "future",
        "Asia/Kolkata",
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
    ],
)
def test_invalid_input(
    service,
    amount,
    unit,
    direction,
):

    with pytest.raises(ValueError):
        service.calculate_relative_datetime(
            amount,
            unit,
            direction,
        )


@pytest.mark.service
def test_zero_amount(service, frozen_time):

    result = service.calculate_relative_datetime(
        0,
        "hours",
        "future",
        "Asia/Kolkata",
    )

    assert result["result_date"] == "2026-11-05"
    assert result["result_time"] == "15:30:00"


@pytest.mark.service
def test_24_elapsed_hours_across_dst(service, monkeypatch):

    starting_datetime = datetime(
        2026,
        3,
        7,
        12,
        0,
        0,
        tzinfo=ZoneInfo("America/New_York"),
    )

    monkeypatch.setattr(
        "services.relative_datetime.get_current_datetime",
        lambda timezone: starting_datetime,
    )

    result = service.calculate_relative_datetime(
        24,
        "hours",
        "future",
        "America/New_York",
    )

    # 24 elapsed hours later, local time becomes 13:00
    # because the timezone moved from UTC-05:00 to UTC-04:00.
    assert result["result_date"] == "2026-03-08"
    assert result["result_time"] == "13:00:00"
    assert result["calculation_type"] == "elapsed_duration"

@pytest.mark.service
def test_relative_datetime_uses_same_reference_instant(service):

    result = service.calculate_relative_datetime(
        amount=100,
        unit="hours",
        direction="future",
        timezone="Asia/Kolkata",
        reference_datetime="2026-11-10T11:46:26+05:30",
    )

    assert result["original_datetime"] == (
        "2026-11-10T11:46:26+05:30"
    )

    assert result["result_datetime"] == (
        "2026-11-14T15:46:26+05:30"
    )

    assert result["reference_supplied"] is True


@pytest.mark.service
def test_relative_datetime_uses_naive_reference_as_local_time(service):

    result = service.calculate_relative_datetime(
        amount=2,
        unit="hours",
        direction="future",
        timezone="Asia/Kolkata",
        reference_datetime="2026-11-10T10:00:00",
    )

    assert result["result_datetime"] == (
        "2026-11-10T12:00:00+05:30"
    )
