import pytest

from services.time_difference import TimeDifferenceService


@pytest.fixture
def service():
    return TimeDifferenceService()


def test_time_difference(service):

    result = service.calculate_time_difference(
        "2026-11-05T10:00:00+05:30",
        "2026-11-05T15:00:00+05:30",
    )

    assert result["difference_seconds"] == 18000
    assert result["difference_hours"] == 5
    assert result["direction"] == "future"


def test_reverse_time_difference(service):

    result = service.calculate_time_difference(
        "2026-11-05T15:00:00+05:30",
        "2026-11-05T10:00:00+05:30",
    )

    assert result["difference_hours"] == 5
    assert result["direction"] == "past"


def test_timezone_conversion(service):

    result = service.calculate_time_difference(
        "2026-11-05T10:00:00+05:30",
        "2026-11-05T04:30:00+00:00",
    )

    assert result["difference_seconds"] == 0
    assert result["difference_hours"] == 0
    assert result["direction"] == "same_time"


def test_naive_datetime_uses_timezone(service):

    result = service.calculate_time_difference(
        "2026-11-05T10:00:00",
        "2026-11-05T12:00:00",
        "Asia/Kolkata",
    )

    assert result["difference_hours"] == 2


def test_nonexistent_dst_time_is_rejected(service):

    with pytest.raises(
        ValueError,
        match="does not exist",
    ):
        service.calculate_time_difference(
            "2026-03-08T02:30:00",
            "2026-03-08T04:00:00",
            "America/New_York",
        )


def test_ambiguous_dst_time_is_rejected(service):

    with pytest.raises(
        ValueError,
        match="ambiguous",
    ):
        service.calculate_time_difference(
            "2026-11-01T01:30:00",
            "2026-11-01T02:30:00",
            "America/New_York",
        )


def test_explicit_dst_offset_resolves_ambiguity(service):

    result = service.calculate_time_difference(
        "2026-11-01T01:30:00-04:00",
        "2026-11-01T01:30:00-05:00",
        "America/New_York",
    )

    assert result["difference_seconds"] == 3600
    assert result["difference_hours"] == 1


def test_invalid_datetime(service):

    with pytest.raises(ValueError):
        service.calculate_time_difference(
            "invalid",
            "2026-11-05T12:00:00",
        )