import streamlit as st
import requests
from dotenv import load_dotenv
import os
from groq import Groq 

load_dotenv()
client=Groq(api_key=os.getenv("groq_api_key"))
st.header(" 🤖 my_chatbot")
st.markdown(
    """
    <div style="background-color:#E6E6FA;padding:10px;border-radius:10px">
    <h4 style="color:#4B0082;">Welcome to My Chatbot!</h4>
    """,
    unsafe_allow_html=True
)
if"page"not in st.session_state:
    st.session_state.page="chat"
if "messages" not in st.session_state:
    st.session_state.messages = []

with st.sidebar :
    st.write("🤖 My Chatbot")
    if st.button(" 💬 New Chat"):
        st.session_state.page="chat"
    if st.button(" 📚 library "):
        st.session_state.page="library"
    if st.button(" 📁 projects"):
        st.session_state.page="projects"
    if st.button(" 🔍 search chat"):
        st.session_state.page="search"

st.sidebar.text("chat history")

st.scrollable_container = st.sidebar.container()
    
for i in range(1,6):
    st.scrollable_container.button(f"chat {i}")


if st.session_state.page == "chat":
    st.subheader("💬 Chat Page")
    user_input = st.chat_input("Type your message...")
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])
    if not st.session_state.messages: 
        st.info("Welcome! Start typing a message to chat with the assistant.")

elif st.session_state.page == "library":
    st.subheader("📚 Library Page")
    st.info("Here you can access all your saved chats and resources.")

elif st.session_state.page == "projects":
    st.subheader("📁 Projects Page")
    st.info("Manage and explore your projects here.")

elif st.session_state.page == "search":
    st.subheader("🔍 Search Page")
    st.info("Search through your chat history or library here.")

if user_input:
    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })

    response=client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=st.session_state.messages
    )

    bot_reply = response.choices[0].message.content

    st.session_state.messages.append({
        "role": "assistant",
        "content": bot_reply
    })

    st.rerun()

