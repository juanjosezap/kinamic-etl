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
    ### Want to learn more?
    - Check out [streamlit.io](https://streamlit.io)
    - Jump into our [documentation](https://docs.streamlit.io)
    - Ask a question in our [community
        forums](https://discuss.streamlit.io)
    ### See more complex demos
    - Use a neural net to [analyze the Udacity Self-driving Car Image
        Dataset](https://github.com/streamlit/demo-self-driving)
    - Explore a [New York City rideshare dataset](https://github.com/streamlit/demo-uber-nyc-pickups)
"""
)