import streamlit as st

st.set_page_config(
    page_title="Welcome to Code Vert",
    page_icon="👋",
)

st.write("# Welcome to Code Vert! 👋")

st.sidebar.success("Head to the Devpost Analysis to interact with the Code Vert environmental analysis client.")

st.markdown(
    """
    Code Vert provides feedback on the environmental impact of hackathon projects and proposes strategies for risk mitigation. 
    Contestants can gain a competitive advantage by using the Demo Assets feature to write their Devpost pages and compose their demo presentation video.
    
    """
)