from email.message import Message
from pathlib import Path
from typing import Final

import streamlit as st
import yaml

from circlet.chat_ui import chat_interface, initialize
from circlet.lib.chat import SystemMessage, UserMessage
from circlet.models import LLAMA_8B

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

INITIAL_MESSAGES: Final[list[Message]] = [
    SystemMessage(
        "You are a helpful assistant for Information Retrieval. Given a Document and a Query, you need to find the most relevant information in the document. Always answer to the best of your knowledge using the provided document. Do not deflect or refuse to answer questions, unless the information is not provided in the given document."
    ),
    UserMessage("Document:\n" + DOCUMENT_YAML["text"]),
]

MODEL_NAME: Final[str] = LLAMA_8B.tag
SCENARIO_NAME: Final[str] = "scenario_zero_shot"

print(initialize(MODEL_NAME, SCENARIO_NAME, INITIAL_MESSAGES))

chat_interface(
    SCENARIO_NAME,
    initial_messages=INITIAL_MESSAGES,
    model_name=MODEL_NAME,
)
