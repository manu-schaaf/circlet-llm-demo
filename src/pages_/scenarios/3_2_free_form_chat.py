from typing import Final

import streamlit as st

from circlet.chat_ui import chat_interface
from circlet.lib.chat import SystemMessage, InitialUserMessage

st.title("Information Retrieval")
st.header("Free Form Chat")

if (
    "ff_system_prompt" not in st.session_state
    or "ff_initial_message" not in st.session_state
    or "ff_model" not in st.session_state
):
    st.warning("Please set the system prompt, initial message, and model in '4. Free-Form: Design Your Own Prompt' before proceeding.")
else:
    SCENARIO_NAME: Final[str] = "scenario_free_form"
    messages = [
        SystemMessage(st.session_state.ff_system_prompt),
        InitialUserMessage(st.session_state.ff_initial_message),
    ]
    model = st.session_state.ff_model
    chat_interface(
        SCENARIO_NAME,
        initial_messages=messages,
        model_name=model,
    )
    if clicked := st.button("Go Back"):
        st.switch_page("pages_/scenarios/3_1_free_form.py")
    