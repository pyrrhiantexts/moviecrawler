from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import sqlite3
from datetime import date

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
    datesheet = []
    for title in c21_titles:
        if title.text:
            titles.append(title.text)
            titlebug = title.text.lower().replace(' ','-')
            #All of these arguments in the selector are necessary because movie-details is the very last class which we can
            #identify the relevant movie title in the element
            dates = driver.find_elements(By.CSS_SELECTOR, f'.movie-details:has(a[href="/movie/{titlebug}"]) .movie-times .session-row .day')
            #I still need to define the actual selector for date -- 
            #this was just a titlebug implementation so far
            for date in dates:
                if date.text == 'Today':
                    times = driver.find_elements(By.CSS_SELECTOR, f'.movie-details:has(a[href="/movie/{titlebug}"]) .movie-times .session-row .time')
                    datesheet.append({'title':{title.text}, 'showtime1':{times[0].text}, 'showtime2':{times[1].text}, 'showtime3':{times[2].text}, 'showtime4':{times[3].text}})
                    #This is the point where I need to start looping for showtimes.
                else:
                    continue
            
    return titles

#Rough early outline for future capability.
#Currently working only on today's showtimes.
#def convert_date(day):
    #if day == 'Today':
        #return date.today()
    #else:
        #weekday, month, dayofmonth = day.split(',')
        #weekday = weekday.strip()




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