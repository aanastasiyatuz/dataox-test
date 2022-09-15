import requests
from bs4 import BeautifulSoup as BS

BASE_URL = 'https://www.kijiji.ca'

def get_soup(url):
    res = requests.get(url)
    if res.status_code != 200:
        print(f"Error {res.status_code}")
    else:
        return BS(res.text, 'lxml')

def get_next_page(url):
    soup = get_soup(url)
    return soup.find('a', {'title':'Next'}).get("href")

def get_news_info(soup:BS):
    news_list = soup.find_all('div', {'class':'search-item'})
    data = []
    for news in news_list:
        try:
            image = news.find('picture').find('img').get("data-src")
        except:
            image = ''
        title = news.find('a', {'class':'title'}).text.strip()
        location = news.find('div', {'class':'location'}).find('span').text.strip()
        desc = ' '.join(news.find('div', {'class':'description'}).text.split())
        try:
            beds = int(news.find('span', {'class':'bedrooms'}).text.replace(' + Den', '').split(':')[-1])
        except:
            beds = 1
        try:
            price = float(news.find('div', {'class':'price'}).text.replace('\n', '').strip().replace(',', '').replace('$', ''))
        except:
            price = 0.0
        data.append({'image':image, 'title':title, 'location':location, 'desc':desc, 'beds':beds, 'price':price})
    return data

def main():
    url = BASE_URL + '/b-apartments-condos/city-of-toronto/c37l1700273'
    soup = get_soup(url)
    res = []
    while soup:
        print(url)
        data = get_news_info(soup)
        res += data
        url = BASE_URL + get_next_page(url)
        soup = get_soup(url)

if __name__ == '__main__':
    main()