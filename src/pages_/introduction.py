import streamlit as st

st.title("CIRCLET - LLM Demo")
st.markdown(
    """
Large Language Models are capable of quickly processing documents and answering relevant questions about their content.
Capabilites like these can be used to build powerful Information Retrieval systems.
However, for almost all intents and purposes, the performance of a LLM is very sensitive to way it is _prompted_.
            
In the following scenarios, you can interact with a LLM using different prompting strategies and see how it affects the model's performance on a simple end-to-end IR task.
The LLM used in this demo is [Llama-3.1](https://arxiv.org/pdf/2407.21783) with 8 billion parameters.

For this demonstration, we have selected a single news article for the model to process, which you can view [here](/example_document).
            
_Choose a scenario from the sidebar to get started._
"""
)
