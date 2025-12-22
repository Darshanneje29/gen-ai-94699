from langchain_openai import ChatOpenAI
from langchain.agents import create_agent
from langchain.tools import tool
from dotenv import load_dotenv
import os
import json
import requests

load_dotenv()

# ---------------- TOOLS ----------------

@tool(description="Solve arithmetic expressions like 2+3, 5*6, etc.")
def calculator(expression: str) -> str:
    """
    Calculator tool to evaluate arithmetic expressions.
    """
    try:
        return str(eval(expression))
    except:
        return "Error: Cannot solve expression"


@tool(description="Get current weather of a city using OpenWeather API")
def get_weather(city: str) -> str:
    """
    Weather tool to fetch current weather data of a city.
    """
    try:
        api_key = os.getenv("OPENWEATHER_API_KEY")
        url = f"https://api.openweathermap.org/data/2.5/weather?appid={api_key}&units=metric&q={city}"
        response = requests.get(url)
        return json.dumps(response.json())
    except:
        return "Error fetching weather"


@tool(description="Read content of a text file from disk")
def read_file(filepath: str) -> str:
    """
    File reader tool to read a file from given path.
    """
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        return f"File error: {str(e)}"


# ---------------- MODEL (LM STUDIO FIX) ----------------

llm = ChatOpenAI(
    model="qwen/qwen3-4b",
    openai_api_base="http://127.0.0.1:1234/v1",
    openai_api_key="not-needed",
)

# ---------------- AGENT ----------------

agent = create_agent(
    model=llm,
    tools=[calculator, get_weather, read_file],
    system_prompt="You are a helpful assistant. Answer in short."
)

# ---------------- CHAT LOOP ----------------

while True:
    user_input = input("You: ")
    if user_input.lower() == "exit":
        break

    result = agent.invoke({
        "messages": [
            {"role": "user", "content": user_input}
        ]
    })

    print("AI:", result["messages"][-1].content)
