from datetime import date, datetime, time
from zoneinfo import ZoneInfo

import pytest

from utils.formatters import (
    format_date,
    format_time,
    format_datetime,
    format_datetime_response,
    format_date_list,
    format_duration,
)


# --------------------------------------------------
# format_date
# --------------------------------------------------

@pytest.mark.unit
def test_format_date_default():
    assert format_date(date(2026, 11, 5)) == "2026-11-05"


@pytest.mark.unit
@pytest.mark.parametrize(
    ("value", "date_format", "expected"),
    [
        (date(2026, 11, 5), "%d-%m-%Y", "05-11-2026"),
        (date(2026, 11, 5), "%A, %B %d, %Y", "Thursday, November 05, 2026"),
        (date(2024, 2, 29), "%Y/%m/%d", "2024/02/29"),
    ],
)
def test_format_date_custom_formats(value, date_format, expected):
    assert format_date(value, date_format) == expected


# --------------------------------------------------
# format_time
# --------------------------------------------------

@pytest.mark.unit
def test_format_time_default():
    assert format_time(time(15, 30, 45)) == "15:30:45"


@pytest.mark.unit
@pytest.mark.parametrize(
    ("value", "time_format", "expected"),
    [
        (time(15, 30, 45), "%I:%M %p", "03:30 PM"),
        (time(0, 0, 0), "%H:%M:%S", "00:00:00"),
        (time(23, 59, 59), "%H:%M:%S", "23:59:59"),
    ],
)
def test_format_time_formats(value, time_format, expected):
    assert format_time(value, time_format) == expected


# --------------------------------------------------
# format_datetime
# --------------------------------------------------

@pytest.mark.unit
def test_format_datetime_default():
    value = datetime(
        2026, 11, 5, 15, 30, 45,
        tzinfo=ZoneInfo("Asia/Kolkata"),
    )

    assert format_datetime(value) == "2026-11-05T15:30:45+0530"


@pytest.mark.unit
def test_format_datetime_custom_format():
    value = datetime(2026, 11, 5, 15, 30, 45)

    assert format_datetime(
        value,
        "%d-%m-%Y %I:%M %p",
    ) == "05-11-2026 03:30 PM"


@pytest.mark.unit
def test_format_datetime_utc():
    value = datetime(
        2026, 11, 5, 10, 0, 0,
        tzinfo=ZoneInfo("UTC"),
    )

    assert format_datetime(value) == "2026-11-05T10:00:00+0000"


@pytest.mark.unit
def test_format_datetime_naive_datetime():
    value = datetime(2026, 11, 5, 15, 30, 45)

    assert format_datetime(value) == "2026-11-05T15:30:45"


# --------------------------------------------------
# format_datetime_response
# --------------------------------------------------

@pytest.mark.unit
def test_format_datetime_response():
    value = datetime(
        2026, 11, 5, 15, 30, 45,
        tzinfo=ZoneInfo("Asia/Kolkata"),
    )

    assert format_datetime_response(value) == {
        "date": "2026-11-05",
        "time": "15:30:45",
        "day": "Thursday",
        "datetime_iso": "2026-11-05T15:30:45+05:30",
        "timezone": "Asia/Kolkata",
        "utc_offset": "+05:30",
    }


@pytest.mark.unit
def test_format_datetime_response_utc():
    value = datetime(
        2026, 11, 5, 10, 0, 0,
        tzinfo=ZoneInfo("UTC"),
    )

    result = format_datetime_response(value)

    assert result["timezone"] == "UTC"
    assert result["utc_offset"] == "+00:00"
    assert result["datetime_iso"] == "2026-11-05T10:00:00+00:00"


@pytest.mark.unit
def test_format_datetime_response_rejects_naive_datetime():
    value = datetime(2026, 11, 5, 15, 30, 0)

    with pytest.raises(
        ValueError,
        match="Datetime must be timezone-aware",
    ):
        format_datetime_response(value)


# --------------------------------------------------
# format_date_list
# --------------------------------------------------

@pytest.mark.unit
def test_format_date_list():
    dates = [
        date(2026, 11, 5),
        date(2026, 11, 6),
        date(2026, 11, 7),
    ]

    assert format_date_list(dates) == [
        {"date": "2026-11-05", "day": "Thursday"},
        {"date": "2026-11-06", "day": "Friday"},
        {"date": "2026-11-07", "day": "Saturday"},
    ]


@pytest.mark.unit
def test_format_date_list_empty():
    assert format_date_list([]) == []


@pytest.mark.unit
def test_format_date_list_leap_day():
    assert format_date_list([date(2024, 2, 29)]) == [
        {"date": "2024-02-29", "day": "Thursday"},
    ]


# --------------------------------------------------
# format_duration
# --------------------------------------------------

@pytest.mark.unit
@pytest.mark.parametrize(
    ("total_seconds", "expected"),
    [
        (
            45,
            {
                "days": 0,
                "hours": 0,
                "minutes": 0,
                "seconds": 45,
                "total_seconds": 45,
            },
        ),
        (
            125,
            {
                "days": 0,
                "hours": 0,
                "minutes": 2,
                "seconds": 5,
                "total_seconds": 125,
            },
        ),
        (
            3665,
            {
                "days": 0,
                "hours": 1,
                "minutes": 1,
                "seconds": 5,
                "total_seconds": 3665,
            },
        ),
        (
            90061,
            {
                "days": 1,
                "hours": 1,
                "minutes": 1,
                "seconds": 1,
                "total_seconds": 90061,
            },
        ),
        (
            0,
            {
                "days": 0,
                "hours": 0,
                "minutes": 0,
                "seconds": 0,
                "total_seconds": 0,
            },
        ),
        (
            -3665,
            {
                "days": 0,
                "hours": 1,
                "minutes": 1,
                "seconds": 5,
                "total_seconds": -3665,
            },
        ),
    ],
)
def test_format_duration(total_seconds, expected):
    assert format_duration(total_seconds) == expected


@pytest.mark.unit
def test_format_duration_multiple_days():
    total_seconds = 3 * 86400 + 2 * 3600 + 15 * 60 + 10

    assert format_duration(total_seconds) == {
        "days": 3,
        "hours": 2,
        "minutes": 15,
        "seconds": 10,
        "total_seconds": total_seconds,
    }