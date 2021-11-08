from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import bs4
import time

# chromedriver 경로 (절대경로로 지정해야 함)
driver = webdriver.Chrome(r"D:\3학년2학기\무선네트워크\무선네트워크_프로젝트\chromedriver.exe")
driver.get("https://vibe.naver.com/today")

# 광고 모달창 끄기
driver.find_elements_by_xpath('//*[@id="app"]/div[2]/div/div/a[2]')[0].click()

# 검색 아이콘 누르기
driver.find_elements_by_xpath('//*[@id="header"]/a[1]')[0].click()
# 검색 바에 검색어 입력하고 엔터누르는 부분
search_input = driver.find_elements_by_xpath('//*[@id="search_keyword"]')[0]
search_input.send_keys("all i want for christmas is you")
search_input.send_keys(Keys.RETURN) # 엔터

# 동적 정보(javascript로 생성된 정보)를 생성하기를 조금 기다려준다
time.sleep(3)

# '노래' 리스트의 첫번째 곡 클릭 (가장 정확한 검색결과일 확률이 높기 때문)
driver.find_elements_by_xpath('//*[@id="content"]/div[2]/div/div[1]/div[2]/div[1]/span[1]/a')[0].click()

time.sleep(3)

"""타이틀, 가수, 가사, 커버 긁어오는 부분"""
source = driver.page_source
bs = bs4.BeautifulSoup(source, 'lxml')  # lxml로 데이터 파싱 (pip로 설치 필요)

cover_url = bs.select_one('#content > div.summary_section > div.summary_thumb > img')['src']
title = bs.select_one('#content > div.summary_section > div.summary > div.text_area > h2 > span.title').get_text()
lyrics = bs.select_one('#content > div:nth-child(3) > p').get_text()


print(title[2:])    # 앞의 '곡명'이라는 글자 빼고 출력
print(lyrics)
print(cover_url)    # src에서 url을 추출해왔음. 이것을 opencv에서 볼 수 있도록 url을 통해 image를 받아오는 코드 짜야 됨. urllib, numpy 이용할 것.



