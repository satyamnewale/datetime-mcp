import pytest

from datetime import date, datetime
from freezegun import freeze_time
from zoneinfo import ZoneInfo


@pytest.fixture
def frozen_time():
    """
    Freeze system time at:
    2026-11-05 10:00:00 UTC
    2026-11-05 15:30:00 Asia/Kolkata
    """
    with freeze_time("2026-11-05 10:00:00", tz_offset=0):
        yield


@pytest.fixture
def timezone_name():
    return "Asia/Kolkata"


@pytest.fixture
def fixed_datetime():
    return datetime(
        2026, 11, 5, 15, 30, 0,
        tzinfo=ZoneInfo("Asia/Kolkata")
    )


@pytest.fixture
def fixed_utc_datetime():
    return datetime(
        2026, 11, 5, 10, 0, 0,
        tzinfo=ZoneInfo("UTC")
    )


@pytest.fixture
def fixed_date():
    return date(2026, 11, 5)


@pytest.fixture
def invalid_timezone():
    return "Invalid/Timezone"


@pytest.fixture
def valid_date_range():
    return "2026-11-01", "2026-11-07"


@pytest.fixture
def invalid_date_range():
    return "2026-11-10", "2026-11-01"