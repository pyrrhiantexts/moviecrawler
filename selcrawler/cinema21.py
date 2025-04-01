from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote import webelement
from selenium.webdriver.chrome.options import Options
import sqlite3
from sys import argv, exit
import re
import time
from datetime import date, datetime

#Opts for headless browser
chrome_options = Options()
chrome_options.add_argument("--headless=new")

MAX_SCREENINGS = 4

pull_c21 = True
pull_hollywood = True

months = {'Jan': 1, 'Feb': 2, 'Mar': 3, 'Apr': 4, 'May': 5, 'June': 6, 'July': 7, 'Aug': 8, 'Sep': 9, 'Oct': 10, 'Nov': 11, 'Dec':12}

#Implement browser option
driver = webdriver.Chrome(options=chrome_options)

def main():

    if len(argv) <= 2:
        try:
            if 'c' not in argv[1]:
                pull_c21 = False
            if 'h' not in argv[1]:
                pull_hollywood = False
        except IndexError:
            pass
        finally:
            tables()
    
    elif len(argv) > 2:
        print('Invalid CLI usage')
        exit



def hollywood():
    driver.get("https://www.hollywoodtheatre.org")

    hwood_movies = driver.find_elements(By.CSS_SELECTOR, ".show-card .show-card__image")
    hwood_titles = []
    dates = []

    #Find titles
    for i in len(hwood_movies):
        hwood_titles[i] = hwood_movies[i].get_dom_attribute("title")
    
    #Find movies on cards
    for title in hwood_titles:
        if title.text:
            titlebug = title.lower().replace(' ','-').replace("'", "").replace('(','')
            #Find show dates
            dateelements = driver.find_elements(By.CSS_SELECTOR, f'.show-card:has(.show-card_header:has(a[href="https://hollywoodtheatre.org/show/{titlebug}/"])) .show-card-events .show-card-events__date')
            #Find show times for today
            for i in len(dateelements):
                dates[i] = dateelements[i].text
                if convert_date(dates[i]) == datetime.today():
                    timelements = driver.find_elements(By.CSS_SELECTOR, f'')
                else:
                    break




    driver.close()




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

                    times = driver.find_elements(By.CSS_SELECTOR, f'.movie-details:has(a[href="/movie/{titlebug}"]) .movie-times .session-row:nth-of-type(1) .time')

                    #The quote mark business is SQL string manipulation
                    datesheet_entry = title.text + '"'

                    for i in range(MAX_SCREENINGS):
                        try:
                            datesheet_entry = datesheet_entry + f', "{times[i].text}"'
                        except IndexError:
                            datesheet_entry = datesheet_entry + ', "None"'

                    datesheet.append(datesheet_entry)
                else:
                    break
    
    driver.close()
    return datesheet


def convert_date(original_date):
    day, month, date = original_date.split(' ')
    month = months[month]
    #Removes comma
    day = day.strip(' ,')
    #Removes textual date suffixes
    date = date[:-2]
    current_year = datetime.now().year
    iso_date =date(current_year, month, date).isoformat()
    return iso_date

def tables():
    conn = sqlite3.connect('Database/Films.db')
    cur = conn.cursor()
    showtimes = cinema21()
    cur.execute("CREATE TABLE IF NOT EXISTS films(title, showtime1, showtime2, showtime3, showtime4);")
    for item in showtimes:
        cur.execute(f'INSERT OR REPLACE INTO films (title, showtime1, showtime2, showtime3, showtime4) VALUES ("{item});')
        conn.commit()

if __name__ == '__main__':
    main()



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