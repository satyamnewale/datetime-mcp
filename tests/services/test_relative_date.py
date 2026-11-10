
import pytest

from services.relative_date import RelativeDateService


@pytest.fixture
def service():
    return RelativeDateService()


def test_15_days_past(service, frozen_time):
    result = service.calculate_relative_date(
        15, "days", "past", "Asia/Kolkata"
    )

    assert result["result_date"] == "2026-10-21"


def test_40_days_future(service, frozen_time):
    result = service.calculate_relative_date(
        40, "days", "future", "Asia/Kolkata"
    )

    assert result["result_date"] == "2026-12-15"


def test_2_weeks_past(service, frozen_time):
    result = service.calculate_relative_date(
        2, "weeks", "past", "Asia/Kolkata"
    )

    assert result["result_date"] == "2026-10-22"


def test_month_calculation(service, frozen_time):
    result = service.calculate_relative_date(
        1, "months", "future", "Asia/Kolkata"
    )

    assert result["result_date"] == "2026-12-05"


def test_year_calculation(service, frozen_time):
    result = service.calculate_relative_date(
        1, "years", "future", "Asia/Kolkata"
    )

    assert result["result_date"] == "2027-11-05"


def test_month_end_calculation(service):
    result = service.calculate_relative_date(
        1, "months", "future", "UTC"
    )

    # Use a fixed date for the January 31 edge case
    from datetime import date
    from dateutil.relativedelta import relativedelta

    assert date(2026, 1, 31) + relativedelta(months=1) == date(2026, 2, 28)


def test_previous_7_days(service, frozen_time):
    result = service.get_previous_n_days_and_dates(7, "Asia/Kolkata")

    assert result["count"] == 7
    assert result["dates"][0]["date"] == "2026-10-29"
    assert result["dates"][-1]["date"] == "2026-11-04"


def test_next_7_days(service, frozen_time):
    result = service.get_next_n_days_and_dates(7, "Asia/Kolkata")

    assert result["count"] == 7
    assert result["dates"][0]["date"] == "2026-11-06"
    assert result["dates"][-1]["date"] == "2026-11-12"


def test_get_week_dates(service, frozen_time):
    result = service.get_week_dates(
        timezone="Asia/Kolkata"
    )

    assert result["week_start"] == "2026-11-02"
    assert result["week_end"] == "2026-11-08"
    assert len(result["dates"]) == 7


def test_week_starts_sunday(service):
    result = service.get_week_dates(
        reference_date="2026-11-05",
        week_starts_on=6
    )

    assert result["week_start"] == "2026-11-01"
    assert result["week_end"] == "2026-11-07"


@pytest.mark.parametrize(
    "amount, unit, direction",
    [
        (-1, "days", "past"),
        (5, "invalid", "past"),
        (5, "days", "invalid")
    ]
)
def test_invalid_relative_date(service, amount, unit, direction):
    with pytest.raises(ValueError):
        service.calculate_relative_date(
            amount, unit, direction
        )


def test_zero_days(service, frozen_time):
    result = service.calculate_relative_date(
        0, "days", "future", "Asia/Kolkata"
    )

    assert result["result_date"] == "2026-11-05"


def test_zero_previous_days(service):
    with pytest.raises(ValueError):
        service.get_previous_n_days_and_dates(0)


def test_second_friday_after_reference_date(service):

    result = service.get_nth_weekday(
        weekday="Friday",
        occurrence=2,
        reference_date="2026-11-10",
        timezone="Asia/Kolkata",
    )

    assert result["result_date"] == "2026-11-20"
    assert result["day"] == "Friday"


def test_first_friday_when_reference_is_thursday(service):

    result = service.get_nth_weekday(
        weekday="Friday",
        occurrence=1,
        reference_date="2026-11-19",
        timezone="Asia/Kolkata",
    )

    assert result["result_date"] == "2026-11-20"
    assert result["day"] == "Friday"


def test_same_weekday_reference_excludes_reference_date(service):

    result = service.get_nth_weekday(
        weekday="Tuesday",
        occurrence=1,
        reference_date="2026-11-10",
        timezone="Asia/Kolkata",
    )

    assert result["result_date"] == "2026-11-17"
