# iot-music-player

## 개요
- 음악의 커버 사진을 LED 불빛으로 시각화해서 보여주는 프로젝트
- 곡명과 가수 등을 입력하면 음악 사이트에서 커버 사진을 크롤링해와 5가지 색상을 추출한 다음, 아두이노의 삼색 LED와 연동해 색을 부드럽게 전환시키며 보여준다.

## library
### install
1. 크롬 드라이버 설치 참고자료
- 라즈베리 파이 환경<br>
https://m.blog.naver.com/dsz08082/221877958842 <br>
- 윈도우 환경<br>
https://book.coalastudy.com/data_crawling/week6/stage2 <br>

2. pip 으로 라이브러리 설치<br>
- windows 환경에서는 cmd로 python이 설치된 디렉토리 밑의 Scripts 폴더로 이동해 설치할 것 (C:\Users\com\AppData\Local\Programs\Python\Python38\Scripts)

> pip install beautifulsoup4

> pip install selenium

> pip install lxml

> pip install numpy

> pip install opencv-python

> pip install scikit-learn

> pip install pyperclip
<br>

### 설명
1. beautifulsoup4 - 크롤링(동적정보도 가능)
2. selenium - 크롤링(동적정보 불가) & 마우스,키보드 입력 자동화
3. lxml - beautifulsoup에서 필요한 parser
4. numpy - 벡터 및 행렬연산
6. opencv-python - 이미지 처리
7. sklearn - k-means 통해 색상추출할 때 필요
8. 소스 코드의 import urllib.request 는 파이썬 내장 라이브러리이므로 다운받을 필요 X
9. 셀리니움으로 네이버와 크롬에서 로그인을 시조할시 로봇임을 탐지하는 캠처가 뜨지 않고 온전히 로그인 하기 위한것
<br>

## 얼굴 표정 인식
아래 블로그 참고
https://m.blog.naver.com/roboholic84/221633210887

이 글에서는 아나콘다를 설치해 주피터 노트북 환경에서 실습하고 있는데, 그럴 필요 없음.
다음과 같이 하면 아나콘다, 주피터노트북 필요 X

1) 필요 모듈 pip으로 설치
tensorflow / keras / opencv-python / numpy

2) 인터넷 창에 링크 붙여넣기 하고 화면에 대고 오른쪽 버튼 눌러 다른이름으로 저장해서 다운.
다음 파일들을 표정인식 py 프로그램과 같은 디렉토리에 넣어놓기.
- 얼굴인식 학습결과 파일
https://raw.githubusercontent.com/opencv/opencv/master/data/haarcascades/haarcascade_frontalface_default.xml
- 표정인식 학습결과 파일
https://mechasolution.vn/source/blog/AI-tutorial/Emotion_Recognition/emotion_model.hdf5

3) 파이썬 파일에 블로그에 있는 코드 붙여넣고 실행 (웹캠이 연결된 상태여야함)
난 안경을 쓰고 앞머리가 있어서 그런지 인식이 잘 안됐음.
인식이 잘 안된다면 안경을 벗거나 눈썹이 잘 보이도록 할 것.
