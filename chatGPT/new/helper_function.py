import streamlit as st
import numpy as np

# from app import input_value


if "history" not in st.session_state:
    st.session_state.history = []
    st.session_state.history.append({"message": "how can I help you today?", "is_user": False} )
    st.session_state.history.append({"message": "Tell me more about you", "is_user": True} )

if 'input_value' not in st.session_state:
    st.session_state.input_value = ""

# # agent_message  = st.text_input(bot_message)
pre_questions = ['who are you?',
                 'What are you doing?',
                 'How old are you?']

pre_answers = ["I don't know",
                 "I'm working at hexamind",
                 "I like NLP",
                 "I live in Paris",
                 "My name is HexaBot",
                 "TGIF",
                 "I'm sorry I dont'understand"]



# Define the callback functions to update the text input value
def update_input_value(button_text):
    # Update the input value to the text of the clicked button
    st.session_state.input_value = button_text
    