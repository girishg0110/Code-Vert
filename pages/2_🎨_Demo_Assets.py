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
n_slides = st.sidebar.slider("Slide count", min_value=1, max_value=20)
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
    # req = \
    #     f"""Write {n_slides} sentences presenting the following hackathon project.\n\n{devpost_text}"""
    # message_history.append({"role": "user", "content": req})

    # response = openai.ChatCompletion.create(
    #   model="gpt-3.5-turbo",
    #   messages=message_history,
    #   max_tokens=300
    # )
    # cv_resp = response["choices"][0]["message"]
    # message_history.append(cv_resp)
    # #cv_json = json.loads(cv_resp.content) # title, narration, image_description
    # cv = cv_resp.content
    # #print(cv_json)
    # print(cv)

    # return cv

    cv = """Our hackathon project, SeedSwap, is a website that connects growers and gardeners in local communities, allowing them to share and exchange seeds and best practices. Through our platform, users can post their excess seeds and find others interested in swapping for seeds they need for their own gardens. SeedSwap is built using a Flask backend API, React frontend, and utilizes MongoDB to manage outstanding offers.

One of the challenges we faced during the development process was connecting the frontend and backend, which we overcame by thoroughly studying documentation and gaining a deeper understanding of React. We're especially proud of the beautifully designed UI on the offers page, inspired by Bootstrap.js example components, and 
it marks our first successful endeavor in frontend development.

Through this project, we learned valuable skills in using React and connecting a frontend to a backend in a web application. Our next step for SeedSwap is to deploy it on a GC instance, allowing growers to start utilizing the platform and benefiting from the seed swapping community."""

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
    
    # all_urls = []
    # for i in range(n_slides):
    #     slide = script[i]
    #     url = get_image_asset(slide)
    #     all_urls.append(url)
    # print(all_urls)
    # return all_urls
    return ['https://oaidalleapiprodscus.blob.core.windows.net/private/org-P3QAG6EMESgbD78EY3TzAzKV/user-GBWmktfjnGjWbIlO2zgI4WvB/img-LyoLCxD2upnpVqdZM1KO3QQo.png?st=2023-07-23T11%3A46%3A41Z&se=2023-07-23T13%3A46%3A41Z&sp=r&sv=2021-08-06&sr=b&rscd=inline&rsct=image/png&skoid=6aaadede-4fb3-4698-a8f6-684d7786b067&sktid=a48cca56-e6da-484e-a814-9c849652bcb3&skt=2023-07-22T23%3A42%3A23Z&ske=2023-07-23T23%3A42%3A23Z&sks=b&skv=2021-08-06&sig=SccDuMx/g55x97DEZgJRTEBO86quYIYoxZkXFQzhFVQ%3D', 'https://oaidalleapiprodscus.blob.core.windows.net/private/org-P3QAG6EMESgbD78EY3TzAzKV/user-GBWmktfjnGjWbIlO2zgI4WvB/img-xUzCjJdcySNxF27G8IryPiQX.png?st=2023-07-23T11%3A46%3A47Z&se=2023-07-23T13%3A46%3A47Z&sp=r&sv=2021-08-06&sr=b&rscd=inline&rsct=image/png&skoid=6aaadede-4fb3-4698-a8f6-684d7786b067&sktid=a48cca56-e6da-484e-a814-9c849652bcb3&skt=2023-07-22T23%3A31%3A06Z&ske=2023-07-23T23%3A31%3A06Z&sks=b&skv=2021-08-06&sig=pWojAbkW1hWrC4waZvOjzcaoM/APjKxHMb0xVS99mt4%3D', 'https://oaidalleapiprodscus.blob.core.windows.net/private/org-P3QAG6EMESgbD78EY3TzAzKV/user-GBWmktfjnGjWbIlO2zgI4WvB/img-oJSI3295tJjSgLtiW7J5KbNN.png?st=2023-07-23T11%3A46%3A54Z&se=2023-07-23T13%3A46%3A54Z&sp=r&sv=2021-08-06&sr=b&rscd=inline&rsct=image/png&skoid=6aaadede-4fb3-4698-a8f6-684d7786b067&sktid=a48cca56-e6da-484e-a814-9c849652bcb3&skt=2023-07-22T23%3A36%3A27Z&ske=2023-07-23T23%3A36%3A27Z&sks=b&skv=2021-08-06&sig=s4srwgwlc4jO8Da%2B1x66sqkkTzmHEeDte5PGhiuUZ1c%3D']

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
