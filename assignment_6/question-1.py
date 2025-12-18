import streamlit as st
import requests
import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

st.set_page_config(page_title="LLM Chat App")
st.title("🤖 Multi-LLM Chat Application")

st.sidebar.header("Model Selection")
model_choice = st.sidebar.radio(
    "Select LLM",
    ["Groq (Cloud)", "LM Studio (Local)"]
)

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

question = st.text_input("Enter your question:")


def groq_response(question):
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "user", "content": question}
        ],
        
    )
    return response.choices[0].message.content

def lmstudio_response(question):
    response = requests.post(
        "http://127.0.0.1:1234/v1/chat/completions",
        headers={"Content-Type": "application/json"},
        json={
            "model": "microsoft/phi-4-mini-reasoning",
            "messages": [{"role": "user", "content": question}],
        },
    )

    data = response.json()

    if "choices" in data:
        choice = data["choices"][0]
        if "message" in choice:
            return choice["message"]["content"]
        elif "text" in choice:
            return choice["text"]

    if "response" in data:
        return data["response"]



if st.button("Ask"):
    if question:
        if model_choice == "Groq (Cloud)":
            answer = groq_response(question)
        else:
            answer = lmstudio_response(question)

        st.session_state.chat_history.append(
            {"question": question, "answer": answer}
        )

st.subheader("💬 Chat History")
for chat in st.session_state.chat_history:
    st.markdown(f"**User:** {chat['question']}")
    st.markdown(f"**Model:** {chat['answer']}")
    st.markdown("---")
