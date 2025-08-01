import streamlit as st
from streamlit_extras.stylable_container import stylable_container
import pandas as pd
import numpy as np

from huggingface_hub import InferenceClient
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

st.title("Fitness Coach Chat")

client = InferenceClient(api_key=st.secrets["HF_TOKEN"])

# List of Dictionaries to store chat history, where key is role and value is the message
if "messages" not in st.session_state: 
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user input
if prompt := st.chat_input("How can I help you?"):
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(f"{st.session_state['selected_user']}: {prompt}")
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": f"{st.session_state['selected_user']}: {prompt}"})

    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        response = ""

        daily_entries_data = database.get_daily_entries_data_for_ai(st.session_state['selected_user'], date.today() - timedelta(days= 30), 30)
        workout_entries_data = database.get_workout_entries_data_for_ai(st.session_state['selected_user'], date.today() - timedelta(days= 30), 30)
        
        messages = [
            {"role": "system", "content": "You are a friendly fitness coach named Coach. Always start your responses with 'Coach:'. Give brief, helpful answers. Only provide detailed information when specifically asked."},
            {"role": "system", "content": f"Here are the user's data from the last 30 days: \nDaily Entries:\n{daily_entries_data}\n\nWorkout Entries:\n{workout_entries_data}\n\nAnalyze this data to give personalized advice when asked."}
            ]
        messages += st.session_state.messages

        stream = client.chat.completions.create(
            model="mistralai/Mistral-7B-Instruct-v0.2",
            messages=messages,
            stream=True,
        )

        for chunk in stream:
            response += chunk.choices[0].delta.content
            message_placeholder.markdown(response)
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})
