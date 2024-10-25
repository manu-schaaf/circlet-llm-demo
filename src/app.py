import streamlit as st
from openai import OpenAI
from requests import get

from circlet.lib.response import Response

if "client" not in st.session_state:
    st.session_state.client = OpenAI(
        base_url="http://gondor.hucompute.org:11434/v1/", api_key="sk-1234567890"
    )

status = Response.process(
    get("http://gondor.hucompute.org:11434/v1/models", timeout=10)
)
if status.ok() and st.session_state.get("client") is not None:
    if "status_ok" not in st.session_state:
        st.toast("Connection Established!", icon="🎉")
        st.session_state.status_ok = True
else:
    err_msg = (
        "Could not connect to the LLM server."
        if status.ok()
        else "Could not establish a client connection."
    )
    st.toast("Error: ", icon="🚨")

if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = {
        "scneario_1": "llama3.1:8b-instruct-q5_K_M",
        "scneario_2": "llama3.1:8b-instruct-q5_K_M",
        "scneario__": "llama3.1:70b-instruct-q4_K_M",
        "scneario___": "nemotron:latest",
    }


page_home = st.Page("pages/home.py", title="Home")
page_scenario_1 = st.Page(
    "pages/scenarios/scenario_1.py",
    title="1. Information Retrieval",
)
page_scenario_2 = st.Page(
    "pages/scenarios/scenario_2.py",
    title="2. Chain-of-Thought Prompting",
)

pg = st.navigation([page_home, page_scenario_1, page_scenario_2])
pg.run()
