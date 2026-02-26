"""
Budget Planner agent will use this to compute category totals and verify
the grand total against the traveller's given budget.
"""

from travel_planner.logger import get_logger

log = get_logger(__name__)


def calculate_budget(
    accommodation_per_night: float,
    food_per_day: float,
    transport_total: float,
    activities_total: float,
    num_nights: int,
    num_days: int,
) -> dict:
   
    log.debug(
        f"[Calculator] accommodation/night={accommodation_per_night}, "
        f"food/day={food_per_day}, transport={transport_total}, "
        f"activities={activities_total}, nights={num_nights}, days={num_days}"
    )

    try:
        accommodation = round(accommodation_per_night * num_nights, 2)
        food          = round(food_per_day * num_days, 2)
        transport     = round(transport_total, 2)
        activities    = round(activities_total, 2)
        total         = round(accommodation + food + transport + activities, 2)

        breakdown = {
            "accommodation": accommodation,
            "food":          food,
            "transport":     transport,
            "activities":    activities,
            "total":         total,
        }
        log.info(f"[Calculator] Breakdown: {breakdown}")
        return breakdown

    except Exception as e:
        log.exception(f"[Calculator] Calculation failed: {e}")
        return {
            "accommodation": 0.0,
            "food":          0.0,
            "transport":     0.0,
            "activities":    0.0,
            "total":         0.0,
            "error":         str(e),
        }