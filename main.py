from flask import Flask, request, jsonify

import requests
import json
from datetime import datetime
from datetime import timedelta

response = requests.get(
    '[API KEY]')
jsonObj = json.loads(response.text)

# 미래 초미세먼지
tomorrow = datetime.today() - timedelta(days=1)
url_pm25_f = 'http://apis.data.go.kr/B552584/ArpltnInforInqireSvc/getMinuDustWeekFrcstDspth'
params_pm25 = {'serviceKey': '[API KEY]',
               'returnType': 'JSON', 'numOfRows': '100', 'pageNo': '1', 'searchDate': tomorrow.strftime('%Y-%m-%d')}
response_pm25 = requests.get(url_pm25_f, params=params_pm25)
jsonObj_pm25 = json.loads(response_pm25.text)
# 내일,모레 초미세먼지
pm25_f1 = jsonObj_pm25['response']['body']['items'][0]['frcstOneCn'][5:7]
pm25_f2 = jsonObj_pm25['response']['body']['items'][0]['frcstTwoCn'][5:7]
pm25_f3 = jsonObj_pm25['response']['body']['items'][0]['frcstThreeCn'][5:7]

# 미래 미세먼지 // API 호출 날짜 설정 일단 현재 날짜 -1 로 함 바꿔야함.
url_pm10_f = 'http://apis.data.go.kr/B552584/ArpltnInforInqireSvc/getMinuDustFrcstDspth'
params_pm10 = {'serviceKey': '[API KEY]',
               'returnType': 'JSON', 'numOfRows': '100', 'pageNo': '1', 'searchDate': tomorrow.strftime('%Y-%m-%d'),
               'InformCode': 'PM10'}
response_pm10 = requests.get(url_pm10_f, params=params_pm10)
jsonObj_pm10 = json.loads(response_pm10.text)
# 내일,모레 미세먼지
pm10_f1 = jsonObj_pm10['response']['body']['items'][1]['informGrade'][5:7]
pm10_f2 = jsonObj_pm10['response']['body']['items'][2]['informGrade'][5:7]
pm10_f3 = jsonObj_pm10['response']['body']['items'][3]['informGrade'][5:7]

application = Flask(__name__)


def Temp_c(num1, num2, num3):
    response = requests.get(
        '[API KEY]')
    jsonObj = json.loads(response.text)

    if num3 == 0:
        temp_c = jsonObj['current']['temp_c']
    elif num3 == 1:
        temp_c = jsonObj['forecast']['forecastday'][num1]['hour'][num2]['temp_c']

    if temp_c >= 27:
        temp_c_m = "더운 날씨에요. 반팔, 나시티, 반바지, 민소매 추천해요."
    elif temp_c >= 23 and temp_c < 27:
        temp_c_m = "조금 더운 날씨에요. 얇은 셔츠, 얇은 긴팔, 반팔, 니트반팔도 입을만해요."
    elif temp_c >= 20 and temp_c < 23:
        temp_c_m = "시원한 날씨에요. 긴팔, 가디건, 맨투맨, 후드티도 입을만해요."
    elif temp_c >= 17 and temp_c < 20:
        temp_c_m = "선선한 날씨에요. 니트, 가디건, 맨투맨이나 가벼운 자켓을 걸쳐도 좋아요."
    elif temp_c >= 12 and temp_c < 17:
        temp_c_m = "조금 추울 수 있어요. 가디건, 트렌치코트, 두꺼운 니트만 입어도 좋아요. "
    elif temp_c >= 10 and temp_c < 12:
        temp_c_m = "쌀쌀해요. 가벼운 코트, 두꺼운 자켓이나 가벼운 옷 여러겹도 좋아요. "
    elif temp_c >= 6 and temp_c < 10:
        temp_c_m = "추운 날씨에요. 코트나 무스탕을 입는 것을 추천해요."
    elif temp_c < 6:
        temp_c_m = "매운 추워요. 여러옷을 꼭 껴입고, 패딩입는 것도 좋아요. "

    return str(temp_c_m)


def Uv(num1, num2, num3):
    response = requests.get(
        '[API KEY]')
    jsonObj = json.loads(response.text)

    if num3 == 0:
        uv = float(jsonObj['current']['uv'])
    elif num3 == 1:
        uv = float(jsonObj['forecast']['forecastday']
                   [num1]['hour'][num2]['uv'])
    if uv >= 11:
        uv_m = "자외선지수가 위험한 수준으로 높아요. 외출은 삼가해주세요."
    elif uv >= 8 and uv < 11:
        uv_m = "자외선지수가 높아요. 선크림은 필수. 햇빛 노출 1시간미만 권장"
    elif uv >= 6 and uv < 8:
        uv_m = "자외선지수가 높은편이에요. 선크림은 필수. 햇빛 노출 2시간미만 권장"
    elif uv >= 3 and uv < 6:
        uv_m = "자외선지수가 보통이에요. 선크림은 권장. 햇빛 노출 3시간미만 권장"
    elif uv < 3:
        uv_m = "자외선지수가 낮은편이에요. 선크림은 선택. 햇볕 노출에 대한 조치 필요하지 않아요."

    return str(uv_m)


