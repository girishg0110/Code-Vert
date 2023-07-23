import streamlit as st
import openai

openai.organization = st.secrets["OPENAI_ORG_ID"]
openai.api_key = st.secrets["OPENAI_SECRET_KEY"]

st.set_page_config(
    page_title="Welcome to Code Vert",
    page_icon="👋",
)

st.write("# Welcome to Code Vert! 👋")

st.sidebar.success("Head to the Devpost Analysis to interact with the Code Vert environmental analysis client.")

st.markdown(
    """
    Code Vert provides feedback on the environmental impact of hackathon projects and proposes strategies for risk mitigation. 
    Contestants can gain a competitive advantage by using the Demo Assets feature to compose their demo presentation video.
    
    * assess and address the environmental risks of your projects 🍃
    * optimize your time distribution between building and presenting ⏰
    * perform better in the final judging 👑 
    """
)
st.markdown("<p style=\"text-align:center\"><em>Good code is green code.</em></p>", unsafe_allow_html=True)