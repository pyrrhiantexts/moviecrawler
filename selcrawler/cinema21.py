from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

#this option makes the browser 'headless' which means Chrome doesn't
#briefly open to pull the HTML
options = Options()
options.add_argument("--headless")

#this defines which browser to use and runs the request to pull
driver = webdriver.Chrome(chrome_options=options)

def cinema21():

    driver.get("https://www.cinema21.com")

    movie_titles = driver.find_elements(By.CSS_SELECTOR, ".movie-info h2")
    for title in movie_titles:
        print(title.text)

def hollywood():
    driver.get("https://www.hollywoodtheatre.com")
    hollywood_titles = driver.find_elements(By.CSS_SELECTOR, #TODO)
                                            
