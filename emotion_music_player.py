from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import bs4
import cv2
import urllib.request
import numpy as np   
from keras.preprocessing.image import img_to_array
from keras.models import load_model
from sklearn.cluster import KMeans
import pyperclip
import time

""" 얼굴 표정 추출 """
# Face detection XML load and trained model loading
face_detection = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
emotion_classifier = load_model('emotion_model.hdf5', compile=False)
EMOTIONS = ["Angry" ,"Disgusting","Fearful", "Happy", "Sad", "Surpring", "Neutral"]
preds = None

# Video capture using webcam
camera = cv2.VideoCapture(0)

while True:
    # Capture image from camera
    ret, frame = camera.read()
    
    # Convert color to gray scale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    # Face detection in frame
    faces = face_detection.detectMultiScale(gray,
                                            scaleFactor=1.1,
                                            minNeighbors=5,
                                            minSize=(30,30))
    
    # Create empty image
    canvas = np.zeros((250, 300, 3), dtype="uint8")
    
    # Perform emotion recognition only when face is detected
    if len(faces) > 0:
        # For the largest image
        face = sorted(faces, reverse=True, key=lambda x: (x[2] - x[0]) * (x[3] - x[1]))[0]
        (fX, fY, fW, fH) = face
        # Resize the image to 48x48 for neural network
        roi = gray[fY:fY + fH, fX:fX + fW]
        roi = cv2.resize(roi, (48, 48))
        roi = roi.astype("float") / 255.0
        roi = img_to_array(roi)
        roi = np.expand_dims(roi, axis=0)
        
        # Emotion predict
        preds = emotion_classifier.predict(roi)[0]
        emotion_probability = np.max(preds)
        label = EMOTIONS[preds.argmax()]
        
        # Assign labeling
        cv2.putText(frame, label, (fX, fY - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 0, 255), 2)
        cv2.rectangle(frame, (fX, fY), (fX + fW, fY + fH), (0, 0, 255), 2)
 
        # Label printing
        for (i, (emotion, prob)) in enumerate(zip(EMOTIONS, preds)):    # zip은 두 인자를 튜플쌍의 형태로 반환 (EMOTIONS값 1, preds값 1),(EMOTIONS값 2, preds값 2) 
            text = "{}: {:.2f}%".format(emotion, prob * 100)    # 아마도 비율?
            w = int(prob * 300)
            cv2.rectangle(canvas, (7, (i * 35) + 5), (w, (i * 35) + 35), (0, 0, 255), -1)
            cv2.putText(canvas, text, (10, (i * 35) + 23), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (255, 255, 255), 2)
        
        
    # Open two windows
    ## Display image ("Emotion Recognition")
    ## Display probabilities of emotion
    cv2.imshow('Emotion Recognition', frame)
    cv2.imshow("Probabilities", canvas)

    time.sleep(0.1) # 프레임을 조금 낮춰주기 위함
    
    # q to quit
    k = cv2.waitKey(1) & 0xFF
    if k == ord('q') or k == 27:
        break
    if k == ord('c'):
        percent = max(preds)    # 표정 예측치 중 가장 큰 값
        index = np.where(percent == preds)[0][0]    # 가장 큰 표정 예측치의 index 값 구하기
        print(EMOTIONS[index], percent*100)
        break #c를 누르면 바로 나가짐 

#플레이리스트의 이름과 비교해줄 것임    
maxEmotion = EMOTIONS[index]
print(maxEmotion)

# Clear program and close windows
camera.release()
cv2.destroyAllWindows()

# chromedriver.exe 위치 (chromedriver는 이 py 프로그램과 같은 폴더에 있어야 하고, 절대경로로 지정해야 함)
driver = webdriver.Chrome(r"C:/testp/chromedriver.exe")
driver.get("https://vibe.naver.com/today")


# 광고 모달창 끄기 find_* 이게 그 요소
driver.find_elements_by_xpath('//*[@id="app"]/div[2]/div/div/a[2]')[0].click()

""" 로그인 처리 """
# 로그인박스 클릭하여 로그인 창으로 이동 -> 로그인 창으로 이동을 하고나서 로그인 돼 있는지 확인 
driver.find_elements_by_xpath('//*[@id="header"]/div[1]/div[1]/a')[0].click()

    
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

# 혹시나 로그인 돼 있을 때 
try :
    nick_name = driver.find_element_by_css_selector('#header > div.my_menu > div.profile_area > div > a > div.nickname')
    print(nick_name.text , "님 안녕하세요")
except :
    login()

time.sleep(1)

# 보관함 이동
library_btn = driver.find_element_by_xpath('//*[@id="header"]/div[1]/div[3]/div/div[2]/ul/li[7]/a').click()

#보관함 -> 플레이리스트 이동
playlist_btn = driver.find_element_by_xpath('//*[@id="content"]/div/div[1]/div[1]/ul/li[5]/a').click()

#플레이리스트 이름 갖고오기 
#li:nth-child() -> :nth-child()을 제거 해줘야 자식 요소들을 다 갖고 옴
plist_names = driver.find_elements_by_css_selector('#content > div > div.sub_list.playlists > ul > li > div > div.info > a > span.text')

plist = []
#text형식으로 plist에 플레이리스트 이름을 넣어줌
for plist_name in plist_names:
    plist.append(plist_name.text)

print(plist)
plist.pop(-1) #무조건 마지막 기본 플레이리스트 이름 제거

#추출한 표정이 플레이리스트에 있는지 확인 없으면 "플레이리스트를 추가해주세요"
if maxEmotion in plist:
    print('리스트에 값이 있어요')
    # for문으로 돌리며 플레이 리스트들의 인덱스번호와 값을 enumerate로 가져옴 
    for idx, val in enumerate(plist):
        if val == maxEmotion:
            print("그 표정의 값은 {}이고 이 표정의 인덱스 값은 {}이다".format(val, idx))
            #이 표정의 인덱스에 해당하는 플레이리스트 이름 자동 클릭, 지금 idx가 표정에 따른 플레이리트의 인덱스 번호임
            plist_names[idx].click()
            time.sleep(1)
            #랜덤 버튼 클릭 
            random_play_btn = driver.find_element_by_xpath('//*[@id="content"]/div[1]/div[1]/div[2]/div[2]/div/div[1]/span[2]/a').click()

else:
    print('리스트에 값이 없어요')



