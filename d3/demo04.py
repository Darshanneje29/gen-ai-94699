from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

chrome_options=Options()
chrome_options.add_argument("--headless")
driver=webdriver.Chrome(options=chrome_options)

driver.get("https://nilesh-g.github.io/learn-web/HTML/demo14.html")
print("page title1:",driver.title)

driver.implicitly_wait(5)

table_body=driver.find_element(By.TAG_NAME,"tbody")
table_rows=table_body.find_elements(By.TAG_NAME,"tr")

for row in table_rows:
    collumns=row.find_elements(By.TAG_NAME,"td")
    info={
        "sr": collumns[0].text,
        "title": collumns[1].text,
        "author": collumns[2].text,
        "category": collumns[3].text,
        "price": collumns[4].text
    }
print(info)
driver.quit()