def current_pm10():
    response = requests.get(
        '[API KEY]')
    jsonObj = json.loads(response.text)

    pm10 = jsonObj['current']['air_quality']['pm10']

    if pm10 >= 150:
        pm10_m = "미세먼지가 매우나쁨이에요. 외출시 마스크 착용 필수. 장시간 실외활동 자제."
    elif pm10 >= 80 and pm10 < 150:
        pm10_m = "미세먼지가 나쁨이에요. 외출시 마스크 착용 필수. 장시간 실외활동 자제."
    elif pm10 >= 30 and pm10 < 80:
        pm10_m = "미세먼지가 보통이에요. 외출시 마스크 착용 권장."
    elif pm10 >= 0 and pm10 < 30:
        pm10_m = "미세먼지가 좋음이에요. 마스크 쓸 필요가 없어요."

    return str(pm10_m)


def current_pm2_5():
    response = requests.get(
        '[API KEY]')
    jsonObj = json.loads(response.text)

    pm2_5 = jsonObj['current']['air_quality']['pm2_5']

    if pm2_5 >= 75:
        pm2_5_m = "초미세먼지가 매우나쁨이에요. 외출시 마스크 착용 필수. 장시간 실외활동 자제."
    elif pm2_5 >= 35 and pm2_5 < 75:
        pm2_5_m = "초미세먼지가 나쁨이에요. 외출시 마스크 착용 필수. 장시간 실외활동 자제."
    elif pm2_5 >= 15 and pm2_5 < 35:
        pm2_5_m = "초미세먼지가 보통이에요. 외출시 마스크 착용 권장."
    elif pm2_5 >= 0 and pm2_5 < 15:
        pm2_5_m = "초미세먼지가 좋음이에요. 마스크 쓸 필요가 없어요."

    return str(pm2_5_m)


# 미래 미세먼지
def future_pm10(str):
    pm10 = 0
    if str == "좋음":
        pm10 = 0
    elif str == "보통":
        pm10 = 10
    elif str == "나쁨":
        pm10 = 40
    return pm10


# 미래 초미세먼지
def future_pm2_5(str):
    pm2_5 = 0
    if str == "좋음":
        pm2_5 = 5
    elif str == "나쁨":
        pm2_5 = 40
    return pm2_5


def Wind_mps(num1, num2, num3):
    response = requests.get(
        '[API KEY]')
    jsonObj = json.loads(response.text)

    if num3 == 0:
        # mph을 m/s로 변환
        wind_mps = float((jsonObj['current']['wind_mph']) / 2.237)
    elif num3 == 1:
        wind_mps = float(
            (jsonObj['forecast']['forecastday'][num1]['hour'][num2]['wind_mph']) / 2.237)  # mph을 m/s로 변환

    # 보퍼트 풍력 계급 기준으로 분리
    if wind_mps <= 1.5:
        wind_mps_m = "풍향계가 움직이지 않을 정도에 바람이 약간 불고 수면은 잔잔해요."
    elif wind_mps > 1.5 and wind_mps <= 5.4:
        wind_mps_m = "바람이 얼굴에 느껴지고 나뭇잎이 흔들리며 물결이 작게 생겨요."
    elif wind_mps > 5.4 and wind_mps <= 10.7:
        wind_mps_m = "먼지와 종잇조각이 날리고 작은나무가 흔들리고 파도가 생겨요."
    elif wind_mps > 10.7 and wind_mps <= 13.8:
        wind_mps_m = "큰 나뭇가지가 흔들리고 우산받기가 곤란해요."
    elif wind_mps > 13.8 and wind_mps <= 20.7:
        wind_mps_m = "나무 전체가 흔들리며 바람을 안고 걷기가 어렵거나 불가능해요."
    else:
        wind_mps_m = "가옥에 손해가 있고 위험해 외출을 삼가해주세요."

    return str(wind_mps_m)


