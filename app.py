import streamlit as st
from UI.navigation import render_navigation

st.set_page_config(
    page_title="AI Learning Assistant",
    page_icon="🧑‍💻",
    layout="wide",
)

render_navigation()
