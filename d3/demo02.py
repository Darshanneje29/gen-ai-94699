from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

driver=webdriver.Chrome()
driver.implicitly_wait(5)
driver.get("https://www.youtube.com/")
print("page title:",driver.title)

search_box=driver.find_element(By.NAME, "search_query")
search_box.click()

time.sleep(2)
search_box.send_keys("kk songs")
search_box.send_keys(Keys.ENTER)
driver.find_elements(By.ID, "video-title")[0].click()

time.sleep(8)
driver.quit()