import streamlit as st
from openai import OpenAI

from circlet.models import MODELS_BY_NAME

if "client_gondor" not in st.session_state:
    st.session_state.client_gondor = OpenAI(
        base_url="http://gondor.hucompute.org:11434/v1/", api_key="sk-1234567890"
    )
# if "client_geltlin" not in st.session_state:
#     st.session_state.client_geltlin = OpenAI(
#         base_url="http://geltlin.hucompute.org:11434/v1/", api_key="sk-1234567890"
#     )

if "client_lookup" not in st.session_state:
    st.session_state.client_lookup = {
        name: (
            st.session_state.client_gondor
            # if not "8b" in name
            # else st.session_state.client_geltlin
        )
        for name in MODELS_BY_NAME
    }

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