# 오늘: 0, 내일:1, 모레:2
def send_weather(num1, num2):
    response = requests.get(
        '[API KEY]')
    jsonObj = json.loads(response.text)

    temp_c_1 = str(jsonObj['forecast']['forecastday'][num1]['hour'][num2]['temp_c'])
    uv_1 = str(jsonObj['forecast']['forecastday'][num1]['hour'][num2]['uv'])
    wind_mps_1 = round((jsonObj['forecast']['forecastday'][num1]['hour'][num2]['wind_mph']) / 2.237, 2)
    wind_mps_1 = str(wind_mps_1)
    num2_s = str(num2)

    if num1 == 0:
        send_future = {"version": "2.0",
                       "template": {
                           "outputs": [{
                               "simpleText": {
                                   "text": "오늘" + num2_s + "시 기온:" + temp_c_1 + "\n" + Temp_c(num1, num2, 1) + "\n" +
                                           "오늘" + num2_s + "시 자외선지수: " + uv_1 + "\n" + Uv(num1, num2, 1) + "\n" +
                                           "오늘" + num2_s + "시 풍속(m/s): " + wind_mps_1 + "\n" + Wind_mps(num1, num2,
                                                                                                        1) + "\n" +
                                           "오늘" + num2_s + "시 미세먼지: " + pm10_f1 + "\n" +
                                           "오늘" + num2_s + "시 초미세먼지: " + pm25_f1}
                           }
                           ]
                       }
                       }

    elif num1 == 1:
        send_future = {"version": "2.0",
                       "template": {
                           "outputs": [{
                               "simpleText": {
                                   "text": "내일" + num2_s + "시 기온: " + temp_c_1 + "\n" + Temp_c(num1, num2, 1) + "\n" +
                                           "내일" + num2_s + "시 자외선지수: " + uv_1 + "\n" + Uv(num1, num2, 1) + "\n" +
                                           "내일" + num2_s + "시 풍속(m/s): " + wind_mps_1 + "\n" + Wind_mps(num1, num2,
                                                                                                        1) + "\n" +
                                           "내일" + num2_s + "시 미세먼지: " + pm10_f2 + "\n" +
                                           "내일" + num2_s + "시 초미세먼지: " + pm25_f2}
                           }
                           ]
                       }
                       }

    elif num1 == 2:
        send_future = {"version": "2.0",
                       "template": {
                           "outputs": [{
                               "simpleText": {
                                   "text": "모레" + num2_s + "시 기온: " + temp_c_1 + "\n" + Temp_c(num1, num2, 1) + "\n" +
                                           "모레" + num2_s + "시 자외선지수: " + uv_1 + "\n" + Uv(num1, num2, 1) + "\n" +
                                           "모레" + num2_s + "시 풍속(m/s): " + wind_mps_1 + "\n" + Wind_mps(num1, num2,
                                                                                                        1) + "\n" +
                                           "모레" + num2_s + "시 미세먼지: " + pm10_f3 + "\n" +
                                           "모레" + num2_s + "시 초미세먼지: " + pm25_f3}
                           }
                           ]
                       }
                       }
    return send_future


# 드라이브지수
def Drive(num1, num2, num3):
    response = requests.get(
        '[API KEY]')
    jsonObj = json.loads(response.text)

    if num3 == 0:
        temp_c = abs(float(jsonObj['current']['temp_c'] - 18) * 0.12)
        wind_mph = float((jsonObj['current']['wind_mph'] - 3.3554) * 0.44704) * 0.12
        pm10 = float(jsonObj['current']['air_quality']['pm10']) * 0.0417
        cloud = float(jsonObj['current']['cloud']) * 0.028
        uv = float(jsonObj['current']['uv'] - 2) * 0.17
        humidity = abs(float((jsonObj['current']['humidity'] - 50) * 0.021))
        precip_mm = float(jsonObj['current']['precip_mm'])
        last_updated = jsonObj['current']['last_updated']

    elif num3 == 1:
        temp_c = abs(float(jsonObj['forecast']['forecastday'][num1]['hour'][num2]['temp_c'] - 18) * 0.12)
        wind_mph = float((jsonObj['forecast']['forecastday'][num1]['hour'][num2]['wind_mph'] - 3.3554) * 0.44704) * 0.12
        cloud = float(jsonObj['forecast']['forecastday'][num1]['hour'][num2]['cloud']) * 0.028
        uv = float(jsonObj['forecast']['forecastday'][num1]['hour'][num2]['uv'] - 2) * 0.17
        humidity = abs(float(jsonObj['forecast']['forecastday'][num1]['hour'][num2]['humidity'] - 50) * 0.021)
        precip_mm = float(jsonObj['forecast']['forecastday'][num1]['hour'][num2]['precip_mm'])
        if num1 == 0:
            pm10 = future_pm10(pm10_f1)
        elif num1 == 1:
            pm10 = future_pm10(pm25_f2)
        elif num1 == 2:
            pm10 = future_pm10(pm25_f3)

    if wind_mph <= 0:
        wind_mph = 0
    if uv <= 0:
        uv = 0
    Drive = (10 - (temp_c + wind_mph + pm10 / 10 + cloud + uv + humidity)) * 10
    int(Drive)
    if Drive < 0:
        Drive = 10
    if precip_mm - 0.5 > 0:
        Drive = 0
    if num3 == 0:
        return round(Drive), last_updated
    elif num3 == 1:
        return round(Drive)


