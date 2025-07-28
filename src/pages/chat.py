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

st.title("Fitness Coach Chat")

# List of Dictionaries to store chat history, where key is role and value is the message
if "messages" not in st.session_state: 
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# React to user input
if prompt := st.chat_input("How can I help you?"):
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(f"{st.session_state['selected_user']}: {prompt}")
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

    response = f"Coach: {prompt}"
    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        st.markdown(response)
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})
