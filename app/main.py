# main.py

import streamlit as st
from datetime import date
from app.database import initialize_database, save_log_entry, get_logs_for_user, get_weights_for_user, get_or_create_user
from app.analytics import calculate_rolling_average, calculate_tdee, estimate_confidence, project_weight
from app.charts import weight_trend_chart, calories_chart

st.set_page_config(page_title="Fitness Tracker", layout="wide")
initialize_database

st.title("Fitness Tracker")

user_name = st.selectbox("Who are you?", ["Dom", "Ari"])
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
