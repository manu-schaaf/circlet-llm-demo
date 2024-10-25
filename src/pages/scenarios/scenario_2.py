import streamlit as st

from pages.scenarios.base import chat_interface

st.title("Information Retrieval")
st.header("Few-Shot Prompting")


chat_interface("scenario_2")
