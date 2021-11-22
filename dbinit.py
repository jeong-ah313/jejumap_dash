import pymongo
from pymongo import MongoClient
import requests
from bs4 import BeautifulSoup
import time
from selenium import webdriver

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
#
chrome_driver_dir = './chromedriver'
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('headless')
driver = webdriver.Chrome(chrome_driver_dir, chrome_options=chrome_options)

client = MongoClient('mongodb://test:test@54.180.143.57', 27017)
#client = MongoClient('localhost', 27017)
db = client.mapJEJU


def getImg(url):
    print(url)
    driver.get(url)
    time.sleep(1)
    html = driver.page_source

    soup = BeautifulSoup(html, 'html.parser')

    # https://t1.kakaocdn.net/thumb/T800x0.q80/?fname=http%3A%2F%2Ft1.daumcdn.net%2Flocalfiy%2FF5609B05083C45A996FA6DD11C2CE438
    # //t1.kakaocdn.net/thumb/T800x0.q80/?fname=http%3A%2F%2Ft1.daumcdn.net%2Flocalfiy%2FF5609B05083C45A996FA6DD11C2CE438

    if soup.select_one('#mArticle > div.cont_essential > div:nth-child(1) > div.details_present > a > span.bg_present') is None:
        target_url = soup.select_one('meta[property="og:image"]')['content']
        img_url = target_url

    else:
        target_url = soup.select_one(
            '#mArticle > div.cont_essential > div:nth-child(1) > div.details_present > a > span.bg_present')[
            'style'].split('//')[1].split("')")[0]
        base = "https://"

        img_url = base + target_url
        # print(img_url)
    return img_url


def getMapInfo(region, page):
    url = 'https://dapi.kakao.com/v2/local/search/keyword.json'
    params = {'query': region, 'page': page}
    print(str(page) + " 페이지")
    headers = {"Authorization": "KakaoAK f125077f7269da21224fea8b3965ab29"}

    places = requests.get(url, params=params, headers=headers).json()['documents']
    total = requests.get(url, params=params, headers=headers).json()['meta']["total_count"]
    # print(places)
    for place in places:
        baseurl = place["place_url"],

        img_url = getImg(baseurl[0])

        doc = {
            "id": place["id"],
            "name": place["place_name"],
            "category": place["category_group_name"],
            "address": place["road_address_name"],
            "url": place["place_url"],
            "img_url": img_url,
            "phone": place["phone"],
            "x": place["x"],
            "y": place["y"]
        }
        db.TRAVEL.insert_one(doc)
        print(doc)


for i in range(1, 6):
    getMapInfo("제주관광지", i)

driver.quit()
