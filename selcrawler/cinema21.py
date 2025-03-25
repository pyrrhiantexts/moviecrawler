from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import sqlite3

#this option makes the browser 'headless' which means Chrome doesn't
#briefly open to pull the HTML
chrome_options = Options()
chrome_options.add_argument("--headless=new")

#Define browser choice and implement options
driver = webdriver.Chrome(options=chrome_options)

def cinema21():
    #Get page
    driver.get("https://www.cinema21.com")
    #Save titles
    c21_titles = driver.find_elements(By.CSS_SELECTOR, ".movie-info h2")
    titles = []
    for title in c21_titles:
        if title.text:
            titles.append(title.text)
    return titles


#def hollywood():
    #driver.get("https://www.hollywoodtheatre.org")
    #hollywood_titles = driver.find_elements(By.CSS_SELECTOR, "#TODO")

def tables():
    conn = sqlite3.connect('Database/Films.db')
    cur = conn.cursor()
    titles = cinema21()
    cur.execute("CREATE TABLE IF NOT EXISTS films(title);")
    for item in titles:
        cur.execute(f'INSERT OR REPLACE INTO films (title) VALUES ("{item}");')
        conn.commit()

if __name__ == '__main__':
    tables()