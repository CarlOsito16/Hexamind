import os
import streamlit as st
import openai

from streamlit_chat import message as st_message


st.title('Demo of chatGPT')

# api_key = os.environ.get('chagpt_API_KEY')
openai.api_key = os.environ["OPENAI_API_KEY"]



if "history" not in st.session_state:
    st.session_state.history = []
    
# if "input_text" not in st.session_state:
#     st.session_state.input_text = ""
    



def get_model_reply(query, context=[]):
    # combines the new question with a previous context
    context += [query]
    
    # given the most recent context (4096 characters)
    # continue the text up to 2048 tokens ~ 8192 charaters
    completion = openai.Completion.create(
        engine='text-davinci-003', # one of the most capable models available
        prompt='\n\n'.join(context)[:4096],
        max_tokens = 100,
        temperature = 0.0, # Lower values make the response more deterministic
    )
    
    # append response to context
    response = completion.choices[0].text.strip('\n')
    context += [response]
    
    # list of (user, bot) responses. We will use this format later
    responses = [(u,b) for u,b in zip(context[::2], context[1::2])]

    
    return responses, context


def generate_answer():
    user_message = st.session_state.input_text
    responses, context = get_model_reply(user_message)
    bot_message = responses[-1][1]
    st.session_state.history.append({"message": user_message, "is_user": True})
    st.session_state.history.append({"message": bot_message, "is_user": False})




container = st.empty()
user_input = st.text_input("What is on your mind?",
    key = 'input_text',
    on_change=generate_answer)
# Clear the container to remove the widget from the screen once the user hits enter
if user_input.strip():
    container.empty()


for chat in st.session_state.history:
    st_message(**chat)  # unpacking


# st.write(f"Q : {responses[-1][0]}")
# st.write(f"A : {responses[-1][1]}")

# query = 'Which is the largest country by area in the world?'
# responses, context = get_model_reply(query, context=[])

# st.write('<USER> ' + responses[-1][0])
# st.write('<BOT> ' + responses[-1][1])


import requests

url = "https://weatherapi-com.p.rapidapi.com/current.json"

querystring = {"q":"Bangkok"}

headers = {
	"X-RapidAPI-Key": "f54ad8a758msh929bb66b74f430fp15e1f8jsnabec54e98778",
	"X-RapidAPI-Host": "weatherapi-com.p.rapidapi.com"
}

response = requests.request("GET", url, headers=headers, params=querystring)

st.json(response.text)