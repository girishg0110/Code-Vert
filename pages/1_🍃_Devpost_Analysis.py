import streamlit as st
from bs4 import BeautifulSoup
import requests
import openai
import json

st.title("Code Vert")
message_history = []
###
devpost_link = st.sidebar.text_input(
    "Enter Devpost link:"   
)
has_gallery = st.sidebar.radio("Devpost gallery?", ("Yes", "No"))
user_submit = st.sidebar.button("Evaluate")
st.sidebar.divider()
risk_areas = st.sidebar.multiselect(
    "Target risk areas",
    options=["Sustainability", "Energy Efficiency", "Reduced Carbon Footprint"],
    default=[]
)
n_members = st.sidebar.slider(
    "Team size",
    min_value = 1,
    max_value = 6
)
###

def get_devpost(devpost_link, has_gallery=has_gallery):
    soup = BeautifulSoup(requests.get(devpost_link).text)
    app_details = soup.find(attrs={"id":"app-details-left"})
    devpost_details = app_details.find_all("div")[2 if has_gallery == "Yes" else 0]
    devpost_json = []
    for heading, paragraph in zip(devpost_details.find_all('h2'), devpost_details.find_all('p')):
        devpost_json.append((heading.text, paragraph.text))
    return devpost_json

def analyze_devpost(devpost_text, risk_areas, message_history=message_history):
    system_message = f"""
        You are an API that receives descriptions of hackathon projects and returns JSON with the three following fields: 
        (1) "assessment": an assessment of the environmental risks of the following hackathon project especially pertaining to [{','.join(risk_areas)}] 
        (2) "modifications": a list of {n_members} specific code modifications to the project to mitigate those risks and 
        (3) "sources": "link"s to articles providing more information about the risk and the "organization" behind that article.
    """
    if not message_history:
        message_history = [{"role": "system", "content": system_message}]
    message_history.append({"role": "user", "content": devpost_text})

    response = openai.ChatCompletion.create(
       model="gpt-3.5-turbo",
       messages=message_history
    )
    cv_resp = response["choices"][0]["message"]
    message_history.append(cv_resp)
    cv_json = json.loads(cv_resp.content) # assessment, modifications, sources
    return cv_json

def write_dv(devpost_json):
    devpost_text = ""
    for (heading, paragraph) in devpost_json:
        st.subheader(heading)
        st.write(paragraph)
        devpost_text += (f'{heading}:{paragraph}\n')
    return devpost_text

if user_submit:
    # Show parsed
    with st.spinner(text="Retrieving your Devpost..."):
        devpost_json = get_devpost(devpost_link)
        with st.expander("Current Devpost"):
           devpost_text = write_dv(devpost_json)

    # Get feedback
    with st.spinner(text="Analyzing your Devpost..."):
        feedback = analyze_devpost(devpost_text, risk_areas)
    print(feedback)
    st.subheader("Assessment")
    st.write(feedback['assessment'])

    # Get action items
    st.subheader("Action Items")
    for i, action_item in enumerate(feedback["modifications"]):
        st.markdown(f"{i+1}. {action_item}")

    # Display sources of additional information
    st.subheader("Sources")
    for i, source in enumerate(feedback["sources"]):
        st.markdown(f"<a href=\"{source['link']}\">{source['organization']}</a>", unsafe_allow_html = True)
