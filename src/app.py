import streamlit as st
from langchain_core.messages import AIMessage, HumanMessage
from langchain_community.document_loaders import WebBaseLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.chains import create_history_aware_retriever, create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain

st.set_page_config(page_title="questionME", page_icon="🤖")

"""
SOME INFO 
most llms cant take huge websites they have context windows that can take limited number of tokens
split the web text into different chunks => pass through embdeddings models => vector storage => semantic search on input to 
find relevent text => return text => send to llm
"""

def getResponse(mess):
    return "NO"

def getVectorStorage(url):
    # get the text in document form
    loader = WebBaseLoader(url)
    documents = loader.load()
    return documents

    # split the document into chunks
    # text_splitter = RecursiveCharacterTextSplitter()
    # document_chunks = text_splitter.split_documents(document)

    # create a vectorstore from the chunks
    # vector_store = Chroma.from_documents(document_chunks, OpenAIEmbeddings())
    #
    # return vector_store


if "history" not in st.session_state:
    st.session_state.history = [
        AIMessage(content="Yo what's good! What do you want to know?")
    ]

st.title("QuestionME about this website")

with st.sidebar:
    st.header("Settings")
    link = st.text_input("Link/URL")

if link is None or link == "":
    st.info("Enter URL please")
else:
    documents = getVectorStorage(link)
    with st.sidebar:
        st.write(documents)
    user_message = st.chat_input("Type your message here...")
    #adding interactivity to user input
    if user_message is not None and user_message != "":
        response = getResponse(user_message)
        st.session_state.history.append(HumanMessage(content=user_message))
        st.session_state.history.append(AIMessage(content=response))

    #conversation
    for message in st.session_state.history:
        if isinstance(message, AIMessage):
            with st.chat_message("AI"):
                st.write(message.content)
        elif isinstance(message, HumanMessage):
            with st.chat_message("Human"):
                st.write(message.content)



