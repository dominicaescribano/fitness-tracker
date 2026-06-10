# test_analytics.py

import pytest
from app.analytics import calculate_tdee, calculate_rolling_average, estimate_confidence, project_weight

def test_calculate_tdee_basic_calculation():
    assert calculate_tdee(-1.0,2300.0) == pytest.approx(2800, abs=50)

def test_calculate_tdee_when_calories_are_zero():
    with pytest.raises(ValueError):
        calculate_tdee(-1.0,0)

def test_calculate_tdee_with_unrealistic_weight_change():
    with pytest.raises(ValueError):
        calculate_tdee(25,2500)

def test_calculate_rolling_average_basic_calculation():
    assert calculate_rolling_average([100,102,98,100,101,99,100],7) == 100

def test_calculate_rolling_average_with_insufficient_entries():
    assert calculate_rolling_average([1,2,3],7) is None

def test_project_weight_loss_basic_calculation():
    assert project_weight(180.0,2500.0,2000.0,21) == pytest.approx(177, abs=0.1)

def test_estimate_confidence_insufficient_data():
    assert estimate_confidence(0) == 0.0

def test_estimate_confidence_high():
    assert estimate_confidence(4) == 1.0