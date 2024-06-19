import streamlit as st
from langchain_core.messages import AIMessage, HumanMessage
from langchain_community.document_loaders import WebBaseLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.chains import create_history_aware_retriever, create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain

load_dotenv()

st.set_page_config(page_title="QuestionME", page_icon="🤖")


# SOME INFO
# most llms cant take huge websites they have context windows that can take limited number of tokens
# split the web text into different chunks => pass through embdeddings models => vector storage => semantic search on input to
# find relevent text => return text => send to llm


def getVectorStorage(url):
    # get the text in document form
    loader = WebBaseLoader(url)
    documents = loader.load()

    # split the document into chunks
    text_splitter = RecursiveCharacterTextSplitter()
    document_chunks = text_splitter.split_documents(documents)

    # create a vectorstore from the chunks
    vecStorage = Chroma.from_documents(document_chunks, OpenAIEmbeddings())
    #
    return vecStorage

def getContextWindowFromLLM(vector_store):
    llm = ChatOpenAI()

    retriever = vector_store.as_retriever()

    prompt = ChatPromptTemplate.from_messages([
        MessagesPlaceholder(variable_name="history"),
        ("user", "{input}"),
        ("user",
         "Given the above conversation, generate a search query to look up in order to get information relevant to the conversation")
    ])

    chain = create_history_aware_retriever(llm, retriever, prompt)

    return chain

def getFinalAnswer(chain):
    llm = ChatOpenAI()

    prompt = ChatPromptTemplate.from_messages([
        ("system", "Answer the user's questions based on the below context:\n\n{context}"),
        MessagesPlaceholder(variable_name="history"),
        ("user", "{input}"),
    ])

    stuff_docs = create_stuff_documents_chain(llm, prompt)

    return create_retrieval_chain(chain, stuff_docs)

def getResponse(mess):
    chain = getContextWindowFromLLM(st.session_state.documents)
    convoChain = getFinalAnswer(chain)

    response = convoChain.invoke({
        "history": st.session_state.history,
        "input": user_message
    })

    return response['answer']


st.title("Ask me anything about the inputted website")

with st.sidebar:
    st.header("Settings")
    link = st.text_input("Link/URL")

if link is None or link == "":
    st.info("Enter URL please")
else:

    if "history" not in st.session_state:
        st.session_state.history = [
            AIMessage(content="Hi! What do you want to know?")
        ]

    if "vector_store" not in st.session_state:
        st.session_state.documents = getVectorStorage(link)

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



