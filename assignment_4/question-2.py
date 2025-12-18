import streamlit as st
import requests
from dotenv import load_dotenv
import os
from groq import Groq
import pandas as pd
from datetime import datetime

load_dotenv()
client = Groq(api_key=os.getenv("groq_api_key"))

if "page" not in st.session_state:
    st.session_state.page = "home"

if "messages" not in st.session_state:
    st.session_state.messages = []

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if "userid" not in st.session_state:
    st.session_state.userid = None

if not os.path.exists("users.csv"):
    pd.DataFrame(columns=["userid", "password"]).to_csv("users.csv", index=False)

if not os.path.exists("userfiles.csv"):
    pd.DataFrame(columns=["userid", "filename", "upload_datetime"]).to_csv("userfiles.csv", index=False)

st.header(" 🤖 my_chatbot")
st.markdown(
    """
    <div style="background-color:#E6E6FA;padding:10px;border-radius:10px">
    <h4 style="color:#4B0082;">Welcome to My Chatbot!</h4>
    </div>
    """,
    unsafe_allow_html=True
)

with st.sidebar:
    st.write("🤖 My Chatbot")

    if not st.session_state.authenticated:
        if st.button("🏠 Home"):
            st.session_state.page = "home"
        if st.button("🔐 Login"):
            st.session_state.page = "login"
        if st.button("📝 Register"):
            st.session_state.page = "register"
    else:
        st.success(f"Logged in as {st.session_state.userid}")
        if st.button("💬 Chat"):
            st.session_state.page = "chat"
        if st.button("📂 Explore CSV"):
            st.session_state.page = "explore_csv"
        if st.button("🕘 See History"):
            st.session_state.page = "history"
        if st.button("🚪 Logout"):
            st.session_state.authenticated = False
            st.session_state.userid = None
            st.session_state.page = "home"
            st.rerun()

            st.session_state.authenticated = False
            st.session_state.userid = None
            st.session_state.page = "home"


if st.session_state.page == "home":
    st.subheader("🏠 Home")
    st.info("Please login or register to use the chatbot.")

elif st.session_state.page == "register":
    st.subheader("📝 Register")

    new_user = st.text_input("User ID")
    new_pass = st.text_input("Password", type="password")

    if st.button("Register"):
        users = pd.read_csv("users.csv")
        if new_user in users["userid"].values:
            st.error("User already exists")
        else:
            users.loc[len(users)] = [new_user, new_pass]
            users.to_csv("users.csv", index=False)
            st.success("Registration successful!")

elif st.session_state.page == "login":
    st.subheader("🔐 Login")

    user = st.text_input("User ID")
    pwd = st.text_input("Password", type="password")

    if st.button("Login"):
        users = pd.read_csv("users.csv")
        match = users[(users.userid == user) & (users.password == pwd)]
        if not match.empty:
            st.session_state.authenticated = True
            st.session_state.userid = user
            st.session_state.page = "chat"
            st.success("Login successful!")
            st.rerun()
        else:
            st.error("Invalid credentials")

elif st.session_state.page == "chat" and st.session_state.authenticated:
    st.subheader("💬 Chat Page")

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    if not st.session_state.messages:
        st.info("Welcome! Start typing a message to chat with the assistant.")

    user_input = st.chat_input("Type your message...")

    if user_input:
        st.session_state.messages.append({
            "role": "user",
            "content": user_input
        })

        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=st.session_state.messages
        )

        bot_reply = response.choices[0].message.content

        st.session_state.messages.append({
            "role": "assistant",
            "content": bot_reply
        })

        st.rerun()


elif st.session_state.page == "explore_csv" and st.session_state.authenticated:
    st.subheader("📂 Upload CSV File")

    file = st.file_uploader("Choose a CSV file", type=["csv"])

    if file:
        df = pd.read_csv(file)
        st.dataframe(df)

        history = pd.read_csv("userfiles.csv")
        history.loc[len(history)] = [
            st.session_state.userid,
            file.name,
            datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ]
        history.to_csv("userfiles.csv", index=False)

        st.success("CSV uploaded & history saved")


elif st.session_state.page == "history" and st.session_state.authenticated:
    st.subheader("🕘 Upload History")

    history = pd.read_csv("userfiles.csv")
    user_history = history[history.userid == st.session_state.userid]

    if user_history.empty:
        st.info("No uploads found")
    else:
        st.dataframe(user_history)
