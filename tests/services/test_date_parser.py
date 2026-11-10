
import pytest

from services.date_parser import DateParserService


@pytest.fixture
def service():
    return DateParserService()


@pytest.mark.parametrize(
    "expression, expected_date",
    [
        ("November 10, 2026", "2026-11-10"),
        ("November 20, 2026", "2026-11-20"),
        ("November 5, 2026", "2026-11-05")
    ]
)
def test_explicit_date_parser(
    service,
    frozen_time,
    expression,
    expected_date
):
    result = service.parse_natural_datetime(
        expression,
        "Asia/Kolkata"
    )

    assert result["success"] is True
    assert result["date"] == expected_date


def test_datetime_parser(service, frozen_time):
    result = service.parse_natural_datetime(
        "November 10, 2026 at 5 PM",
        "Asia/Kolkata"
    )

    assert result["success"] is True
    assert result["date"] == "2026-11-10"
    assert result["time"].startswith("17:00")


def test_invalid_expression(service):
    result = service.parse_natural_datetime(
        "some completely invalid date expression",
        "Asia/Kolkata"
    )

    assert result["success"] is False


def test_invalid_timezone(service):
    result = service.parse_natural_datetime(
        "Tomorrow",
        "Invalid/Timezone"
    )

    assert result["success"] is False


def test_next_weekday_datetime(service, frozen_time):
    result = service.parse_natural_datetime(
        "next Thursday at 1 PM",
        "Asia/Kolkata",
    )

    assert result["success"] is True
    assert result["date"] == "2026-11-12"
    assert result["time"].startswith("13:00")