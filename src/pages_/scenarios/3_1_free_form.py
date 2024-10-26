from typing import Final

import streamlit as st

from circlet.models import LLAMA_8B, MODELS_BY_TAG, REFLECTION
from pages_.scenarios.news import DOCUMENT_YAML

st.title("Information Retrieval")
st.header("Design Your Own Prompt")

st.markdown(
    """
Feel free to experiment yourself!
Design your own system prompt and ask the model questions about the text to see how well it can retrieve relevant information.
See below for some information on the available models.
"""
)

with st.expander("Available Models", expanded=False):
    st.markdown("#### Llama-3.1 8B / 70B")
    st.caption(LLAMA_8B.description)

    st.markdown("#### Reflection 70B")
    st.caption(REFLECTION.description)


MODEL_NAME: Final[str] = LLAMA_8B.tag

with st.form("settings", enter_to_submit=False):
    system_prompt = st.text_area(
        "System Prompt",
        value="You are a helpful assistant for Information Retrieval. Given a Document and a Query, you need to find the most relevant information in the document. Always answer to the best of your knowledge using the provided document. Do not deflect or refuse to answer questions, unless the information is not provided in the given document.",
        height=200,
    )
    initial_message = st.text_area(
        "Initial Message (without response)",
        value="Document:\n" + DOCUMENT_YAML["text"],
        height=200,
    )
    model = st.selectbox(
        "Model",
        MODELS_BY_TAG.keys(),
        format_func=lambda m: MODELS_BY_TAG[m].name,
    )
    submitted = st.form_submit_button("Submit")

if submitted:
    st.session_state.ff_system_prompt = system_prompt
    st.session_state.ff_initial_message = initial_message
    st.session_state.ff_model = model
    st.switch_page(st.Page("pages_/scenarios/3_2_free_form_chat.py"))
