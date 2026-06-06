# analytics.py

from typing import Optional

def calculate_tdee(
    weekly_weight_change_lbs: float,
    average_daily_calories: float
) -> float:
  
    CALORIES_PER_LB = 3500

    if average_daily_calories <= 0:
        raise ValueError("average_daily_calories must be greater than 0")
    if not (-3.0 <= weekly_weight_change_lbs <= 3.0):
        raise ValueError("weekly_weight_change_lbs seems unrealistic, verify your input")
    if not (500 <= average_daily_calories <= 10000):
        raise ValueError("average_daily_calories seems unrealistic, verify your input")

    daily_surplus_or_deficit = (weekly_weight_change_lbs * CALORIES_PER_LB) / 7

    estimated_tdee = average_daily_calories - daily_surplus_or_deficit

    return estimated_tdee

def calculate_rolling_average(
    weights: list[float],
    window: int = 7
) -> Optional[float]:

    if len(weights) < window:
        return None
    
    return sum(weights[-window:]) / window