from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import sqlite3
from datetime import date

#Opts for headless browser
chrome_options = Options()
chrome_options.add_argument("--headless=new")

MAX_SCREENINGS = 4

#Implement browser option
driver = webdriver.Chrome(options=chrome_options)

def cinema21():

    driver.get("https://www.cinema21.com")

    c21_titles = driver.find_elements(By.CSS_SELECTOR, ".movie-info h2")

    titles = []
    datesheet = []

    for title in c21_titles:
        if title.text:
            titles.append(title.text)
            titlebug = title.text.lower().replace(' ','-').replace("'", "").replace('(','')

            #All of these arguments in the selector are necessary because movie-details is the very last class which we can
            #identify the relevant movie title in the element
            dates = driver.find_elements(By.CSS_SELECTOR, f'.movie-details:has(a[href="/movie/{titlebug}"]) .movie-times .session-row .day')

            for date in dates:
                if date.text == 'Today':
                    #NEED TO WRITE :has() SELECTOR BEFORE RUNNING TEST
                    times = driver.find_elements(By.CSS_SELECTOR, f'.movie-details:has(a[href="/movie/{titlebug}"]) .movie-times .session-row:has(...) .time')
                    screenings = len(times)

                    datesheet_entry = title.text

                    for i in range(1, MAX_SCREENINGS):
                        try:
                            datesheet_entry = datesheet_entry + f', {times[i].text}'
                        except IndexError:
                            datesheet_entry = datesheet_entry + ', '

                    datesheet.append(datesheet_entry)
                else:
                    break
            
    return datesheet



def tables():
    conn = sqlite3.connect('Database/Films.db')
    cur = conn.cursor()
    showtimes = cinema21()
    cur.execute("CREATE TABLE IF NOT EXISTS films(title, showtime1, showtime2, showtime3, showtime4);")
    for item in showtimes:
        cur.execute(f'INSERT OR REPLACE INTO films (title, showtime1, showtime2, showtime3, showtime4) VALUES ("{item}");')
        conn.commit()

if __name__ == '__main__':
    tables()



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