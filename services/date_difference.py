from datetime import date


class DateDifferenceService:

    def calculate_date_difference(
        self,
        start_date: str,
        end_date: str
    ) -> dict:

        start = date.fromisoformat(start_date)
        end = date.fromisoformat(end_date)

        difference = (end - start).days

        return {
            "start_date": start.isoformat(),
            "end_date": end.isoformat(),
            "difference_days": abs(difference),
            "signed_difference_days": difference,
            "difference_weeks": abs(difference) // 7,
            "remaining_days": abs(difference) % 7,
            "direction": (
                "future" if difference > 0
                else "past" if difference < 0
                else "same_date"
            )
        }