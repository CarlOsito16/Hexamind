import streamlit as st

from streamlit_chat import message as st_message


st.title('Demo of RASA')


if "history" not in st.session_state:
    st.session_state.history = []
    
    
def generate_answer():
    user_message = st.session_state.input_text
    bot_message = #THIS IS WHERE YOU A RASA FUNCTION THAT TAKE `user_message` AS INPUT
    st.session_state.history.append({"message": user_message, "is_user": True})
    st.session_state.history.append({"message": bot_message, "is_user": False})
    
    
user_input = st.text_input("What is on your mind?",
    key = 'input_text',
    on_change=generate_answer)

for chat in st.session_state.history:
    st_message(**chat)  