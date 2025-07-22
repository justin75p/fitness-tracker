import streamlit as st
from streamlit_extras.stylable_container import stylable_container
import pandas as pd
import numpy as np

from datetime import date, datetime, time, timedelta
from trackables import User, DailyEntry, WorkoutEntry
from database import Database

st.set_page_config(layout="wide")

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

# ---------- Retrieve workout minutes from Workout Entries to display on the total workout minutes metric ---------- #
this_week_minutes = [workout_entry.minutes for workout_entry in this_week_workout_entries if workout_entry.minutes is not None]
last_week_minutes = [workout_entry.minutes for workout_entry in last_week_workout_entries if workout_entry.minutes is not None]

this_week_total_minutes = sum(this_week_minutes) if this_week_minutes else 0
last_week_total_minutes = sum(last_week_minutes) if last_week_minutes else 0

if this_week_total_minutes != 0:
    minutes_display = f"{this_week_total_minutes:.1f} mins"

    if last_week_total_minutes != 0:
        minutes_delta = f"{this_week_total_minutes - last_week_total_minutes:.1f} mins"
    else:   
        minutes_delta = "N/A"
else:
    minutes_display = "N/A"
    minutes_delta = None

# Metrics for weight, calories consumed and water consumed
col1, col2, col3 = st.columns(3)
col1.metric("Weight", weight_display, weight_delta, border= True,
            help= "Your average weight this week compared to last week.")
col2.metric("Calories Consumed", calories_display, calories_delta, border= True,
            help= "The average amount of calories consumed this week compared to last week.")
col3.metric("Water Consumed", water_display, water_delta, border= True,
            help= "The average amount of water you drank everyday this week compared to last week.")

# Metrics for daily steps, daily sleep, and total minutes worked out
col4, col5, col6 = st.columns(3)
col4.metric("Daily Steps", steps_display, steps_delta, border= True,
            help= "The average amount of steps you took everyday this week compared to last week.")
col5.metric("Daily Sleep", sleep_display, sleep_delta, border= True,
            help= "How many hours on average you slept each day this week compared to last week.")
col6.metric("Total Workout Time", minutes_display, minutes_delta, border= True,
            help= "The total amount of minutes you spent working out this week compared to last week.")

st.divider()

# Get data from start of current year
current_year = date.today().year
start_of_year = date(current_year, 1, 1)
# days_since_start = (date.today() - start_of_year).days + 1

daily_entries_data = database.get_daily_entries_from_date(st.session_state['selected_user'], start_of_year, 365)
weight_entries_data = database.get_workout_entries_from_date(st.session_state['selected_user'], start_of_year, 365)

st.subheader("Weight Chart")
# Create a chart to show weight trends
weight_entries = [entry for entry in daily_entries_data if entry.weight is not None]
weight_data = pd.DataFrame({
    'Date': [entry.entry_date for entry in weight_entries], 
    'Weight (lbs)': [entry.weight for entry in weight_entries]
})
st.line_chart(weight_data, x='Date', y='Weight (lbs)')


stepsChart, sleepChart = st.columns(2)
caloriesChart, waterChart = st.columns(2)

with caloriesChart:
    st.subheader("Calories Chart")
    # Create a chart to show calorie trends
    calories_entries = [entry for entry in daily_entries_data if entry.calories is not None]
    calories_data = pd.DataFrame({
        'Date': [entry.entry_date for entry in calories_entries], 
        'Calories Consumed (cals)': [entry.calories for entry in calories_entries]
    })
    st.line_chart(calories_data, x='Date', y='Calories Consumed (cals)')

with waterChart:
    st.subheader("Water Intake Chart")
    # Create a chart to show water intake trends
    water_entries = [entry for entry in daily_entries_data if entry.water is not None]
    water_data = pd.DataFrame({
        'Date': [entry.entry_date for entry in water_entries], 
        'Water Consumed (mL)': [entry.water for entry in water_entries]
    })
    st.line_chart(water_data, x='Date', y='Water Consumed (mL)')

with stepsChart:
    st.subheader("Daily Steps Chart")
    # Create a chart to show step trends
    steps_entries = [entry for entry in daily_entries_data if entry.steps is not None]
    steps_data = pd.DataFrame({
        'Date': [entry.entry_date for entry in steps_entries], 
        'Steps': [entry.steps for entry in steps_entries]
    })
    st.bar_chart(steps_data, x='Date', y='Steps')

with sleepChart:
    st.subheader("Daily Sleep Chart")
    # Create a chart to show sleep trends
    sleep_entries = [entry for entry in daily_entries_data if entry.water is not None]
    sleep_data = pd.DataFrame({
        'Date': [entry.entry_date for entry in sleep_entries], 
        'Time Slept (hrs)': [entry.sleep for entry in sleep_entries]
    })
    st.line_chart(sleep_data, x='Date', y='Time Slept (hrs)')