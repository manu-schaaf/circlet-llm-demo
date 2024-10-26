from email.message import Message
from typing import Final

import streamlit as st

from circlet.chat_ui import chat_interface
from circlet.lib.chat import InitialUserMessage, SystemMessage
from circlet.models import LLAMA_8B
from pages_.scenarios.news import DOCUMENT_YAML

st.title("Information Retrieval")
st.header("Zero-Shot Prompting")

st.markdown(
    """
In this first scenario, the LLM was only given a basic description of the task in its *System Prompt*, which is treated differently from *User Prompts* or *Assistant Responses*, and no examples (_zero-shot_).

The provided System Prompt tries to give the model a general idea of the task and how it should behave. 
Many current models are trained to avoid controversial topics or refuse to answer questions that are in relation to current events or politics ([Dubey et al., 2024](https://arxiv.org/abs/2407.21783)).
To circumvent this &mdash; as our [example document](/example_document) is about a current political topic &mdash; the System Prompt must expressively allow the model to answer questions about the given document.

- Ask the model some questions about the text to see how well it can retrieve relevant information.
- Try asking "plain" questions or prefixing your questions with `Query: ...`.
- Does the model refuse to answer certain questions?

**Example Questions**
1. What is the given document about?
2. Who has the lead in US presidential election polls?
3. What is the history of the swing states in the US presidential election?
"""
)

INITIAL_MESSAGES: Final[list[Message]] = [
    SystemMessage(
        """
You are a helpful assistant for Information Retrieval.
Given a `Document` and a `Query`, you need to find the most relevant information in the document.
Always answer to the best of your knowledge using the provided document.
Assume that the document is a reliable source of information and up-to-date.
You must not deflect or refuse to answer questions, unless the information is not provided in the given document.
"""
    ),
    InitialUserMessage("Document:\n" + DOCUMENT_YAML["text"]),
]

MODEL_NAME: Final[str] = LLAMA_8B.tag
SCENARIO_NAME: Final[str] = "scenario_zero_shot"

chat_interface(
    SCENARIO_NAME,
    initial_messages=INITIAL_MESSAGES,
    model_name=MODEL_NAME,
)
