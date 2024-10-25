from pathlib import Path

import streamlit as st
import yaml
from requests import post

from circlet.lib.chat import SystemMessage, UserMessage
from circlet.lib.response import Response
from pages.scenarios.base import chat_interface

st.title("Information Retrieval")
st.header("Zero-Shot Prompting")

st.markdown(
    """
In this first scenario, the LLM was only given a basic description of the task in its *System Prompt*, which is treated differently from *User Prompts* or *Assistant Responses*, and no examples (_zero-shot_).

Below is an example for a [BBC news article](https://www.bbc.com/news/articles/ce31w8dzepno) from 25. October 2024.

- Ask the model some questions about the text to see how well it can retrieve relevant information.
- Try asking "plain" questions or prefixing your questions with `Query: ...`.

Some example questions:
1. What is the article about?
2. Who has the lead in US election polls?
3. What are is the history of the swing states in the US election?
"""
)

DOCUMENT_PATH = Path(__file__).parent / "news/bbc-ce31w8dzepno.yaml"
DOCUMENT_YAML: dict = yaml.load(
    DOCUMENT_PATH.open("r"),
    yaml.Loader,
)
MODEL_NAME = "llama3.1:8b-instruct-q5_K_M"
SCENARIO_NAME = "scenario_1"

initial_messages = [
    SystemMessage(
        "You are a helpful assistant for Information Retrieval. Given a document and a query, you need to find the most relevant information in the document.\nDocument:\n"
        + DOCUMENT_YAML["text"]
    )
]


@st.cache_resource
def initialize():
    response = Response.process(
        post(
            "http://gondor.hucompute.org:11434/api/generate",
            json={
                "model": MODEL_NAME,
                "keep_alive": 3600 * 24 * 5,
            },
            timeout=600,
        )
    )
    if not response.ok():
        raise Exception(f"Failed to initialize model for {SCENARIO_NAME}")
    response = st.session_state.client.chat.completions.create(
        model=MODEL_NAME, messages=initial_messages
    )
    return response


print(initialize())

chat_interface(
    SCENARIO_NAME,
    initial_messages=initial_messages,
    model_name=MODEL_NAME,
)
