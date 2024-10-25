from email.message import Message
from pathlib import Path
from typing import Final

import streamlit as st
import yaml

from circlet.chat_ui import chat_interface, initialize
from circlet.lib.chat import SystemMessage, UserMessage
from circlet.models import LLAMA_8B

st.title("Information Retrieval")
st.header("Chain-of-Thought Prompting")

st.markdown(
    """
In this second scenario, the LLM is also instructed to carefully explain its reasoning by going step-by-step (_chain-of-thoughts_).
This entails giving the model a short document followed by a few examples of questions and their corresponding answers.
Here, 
"""
)

DOCUMENT_PATH = Path(__file__).parent / "news/bbc-ce31w8dzepno.yaml"
DOCUMENT_YAML: dict = yaml.load(
    DOCUMENT_PATH.open("r"),
    yaml.Loader,
)

INITIAL_MESSAGES: Final[list[Message]] = [
    SystemMessage(
        """
You are a helpful assistant for Information Retrieval. Given a Document and a Query, you need to find the most relevant information in the document. Always answer to the best of your knowledge using the provided document. Do not deflect or refuse to answer questions, unless the information is not provided in the given document.

Analyze the given document carefully and give the rationale before answering.
Go step by step and refer to the given document for each question.

Always start your answer with `Reasoning:` followed by your rationale in an itemized list.
Then, provide the answer to the question starting with `Response:`.
"""
    ),
    UserMessage("Document:\n" + DOCUMENT_YAML["text"]),
]

MODEL_NAME: Final[str] = LLAMA_8B.tag
SCENARIO_NAME: Final[str] = "scenario_cot"


print(initialize(MODEL_NAME, SCENARIO_NAME, INITIAL_MESSAGES))

chat_interface(
    SCENARIO_NAME,
    initial_messages=INITIAL_MESSAGES,
    model_name=MODEL_NAME,
)
