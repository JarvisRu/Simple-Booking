import requests
import pandas as pd
import re
import json
import webbrowser
from datetime import datetime
from bs4 import BeautifulSoup

# 車票資訊：中壢到頭城
fromCity = '1'
fromStation = '1017'
toCity = '14'
toStation = '1816' 
date = '2018-07-24'

# 取得form data
payload = {
    'FromCity': fromCity,
    'FromStation': fromStation,
    'FromStationName': '0',
    'ToCity': toCity,
    'ToStation': toStation,
    'ToStationName': '0',
    'TrainClass': '2',
    'searchdate': '2018-07-24',
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

# 產出訂購網址
# http://railway.hinet.net/Foreign/TW/etno1.html?from_station=108&to_station=077&getin_date=2018/07/24&train_no=562
orderUrl = "http://railway.hinet.net/Foreign/TW/etno1.html?from_station=" + from_station + "&to_station=" + to_station + "&getin_date=" + getin_date + "&train_no=" + train_no

webbrowser.open('http://google.co.kr', new=2)
