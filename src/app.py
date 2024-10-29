import os
from typing import Final

import streamlit as st
from openai import OpenAI

OPENAI_BASE_URL: Final[str] = os.environ.get(
    "OPENAI_BASE_URL", "http://localhost:11434/v1/"
)
OPENAI_API_KEY: Final[str] = os.environ.get("OPENAI_API_KEY", "sk-1234567890")

if "openai_client" not in st.session_state:
    st.session_state.openai_client = OpenAI(
        base_url=OPENAI_BASE_URL,
        api_key=OPENAI_API_KEY,
    )


st.title("Information Retrieval")

page_home = st.Page(
    "pages_/introduction/0_motivation.py",
    icon="🏠",
    title="Motivation",
    default=True,
)
page_article = st.Page(
    "pages_/introduction/1_example_document.py",
    icon="📰",
    title="Example Document",
)
page_scenario_zero = st.Page(
    "pages_/scenarios/1_zero_shot.py",
    icon="🎯",
    title="Zero-Shot Prompting",
)
# page_scenario_2 = st.Page(
#     "pages_/scenarios/scenario_few_shot.py",
#     title="2. Few-Shot Prompting",
# )
page_scenario_cot = st.Page(
    "pages_/scenarios/2_chain_of_thoughts.py",
    icon="🔗",
    title="Chain-of-Thoughts Prompting",
)
page_scenario_dyop = st.Page(
    "pages_/scenarios/3_dyop.py",
    icon="🎨",
    title="Design Your Own Prompt",
)

pg = st.navigation(
    {
        "Introduction": [
            page_home,
            page_article,
        ],
        "Scenarios": [
            page_scenario_zero,
            # page_scenario_2,
            page_scenario_cot,
            page_scenario_dyop,
        ],
    }
)
pg.run()
