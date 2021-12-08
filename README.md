# iot-music-player

## 개요
- 주제: 표정인식 자동 뮤직 플레이어 & 필립스 휴 연동
- 목표: 딥러닝 모델을 바탕으로 표정을 인식한 후, 감정에 적합한 플레이리스트를 자동재생하고, 앨범 커버의 색상을 추출해 LED 불빛으로 시각화하기

## library
### install
1. 크롬 드라이버 설치 참고자료
- 라즈베리 파이 환경<br>
https://m.blog.naver.com/dsz08082/221877958842 <br>
- 윈도우 환경<br>
https://book.coalastudy.com/data_crawling/week6/stage2 <br>

2. pip 으로 라이브러리 설치<br>

> pip install beautifulsoup4

> pip install selenium

> pip install lxml

> pip install pyperclip

> pip install numpy

> pip install opencv-python

> pip install tensorflow

> pip install keras

> pip install scikit-learn
<br>

### 설명
* 자동화 및 크롤링 관련 (로그인 및 노래 재생, 이미지 가져오기)
1. beautifulsoup4 : 크롤링(동적정보 가능)
2. selenium : 크롤링(동적정보 불가) & 마우스,키보드 입력 자동화
3. lxml : beautifulsoup에서 필요한 parser
4. pyperclip : 셀리니움으로 네이버와 크롬에서 로그인을 시도할시 로봇임을 탐지하는 캡차(captcha)가 뜨는 것 방지

* 표정인식 및 색상 추출 관련
1. numpy : 벡터 및 행렬연산
2. opencv-python : 이미지 처리
3. tensorflow, keras : 딥러닝 라이브러리. 표정인식에 필요
4. sklearn : k-means로 색상추출할 때 필요
<br>

## 얼굴 표정 인식
아래 블로그 참고
https://m.blog.naver.com/roboholic84/221633210887

1) 인터넷 창에 링크 붙여넣기 하고 화면에 대고 오른쪽 버튼 눌러 다른이름으로 저장해서 다운.
- 얼굴인식 학습결과 파일
https://raw.githubusercontent.com/opencv/opencv/master/data/haarcascades/haarcascade_frontalface_default.xml
- 표정인식 학습결과 파일
https://mechasolution.vn/source/blog/AI-tutorial/Emotion_Recognition/emotion_model.hdf5

2) 파이썬 파일에 블로그에 있는 코드 붙여넣고 실행 (웹캠이 연결된 상태여야함)
- 표정인식 py 파일에서 머신러닝 결과 파일의 경로를 설정해줘야 한다.
- 인식이 잘 안된다면 안경을 벗거나 눈썹이 잘 보이도록 할 것.
