import streamlit as st

st.set_page_config(
    page_title="Latests Proxies",
    page_icon="",
)
import os

FILE_PATH = "scrapinghub/proxies.txt"  # Update this with your actual file path

st.title("Static Proxy File Viewer 📁")

try:
    # Read proxies from fixed path
    with open(FILE_PATH, "r", encoding="utf-8") as f:
        proxies = [line.strip() for line in f.readlines() if line.strip()]

    if proxies:
        st.success(f"Found {len(proxies)} proxies in file:")
        
        # Display statistics
        col1, col2 = st.columns(2)
        col1.metric("Total Proxies", len(proxies))
        col2.metric("File Location", os.path.abspath(FILE_PATH))

        # Display proxies in a table
        st.dataframe(
            proxies,
            column_config={"value": "Proxy List"},
            height=min(400, len(proxies) * 35),
            use_container_width=True
        )

        # Optional: Show raw text preview
        with st.expander("Raw File Preview"):
            st.code("\n".join(proxies), language="text")

    else:
        st.warning("File exists but contains no valid proxies!")

except FileNotFoundError:
    st.error(f"Proxy file not found at: {os.path.abspath(FILE_PATH)}")
except Exception as e:
    st.error(f"Error reading file: {str(e)}")