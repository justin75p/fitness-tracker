import streamlit as st
from streamlit_extras.stylable_container import stylable_container
import pandas as pd
import numpy as np

from datetime import date, datetime, time, timedelta
from trackables import User, DailyEntry, WorkoutEntry, WeeklySummary
from database import Database

database = Database()

st.title("Fitness Tracker")

user_selection = st.selectbox("Select a user:", database.get_all_user_names(), index= None, placeholder= "Select from dropdown:")

with st.form("user_creation_form", clear_on_submit= True):
    new_user_name = st.text_input("Create a new user:", placeholder= "New user's name")

    starting_weight = st.text_input("Enter your starting weight (lbs):", placeholder= "New user's starting weight")

    goal_weight = st.text_input("Enter your goal weight (lbs):", placeholder= "New user's goal weight")

    maintenance_calories = st.text_input("Enter your maintenance calories:", placeholder= "New user's maintenance calories")
    
    submit = st.form_submit_button("Create user")

    if submit:
        if new_user_name and starting_weight and goal_weight and maintenance_calories:
            database.insert_user(User(new_user_name, starting_weight, goal_weight, maintenance_calories))
            st.session_state["user_created"] = True
            st.rerun()
        else:
            st.warning("Please fill in all required fields!")

    if 'user_created' in st.session_state:
        st.success(f"User '{new_user_name}' Created!")
        del st.session_state['user_created']

col1, col2 = st.columns([0.18, 0.82])

with col1:
    with stylable_container(key= "delete_user_button",
                            css_styles= """
                                button[data-testid="stBaseButton-secondary"] {
                                    -webkit-text-stroke: 0.5px red;
                                    border: 0.5px solid red;
                                }
                            """
                        ):
        delete_user = st.button("Delete User", use_container_width= True)

with col2:
    if delete_user:
        deleted_user_name = st.text_input("", label_visibility='collapsed', placeholder= "Name of user to delete:")
        database.delete_user(deleted_user_name)