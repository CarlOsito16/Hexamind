import os
import numpy as np
import streamlit as st
import requests
from streamlit_chat import message as st_message


url = "https://weatherapi-com.p.rapidapi.com/current.json"
headers = {
	"X-RapidAPI-Key": "f54ad8a758msh929bb66b74f430fp15e1f8jsnabec54e98778",
	"X-RapidAPI-Host": "weatherapi-com.p.rapidapi.com"
}


st.title('Demo screen as an agent')


if "history" not in st.session_state:
    st.session_state.history = []
    
row1_col1, row1_col2 = st.columns([1,1])

container = st.empty()
with row1_col1:
    user_input = st.text_input("What city  would you like to know about the weather",
        key = 'input_text')


    querystring = {"q":user_input}


    response = requests.request("GET", url, headers=headers, params=querystring)

# st.write(response.text['current']['temp_c'])
# st.json(response.text)
# st.write(response.text[1])

    
    clean_response = response.json()
    final_response = clean_response['current']['temp_c']
    

    
    confidence = np.random.randint(low=0, high=100) 
    
    container.write(f"This is the answer from the bot: **{final_response}** C")    
    container.write(f"The confidence level is {confidence}%")
    
    button_col1, button_col2 = st.columns([1,1])
    with button_col1:
        ok_button = st.button("OK with response")
    with button_col2:
        not_ok_button = st.button("I want to intervene")
        
        
            
    if ok_button:
        user_message = st.session_state.input_text
        bot_message = f"Current temperature in {user_message} = {final_response} C"
        st.session_state.history.append({"message": user_message, "is_user": True})
        st.session_state.history.append({"message": bot_message, "is_user": False})
        container.empty()
    
    if not_ok_button:
        container.empty()
        agent_message_input = st.text_input("what should the bot say instead?")
        user_message = st.session_state.input_text
        # agent_message = f"Current temperature in {user_message} = {final_response} C"
        container.write(f"The intervened message is {agent_message_input}C")


with row1_col2:
    for chat in st.session_state.history:
        st_message(**chat)  # unpacking
