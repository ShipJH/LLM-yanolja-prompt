import json
import time
import sys

from bs4 import BeautifulSoup
from selenium import webdriver

URL = 'https://www.yanolja.com/reviews/domestic/10048873?sort=HOST_CHOICE'


def crawl_yanolja_reviews():

    driver = webdriver.Chrome()
    driver.get(URL)

    time.sleep(3)  # 페이지 로드까지 기다려야 해서 3초 대기

    scroll_count = 20  # 스크롤 횟수 (더보기로 리뷰 갯수를 가져오기 때문에 스크롤 필요.)
    for i in range(scroll_count):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)  # 스크롤하면, 디도스 방어때문에 차단당할 수 있으므로 2초 대기

    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')  # 스크롤 파싱

    # 리뷰 텍스트, 별점, 날짜를 가져오자.
    review_containers = soup.select('#__next > section > div > div.css-1js0bc8 > div > div > div')
    review_date = soup.select(
        '#__next > section > div > div.css-1js0bc8 > div > div > div > div > div > div.css-1ivchjf > p')

    review_list = []
    for i in range(len(review_containers)):
        review_text = review_containers[i].find('p', class_='content-text').text
        review_stars = review_containers[i].find_all('path', {'fill': '#FDBD00'})
        star_cnt = len(review_stars)
        date = review_date[i].text

        review_dict = {
            'review': review_text,
            'stars': star_cnt,
            'date': date
        }

        review_list.append(review_dict)  # 리스트에 추가

    with open(f'./res/ninetree_yongsan.json', 'w', encoding='utf-8') as f:
        json.dump(review_list, f, indent=4, ensure_ascii=False)  # json 파일로 저장


if __name__ == '__main__':
    crawl_yanolja_reviews()
