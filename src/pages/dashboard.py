import streamlit as st
from streamlit_extras.stylable_container import stylable_container
import pandas as pd
import numpy as np

from datetime import date, datetime, time, timedelta
from trackables import User, DailyEntry, WorkoutEntry
from database import Database

if not st.session_state.get('user_authenticated'):
    st.error('⚠️ Please login from the home page and try again.')
    if st.button("Go Back"):
        st.switch_page("main.py")
    st.stop()

database = Database()

st.title(f"Welcome back, {st.session_state['selected_user']}! 💪")
st.subheader("Your weekly averages so far:")

# Gather dates used for the averages of this week so far, and last week
today = date.today()
this_monday = today - timedelta(days=today.weekday())
last_monday = this_monday - timedelta(days=7)

# Gather Daily Entries from this week and last week
this_week_daily_entries = database.get_daily_entries_from_date(st.session_state['selected_user'], this_monday, 7)
last_week_daily_entries = database.get_daily_entries_from_date(st.session_state['selected_user'], last_monday, 7)

# Gather Workout Entries from this week and last week
this_week_workout_entries = database.get_workout_entries_from_date(st.session_state['selected_user'], this_monday, 7)
last_week_workout_entries = database.get_workout_entries_from_date(st.session_state['selected_user'], last_monday, 7)

this_week_weights = [entry.weight for entry in this_week_daily_entries if entry.weight is not None]
last_week_weights = [entry.weight for entry in last_week_daily_entries if entry.weight is not None]

if this_week_weights:
    avg_weight_this_week = sum(this_week_weights) / len(this_week_weights)
    weight_display = f"{avg_weight_this_week:.2f} Lbs"

    if last_week_weights:
        avg_weight_last_week = sum(last_week_weights) / len(last_week_weights)
        weight_delta = f"{avg_weight_this_week - avg_weight_last_week:.2f} Lbs"
    else:
        weight_delta = "N/A"
else:
    weight_display = "N/A"
    weight_delta = None


col1, col2, col3 = st.columns(3)
col1.metric("Weight", weight_display, weight_delta, border= True, help= "Your average weight this week compared to last week")
col2.metric("Calories Consumed", "9 mph", "-8%", border= True)
col3.metric("Daily Steps", "86%", "4%", border= True)

col4, col5, col6 = st.columns(3)
col4.metric("Sleep", "70 °F", "1.2 °F", border= True)
col5.metric("", "9 mph", "-8%", border= True)
col6.metric("Daily Steps", "86%", "4%", border= True)