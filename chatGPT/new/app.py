import streamlit as st
from streamlit_chat import message as st_message
from helper_function import *

if "history" not in st.session_state:
    st.session_state.history = []
    st.session_state.history.append({"message": "how can I help you today?", "is_user": False} )
    st.session_state.history.append({"message": "Tell me more about you", "is_user": True} )

if 'input_value' not in st.session_state:
    st.session_state.input_value = ""

row1_col1, row1_col2 = st.columns([2,1])
row2_col1, row2_col2 = st.columns([2,1])

# button1_text, button2_text, button3_text = np.random.choice(a= pre_answers, size=3 ,replace=False)
button1_text = pre_answers[0]
button2_text = pre_answers[1]
button3_text = pre_answers[2]


def send_message():
    global button1_text, button2_text, button3_text
    st.session_state.history.append({"message": input_value  , "is_user": False})
    st.session_state.history.append({"message": f"{np.random.choice(pre_questions)} + {np.random.randint(low= 0,high =100, size=1)}"   , "is_user": True})


with row1_col1:
    st.write("#### Conversation Screen:")
    for chat in st.session_state.history:
        st_message(**chat)
        

        
with row2_col2:
    st.markdown("---")
    st.write("#### Candidate answers:")
    button1_clicked = st.button(button1_text)
    button2_clicked = st.button(button2_text)
    button3_clicked = st.button(button3_text)
    
# Call the callback function when a button is clicked
if button1_clicked:
    update_input_value(button1_text)
if button2_clicked:
    update_input_value(button2_text)
if button3_clicked:
    update_input_value(button3_text)
    
with row2_col1:
    st.markdown("---")
    st.write("#### Agent Placeholder:")
    # Update the default value of the text input widget
    input_value = st.text_input('Enter a value',
                                st.session_state.input_value)
    send_message_button = st.button("Send the message",
                                    on_click=send_message)