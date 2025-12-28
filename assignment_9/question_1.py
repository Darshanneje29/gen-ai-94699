from langchain.chat_models import init_chat_model
from langchain.agents import create_agent
from langchain.tools import tool

import pandas as pd
from pandasql import sqldf

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


@tool
def csv_tool(filepath: str, sql_query: str):
    """
    CSV Question Answering Tool
    """
    try:
        df = pd.read_csv(filepath)
        result = sqldf(sql_query, {"data": df})
        return result.to_string(index=False)
    except FileNotFoundError:
        return "CSV file not found."
    except Exception as e:
        return f"Error while processing CSV: {str(e)}"


@tool
def batch_fee_scrape() -> list:
    """
    Scrapes batch schedule and fee details from the Sunbeam internship portal
    and returns structured batch information.
    """
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(options=chrome_options)

    driver.get("https://www.sunbeaminfo.in/internship")
    driver.implicitly_wait(10)

    t_base_class = driver.find_element(By.CLASS_NAME, "table-responsive")
    t_css = t_base_class.find_element(By.CSS_SELECTOR, "table.table-bordered.table-striped")
    t_body = t_css.find_element(By.TAG_NAME, "tbody")
    t_row = t_body.find_elements(By.TAG_NAME, "tr")

    internships = []

    for row in t_row:
        cols = row.find_elements(By.TAG_NAME, "td")
        if len(cols) < 7:
            continue

        internships.append({
            "Sr. No.": cols[0].text.strip(),
            "Batch": cols[1].text.strip(),
            "Batch Duration": cols[2].text.strip(),
            "Start Date": cols[3].text.strip(),
            "End Date": cols[4].text.strip(),
            "Time": cols[5].text.strip(),
            "Fees": cols[6].text.strip(),
        })

    driver.quit()
    return internships


@tool
def web_scrape() -> list:
    """
    web_scrape() tool scrapes the data from the Sunbeam portal.
    """
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(options=chrome_options)

    driver.get("https://www.sunbeaminfo.in/internship")
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    wait = WebDriverWait(driver, 10)
    plus_button = wait.until(
        EC.element_to_be_clickable((By.XPATH, "//a[@href='#collapseSix']"))
    )
    driver.execute_script("arguments[0].scrollIntoView(true);", plus_button)
    plus_button.click()

    t_div = driver.find_element(By.ID, "collapseSix")
    t_class = t_div.find_element(By.TAG_NAME, "table")
    t_body = t_class.find_element(By.TAG_NAME, "tbody")
    t_row = t_body.find_elements(By.TAG_NAME, "tr")

    internships = []

    for row in t_row:
        cols = row.find_elements(By.TAG_NAME, "td")
        if len(cols) < 5:
            continue

        internships.append({
            "Technology": cols[0].text.strip(),
            "Aim": cols[1].text.strip(),
            "Prerequisite": cols[2].text.strip(),
            "Learning": cols[3].text.strip(),
            "Location": cols[4].text.strip()
        })

    driver.quit()
    return internships


llm = init_chat_model(
    model="qwen/qwen3-4b",
    model_provider="openai",
    base_url="http://127.0.0.1:1234/v1",
    api_key="dummy-key"
)


agent = create_agent(
    model=llm,
    tools=[
        csv_tool,
        web_scrape,
        batch_fee_scrape
    ],
    system_prompt=(
        """
        You are an intelligent tool-using assistant.

        Instructions:
        1. Analyze the user question and choose the correct tool automatically.
        2. For CSV-related questions:
            - Convert the question into a valid SQL query using table name `data`
            - Call csv_tool with the CSV file path and SQL query
            - Return only the final answer, not the SQL
        3. For internship-related questions (technology, aim, prerequisites, learning, location):
            - Call web_scrape once and answer strictly from its output
        4. For batch-related questions (schedule, duration, dates, time, fees):
            - Call batch_fee_scrape once and answer strictly from its output
        5. Do not ask the user for URLs or re-scrape data for follow-up questions.
        6. Respond in simple, short, and factual English only.
        """
    )
)

conversation = []

while True:
    user_prompt = input("Ask: ")
    if user_prompt.lower() == "exit":
        break

    result = agent.invoke({
        "messages": [
            {"role": "user", "content": user_prompt}
        ]
    })

    ai_msg = result["messages"][-1].content
    print("AI msg:", ai_msg)

    conversation.append({
        "user": user_prompt,
        "assistant": ai_msg
    })
