import requests
import pandas as pd
import re
import json
import webbrowser
from datetime import datetime
from bs4 import BeautifulSoup

# For 車票資訊 :
#   桃園 + 中壢 : 1 + 1017 
#   宜蘭 + 頭城 : 14 + 1816
# For 訂票資訊 :
#   中壢 : 108
#   頭城 : 077

def search_train(mode, month, date):

    # 0 : 頭城到中壢 |  1 : 中壢到頭城
    if mode == 0:
        fromCity = '14'
        fromStation = '1816'
        toCity = '1'
        toStation = '1017'
    elif mode == 1:
        fromCity = '1'
        fromStation = '1017'
        toCity = '14'
        toStation = '1816'

    # set time
    time = '2018-' + month + '-' + date

    # 取得form data
    payload = {
        'FromCity': fromCity,
        'FromStation': fromStation,
        'FromStationName': '0',
        'ToCity': toCity,
        'ToStation': toStation,
        'ToStationName': '0',
        'TrainClass': '2',
        'searchdate': time,
        'FromTimeSelect': '0000',
        'ToTimeSelect': '2359',
        'Timetype': '1'
    }

    # initial set
    res = requests.post("http://twtraffic.tra.gov.tw/twrail/TW_SearchResult.aspx", data = payload)
    soup = BeautifulSoup(res.text,"html.parser")

    # 取得時刻表資訊
    trainDetail = soup.find("script", string=re.compile("var JSONData*")).text[13:-1]

    # to list
    trainList = json.loads(trainDetail)
    trainType = []
    trainNum = []
    viaRoad = []
    departureTime = []
    arrivalTime = []
    needTime = []
    money = []

    for num in trainList:
        if(num['Class_Code'] == '1111' or num['Class_Code'] == '1110'):
            trainType.append('Chu-Kuang')
        elif(num['Class_Code'] == '1132'):
            trainType.append('Local Train Fast')
        elif(num['Class_Code'] == '1131'):
            trainType.append('Local Train')
        elif(num['Class_Code'] == '1108'):
            trainType.append('Tze-Chiang')
        else:
            trainType.append('Others')

        if(num['MainViaRoad'] == '0'):
            viaRoad.append('-')
        elif(num['MainViaRoad'] == '1'):
            viaRoad.append('M')
        elif(num['MainViaRoad'] == '2'):
            viaRoad.append('S')

        trainNum.append(num['Train_Code'])
        departureTime.append(num['From_Departure_Time'])
        arrivalTime.append(num['To_Arrival_Time'])
        time = datetime.strptime(num['To_Arrival_Time'], "%H%M") - datetime.strptime(num['From_Departure_Time'], "%H%M")
        needTime.append(time)
        money.append(num['Fare'])

    # 轉為dataFrame
    df = pd.DataFrame(
        {'Type' : trainType,
        'TrainCode' : trainNum,
        'Via' : viaRoad,
        'Departure Time' : departureTime, 
        'Arrival Time' : arrivalTime, 
        'Need Time' : needTime,
        'Money' : money },
        columns=['Type', 'TrainCode', 'Via', 'Departure Time', 'Arrival Time', 'Need Time', 'Money']
    )
    print(df)

