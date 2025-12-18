import requests
from dotenv import load_dotenv
import os
def chat_bot(prompt):
    load_dotenv()
    api = os.getenv("groq_api")

    if not api:
        return "GROQ_API_KEY not found in .env"

    url = "https://api.groq.com/openai/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {api}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "llama-3.1-8b-instant",
        "messages": [
            {"role": "user", "content": prompt}
        ]
    }

    response = requests.post(url, json=data, headers=headers)

    try:
        res = response.json()
    except Exception:
        return " Could not parse API response"

    if "choices" not in res:
        return f" API Error:\n{res}"

    return res["choices"][0]["message"]["content"]

if __name__ == "__main__":
    print(chat_bot("write a python code of hallo world"))