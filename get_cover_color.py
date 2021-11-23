from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import bs4
import time
import urllib.request
import numpy as np
import cv2
from sklearn.cluster import KMeans

def url_to_image(url, readFlag=cv2.IMREAD_COLOR):
    # download the image, convert it to a NumPy array, and then read
    # it into OpenCV format
    resp = urllib.request.urlopen(url)
    image = np.asarray(bytearray(resp.read()), dtype="uint8")
    image = cv2.imdecode(image, cv2.IMREAD_COLOR)

    # return the image
    return image

# 각 컬러의 분율 알아보기
def centroid_histogram(clt):
    # grab the number of different clusters and create a histogram
    # based on the number of pixels assigned to each cluster
    numLabels = np.arange(0, len(np.unique(clt.labels_)) + 1)
    (hist, _) = np.histogram(clt.labels_, bins=numLabels)

    # normalize the histogram, such that it sums to one
    hist = hist.astype("float")
    hist /= hist.sum()

    # return the histogram
    return hist


# chromedriver.exe 위치 (chromedriver는 이 py 프로그램과 같은 폴더에 있어야 하고, 절대경로로 지정해야 함)
driver = webdriver.Chrome(r"D:\3학년2학기\무선네트워크\무선네트워크_프로젝트\chromedriver.exe")
driver.get("https://vibe.naver.com/today")

# 광고 모달창 끄기
driver.find_elements_by_xpath('//*[@id="app"]/div[2]/div/div/a[2]')[0].click()

# 검색어 input박스 찾기
search_input = driver.find_elements_by_xpath('//*[@id="search_keyword"]')[0]

while True:
    music_name = input("검색어 입력(종료: /quit) :")
    if music_name == "/quit" or music_name == "/QUIT":
        break
    # 검색 바에 검색어 전달 및 엔터
    search_input.send_keys(music_name)
    search_input.send_keys(Keys.RETURN) # 엔터

    # 동적 정보(javascript로 생성된 정보)를 조금 기다려준다
    time.sleep(3)

    # '노래' 리스트의 첫번째 곡 클릭 (가장 정확한 검색결과일 확률이 높기 때문)
    driver.find_elements_by_xpath('//*[@id="content"]/div[2]/div/div[1]/div[1]/div[2]/div[1]/span[1]/a')[0].click()
    time.sleep(3)

    """타이틀, 가수, 가사, 커버 긁어오는 부분"""
    source = driver.page_source
    bs = bs4.BeautifulSoup(source, 'lxml')  # lxml로 데이터 파싱 (pip로 설치 필요)

    cover_url = bs.select_one('#content > div.summary_section > div.summary_thumb > img')['src']
    title = bs.select_one('#content > div.summary_section > div.summary > div.text_area > h2 > span.title').get_text()
    lyrics = bs.select_one('#content > div.end_section.section_lyrics > p').get_text()

    # print(title[2:] + '\n')    # 앞의 '곡명'이라는 글자 빼고 출력
    if lyrics != None:
        print(lyrics)


    """-------이미지 처리 및 색과 분율 추출---------"""
    image = url_to_image(cover_url)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)  # RBG 형태를 RGB로 변환
    image = image.reshape((image.shape[0] * image.shape[1], 3)) # width와 height 곱해서 픽셀 수 한 개로 통합 (예) - (230400, 3)

    k = 5
    clt = KMeans(n_clusters = k)
    clt.fit(image)

    # RGB 출력
    for center in clt.cluster_centers_:
        print(center.astype(int))   # 그대로 출력하면 float인데 그렇게까지는 필요없으니 정수로 바꿔준다.


    hist = centroid_histogram(clt)
    print(hist)
