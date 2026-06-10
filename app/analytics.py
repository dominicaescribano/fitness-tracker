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

def estimate_confidence(
        weeks_of_data: int
) -> float:
    if weeks_of_data < 1:
        return 0.0
    elif weeks_of_data == 1:
        return 0.5
    elif weeks_of_data == 2:
        return 0.7
    elif weeks_of_data == 3:
        return 0.85
    else:
        return 1.0
    
def project_weight(
        current_weight_lbs: float,
        estimated_tdee: float,
        average_daily_calories: float,
        days: int = 30
) -> float:
    net_caloric_gain = (average_daily_calories - estimated_tdee) * days
    net_weight_gain = net_caloric_gain / 3500
    projected_weight = current_weight_lbs + net_weight_gain
    return projected_weight
