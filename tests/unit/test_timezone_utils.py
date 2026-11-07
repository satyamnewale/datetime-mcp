from datetime import datetime, timezone as utc_timezone
from zoneinfo import ZoneInfo

import pytest

import utils.timezone_utils as timezone_utils

from utils.timezone_utils import (
    get_timezone,
    validate_timezone,
    get_local_datetime,
    convert_timezone,
    convert_to_utc,
    get_utc_offset,
    get_timezone_details,
)


# --------------------------------------------------
# validate_timezone
# --------------------------------------------------

@pytest.mark.unit
@pytest.mark.parametrize(
    "timezone_name",
    [
        "UTC",
        "Asia/Kolkata",
        "Asia/Tokyo",
        "Europe/London",
        "America/New_York",
    ],
)
def test_valid_timezone(timezone_name):
    assert validate_timezone(timezone_name) is True


@pytest.mark.unit
@pytest.mark.parametrize(
    "timezone_name",
    [
        "Invalid/Timezone",
        "Asia/Invalid",
        "",
        "NotATimezone",
    ],
)
def test_invalid_timezone(timezone_name):
    assert validate_timezone(timezone_name) is False


# --------------------------------------------------
# get_timezone
# --------------------------------------------------

@pytest.mark.unit
def test_get_timezone():
    result = get_timezone("Asia/Kolkata")

    assert isinstance(result, ZoneInfo)
    assert str(result) == "Asia/Kolkata"


@pytest.mark.unit
def test_get_timezone_utc():
    result = get_timezone("UTC")

    assert isinstance(result, ZoneInfo)
    assert str(result) == "UTC"


@pytest.mark.unit
def test_get_timezone_invalid():
    with pytest.raises(ValueError, match="Invalid timezone"):
        get_timezone("Invalid/Timezone")


# --------------------------------------------------
# get_local_datetime
# --------------------------------------------------

@pytest.mark.unit
@pytest.mark.parametrize(
    "timezone_name",
    ["UTC", "Asia/Kolkata", "America/New_York"],
)
def test_get_local_datetime_returns_datetime_in_requested_timezone(
    timezone_name,
):
    result = get_local_datetime(timezone_name)

    assert isinstance(result, datetime)
    assert result.tzinfo is not None
    assert str(result.tzinfo) == timezone_name


@pytest.mark.unit
def test_get_local_datetime_invalid_timezone():
    with pytest.raises(ValueError, match="Invalid timezone"):
        get_local_datetime("Invalid/Timezone")


# --------------------------------------------------
# convert_timezone
# --------------------------------------------------

@pytest.mark.unit
def test_convert_timezone_kolkata_to_new_york():
    value = datetime(
        2026, 1, 15, 12, 0,
        tzinfo=ZoneInfo("Asia/Kolkata"),
    )

    result = convert_timezone(value, "America/New_York")

    expected = datetime(
        2026, 1, 15, 1, 30,
        tzinfo=ZoneInfo("America/New_York"),
    )

    assert result == expected
    assert str(result.tzinfo) == "America/New_York"


@pytest.mark.unit
def test_convert_timezone_preserves_same_instant():
    value = datetime(
        2026, 7, 15, 12, 0,
        tzinfo=ZoneInfo("Asia/Kolkata"),
    )

    result = convert_timezone(value, "UTC")

    assert (
        result.astimezone(utc_timezone.utc)
        == value.astimezone(utc_timezone.utc)
    )


@pytest.mark.unit
def test_convert_timezone_rejects_naive_datetime():
    value = datetime(2026, 11, 5, 15, 30)

    with pytest.raises(
        ValueError,
        match="Datetime must be timezone-aware",
    ):
        convert_timezone(value, "UTC")


@pytest.mark.unit
def test_convert_timezone_rejects_invalid_target_timezone():
    value = datetime(
        2026, 11, 5, 15, 30,
        tzinfo=ZoneInfo("UTC"),
    )

    with pytest.raises(ValueError, match="Invalid timezone"):
        convert_timezone(value, "Invalid/Timezone")


# --------------------------------------------------
# convert_to_utc
# --------------------------------------------------

@pytest.mark.unit
def test_convert_to_utc_from_kolkata():
    value = datetime(
        2026, 11, 5, 15, 30,
        tzinfo=ZoneInfo("Asia/Kolkata"),
    )

    result = convert_to_utc(value)

    expected = datetime(
        2026, 11, 5, 10, 0,
        tzinfo=utc_timezone.utc,
    )

    assert result == expected
    assert result.tzinfo is utc_timezone.utc


@pytest.mark.unit
def test_convert_to_utc_from_new_york_winter():
    value = datetime(
        2026, 1, 15, 12, 0,
        tzinfo=ZoneInfo("America/New_York"),
    )

    result = convert_to_utc(value)

    expected = datetime(
        2026, 1, 15, 17, 0,
        tzinfo=utc_timezone.utc,
    )

    assert result == expected


