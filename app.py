import streamlit as st

st.set_page_config(
    page_title="Berlin Emergency Services",
    layout="wide"
)

st.title("🚨 Berlin Emergency Services Analysis (2020–2025)")

st.markdown("""
### Project Scope
This project integrates **mission-level** and **regional planning data**
from Berliner Feuerwehr to analyze:
- Emergency demand growth
- Response efficiency
- Regional preparedness & inequality

📍 Data: Open Data Berlin Fire Brigade  
📅 Period: 2020–2025
""")

st.success("⬅️ Navigate using the sidebar")
