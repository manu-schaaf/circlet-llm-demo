import streamlit as st

from pages_.scenarios.news import DOCUMENT_YAML

st.title("Information Retrieval")
st.header("Example Document")

st.markdown(
    "Below is the text of a [BBC news article](https://www.bbc.com/news/articles/ce31w8dzepno) from 25. October 2024."
)
with st.container(border=True):
    st.markdown(DOCUMENT_YAML["text"])
