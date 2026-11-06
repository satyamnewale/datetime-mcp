from datetime import date, datetime, timedelta
from zoneinfo import ZoneInfo
from dateutil.relativedelta import relativedelta


class RelativeDateService:

    def calculate_relative_date(
        self,
        amount: int,
        unit: str,
        direction: str,
        timezone: str = "Asia/Kolkata"
    ) -> dict:

        today = datetime.now(ZoneInfo(timezone)).date()

        if amount < 0:
            raise ValueError("Amount must be non-negative")

        if direction not in ("past", "future"):
            raise ValueError("Direction must be past or future")

        if unit not in ("days", "weeks", "months", "years"):
            raise ValueError("Unsupported date unit")

        sign = -1 if direction == "past" else 1

        if unit == "days":
            result = today + timedelta(days=sign * amount)
        elif unit == "weeks":
            result = today + timedelta(weeks=sign * amount)
        elif unit == "months":
            result = today + relativedelta(months=sign * amount)
        else:
            result = today + relativedelta(years=sign * amount)

        return {
            "original_date": today.isoformat(),
            "result_date": result.isoformat(),
            "day": result.strftime("%A"),
            "amount": amount,
            "unit": unit,
            "direction": direction,
            "timezone": timezone
        }

    def get_previous_n_days_and_dates(
        self,
        n: int,
        timezone: str = "Asia/Kolkata"
    ) -> dict:

        if n < 1:
            raise ValueError("n must be at least 1")

        today = datetime.now(ZoneInfo(timezone)).date()

        dates = [
            today - timedelta(days=i)
            for i in range(n, 0, -1)
        ]

        return {
            "dates": [
                {"date": d.isoformat(), "day": d.strftime("%A")}
                for d in dates
            ],
            "count": len(dates),
            "timezone": timezone
        }

    def get_next_n_days_and_dates(
        self,
        n: int,
        timezone: str = "Asia/Kolkata"
    ) -> dict:

        if n < 1:
            raise ValueError("n must be at least 1")

        today = datetime.now(ZoneInfo(timezone)).date()

        dates = [
            today + timedelta(days=i)
            for i in range(1, n + 1)
        ]

        return {
            "dates": [
                {"date": d.isoformat(), "day": d.strftime("%A")}
                for d in dates
            ],
            "count": len(dates),
            "timezone": timezone
        }

    def get_week_dates(
        self,
        reference_date: str | None = None,
        week_starts_on: int = 0,
        timezone: str = "Asia/Kolkata"
    ) -> dict:

        if not 0 <= week_starts_on <= 6:
            raise ValueError("week_starts_on must be between 0 and 6")

        if reference_date:
            current = date.fromisoformat(reference_date)
        else:
            current = datetime.now(ZoneInfo(timezone)).date()

        offset = (current.weekday() - week_starts_on) % 7
        start = current - timedelta(days=offset)

        dates = [
            start + timedelta(days=i)
            for i in range(7)
        ]

        return {
            "week_start": dates[0].isoformat(),
            "week_end": dates[-1].isoformat(),
            "dates": [
                {"date": d.isoformat(), "day": d.strftime("%A")}
                for d in dates
            ],
            "timezone": timezone
        }