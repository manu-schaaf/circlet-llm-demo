from typing import Final

import streamlit as st

from circlet.chat_ui import chat_interface
from circlet.lib.chat import InitialUserMessage, SystemMessage
from circlet.models import LLAMA_8B, MODELS_BY_NAME, REFLECTION
from pages_.scenarios.news import DOCUMENT_YAML

SCENARIO_NAME: Final[str] = "scenario_dyop"

st.header("Design Your Own Prompt")

st.markdown(
    """
Feel free to experiment yourself!
Design your own _System Prompt_ and ask the model questions about the text to see how well it can retrieve relevant information.
You can also try the prompt on a different document, by changing the _Initial Message_.

See below for some information on the available models.
"""
)

with st.expander("_Available Models_", expanded=False):
    st.markdown("#### Llama-3.1 8B / 70B")
    st.caption(LLAMA_8B.description)

    st.markdown("#### Reflection 70B")
    st.caption(REFLECTION.description)

if "dyop_mode" not in st.session_state:
    st.session_state.dyop_mode = "setup"

if "dyop_system_prompt" not in st.session_state:
    st.session_state.dyop_system_prompt = """You are a helpful assistant for Information Retrieval.
Given a `Document` and a `Query`, you need to find the most relevant information in the document.
Always answer to the best of your knowledge using the provided document.
Assume that the document is a reliable source of information and up-to-date.
You must not deflect or refuse to answer questions, unless the information is not provided in the given document."""

if "dyop_initial_message" not in st.session_state:
    st.session_state.dyop_initial_message = "Document:\n" + DOCUMENT_YAML["text"]

if "dyop_model" not in st.session_state:
    st.session_state.dyop_model = LLAMA_8B.name

with st.expander("**Configuration**", expanded=st.session_state.dyop_mode == "setup"):
    with st.form("dyop_conf", enter_to_submit=False, border=False):
        st.session_state.dyop_system_prompt = st.text_area(
            "System Prompt",
            value=st.session_state.dyop_system_prompt,
            height=200,
        )
        st.session_state.dyop_initial_message = st.text_area(
            "Initial Message (without response)",
            value=st.session_state.dyop_initial_message,
            height=200,
        )
        model_names = list(MODELS_BY_NAME.keys())
        st.session_state.dyop_model = st.selectbox(
            "Model",
            model_names,
            format_func=lambda m: MODELS_BY_NAME[m].pretty,
            index=model_names.index(st.session_state.dyop_model),
        )
        submitted = st.form_submit_button(
            "Save Configuration"
            if st.session_state.dyop_mode == "setup"
            else "Update Configuration"
        )
    if submitted:
        st.session_state.dyop_mode = "chat"
        st.rerun()

if st.session_state.dyop_mode == "chat":
    chat_interface(
        SCENARIO_NAME,
        initial_messages=[
            SystemMessage(st.session_state.dyop_system_prompt),
            InitialUserMessage(st.session_state.dyop_initial_message),
        ],
        model_name=st.session_state.dyop_model,
    )
else:
    st.markdown("_Design your own prompt above!_")