# 한강지수
def hangang(num1, num2, num3):
    response = requests.get(
        '[API KEY]')
    jsonObj = json.loads(response.text)

    if num3 == 0:
        temp_c = abs(jsonObj['current']['temp_c'] - 18)
        humidity = jsonObj['current']['humidity'] - 30
        wind_mph = jsonObj['current']['wind_mph']
        Uv = jsonObj['current']['uv'] - 2
        pm10 = jsonObj['current']['air_quality']['pm10'] - 30
        pm2_5 = jsonObj['current']['air_quality']['pm2_5'] - 15
        last_updated = jsonObj['current']['last_updated']

        if pm10 <= 0:
            pm10 = 0
        elif pm10 > 0 and pm10 <= 50:
            pm10 = pm10 * 0.3
        elif pm10 > 51 and pm10 <= 120:
            pm10 = 15 + pm10 * 0.5
        else:
            pm10 = 100

        if pm2_5 <= 0:
            pm2_5 = 0
        elif pm2_5 > 1 and pm2_5 <= 20:
            pm2_5 = pm2_5 * 0.75
        elif pm2_5 > 21 and pm2_5 <= 60:
            pm2_5 = 15 + pm2_5
        else:
            pm2_5 = 100


    elif num3 == 1:
        temp_c = abs(jsonObj['forecast']['forecastday'][num1]['hour'][num2]['temp_c'] - 18)
        humidity = jsonObj['forecast']['forecastday'][num1]['hour'][num2]['humidity'] - 30
        wind_mph = jsonObj['forecast']['forecastday'][num1]['hour'][num2]['wind_mph']
        Uv = jsonObj['forecast']['forecastday'][num1]['hour'][num2]['uv'] - 2
        pm2_5 = 0
        pm10 = 0
        if num1 == 0:
            pm10 = future_pm10(pm10_f1)
            pm2_5 = future_pm2_5(pm25_f1)
        elif num1 == 1:
            pm10 = future_pm10(pm25_f2)
            pm2_5 = future_pm2_5(pm25_f2)
        elif num1 == 2:
            pm10 = future_pm10(pm10_f3)
            pm2_5 = future_pm2_5(pm25_f3)

    if temp_c > 10:
        temp_c = 10
    else:
        temp_c = temp_c * 5
    if humidity < 0:
        humidity = 0
    elif humidity >= 90:
        humidity = 50
    else:
        humidity = humidity * 0.5
    if Uv <= 0:
        Uv = 0
    elif Uv >= 6:
        Uv = 100
    else:
        Uv = Uv * 10

    hangang = 100 - (temp_c) - humidity - wind_mph - Uv - pm10 - pm2_5
    if hangang < 0:
        hangang = 20

    if num3 == 0:
        return round(hangang), last_updated
    elif num3 == 1:
        return round(hangang)


# 런닝지수, 왜 미세먼지만 들어가있지?
def running(num1, num2, num3):
    response = requests.get(
        '[API KEY]')
    jsonObj = json.loads(response.text)

    if num3 == 0:
        temp_c = abs(float(jsonObj['current']['temp_c'] - 18) * 0.16)
        wind_mph = float((jsonObj['current']['wind_mph'] - 3.3554) * 0.44704) * 0.21
        pm10 = float(jsonObj['current']['air_quality']['pm10'] * 0.044)
        cloud = float(jsonObj['current']['cloud']) * 0.01
        uv = float(jsonObj['current']['uv'] - 2) * 0.23
        humidity = abs(float((jsonObj['current']['humidity'] - 50) * 0.026))
        precip_mm = float(jsonObj['current']['precip_mm'])
        last_updated = jsonObj['current']['last_updated']

    elif num3 == 1:
        temp_c = abs(float(jsonObj['forecast']['forecastday'][num1]['hour'][num2]['temp_c'] - 18) * 0.16)
        wind_mph = float((jsonObj['forecast']['forecastday'][num1]['hour'][num2]['wind_mph'] - 3.3554) * 0.44704) * 0.21
        cloud = float(jsonObj['forecast']['forecastday'][num1]['hour'][num2]['cloud']) * 0.01
        humidity = abs(float(jsonObj['forecast']['forecastday'][num1]['hour'][num2]['humidity'] - 50) * 0.026)
        precip_mm = float(jsonObj['forecast']['forecastday'][num1]['hour'][num2]['precip_mm'])
        uv = (jsonObj['forecast']['forecastday'][num1]['hour'][num2]['uv'] - 2) * 0.23

    if wind_mph <= 0:
        wind_mph = 0
    if uv <= 0:
        uv = 0

    if num3 == 0:
        running = (10 - (temp_c + wind_mph + pm10 +
                         cloud + uv + humidity)) * 10
    elif num3 == 1:
        running = (10 - (temp_c + wind_mph + cloud + uv + humidity)) * 10
    if precip_mm - 0.5 > 0:
        running = 0

    if running < 0:
        running = 0
    if num3 == 0:
        return round(running), last_updated
    elif num3 == 1:
        return round(running)

# 우산지수
def Umbrella(num1, num2, num3):
    response = requests.get(
        '[API KEY]')
    jsonObj = json.loads(response.text)

    if num3 == 0:
        precip_mm = float(jsonObj['current']['precip_mm'])
        humidity = float(jsonObj['current']['humidity']) / 81.5
        cloud = float(jsonObj['current']['cloud']) / 74
        wind_mph = float(jsonObj['current']['wind_mph']) * 0.44704 / 9.7
        last_updated = jsonObj['current']['last_updated']
        if precip_mm > 0 and precip_mm <= 0.5:
            precip_mm = 1
        elif precip_mm > 0.5 and precip_mm <= 1:
            precip_mm = 2
        elif precip_mm > 1 and precip_mm <= 1.5:
            precip_mm = 3
        elif precip_mm > 1.5 and precip_mm <= 2:
            precip_mm = 4
        elif precip_mm > 2 and precip_mm <= 2.5:
            precip_mm = 5
        elif precip_mm > 2.5 and precip_mm <= 3:
            precip_mm = 6
        elif precip_mm > 3 and precip_mm <= 3.6:
            precip_mm = 7
        elif precip_mm > 3.6 and precip_mm <= 4.2:
            precip_mm = 8
        elif precip_mm > 4.2 and precip_mm <= 5:
            precip_mm = 9

        Umbrella = (precip_mm + humidity + cloud + wind_mph) * 10
        if precip_mm > 5:
            Umbrella = 0

    elif num3 == 1:
        chance_of_rain = float(
            jsonObj['forecast']['forecastday'][num1]['hour'][num2]['chance_of_rain']) / 10.8
        Umbrella = chance_of_rain

    if Umbrella >= 65 and Umbrella <= 100:
        com = "우산 꼭 챙겨가시길 바래요"
    elif Umbrella >= 30 and Umbrella < 65:
        com = "우산을 챙겨 가시는 것을 추천해요"
    elif Umbrella >= 0 and Umbrella < 30:
        com = "우산 없이 외출해도 좋아요"

    if num3 == 0:
        return round(Umbrella), com, last_updated
    elif num3 == 1:
        return round(Umbrella), com


