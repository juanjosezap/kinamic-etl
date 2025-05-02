import streamlit as st


# Page config
st.set_page_config(page_title="Read Me")
# Basic method
def load_readme():
    with open("README.md", "r", encoding="utf-8") as f:
        return f.read()

st.markdown(load_readme(), unsafe_allow_html=True)