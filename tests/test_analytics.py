# test_analytics.py

import pytest
from app.analytics import calculate_tdee, calculate_rolling_average

def test_tdee_basic_calculation():
    assert calculate_tdee(-1.0,2300.0) == pytest.approx(2800, abs=50)

def test_calculate_tdee_when_calories_are_zero():
    with pytest.raises(ValueError):
        calculate_tdee(-1.0,0)

def test_calculate_tdee_with_unrealistic_weight_change():
    with pytest.raises(ValueError):
        calculate_tdee(25,2500)

def test_calculate_rolling_average_with_insufficient_entries():
    assert calculate_rolling_average([1,2,3],7) is None
