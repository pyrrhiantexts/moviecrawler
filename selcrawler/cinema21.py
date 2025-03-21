from selenium import webdriver
from selenium.webdriver.common.by import By

driver = webdriver.Chrome()
driver.get("https://www.cinema21.com")

movie_titles = driver.find_elements(By.CSS_SELECTOR, ".movie-info h2")
for title in movie_titles:
    print(title.text)