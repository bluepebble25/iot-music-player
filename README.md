# iot-music-player

## 개요
- 음악의 커버 사진을 LED 불빛으로 시각화해서 보여주는 프로젝트
- 곡명과 가수 등을 입력하면 음악 사이트에서 커버 사진을 크롤링해와 5가지 색상을 추출한 다음, 아두이노의 삼색 LED와 연동해 색을 부드럽게 전환시키며 보여준다.

## library
### install
windows 환경에서는 cmd로 python이 설치된 디렉토리 밑의 Scripts 폴더로 이동해 설치할 것 (C:\Users\com\AppData\Local\Programs\Python\Python38\Scripts)


> pip install beautifulsoup4

> pip install selenium

> pip install lxml

> pip install numpy

> pip install urllib

> pip install opencv-python

> pip install sklearn
<br>

### 설명
1. beautifulsoup4 - 크롤링(동적정보도 가능)
2. selenium - 크롤링(동적정보 불가) & 마우스,키보드 입력 자동화
3. lxml - beautifulsoup에서 필요한 parser
4. numpy - 벡터 및 행렬연산
5. urllib - url로 이미지 받을 수 있게 함
6. opencv-python - 이미지 처리
7. sklearn - k-means 통해 색상추출할 때 필요
