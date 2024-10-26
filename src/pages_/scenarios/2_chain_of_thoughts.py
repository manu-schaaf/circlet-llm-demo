from email.message import Message
from typing import Final

import streamlit as st

from circlet.chat_ui import chat_interface
from circlet.lib.chat import InitialUserMessage, SystemMessage
from circlet.models import LLAMA_8B
from pages_.scenarios.news import DOCUMENT_YAML

st.title("Information Retrieval")
st.header("Chain-of-Thought Prompting")

st.markdown(
    """
In this second scenario, the LLM is also instructed to carefully explain its reasoning by going step-by-step (_Chain-of-Thoughts Prompting_, [Wei et al., 2022](https://proceedings.neurips.cc/paper_files/paper/2022/hash/9d5609613524ecf4f15af0f7b31abca4-Abstract-Conference.html)).
This simple technique has been shown to significantly improve the quality of the model's responses.

In our case, we could expect the model to more closely adhere to the actual content of the provided document and thus provide more accurate answers.

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
You must not deflect or refuse to answer questions, unless the information is not provided in the given document.

Analyze the given document carefully and describe your reasoning before answering.
Go step by step and refer to the given document for each question.

Always start your answer with `Reasoning:`, followed by an outline of your rationale in an itemized list.
Then, provide your answer to the question starting with `Response:`.
"""
    ),
    InitialUserMessage("Document:\n" + DOCUMENT_YAML["text"]),
]

MODEL_NAME: Final[str] = LLAMA_8B.tag
SCENARIO_NAME: Final[str] = "scenario_cot"


chat_interface(
    SCENARIO_NAME,
    initial_messages=INITIAL_MESSAGES,
    model_name=MODEL_NAME,
)
