import streamlit as st
from bs4 import BeautifulSoup
import requests
import cohere

st.title("Code Vert")
###
devpost_link = st.sidebar.text_input(
    "Enter Devpost link:"   
)
user_submit = st.sidebar.button("Evaluate")
st.sidebar.divider()
risk_areas = st.sidebar.multiselect(
    "Target risk areas",
    options=["Sustainability", "Energy Efficiency", "Reduced Carbon Footprint"],
    default=[]
)
###

co = cohere.Client(st.secrets["COHERE_TEMP_KEY"])

def get_devpost(devpost_link):
    soup = BeautifulSoup(requests.get(devpost_link).text)
    app_details = soup.find(attrs={"id":"app-details-left"})
    devpost_details = app_details.find_all("div")[2]
    devpost_json = []
    for heading, paragraph in zip(devpost_details.find_all('h2'), devpost_details.find_all('p')):
        devpost_json.append((heading.text, paragraph.text))
    return devpost_json

def analyze_devpost(devpost_text, risk_areas):
    response = co.generate(
        prompt="Return a JSON containing (1) an assessment of the environmental risks of the following hackathon project" \
                    + (f"especially pertaining to {','.join(risk_areas)}" if risk_areas else "") + \
                    f" (2) proposed modifications to the project to mitigate those risks and \
                    (3) sources of information to learn more about those risks.\n\n{devpost_text}",
        max_tokens=200
    )
    analysis = response.generations[0].text

    return analysis, ['hello', 'goodbye']

def modify_devpost(devpost_json, action_confirm):
    return 0

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
        feedback, action_items = analyze_devpost(devpost_text, risk_areas)
    st.write(feedback)

    # Get action items - checkboxes; submit
    for item in action_items:
        st.select(item)
    action_confirm = st.button("Action taken!")

    # Updated Devpost --> devpost access token??
    if action_confirm:
        with st.spinner(text="Rewriting your Devpost..."):
            updated_devpost = modify_devpost(devpost_json, action_confirm)
        st.write(updated_devpost)
    