# 감기위험지수
def cold(num1, num2, num3):
    response = requests.get(
        '[API KEY]')
    jsonObj = json.loads(response.text)

    if num3 == 0:
        mintemp_c = float(jsonObj['forecast']['forecastday'][0]['day']['mintemp_c'])
        maxtemp_c = float(jsonObj['forecast']['forecastday'][0]['day']['maxtemp_c'])
        dailyrange = maxtemp_c - mintemp_c
        humidity = abs(float(jsonObj['current']['humidity']))
        pressure = float(jsonObj['current']['pressure_mb'])
        last_updated = jsonObj['current']['last_updated']
    elif num3 == 1:
        mintemp_c = float(jsonObj['forecast']['forecastday'][num1]['day']['mintemp_c'])
        maxtemp_c = float(jsonObj['forecast']['forecastday'][num1]['day']['maxtemp_c'])
        dailyrange = maxtemp_c - mintemp_c
        humidity = abs(float(jsonObj['forecast']['forecastday'][num1]['hour'][num2]['humidity']))
        pressure = float(jsonObj['forecast']['forecastday'][num1]['hour'][num2]['pressure_mb'])
    if mintemp_c > 20:
        mintemp_c = 0
    elif mintemp_c > 10 and mintemp_c <= 20:
        mintemp_c = 5
    elif mintemp_c <= 10 and mintemp_c > 0:
        mintemp_c = 15
    elif mintemp_c <= 0 and mintemp_c > -12:
        mintemp_c = 25
    else:
        mintemp_c = 30
    if dailyrange > 20:
        dailyrange = 25
    elif dailyrange <= 20 and dailyrange > 15:
        dailyrange = 20
    elif dailyrange <= 15 and dailyrange > 10:
        dailyrange = 15
    else:
        dailyrange = 10
    if dailyrange >= 74:
        humidity = 5
    elif dailyrange < 74 and dailyrange >= 59.3:
        humidity = 10
    elif dailyrange < 59.3 and dailyrange >= 43.9:
        humidity = 15
    else:
        humidity = 20

    if pressure >= 1019.2:
        pressure = 25
    elif pressure < 1019.2 and pressure >= 1012.9:
        pressure = 15
    elif pressure < 1012.9 and pressure >= 1004.8:
        pressure = 10
    else:
        pressure = 5
    cold = pressure + humidity + dailyrange + mintemp_c

    if cold < 0:
        cold = 0
    if num3 == 0:
        return round(cold), last_updated
    elif num3 == 1:
        return round(cold)


# 세차지수
def Car_Washing(num1, num2, num3):
    response = requests.get(
        '[API KEY]')
    jsonObj = json.loads(response.text)

    if num3 == 0:
        temp_c = abs(float(jsonObj['current']['temp_c'] - 18) * 0.09)
        wind_mph = float((jsonObj['current']['wind_mph'] - 3.3554) * 0.44704) * 0.09
        pm10 = float(jsonObj['current']['air_quality']['pm10']) * 0.0425
        uv = float(jsonObj['current']['uv'] - 2) * 0.26
        humidity = abs(float((jsonObj['current']['humidity'] - 50) * 0.026))
        precip_mm = float(jsonObj['current']['precip_mm'])
        last_updated = jsonObj['current']['last_updated']

    elif num3 == 1:
        temp_c = abs(float(jsonObj['forecast']['forecastday'][num1]['hour'][num2]['temp_c'] - 18) * 0.09)
        wind_mph = float((jsonObj['forecast']['forecastday'][num1]['hour'][num2]['wind_mph'] - 3.3554) * 0.44704) * 0.09
        uv = float(jsonObj['forecast']['forecastday'][num1]['hour'][num2]['uv'] - 2) * 0.26
        humidity = abs(float(jsonObj['forecast']['forecastday'][num1]['hour'][num2]['humidity'] - 50) * 0.026)
        precip_mm = float(jsonObj['forecast']['forecastday'][num1]['hour'][num2]['precip_mm'])

    if wind_mph <= 0:
        wind_mph = 0
    if uv <= 0:
        uv = 0
    Car_Washing = (10 - (temp_c + wind_mph + uv + humidity)) * 10
    if Car_Washing < 0:
        Car_Washing = 10
    elif Car_Washing > 100:
        Car_Washing = 100

    if precip_mm - 0.5 > 0:
        Car_Washing = 0
    if num3 == 0:
        return round(Car_Washing), last_updated
    elif num3 == 1:
        return round(Car_Washing)


