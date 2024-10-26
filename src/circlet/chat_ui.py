import streamlit as st
from requests import post

from circlet.lib.response import Response
from circlet.models import LLAMA_70B


def chat_interface(
    scenario_name: str,
    model_name: str = LLAMA_70B.tag,
    initial_messages=None,
    no_reset=False,
):
    print(initialize_scenario(model_name, scenario_name, initial_messages))

    client = st.session_state.client_lookup[model_name]
    initial_messages = initial_messages or []
    if "messages" not in st.session_state:
        st.session_state.messages = {}

    def reset_chat():
        st.session_state.messages[scenario_name] = initial_messages.copy()

    if scenario_name not in st.session_state.messages:
        reset_chat()

    if not no_reset:
        st.button("Reset Chat", on_click=reset_chat, key="reset_chat_top")

    message_container = st.container(border=True)
    for message in st.session_state.messages[scenario_name]:
        with message_container.chat_message(
            message["role"],
            avatar=":material/settings:" if message["role"] == "system" else None,
        ):
            if message["role"] == "system":
                st.code(message["content"], wrap_lines=True, language="markdown")
            else:
                container = st
                if message.get("initial", False):
                    container = st.expander(
                        "_Initial Message (click to expand)_", expanded=False
                    )
                container.markdown(message["content"])

    if prompt := st.chat_input("Query: Ask a question..."):
        st.session_state.messages[scenario_name].append(
            {"role": "user", "content": prompt}
        )
        with message_container:
            with message_container.chat_message("user"):
                st.markdown(prompt)

            with message_container.chat_message("assistant"):
                stream = client.chat.completions.create(
                    model=model_name,
                    messages=st.session_state.messages[scenario_name],
                    stream=True,
                )
                response = st.write_stream(stream)
        st.session_state.messages[scenario_name].append(
            {"role": "assistant", "content": response}
        )

    if not no_reset:
        st.button("Reset Chat", on_click=reset_chat, key="reset_chat_bottom")


@st.cache_resource
def initialize_scenario(model_name, scenario_name, initial_messages=None):
    client = st.session_state.client_lookup[model_name]
    base_url = str(client.base_url).split("/v1")[0]

    response = Response.process(
        post(
            f"{base_url}/api/generate",
            json={
                "model": model_name,
                "keep_alive": 3600 * 24 * 5,
            },
            timeout=600,
        )
    )
    if not response.ok():
        raise Exception(f"Failed to initialize model for {scenario_name}")

    if initial_messages:
        response = client.chat.completions.create(
            model=model_name,
            messages=initial_messages,
            max_tokens=1,
        )
    return response
