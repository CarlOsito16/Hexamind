import streamlit as st
from streamlit_extras.add_vertical_space import add_vertical_space
from markdownlit import mdlit

st.set_page_config(
    page_title = 'Streamlit Sample Dashboard Template',
    page_icon = '✅',
    layout = 'wide'
)

# col1, col2 = st.columns([1,0.8])

# with col1:
#     st.image("chatGPT/new/UI-element/hexamind-pic.png")
    
# with col2:
#     st.write("""
#              ### Unleash your customer service with
#              # Hexamind Plus
#              """)   
    # st.write("# **Hexamind Plus**")
col1, col2, col3 = st.columns([1.5,3,1.5])
with col2:
    st.image("chatGPT/new/UI-element/hexamind-pic.png")
    
    

add_vertical_space(3)
st.markdown("<h4 style='text-align: center; color: black;'>Unleash your customer service chatbot with</h4>", unsafe_allow_html=True)
st.markdown("""
            <h1 style='text-align: center; 
            color: black;padding-top: 0px'>Hexamind Plus</h1>
            """, unsafe_allow_html=True)
# mdlit("""@(https://www.hexamind.ai)""")