@pytest.mark.unit
def test_convert_to_utc_rejects_naive_datetime():
    value = datetime(2026, 11, 5, 15, 30)

    with pytest.raises(
        ValueError,
        match="Datetime must be timezone-aware",
    ):
        convert_to_utc(value)


# --------------------------------------------------
# get_utc_offset
# --------------------------------------------------

@pytest.mark.unit
@pytest.mark.parametrize(
    ("value", "expected"),
    [
        (
            datetime(
                2026, 11, 5, 15, 30,
                tzinfo=ZoneInfo("Asia/Kolkata"),
            ),
            "+05:30",
        ),
        (
            datetime(
                2026, 11, 5, 10, 0,
                tzinfo=ZoneInfo("UTC"),
            ),
            "+00:00",
        ),
        (
            datetime(
                2026, 1, 15, 12, 0,
                tzinfo=ZoneInfo("America/New_York"),
            ),
            "-05:00",
        ),
        (
            datetime(
                2026, 7, 15, 12, 0,
                tzinfo=ZoneInfo("America/New_York"),
            ),
            "-04:00",
        ),
    ],
)
def test_get_utc_offset(value, expected):
    assert get_utc_offset(value) == expected


@pytest.mark.unit
def test_get_utc_offset_rejects_naive_datetime():
    value = datetime(2026, 11, 5, 15, 30)

    with pytest.raises(
        ValueError,
        match="Datetime must be timezone-aware",
    ):
        get_utc_offset(value)


# --------------------------------------------------
# get_timezone_details
# --------------------------------------------------

class FrozenDateTime(datetime):
    """Datetime test double that returns a fixed instant from now()."""

    fixed_instant = None

    @classmethod
    def now(cls, tz=None):
        if cls.fixed_instant is None:
            raise AssertionError("Set fixed_instant before calling now()")

        if tz is None:
            return cls.fixed_instant.replace(tzinfo=None)

        return cls.fixed_instant.astimezone(tz)


@pytest.mark.unit
def test_timezone_details_kolkata(monkeypatch):
    FrozenDateTime.fixed_instant = datetime(
        2026, 11, 5, 10, 0,
        tzinfo=utc_timezone.utc,
    )

    monkeypatch.setattr(
        timezone_utils,
        "datetime",
        FrozenDateTime,
    )

    result = get_timezone_details("Asia/Kolkata")

    assert result == {
        "timezone": "Asia/Kolkata",
        "utc_offset": "+05:30",
        "timezone_abbreviation": "IST",
        "is_dst": False,
        "current_datetime": "2026-11-05T15:30:00+05:30",
    }


@pytest.mark.unit
def test_timezone_details_utc(monkeypatch):
    FrozenDateTime.fixed_instant = datetime(
        2026, 11, 5, 10, 0,
        tzinfo=utc_timezone.utc,
    )

    monkeypatch.setattr(
        timezone_utils,
        "datetime",
        FrozenDateTime,
    )

    result = get_timezone_details("UTC")

    assert result == {
        "timezone": "UTC",
        "utc_offset": "+00:00",
        "timezone_abbreviation": "UTC",
        "is_dst": False,
        "current_datetime": "2026-11-05T10:00:00+00:00",
    }


@pytest.mark.unit
def test_timezone_details_new_york_winter(monkeypatch):
    FrozenDateTime.fixed_instant = datetime(
        2026, 1, 15, 17, 0,
        tzinfo=utc_timezone.utc,
    )

    monkeypatch.setattr(
        timezone_utils,
        "datetime",
        FrozenDateTime,
    )

    result = get_timezone_details("America/New_York")

    assert result["utc_offset"] == "-05:00"
    assert result["timezone_abbreviation"] == "EST"
    assert result["is_dst"] is False
    assert result["current_datetime"] == "2026-01-15T12:00:00-05:00"


@pytest.mark.unit
def test_timezone_details_new_york_summer(monkeypatch):
    FrozenDateTime.fixed_instant = datetime(
        2026, 7, 15, 16, 0,
        tzinfo=utc_timezone.utc,
    )

    monkeypatch.setattr(
        timezone_utils,
        "datetime",
        FrozenDateTime,
    )

    result = get_timezone_details("America/New_York")

    assert result["utc_offset"] == "-04:00"
    assert result["timezone_abbreviation"] == "EDT"
    assert result["is_dst"] is True
    assert result["current_datetime"] == "2026-07-15T12:00:00-04:00"


@pytest.mark.unit
def test_timezone_details_invalid():
    with pytest.raises(ValueError, match="Invalid timezone"):
        get_timezone_details("Invalid/Timezone")