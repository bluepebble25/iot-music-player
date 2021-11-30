from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import bs4
import time
import urllib.request
import numpy as np
import cv2
from sklearn.cluster import KMeans
import pyperclip

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

# 로그인 함수
def login() :
    while True :
        id = input("당신의 네이버 아이디를 입력하세요 : ")
        pyperclip.copy(id) #캡차를 피하기위한 작업
        driver.find_element_by_id('id').send_keys(Keys.CONTROL + 'v')
        time.sleep(0.5)

        pw = input("당신의 네이버 패스워드를 입력하세요 : ")
        pyperclip.copy(pw)
        time.sleep(0.5)
        driver.find_element_by_id('pw').send_keys(Keys.CONTROL + 'v')

        driver.find_element_by_id('log.login').click()
        time.sleep(1)

        # 로그인 성공여부에 따른 처리
        try :
            # 로그인 실패시 메세지가 생기기 때문에 그에 관련된 박스를 찾음
            login_error = driver.find_element_by_css_selector('#err_common > div') 
            print("로그인 실패", login_error.text) # 실패시 관련문제 알려주기
            driver.find_element_by_id('id').clear() # 그전에 썻던 아이디 input창에서 지우기
        except :
            print("로그인 성공")
            # 로그인 성공시 알려주고 아이디와 패스워드 등록여부 거절누르기
            driver.find_elements_by_xpath('//*[@id="new.dontsave"]')[0].click()
            time.sleep(2)
            break


# chromedriver.exe 위치 (chromedriver는 이 py 프로그램과 같은 폴더에 있어야 하고, 절대경로로 지정해야 함)
driver = webdriver.Chrome(r"D:\3학년2학기\무선네트워크\무선네트워크_프로젝트\chromedriver.exe")
driver.get("https://vibe.naver.com/today")

# 광고 모달창 끄기
driver.find_elements_by_xpath('//*[@id="app"]/div[2]/div/div/a[2]')[0].click()

# 로그인박스 클릭하여 로그인 창으로 이동
driver.find_elements_by_xpath('//*[@id="header"]/div[1]/div[1]/a')[0].click()

#가장 먼저 로그인 먼저 실행
# 혹시나 로그인 되있을때를 위한 대비
try :
    nick_name = driver.find_element_by_css_selector('#header > div.my_menu > div.profile_area > div > a > div.nickname')
    print(nick_name.text , "님 안녕하세요")
except :
    login()

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
    
    #재생을 눌러야지 총 재생시간을 알수 있음
    driver.find_element_by_xpath('//*[@id="content"]/div[1]/div[2]/div[2]/div/div[1]/a[1]').click()
    time.sleep(5)

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
    
    # 해당 태그 영역에 이 클래스를 가진 정보가져오기
    play_time = bs.find("span",{"class":"remain"})
    #총 플레이 타임 보여주기
    print(play_time.text)
