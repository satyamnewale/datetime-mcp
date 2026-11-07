
from services.date_difference import DateDifferenceService


def test_date_difference():
    service = DateDifferenceService()

    result = service.calculate_date_difference(
        "2026-11-01",
        "2026-11-05"
    )

    assert result["difference_days"] == 4
    assert result["difference_weeks"] == 0
    assert result["remaining_days"] == 4
    assert result["direction"] == "future"


def test_reverse_date_difference():
    service = DateDifferenceService()

    result = service.calculate_date_difference(
        "2026-11-05",
        "2026-11-01"
    )

    assert result["difference_days"] == 4
    assert result["signed_difference_days"] == -4
    assert result["direction"] == "past"


def test_same_date():
    service = DateDifferenceService()

    result = service.calculate_date_difference(
        "2026-11-05",
        "2026-11-05"
    )

    assert result["difference_days"] == 0
    assert result["direction"] == "same_date"
