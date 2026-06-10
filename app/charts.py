# charts.py

import plotly.graph_objects as go

def weight_trend_chart(dates: list, weights: list, rolling_averages: list) -> go.Figure:
    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=dates,
        y=weights,
        mode="lines+markers",
        name="Daily weight"
    ))

    fig.add_trace(go.Scatter(
        x=dates,
        y=rolling_averages,
        mode="lines",
        name="Rolling averages"
    ))

    fig.update_layout(
        title="Weight Trend"
    )
    return fig

def calories_chart(dates: list, average_daily_calories: list, calorie_target: int) -> go.Figure:
    fig = go.Figure()

    fig.add_trace(go.Bar(
        x=dates,
        y=average_daily_calories,
        name="Daily calories"
    ))

    fig.add_trace(go.Scatter(
        x=dates,
        y=[calorie_target] * len(dates),
        mode="lines",
        name="Calorie target"
    ))

    fig.update_layout(
        title="Daily Caloric Intake"
    )
    return fig