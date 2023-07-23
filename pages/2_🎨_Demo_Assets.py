import streamlit as st
from bs4 import BeautifulSoup
import requests
import openai
import json
import pandas as pd

st.title("Code Vert")
message_history = []
###
devpost_link = st.sidebar.text_input(
    "Enter Devpost link:"   
)
has_gallery = st.sidebar.radio("Devpost gallery?", ("Yes", "No"))
user_submit = st.sidebar.button("Create demo!")
st.sidebar.divider()
n_slides = st.sidebar.slider("Slide count", min_value=1, max_value=5)
###

def get_devpost(devpost_link, has_gallery=has_gallery):
    soup = BeautifulSoup(requests.get(devpost_link).text)
    app_details = soup.find(attrs={"id":"app-details-left"})
    devpost_details = app_details.find_all("div")[2 if has_gallery == "Yes" else 0]
    devpost_json = []
    for heading, paragraph in zip(devpost_details.find_all('h2'), devpost_details.find_all('p')):
        devpost_json.append((heading.text, paragraph.text))
    return devpost_json

def get_script(devpost_text, n_slides=n_slides, message_history=message_history):
    req = \
        f"""Write {n_slides} sentences presenting the following hackathon project.\n\n{devpost_text}"""
    message_history.append({"role": "user", "content": req})

    response = openai.ChatCompletion.create(
      model="gpt-3.5-turbo",
      messages=message_history,
      max_tokens=300
    )
    cv_resp = response["choices"][0]["message"]
    message_history.append(cv_resp)
    cv = cv_resp.content # title, narration, image_description
    return [sent + '.' for sent in cv.split('.')]

def get_assets(script, n_slides=n_slides):
    def get_image_asset(desc):
        response = openai.Image.create(
            prompt=desc,
            n=1,
            size="256x256"
        )
        print(response)
        image_url = response['data'][0]['url']
        return image_url
    
    all_urls = []
    for i in range(n_slides):
        slide = script[i]
        url = get_image_asset(slide)
        all_urls.append(url)
    print(all_urls)
    return all_urls

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

    # Write script w/ slides
    with st.spinner(text="Composing a script..."):
        script = get_script(devpost_text)

    # Get images per slide
    with st.spinner(text="Painting a better picture..."):
        assets = get_assets(script)

    # Display slideshow
    slideshow_df = pd.DataFrame(columns=["narration", "image_link"])
    for i, (slide, asset) in enumerate(zip(script[:n_slides], assets)):
        st.subheader(f"Slide {i+1}")
        st.image(asset, caption=slide)
        slideshow_df.loc[i] = [slide, asset]
    st.dataframe(slideshow_df)
    st.download_button(
        "Download slideshow", 
        slideshow_df.to_csv(index=False).encode('utf-8'),    
        "slideshow.csv",
        "text/csv",
        key='download-csv'
   )
