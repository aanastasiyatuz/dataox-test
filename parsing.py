import requests
from bs4 import BeautifulSoup as BS
from db.models import News
from config import pg_database

BASE_URL = 'https://www.kijiji.ca'

def get_soup(url):
    res = requests.get(url)
    if res.status_code != 200:
        print(f"Error {res.status_code}")
    else:
        return BS(res.text, 'lxml')

def get_next_page(url):
    soup = get_soup(url)
    if soup.find('a', {'title':'Next'}):
        return soup.find('a', {'title':'Next'}).get("href")

def get_news_info(soup:BS):
    from datetime import datetime
    news_list = soup.find_all('div', {'class':'search-item'})
    for news in news_list:
        try:
            image = news.find('picture').find('img').get("data-src")
        except:
            image = ''
        title = news.find('a', {'class':'title'}).text.strip()
        location = news.find('div', {'class':'location'}).find('span').text.strip()
        desc = ' '.join(news.find('div', {'class':'description'}).text.split())
        date = news.find('span', {'class':'date-posted'}).text
        if 'ago' in date:
            date = datetime.now()
        elif 'Yesterday' in date:
            now = datetime.now()
            date = datetime(now.year, now.month, now.day-1)
        else:
            day, month, year = date.split('/')
            date = datetime(int(year), int(month), int(day))
        try:
            beds = int(news.find('span', {'class':'bedrooms'}).text.replace(' + Den', '').split(':')[-1])
        except:
            beds = 1
        try:
            price = float(news.find('div', {'class':'price'}).text.replace('\n', '').strip().replace(',', '').replace('$', ''))
        except:
            price = 0.0
        News.create(image=image, title=title, location=location, desc=desc, beds=beds, price=price, date=date)

def main():
    pg_database.create_tables([News])
    url = BASE_URL + '/b-apartments-condos/city-of-toronto/c37l1700273'
    soup = get_soup(url)
    next_page = get_next_page(url)
    while next_page:
        get_news_info(soup)
        url = BASE_URL + next_page
        next_page = get_next_page(url)
        print(url)
        soup = get_soup(url)
    get_news_info(soup)
    pg_database.close()

if __name__ == '__main__':
    main()