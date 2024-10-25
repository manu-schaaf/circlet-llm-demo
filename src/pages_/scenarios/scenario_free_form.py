from pathlib import Path
from typing import Final

import streamlit as st
import yaml

from circlet.models import LLAMA_8B, MODELS_BY_TAG

st.title("Information Retrieval")
st.header("Design Your Own Prompt")

st.markdown(
    """
Feel free to experiment yourself!
Design your own system prompt and ask the model questions about the text to see how well it can retrieve relevant information.
Here are the available models:
"""
)

with st.expander("Models", expanded=False):
    for model in MODELS_BY_TAG.values():
        st.markdown(f"#### {model.name}")
        st.caption(model.description)

DOCUMENT_PATH = Path(__file__).parent / "news/bbc-ce31w8dzepno.yaml"
DOCUMENT_YAML: dict = yaml.load(
    DOCUMENT_PATH.open("r"),
    yaml.Loader,
)

MODEL_NAME: Final[str] = LLAMA_8B.tag

with st.form("settings", enter_to_submit=False):
    system_prompt = st.text_area(
        "System Prompt",
        value="You are a helpful assistant for Information Retrieval. Given a Document and a Query, you need to find the most relevant information in the document. Always answer to the best of your knowledge using the provided document. Do not deflect or refuse to answer questions, unless the information is not provided in the given document.",
    )
    initial_message = st.text_area(
        "Initial Message (without response)",
        value="Document:\n" + DOCUMENT_YAML["text"],
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
    st.switch_page(st.Page("pages_/free_form_chat.py"))