# 빨래지수, 초미세먼지 고려 X
def Washing(num1, num2, num3):
    response = requests.get(
        '[API KEY]')
    jsonObj = json.loads(response.text)

    if num3 == 0:
        temp_c = abs(float(jsonObj['current']['temp_c']) * 7.36 / 18)
        wind_mph = float((jsonObj['current']['wind_mph']) * 0.44704) / 4.23
        pm10 = float(jsonObj['current']['air_quality']['pm10']) * 0.0417
        humidity = float(jsonObj['current']['humidity']) / 47
        precip_mm = float(jsonObj['current']['precip_mm'])
        last_updated = jsonObj['current']['last_updated']

    elif num3 == 1:
        temp_c = abs(float(jsonObj['forecast']['forecastday'][num1]['hour'][num2]['temp_c']) * 7.36 / 18)
        wind_mph = float((jsonObj['forecast']['forecastday'][num1]['hour'][num2]['wind_mph']) * 0.44704 / 4.23)
        humidity = float(jsonObj['forecast']['forecastday'][num1]['hour'][num2]['humidity']) / 47
        precip_mm = float(jsonObj['forecast']['forecastday'][num1]['hour'][num2]['precip_mm'])

    Washing = ((temp_c + 1) / humidity + wind_mph) * 10
    if precip_mm - 0.5 > 0:
        Washing = 0
    if Washing < 0:
        Washing = 0
    elif Washing > 100:
        Washing = 100

    if num3 == 0:
        return round(Washing), last_updated
    elif num3 == 1:
        return round(Washing)


# 식중독위험지수
def poison(num1, num2, num3):
    response = requests.get(
        '[API KEY]')
    jsonObj = json.loads(response.text)

    if num3 == 0:
        avgtemp_c = float(jsonObj['forecast']['forecastday'][0]['day']['avgtemp_c'] - 18)
        mintemp_c = float(jsonObj['forecast']['forecastday'][0]['day']['mintemp_c'])
        humidity = float(jsonObj['current']['humidity'])
        pm10 = float(jsonObj['current']['air_quality']['pm10'])
        last_updated = jsonObj['current']['last_updated']
    elif num3 == 1:
        avgtemp_c = float(jsonObj['forecast']['forecastday'][num1]['day']['avgtemp_c'] - 18)
        mintemp_c = float(jsonObj['forecast']['forecastday'][num1]['day']['mintemp_c'])
        humidity = float(jsonObj['forecast']['forecastday'][num1]['hour'][num2]['humidity'])
        pm10 = float(jsonObj['current']['air_quality']['pm10'])
    if avgtemp_c > 2:
        avgtemp_c += 20
    else:
        avgtemp_c = 5
    if mintemp_c > 15:
        mintemp_c += 5
    else:
        mintemp_c = 8
    if humidity > 70:
        humidity = abs((humidity - 100) / 3)
    elif humidity >= 40 and humidity < 70:
        humidity -= 30
    else:
        humidity = abs(humidity - 40)
    if pm10 <= 30:
        pm10 = 20
    elif pm10 > 30 and pm10 <= 80:
        pm10 = 16
    elif pm10 > 80 and pm10 <= 150:
        pm10 = 12
    else:
        pm10 = 8
    poison = int(pm10 + humidity + avgtemp_c + mintemp_c)

    if poison < 0:
        poison = 0
    elif poison > 100:
        poison = 100

    if num3 == 0:
        return round(poison), last_updated
    elif num3 == 1:
        return round(poison)


