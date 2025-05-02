import streamlit as st

st.set_page_config(
    page_title="Scrapinghub Insights",
    page_icon="👋",
)

st.write("# Welcome to the Scrapinghub Insights dashboard! 👋")

st.sidebar.text("Select an option above.")

st.markdown(
    """
    Scrapinghub Insights is an app that was built specifically for
    displaying data from Scrapinghub with Streamlit.
    **👈 Select an option from the sidebar** to see some insights.
    
    This project is a showcase of a full stack data pipeline built with Docker,
    Apache Airflow, Scrapy, and Streamlit. The pipeline is used to scrape art
    data from scrapinghub, process it, and then serve it in a web app built with
    Streamlit. The web app includes a table of scraped data, and a few
    interactive charts.
"""
)