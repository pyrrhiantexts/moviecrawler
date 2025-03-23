from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import sqlite3

#this option makes the browser 'headless' which means Chrome doesn't
#briefly open to pull the HTML
chrome_options = Options()
chrome_options.add_argument("--headless=new")

#this defines which browser to use and runs the request to pull
driver = webdriver.Chrome(options=chrome_options)
c21_titles = []

def cinema21():
    driver.get("https://www.cinema21.com")
    c21_titles = driver.find_elements(By.CSS_SELECTOR, ".movie-info h2")
    print(c21_titles)


#def hollywood():
    #driver.get("https://www.hollywoodtheatre.org")
    #hollywood_titles = driver.find_elements(By.CSS_SELECTOR, "#TODO")

def tables():
    conn = sqlite3.connect('Database/Films.db')
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS films(title)")
    for item in c21_titles:
        command = ("INSERT INTO films VALUES(" + item.text + ")")
        cur.execute(command)

if __name__ == '__main__':
    cinema21()
    tables()