# 호흡기 위험 지수
def respiratory(num1, num2, num3):
    response = requests.get(
        '[API KEY]')
    jsonObj = json.loads(response.text)

    if num3 == 0:
        maxtemp_c = float(jsonObj['forecast']['forecastday'][0]['day']['maxtemp_c'])
        mintemp_c = float(jsonObj['forecast']['forecastday'][0]['day']['mintemp_c'])
        dailyrange = maxtemp_c - mintemp_c
        humidity = float(jsonObj['current']['humidity'])
        pm10 = float(jsonObj['current']['air_quality']['pm10'])
        pm2_5 = float(jsonObj['current']['air_quality']['pm2_5'])
        pressure = float(jsonObj['current']['pressure_mb'])
        last_updated = jsonObj['current']['last_updated']

        if pm10 <= 30:
            pm10 = 20
        elif pm10 > 30 and pm10 <= 80:
            pm10 = 16
        elif pm10 > 80 and pm10 <= 150:
            pm10 = 12
        else:
            pm10 = 8

        if pm2_5 <= 15:
            pm2_5 = 5
        elif pm2_5 > 15 and pm2_5 <= 50:
            pm2_5 = 8
        elif pm2_5 > 50 and pm2_5 <= 100:
            pm2_5 = 12
        elif pm2_5 > 101:
            pm2_5 = 15

    elif num3 == 1:
        maxtemp_c = float(jsonObj['forecast']['forecastday'][num1]['day']['maxtemp_c'])
        mintemp_c = float(jsonObj['forecast']['forecastday'][num1]['day']['mintemp_c'])
        dailyrange = maxtemp_c - mintemp_c
        humidity = float(jsonObj['forecast']['forecastday'][num1]['hour'][num2]['humidity'])
        pressure = float(jsonObj['forecast']['forecastday'][num1]['hour'][num2]['pressure_mb'])
        pm10 = pm2_5 = 0
        if num1 == 0:
            pm10 = future_pm10(pm10_f1)
            pm2_5 = future_pm2_5(pm25_f1)
        elif num1 == 1:
            pm10 = future_pm10(pm25_f2)
            pm2_5 = future_pm2_5(pm25_f2)
        elif num1 == 2:
            pm10 = future_pm10(pm10_f3)
            pm10 = future_pm10(pm25_f3)

    # 일교차
    if dailyrange >= 12.5:
        dailyrange = 15
    elif dailyrange < 12.5 and dailyrange >= 9.9:
        dailyrange = 10
    elif dailyrange < 9.9 and dailyrange >= 7.3:
        dailyrange = 5
    elif dailyrange < 7.3:
        dailyrange = 0

    # 최저기온
    if mintemp_c < -8.1:
        mintemp_c = 15
    elif mintemp_c < 0.6 and mintemp_c >= -8.1:
        mintemp_c = 10
    elif mintemp_c >= 0.6 and mintemp_c < 13.5:
        mintemp_c = 5
    elif mintemp_c >= 13.5:
        mintemp_c = 0

    # 기압
    if pressure >= 1017.9:
        pressure = 15
    elif pressure < 1017.9 and pressure >= 1011.9:
        pressure = 10
    elif pressure < 1011.9 and pressure >= 1005.7:
        pressure = 5
    elif pressure < 1005.7:
        pressure = 0

    # 습도
    if humidity < 37.4:
        humidity = 20
    elif humidity >= 37.4 and humidity < 50.0:
        humidity = 15
    elif humidity >= 50.0 and humidity < 65.9:
        humidity = 10
    elif humidity >= 65.9:
        humidity = 5

    respiratory = mintemp_c + dailyrange + pm2_5 + pm10 + humidity + pressure

    if respiratory < 0:
        respiratory = 0
    elif respiratory > 100:
        respiratory = 100

    if num3 == 0:
        return round(respiratory), last_updated
    elif num3 == 1:
        return round(respiratory)


# 1. 미래지수 블럭
@application.route("/info", methods=['POST'])
def weather_info_f():
    req = request.get_json()
    response = requests.get(
        '[API KEY]')
    jsonObj = json.loads(response.text)


    date = req["action"]["detailParams"]["weather_date"]["value"]
    hour = req["action"]["detailParams"]["weather_hour"]["value"]
    info = req["action"]["detailParams"]["weather_info"]["value"]

    num2 = int(hour)

    send = 1
    num1 = 1
    num3 = 1
    if date == "오늘":
        num1 = 0
    elif date == "내일":
        num1 = 1
    elif date == "모레":
        num1 = 2

    umbrella, com = Umbrella(num1, num2, num3)

    if info == "드라이브지수":
        send = {"version": "2.0",
                "template": {"outputs": [
                    {"simpleText": {"text": date + hour + "시" + info + ":" + str(Drive(num1, num2, num3)) + " 입니다"}}]}}
    elif info == "한강지수":
        send = {"version": "2.0",
                "template": {"outputs": [{"simpleText": {
                    "text": date + hour + "시" + info + ":" + str(hangang(num1, num2, num3)) + " 입니다"}}]}}
    elif info == "런닝지수":
        send = {"version": "2.0",
                "template": {"outputs": [{"simpleText": {
                    "text": date + hour + "시" + info + ":" + str(running(num1, num2, num3)) + " 입니다"}}]}}
    elif info == "우산지수":
        send = {"version": "2.0",
                "template": {"outputs": [{"simpleText": {"text": date + hour + "시" + info + ":" + str(umbrella) + " 입니다" + "\n" + str(com)}}]}}
    elif info == "감기위험지수":
        send = {"version": "2.0",
                "template": {"outputs": [
                    {"simpleText": {"text": date + hour + "시" + info + ":" + str(cold(num1, num2, num3)) + " 입니다"}}]}}
    elif info == "세차지수":
        send = {"version": "2.0",
                "template": {"outputs": [{"simpleText": {
                    "text": date + hour + "시" + info + ":" + str(Car_Washing(num1, num2, num3)) + " 입니다"}}]}}
    elif info == "빨래지수":
        send = {"version": "2.0",
                "template": {"outputs": [{"simpleText": {
                    "text": date + hour + "시" + info + ":" + str(Washing(num1, num2, num3)) + " 입니다"}}]}}
    elif info == "식중독위험지수":
        send = {"version": "2.0",
                "template": {"outputs": [
                    {"simpleText": {"text": date + hour + "시" + info + ":" + str(poison(num1, num2, num3)) + " 입니다"}}]}}
    elif info == "호흡기위험지수":
        send = {"version": "2.0",
                "template": {"outputs": [{"simpleText": {
                    "text": date + hour + "시" + info + ":" + str(respiratory(num1, num2, num3)) + " 입니다"}}]}}

    return jsonify(send)


