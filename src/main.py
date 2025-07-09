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

