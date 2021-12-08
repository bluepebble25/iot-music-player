# 3학년 2학기 무선네트워크 팀프로젝트

## 개요
- 주제: 표정인식 자동 뮤직 플레이어 & 필립스 휴 연동
- 목표: 딥러닝 모델을 바탕으로 표정을 인식한 후, 감정에 적합한 플레이리스트를 자동재생하고, 앨범 커버의 색상을 추출해 LED 불빛으로 시각화하기

## 필요 부품
- 라즈베리파이, 카메라 센서, 필립스 Hue 전구 및 브릿지, 전구 소켓, 110V -> 220V 전압 변환기, LAN선, 무선공유기<br>

![필요부품](https://user-images.githubusercontent.com/71175587/145203707-7c18a52a-2207-4f37-954f-63603d45deb8.PNG)


## 프로그램 구조도
![구조도](https://user-images.githubusercontent.com/71175587/145203735-c703de05-6495-4e59-a8f2-7bfa165f1bae.PNG)

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

## 프로그램
- [emotion_music_player.py](https://github.com/bluepebble25/iot-music-player/blob/main/emotion_music_player.py)
- [Hue 브릿지의 API에 HTTP Request로 조명 컨트롤 요청하는 함수](https://github.com/bluepebble25/iot-music-player/blob/main/control_hue.py)
- [코드분석](https://github.com/bluepebble25/iot-music-player/blob/main/%ED%94%84%EB%A1%9C%EC%A0%9D%ED%8A%B8_%EA%B2%B0%EA%B3%BC_%EB%B3%B4%EA%B3%A0%EC%84%9C.md)
<br>

## 결과
<img width="435" alt="실행결과1" src="https://user-images.githubusercontent.com/80368992/144711901-6dc7505a-d133-4655-a260-6bd381a0b645.PNG"></br> 

<img width="594" alt="실행결과3" src="https://user-images.githubusercontent.com/80368992/144711905-942cdbd8-3316-4d8f-a1ce-09d465190e47.PNG">
