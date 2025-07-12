import streamlit as st
from streamlit_extras.stylable_container import stylable_container
import pandas as pd
import numpy as np

from datetime import date, datetime, time, timedelta
from trackables import User, DailyEntry, WorkoutEntry, WeeklySummary
from database import Database

database = Database()

st.title("Welcome to my Fitness Tracker 📊")
st.subheader("Select your profile or create a new one to get started! 🏃‍♂️")

user_selection = st.selectbox("Select a user:", database.get_all_user_names(), index= None, placeholder= "Select from dropdown:")

if user_selection:
    st.session_state['user_authenticated'] = True
    st.session_state['selected_user'] = user_selection
    st.switch_page("pages/dashboard.py")

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
            st.warning("❌ Please fill in all required fields!")

    if 'user_created' in st.session_state:
        st.success(f"✅ User '{new_user_name}' Created!")
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
    if delete_user or st.session_state.get('show_delete_form'):
        st.session_state['show_delete_form'] = True

        with st.form("user_deletion_form", clear_on_submit= True):
            deleted_user_name = st.selectbox("Select a user to delete:", database.get_all_user_names(), index= None, placeholder= "Name of user to delete:")

            col_empty1, col_confirm, col_cancel, col_empty2 = st.columns([0.2, 0.3, 0.3, 0.2])

            with col_confirm:
                submit_delete = st.form_submit_button("Confirm Delete")
            with col_cancel:
                cancel_delete = st.form_submit_button("Cancel Delete")

            if submit_delete and deleted_user_name:
                database.delete_user(deleted_user_name)
                st.session_state["user_deleted"] = deleted_user_name
                st.session_state['show_delete_form'] = False
                st.rerun()
            elif submit_delete and not deleted_user_name:
                st.warning("❌ Please specify a user to delete!")
            elif cancel_delete:
                st.session_state['show_delete_form'] = False
                st.rerun()

    if 'user_deleted' in st.session_state:
        st.success(f"✅ User '{st.session_state['user_deleted']}' Deleted!")
        del st.session_state['user_deleted']