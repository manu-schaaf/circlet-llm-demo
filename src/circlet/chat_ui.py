import streamlit as st
from requests import post

from circlet.lib.response import Response
from circlet.models import LLAMA_70B


def chat_interface(
    scenario_name: str,
    model_name: str = LLAMA_70B.name,
    initial_messages=None,
):
    client = st.session_state.openai_client
    initial_messages = initial_messages or []
    if "messages" not in st.session_state:
        st.session_state.messages = {}

    def reset_chat():
        st.session_state.messages[scenario_name] = initial_messages.copy()

    if scenario_name not in st.session_state.messages:
        reset_chat()

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

    col_chat_input, col_chat_reset = st.columns([0.8, 0.2])
    col_chat_reset.button(
        "Reset Chat",
        type="primary",
        on_click=reset_chat,
        use_container_width=True,
    )

    if prompt := col_chat_input.chat_input("Query: Ask a question..."):
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

    initialize_scenario(model_name, scenario_name, initial_messages)


@st.cache_resource
def initialize_scenario(model_name, scenario_name, initial_messages=None):
    client = st.session_state.openai_client
    base_url = str(client.base_url).split("/v1")[0]

    response = Response.process(
        post(
            f"{base_url}/api/generate",
            json={
                "model": model_name,
                "keep_alive": 300,
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
