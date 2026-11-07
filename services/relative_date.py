from datetime import date

from utils.datetime_utils import (
    get_current_date,
    add_days,
    add_weeks,
    add_months,
    add_years,
    get_week_start,
)
from utils.formatters import format_date, format_date_list

from utils.validator import (
    validate_amount,
    validate_unit,
    validate_week_start,
    validate_date,
    SUPPORTED_DATE_UNITS,
)


class RelativeDateService:

    def calculate_relative_date(
        self,
        amount: int,
        unit: str,
        direction: str,
        timezone: str = "Asia/Kolkata"
    ) -> dict:

        amount = validate_amount(amount)
        unit = validate_unit(unit, SUPPORTED_DATE_UNITS)

        if direction not in ("past", "future") :
            raise ValueError("Direction must be past or future")

        today = get_current_date(timezone)

        sign = -1 if direction == "past" else 1

        operations = {
            "days" : add_days,
            "weeks" : add_weeks,
            "months" : add_months,
            "years" : add_years
        }

        result = operations[unit](today, sign * amount)

        return {
            "original_date": format_date(today),
            "result_date": format_date(result),
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

        n = validate_amount(n, minimum = 1)

        today = get_current_date(timezone)

        dates = [
            add_days(today, i)
            for i in range(-n, 0)
        ]

        return {
            "dates": format_date_list(dates),
            "count": len(dates),
            "timezone": timezone
        }

    def get_next_n_days_and_dates(
        self,
        n: int,
        timezone: str = "Asia/Kolkata"
    ) -> dict:

        n = validate_amount(n, minimum = 1)

        today = get_current_date(timezone)

        dates = [
            add_days(today, i)
            for i in range(1, n + 1)
        ]

        return {
            "dates": format_date_list(dates),
            "count": len(dates),
            "timezone": timezone
        }

    def get_week_dates(
        self,
        reference_date: str | None = None,
        week_starts_on: int = 0,
        timezone: str = "Asia/Kolkata"
    ) -> dict:

        week_starts_on = validate_week_start(week_starts_on)

        current = (
            validate_date(reference_date)
            if reference_date
            else get_current_date(timezone)
        )

        start = get_week_start(current, week_starts_on)

        dates = [
            add_days(start, i)
            for i in range(7)
        ]

        return {
            "week_start": format_date(dates[0]),
            "week_end": format_date(dates[-1]),
            "dates": format_date_list(dates),
            "timezone": timezone
        }