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

# ---------- Retrieve weight from Daily Entries to display on the weight metric ---------- #
this_week_weights = [entry.weight for entry in this_week_daily_entries if entry.weight is not None]
last_week_weights = [entry.weight for entry in last_week_daily_entries if entry.weight is not None]

if this_week_weights:
    avg_weight_this_week = sum(this_week_weights) / len(this_week_weights)
    weight_display = f"{avg_weight_this_week:.2f} lbs"

    if last_week_weights:
        avg_weight_last_week = sum(last_week_weights) / len(last_week_weights)
        weight_delta = f"{avg_weight_this_week - avg_weight_last_week:.2f} lbs"
    else:
        weight_delta = "N/A"
else:
    weight_display = "N/A"
    weight_delta = None

# ---------- Retrieve calories consumed from Daily Entries to display on the calories consumed metric ---------- #
this_week_calories = [entry.calories for entry in this_week_daily_entries if entry.calories is not None]
last_week_calories = [entry.calories for entry in last_week_daily_entries if entry.calories is not None]

if this_week_calories:
    avg_calories_this_week = sum(this_week_calories) / len(this_week_calories)
    calories_display = f"{avg_calories_this_week:.0f} cal"

    if last_week_calories:
        avg_calories_last_week = sum(last_week_calories) / len(last_week_calories)
        calories_delta = f"{avg_calories_this_week - avg_calories_last_week:.0f} cal"
    else:
        calories_delta = "N/A"
else:
    calories_display = "N/A"
    calories_delta = None

# ---------- Retrieve water consumed from Daily Entries to display on the daily water metric ---------- #
this_week_water = [entry.water for entry in this_week_daily_entries if entry.water is not None]
last_week_water = [entry.water for entry in last_week_daily_entries if entry.water is not None]

if this_week_water:
    avg_water_this_week = sum(this_week_water) / len(this_week_water)
    water_display = f"{avg_water_this_week:.0f} mL"

    if last_week_water:
        avg_water_last_week = sum(last_week_water) / len(last_week_water)
        water_delta = f"{avg_water_this_week - avg_water_last_week:.0f} mL"
    else:
        water_delta = "N/A"
else:
    water_display = "N/A"
    water_delta = None

# ---------- Retrieve daily steps from Daily Entries to display on the daily steps metric ---------- #
this_week_steps = [entry.steps for entry in this_week_daily_entries if entry.steps is not None]
last_week_steps = [entry.steps for entry in last_week_daily_entries if entry.steps is not None]

if this_week_steps:
    avg_steps_this_week = sum(this_week_steps) / len(this_week_steps)
    steps_display = f"{avg_steps_this_week:.0f} steps"

    if last_week_steps:
        avg_steps_last_week = sum(last_week_steps) / len(last_week_steps)
        steps_delta = f"{avg_steps_this_week - avg_steps_last_week:.0f} steps"
    else:
        steps_delta = "N/A"
else:
    steps_display = "N/A"
    steps_delta = None

# ---------- Retrieve hours of sleep from Daily Entries to display on the daily sleep metric ---------- #
this_week_sleep = [entry.sleep for entry in this_week_daily_entries if entry.sleep is not None]
last_week_sleep = [entry.sleep for entry in last_week_daily_entries if entry.sleep is not None]

if this_week_sleep:
    avg_sleep_this_week = sum(this_week_sleep) / len(this_week_sleep)
    sleep_display = f"{avg_sleep_this_week:.1f} hrs"

    if last_week_sleep:
        avg_sleep_last_week = sum(last_week_sleep) / len(last_week_sleep)
        sleep_delta = f"{avg_sleep_this_week - avg_sleep_last_week:.1f} hrs"
    else:
        sleep_delta = "N/A"
else:
    sleep_display = "N/A"
    sleep_delta = None

# Gather Workout Entries from this week and last week
this_week_workout_entries = database.get_workout_entries_from_date(st.session_state['selected_user'], this_monday, 7)
last_week_workout_entries = database.get_workout_entries_from_date(st.session_state['selected_user'], last_monday, 7)

col1, col2, col3 = st.columns(3)
col1.metric("Weight", weight_display, weight_delta, border= True,
            help= "Your average weight this week compared to last week.")
col2.metric("Calories Consumed", calories_display, calories_delta, border= True,
            help= "The average amount of calories consumed this week compared to last week.")
col3.metric("Water Consumed", water_display, water_delta, border= True,
            help= "The average amount of water you drank everyday this week compared to last week.")

col4, col5, col6 = st.columns(3)
col4.metric("Daily Steps", steps_display, steps_delta, border= True,
            help= "The average amount of steps you took everyday this week compared to last week.")
col5.metric("Daily Sleep", sleep_display, sleep_delta, border= True,
            help= "How many hours on average you slept each day this week compared to last week.")
col6.metric("Daily Steps", "86%", "4%", border= True)