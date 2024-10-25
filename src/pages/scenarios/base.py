import streamlit as st


def chat_interface(
    scenario_name: str,
    model_name: str = "llama3.1:8b-instruct-q5_K_M",
    initial_messages=None,
):
    initial_messages = initial_messages or []
    if "messages" not in st.session_state:
        st.session_state.messages = {}

    def reset_chat():
        st.session_state.messages[scenario_name] = initial_messages.copy()

    if scenario_name not in st.session_state.messages:
        reset_chat()

    st.button("Reset Chat", on_click=reset_chat)

    messages = st.container(border=True)
    for message in st.session_state.messages[scenario_name]:
        with messages.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("Query: Ask a question..."):
        st.session_state.messages[scenario_name].append(
            {"role": "user", "content": prompt}
        )
        with messages:
            with messages.chat_message("user"):
                st.markdown(prompt)

            with messages.chat_message("assistant"):
                stream = st.session_state.client.chat.completions.create(
                    model=model_name,
                    messages=[
                        {"role": m["role"], "content": m["content"]}
                        for m in st.session_state.messages[scenario_name]
                    ],
                    stream=True,
                )
                response = st.write_stream(stream)
        st.session_state.messages[scenario_name].append(
            {"role": "assistant", "content": response}
        )

    st.button("Reset Chat", on_click=reset_chat, key="reset_chat_2")