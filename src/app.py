import streamlit as st
from langchain_core.messages import AIMessage, HumanMessage


def getResponse(mess):
    return "NO"

st.set_page_config(page_title="questionME", page_icon="🤖")

history = [
    AIMessage(content="Yo what's good! What do you want to know?")
]

st.title("QuestionME about this website")

with st.sidebar:
    st.header("Settings")
    link = st.text_input("Link/URL")

user_message = st.chat_input("Type your message here...")
#adding interactivity to user input
if user_message and user_message != "":
    response = getResponse(user_message)
    history.append(HumanMessage(content=user_message))
    history.append(AIMessage(content=response))
    # with st.chat_message("Human"):
    #     st.write(user_message)
    # with st.chat_message("AI"):
    #     st.write(response)