# 2. 현재지수 블럭
@application.route("/current_info", methods=['POST'])
def current_info_f():
    req = request.get_json()
    response = requests.get(
        '[API KEY]')
    jsonObj = json.loads(response.text)

    info = req["action"]["detailParams"]["weather_info"]["value"]
    send = 1
    num1 = 0
    num2 = 0
    num3 = 0

    Drive_info, Drive_last = Drive(num1, num2, num3)
    str(Drive_info), str(Drive_last)

    hangang_info, hangang_last = hangang(num1, num2, num3)
    str(hangang_info), str(hangang_last)

    running_info, running_last = running(num1, num2, num3)
    str(running_info), str(running_last)

    Umbrella_info, com, Umbrella_last = Umbrella(num1, num2, num3)
    str(Umbrella_info), str(com), str(Umbrella_last)

    cold_info, cold_last = cold(num1, num2, num3)
    str(cold_info), str(cold_last)

    Car_Washing_info, Car_Washing_last = Car_Washing(num1, num2, num3)
    str(Car_Washing_info), str(Car_Washing_last)

    Washing_info, Washing_last = Washing(num1, num2, num3)
    str(Washing_info), str(Washing_last)

    poison_info, poison_last = poison(num1, num2, num3)
    str(poison_info), str(poison_last)

    respiratory_info, respiratory_last = respiratory(num1, num2, num3)
    str(respiratory_info), str(respiratory_last)

    if info == "드라이브지수":
        send = {"version": "2.0",
                "template": {"outputs": [{"simpleText": {
                    "text": "마지막 업데이트: " + str(Drive_last) + "\n" + info + ":" + str(Drive_info) + " 입니다"}}]}}
    elif info == "한강지수":
        send = {"version": "2.0",
                "template": {"outputs": [{"simpleText": {
                    "text": "마지막 업데이트: " + str(hangang_last) + "\n" + info + ":" + str(hangang_info) + " 입니다"}}]}}
    elif info == "런닝지수":
        send = {"version": "2.0",
                "template": {"outputs": [{"simpleText": {
                    "text": "마지막 업데이트: " + str(running_last) + "\n" + info + ":" + str(running_info) + " 입니다"}}]}}
    elif info == "우산지수":
        send = {"version": "2.0",
                "template": {"outputs": [
                    {"simpleText": {"text": "마지막 업데이트: " + str(Umbrella_last) + "\n" + info + ":" + str(Umbrella_info) + "입니다" + "\n" + str(com)}}]}}
    elif info == "감기위험지수":
        send = {"version": "2.0",
                "template": {"outputs": [{"simpleText": {
                    "text": "마지막 업데이트: " + str(cold_last) + "\n" + info + ":" + str(cold_info) + " 입니다"}}]}}
    elif info == "세차지수":
        send = {"version": "2.0",
                "template": {"outputs": [{"simpleText": {
                    "text": "마지막 업데이트: " + str(Car_Washing_last) + "\n" + info + ":" + str(
                        Car_Washing_info) + " 입니다"}}]}}
    elif info == "빨래지수":
        send = {"version": "2.0",
                "template": {"outputs": [{"simpleText": {
                    "text": "마지막 업데이트: " + str(Washing_last) + "\n" + info + ":" + str(Washing_info) + " 입니다"}}]}}
    elif info == "식중독위험지수":
        send = {"version": "2.0",
                "template": {"outputs": [{"simpleText": {
                    "text": "마지막 업데이트: " + str(poison_last) + "\n" + info + ":" + str(poison_info) + " 입니다"}}]}}
    elif info == "호흡기위험지수":
        send = {"version": "2.0",
                "template": {"outputs": [{"simpleText": {
                    "text": "마지막 업데이트: " + str(respiratory_last) + "\n" + info + ":" + str(
                        respiratory_info) + " 입니다"}}]}}

    return jsonify(send)


# 3. 현재날씨 블럭
@application.route("/current", methods=['POST'])
def current_f():
    response = requests.get(
        '[API KEY]')
    jsonObj = json.loads(response.text)

    temp_c = str(jsonObj['current']['temp_c'])
    uv = str(jsonObj['current']['uv'])
    wind_mps = round((jsonObj['current']['wind_mph']) / 2.237, 2)
    wind_mps = str(wind_mps)
    send_current = {"version": "2.0",
                    "template": {
                        "outputs": [{
                            "simpleText": {
                                "text": "현재기온: " + temp_c + "\n" + Temp_c(0, 0, 0) + "\n" +
                                        "자외선지수: " + uv + "\n" + Uv(0, 0, 0) + "\n" +
                                        "풍속(m/s): " + wind_mps + "\n" + Wind_mps(0, 0, 0) + "\n" +
                                        "미세먼지: " + current_pm10() + "\n" +
                                        "초미세먼지: " + current_pm2_5() + "\n"}
                        }
                        ]
                    }
                    }

    print(send_current)

    return send_current


# 미래날씨 블럭
@application.route("/future", methods=['POST'])
def future_f():
    req = request.get_json()
    response = requests.get(
        '[API KEY]')
    jsonObj = json.loads(response.text)

    date_f = req["action"]["detailParams"]["weather_date"]["value"]
    hour_f = req["action"]["detailParams"]["weather_hour"]["value"]

    num2 = int(hour_f)

    num1 = 1

    if date_f == "오늘":
        num1 = 0
    elif date_f == "내일":
        num1 = 1
    elif date_f == "모레":
        num1 = 2

    return send_weather(num1, num2)


if __name__ == "__main__":
    application.run(host='0.0.0.0', port=5000, threaded=True)
