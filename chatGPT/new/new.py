import streamlit as st
from streamlit_chat import message as st_message
import numpy as np



# some_css = """
#  <style>
# [data-testid="stVerticalBlock"] {
#         color: red;
# }

# div.css-1mbg4kq.e1tzin5v0 {
#     color: pink;
#     overflow: auto
# }
# </style>
# """

# st.markdown(some_css, unsafe_allow_html=True)

if "history" not in st.session_state:
    st.session_state.history = []
    st.session_state.history.append({"message": "how can I help you today?", "is_user": False} )
    st.session_state.history.append({"message": "Tell me more about you", "is_user": True} )
    

# # agent_message  = st.text_input(bot_message)
pre_questions = ['who are you?',
                 'What are you doing?',
                 'How old are you?']

pre_answers = ["I don't know",
                 "I'm working at hexamind",
                 "I like NLP"]



if 'input_value' not in st.session_state:
    st.session_state.input_value = ""

col1, col2 = st.columns([2,1])
    

button1_text = pre_answers[0]
button2_text = pre_answers[1]
button3_text = pre_answers[2]

with col2:
    st.write("#### Candidate answers:")
    button1_clicked = st.button(button1_text)
    button2_clicked = st.button(button2_text)
    button3_clicked = st.button(button3_text)
    st.markdown("---")



# Define the callback functions to update the text input value
def update_input_value(button_text):
    # Update the input value to the text of the clicked button
    st.session_state.input_value = button_text
    
def send_message():
    st.session_state.history.append({"message": input_value  , "is_user": False})
    st.session_state.history.append({"message": f"{np.random.choice(pre_questions)} + {np.random.randint(low= 0,high =100, size=1)}"   , "is_user": True})



# Call the callback function when a button is clicked
if button1_clicked:
    update_input_value(button1_text)
if button2_clicked:
    update_input_value(button2_text)
if button3_clicked:
    update_input_value(button3_text)



with col1:
    st.write("#### Agent Placeholder:")
    # Update the default value of the text input widget
    input_value = st.text_input('Enter a value',
                                st.session_state.input_value)

    # Display the updated text input value
    # st.write('Updated value:', st.session_state.input_value)

    send_message_button = st.button("Send the message",
                                    on_click=send_message)
    
    st.markdown("---")

    
    
    with st.container():
        st.write("#### Conversation Screen:")
        for chat in st.session_state.history:
            st_message(**chat)


