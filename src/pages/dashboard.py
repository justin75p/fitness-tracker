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

st.title(f"Welcome back, {st.session_state['selected_user']}! 💪")
st.subheader("Your weekly averages so far:")

col1, col2, col3 = st.columns(3)
col1.metric("Weight", "70 °F", "1.2 °F", border= True)
col2.metric("Calories Consumed", "9 mph", "-8%", border= True)
col3.metric("Daily Steps", "86%", "4%", border= True)

col4, col5, col6 = st.columns(3)
col4.metric("Sleep", "70 °F", "1.2 °F", border= True)
col5.metric("", "9 mph", "-8%", border= True)
col6.metric("Daily Steps", "86%", "4%", border= True)