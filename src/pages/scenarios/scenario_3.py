import streamlit as st

from pages.scenarios.base import chat_interface

st.title("Information Retrieval")
st.header("Chain-of-Thought Prompting")


chat_interface("scenario_2")
