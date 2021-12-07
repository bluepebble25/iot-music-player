import requests
import json
from rgbxy import Converter

# RGB to xy converter (by benknight) 다운 주소
# https://github.com/benknight/hue-python-rgb-converter

# 값 예시
# url = "http://[Bridge IP address]/api/[username]/lights/1/state"
# rgbArr = [255, 0, 0]

def hue_color_change(url, RGB):
    R = rgbArr[0]
    G = rgbArr[1]
    B = rgbArr[2]

    converter = Converter()
    xy_array = converter.rgb_to_xy(R,G,B)

    jsonStr = '{"on":True, "sat":254, "bri":254,"xy":' + xy_array + '}'

    data_on = jsonStr.loads()   # 문자열을 Python Dictionary로 변환

    # request의 결과로 response 객체를 반환한다.
    r = requests.put(url, json.dumps(data_on), timeout=5)

def hue_off(url):
    data_off = {"on":False}
    r = requests.put(url, json.dumps(data_on), timeout=5)

"""
Hue 컨트롤 로직

 앨범에서 추출한 색상들을 RGB_list에 담는다.
 
 for 음악의 재생 시간 동안
   for RGB in RGB_list
     hue_color_change(url, RGB)

 음악의 재생이 끝나면 hue_off() 메서드로 조명 끄고 프로그램 종료
"""
