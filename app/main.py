# main.py

import streamlit as st
from datetime import date
from app.database import initialize_database, save_log_entry, get_logs_for_user, get_weights_for_user, get_or_create_user
from app.analytics import calculate_rolling_average, calculate_tdee, estimate_confidence, project_weight
from app.charts import weight_trend_chart, calories_chart

st.set_page_config(page_title="Fitness Tracker", layout="wide")
initialize_database()

st.title("Fitness Tracker")

user_name = st.selectbox("Who are you?", ["Dom", "Ari","Tony"])
user_id = get_or_create_user(user_name)

tab1, tab2 = st.tabs(["Log today", "Dashboard"])

with tab1:
    st.header("Log today")

    log_date = st.date_input("Date", value=date.today())
    weight_lbs = st.number_input("Weight (lbs)", min_value=50.0, max_value = 500.0, step=0.1)
    calories = st.number_input("Calories", min_value=0, max_value=10000, step=1)
    protein_g = st.number_input("Protein (g)", min_value=0, max_value=500, step=1)
    steps = st.number_input("Steps (Optional)", min_value=0, max_value=100000, step=1)
    notes = st.text_input("Notes (Optional)")

    if st.button("Save entry"):
        save_log_entry(user_id, str(log_date), weight_lbs, calories, protein_g, steps, notes)
        st.success("Entry saved")
        st.rerun()

with tab2:
    st.header("Dashboard")

    logs = get_logs_for_user(user_id)
    weights_data = get_weights_for_user(user_id)

    if not logs:
        st.info("No data yet. Log your first entry in the Log today tab.")
        st.stop()

    dates = [row[0] for row in weights_data]
    weights = [row[1] for row in weights_data]
    calories_list = [row[2] for row in logs]

    rolling_averages = []
    for i in range(len(weights)):
        avg = calculate_rolling_average(weights[:i+1])
        rolling_averages.append(avg if avg is not None else weights[i])

    average_daily_calories = sum(calories_list) / len(calories_list)
    weeks_of_data = len(weights) // 7
    if weeks_of_data < 1:
        st.info("Log at least 7 days of data to see your TDEE estimate.")
    else:
        weekly_weight_change = (weights[0] - weights[-1]) / weeks_of_data

        try:
            tdee = calculate_tdee(weekly_weight_change, average_daily_calories)
            confidence = estimate_confidence(weeks_of_data)
            projected = project_weight(weights[0], tdee, average_daily_calories)

            col1, col2, col3 = st.columns(3)
            col1.metric("Estimated TDEE", f"{tdee:.0f} cal")
            col2.metric("Confidence", f"{confidence:.0%}")
            col3.metric("Projected weight (30 days)", f"{projected:.1f} lbs")

        except ValueError as e:
            st.warning(f"Could not calculate TDEE: {e}")

    st.plotly_chart(weight_trend_chart(dates, weights, rolling_averages))
    st.plotly_chart(calories_chart(dates,calories_list, 2000))
