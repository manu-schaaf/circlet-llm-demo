from email.message import Message
from pathlib import Path
from typing import Final

import streamlit as st
import yaml

from circlet.chat_ui import chat_interface, initialize
from circlet.lib.chat import SystemMessage, UserMessage
from circlet.models import LLAMA_8B

st.title("Information Retrieval")
st.header("Few-Shot Prompting")

st.markdown(
    """
In this second scenario, the LLM is also given a few query-response examples (_few-shot_).
This entails giving the model a short document followed by a few examples of questions and their corresponding answers.
Here, we only give one example.
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

## First Example

Document:
Umbriel (/ˈʌmbriəl/) is the third-largest moon of Uranus. It was discovered on October 24, 1851, by William Lassell at the same time as neighboring moon Ariel. It was named after a character in Alexander Pope's 1712 poem The Rape of the Lock. Umbriel consists mainly of ice with a substantial fraction of rock, and may be differentiated into a rocky core and an icy mantle. The surface is the darkest among Uranian moons, and appears to have been shaped primarily by impacts, but the presence of canyons suggests early internal processes, and the moon may have undergone an early endogenically driven resurfacing event that obliterated its older surface.

Covered by numerous impact craters reaching 210 km (130 mi) in diameter, Umbriel is the second-most heavily cratered satellite of Uranus after Oberon. The most prominent surface feature is a ring of bright material on the floor of Wunda crater. This moon, like all regular moons of Uranus, probably formed from an accretion disk that surrounded the planet just after its formation. Umbriel has been studied up close only once, by the spacecraft Voyager 2 in January 1986. It took several images of Umbriel, which allowed mapping of about 40 percent of the moon's surface.

### First Example - Query 1

Query: When was Umbriel discovered?
Response: Umbriel was discovered on October 24, 1851.

## End of Examples

Apply the same principle to the given document and answer the questions accordingly.
"""
    ),
    UserMessage("Document:\n" + DOCUMENT_YAML["text"]),
]

MODEL_NAME: Final[str] = LLAMA_8B.tag
SCENARIO_NAME: Final[str] = "scenario_few_shot"


print(initialize(MODEL_NAME, SCENARIO_NAME, INITIAL_MESSAGES))

chat_interface(
    SCENARIO_NAME,
    initial_messages=INITIAL_MESSAGES,
    model_name=MODEL_NAME,
)
