import streamlit as st
import pandas as pd
import numpy as np

from datetime import date, datetime, time, timedelta
from trackables import User, DailyEntry, WorkoutEntry, WeeklySummary
from database import Database

database = Database()

st.title("Fitness Tracker")

user_selection = st.selectbox("Select a user:", database.get_all_user_names(), index= 0)
new_user_name = st.text_input("Create a new user:", placeholder= "New user's name")

if new_user_name:
    starting_weight = st.text_input("Enter your starting weight (lbs):", placeholder= "New user's starting weight")
    
    if starting_weight:
        goal_weight = st.text_input("Enter your goal weight (lbs):", placeholder= "New user's goal weight")

        if goal_weight:
            maintenance_calories = st.text_input("Enter your maintenance calories:", placeholder= "New user's maintenance calories")

            if maintenance_calories:
                user_creation_button = st.button("Create User")

                if user_creation_button:
                    database.insert_user(User(new_user_name, starting_weight, goal_weight, maintenance_calories))
                    # TODO: get button to refresh site page