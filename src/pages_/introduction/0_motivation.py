import streamlit as st

st.header("Motivation")
st.markdown(
    """
Large Language Models are capable of quickly processing documents and answering relevant questions about their content.
Capabilites like these can be used to build powerful Information Retrieval (**IR**) systems.
However, for almost all intents and purposes, the performance of a LLM is very sensitive to way it is _prompted_.
            
In the following scenarios, you can interact with a LLM using different prompting strategies and see how it affects the model's performance on a simple end-to-end IR task.
The LLM used in this demo is [Llama-3.1](https://arxiv.org/pdf/2407.21783) with 8 billion parameters.

For this demonstration, we have selected a single news article for the model to process, which you can view here:
"""
)
st.page_link("pages_/introduction/1_example_document.py", label="Example Document", icon="📄")
st.markdown(
"""
_Choose a scenario from the sidebar to get started._
"""
)
