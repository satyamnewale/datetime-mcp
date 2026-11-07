
from utils.datetime_utils import get_date_difference
from utils.formatters import format_date
from utils.validator import validate_date

class DateDifferenceService:

    def calculate_date_difference(
        self,
        start_date: str,
        end_date: str
    ) -> dict:

        start = validate_date(start_date)
        end = validate_date(end_date)

        difference = get_date_difference(start, end)
        absolute_difference = abs(difference)

        return {
            "start_date": format_date(start),
            "end_date": format_date(end),
            "difference_days": absolute_difference,
            "signed_difference_days": difference,
            "difference_weeks": absolute_difference // 7,
            "remaining_days": absolute_difference % 7,
            "direction": (
                "future" if difference > 0
                else "past" if difference < 0
                else "same_date"
            )
        }