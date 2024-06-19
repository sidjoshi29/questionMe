import streamlit as st

st.set_page_config(page_title="questionME", page_icon="🤖")

st.title("QuestionME about this website")

with st.sidebar:
    st.header("Settings")
    link = st.text_input("Link/URL")

st.chat_input("Type your message here...")

with st.chat_message("Bot"):
    st.write("Hi, whats up!")

with st.chat_message("Human"):
    st.write("yo")