import streamlit as st
from openai import OpenAI

from circlet.models import MODELS_BY_TAG

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
        for name in MODELS_BY_TAG
    }


# status = Response.process(
#     get("http://gondor.hucompute.org:11434/v1/models", timeout=10)
# )
# if status.ok() and st.session_state.get("client_gondor") is not None:
#     if "status_ok" not in st.session_state:
#         st.toast("Connection Established!", icon="🎉")
#         st.session_state.status_ok = True
# else:
#     err_msg = (
#         "Could not connect to the LLM server."
#         if status.ok()
#         else "Could not establish a client connection."
#     )
#     st.toast("Error: ", icon="🚨")

page_home = st.Page("pages_/home.py", title="Home")
page_scenario_zero = st.Page(
    "pages_/scenarios/scenario_zero_shot.py",
    title="1. Zero-Shot Prompting",
)
# page_scenario_2 = st.Page(
#     "pages_/scenarios/scenario_few_shot.py",
#     title="2. Few-Shot Prompting",
# )
page_scenario_cot = st.Page(
    "pages_/scenarios/scenario_cot.py",
    title="2. Chain-of-Thought Prompting",
)
page_scenario_ff = st.Page(
    "pages_/scenarios/scenario_free_form.py",
    title="3. Free-Form: Design Your Own Prompt",
)
page_scenario_ff_chat = st.Page(
    "pages_/free_form_chat.py",
    title="4. Free-Form: Chat",
)

pg = st.navigation(
    [
        page_home,
        page_scenario_zero,
        # page_scenario_2,
        page_scenario_cot,
        page_scenario_ff,
        page_scenario_ff_chat,
    ]
)
pg.run()
