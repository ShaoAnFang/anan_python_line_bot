#!/usr/bin/env python3 
# -*- coding: utf-8 -*-

import random
import requests
import json
from bs4 import BeautifulSoup
from flask import Flask, request, abort

from firebase import firebase
firebase = firebase.FirebaseApplication('https://python-f5763.firebaseio.com/',None)
queryAllKeyAndValues = firebase.get('/data',None)


from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

app = Flask(__name__)

line_bot_api = LineBotApi('E3V1P2J74V3qQ5VQsR0Au27E+NwBBlnh8r24mpP5vbkrogwj7PFroxNAKS9MU2iBeDMJiEFiaqe0SvKypYsoPcr70wVac/v4FJfXa1TwGPo0QeI1fkZcaejhJSz09aetC0TaMsblhNOorJaG4J/RlwdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('f2f133f2ba43194cf0e18503586023aa')




@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'

@app.route('/GGWP', methods=['GET'])
def test():
    return "Hello World!"

@app.route('/queryDB/<string:message>', methods=['GET'])
def firebaseQuery(message):
    allKeys = queryAllKeyAndValues.keys()
    for k in allKeys:
        #print(message.find(k))
        #若找不到 返回值是 -1
        if message.find(k) != -1:
            #print(queryAllKeyAndValues[k])
            queryAllValues = queryAllKeyAndValues[k]
            count = len(queryAllValues) - 1
            randomNumber = random.randint(0,count)
            result = queryAllValues[randomNumber]
            return result

@app.route('/insertDB/<string:key>/<string:value>', methods=['GET'])
def firebaseInsert(key,value):
    #key = '冠宏'
    #value = 'OC之神'
    getValues = firebase.get('/data',key)
    if getValues is None:
        new = dict()
        new['0'] = value
        putResult = firebase.put('data',key,new)
    else:    
        getValues.append(value)
        putResult = firebase.put('data',key,getValues)
  
    return "好的 記住了"


@app.route('/deleteDB', methods=['GET'])
def firebaseDelete(deleteKey):
    
    firebase.delete('/data', deleteKey)        
    return '好的 已經遺忘'

@app.route('/fetchDB/<string:key>', methods=['GET'])
def firebaseFetch(key):
       
    string = ''
    getValues = firebase.get('/data',key)
    if getValues is None:
        string = "沒有被寫入呢"
    else:
        for x in getValues:
            string += x + ' , '
        #刪掉最後一個逗號
        last = len(string)
        string = string[0:last]
    return string 
    
def stock(stockNumber):
    url = 'https://www.google.com.hk/finance?q='
    url += stockNumber
    header = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36'}
    res = requests.get(url,headers=header,verify=False)
    res.encoding = 'utf-8'
    soup = BeautifulSoup(res.text,'html.parser')
    title = soup.find('h3')
    title = title.text.strip()
    #print(title)
    
    resultString = ''
    resultString += title + '\n'
    #現價
    nowPrice = ''
    for p in soup.select('.pr'):
        #print(p.text)
        nowPrice += p.text.strip()
    
    #漲跌
    upDown = soup.select('.chr')
    if not upDown :
        upDown = soup.select('.chg')
    uString = ''
    for u in upDown:
        #print(u.text.strip().encode('utf8'))
        uString += u.text.strip()
        #print(uString)
    
    key = []
    for k in soup.select('.key'):
        #print(k.text.strip().encode('utf8'))
        key.append(k.text.strip())
    
    val = list()
    for v in soup.select('.val'):
        #print(v.text.strip().encode('utf8'))
        val.append(v.text.strip())
    
    #現價
    resultString += '-------------' + '\n'
    resultString += '現價 ' + '\n' + nowPrice + '\n'
    resultString += '-------------' + '\n'
    #漲跌
    resultString += '漲跌' + '\n' + uString + '\n'
    resultString += '-------------' + '\n'
    #每股盈餘
    resultString += key[7] + '\n' + val[7] + '\n'
    resultString += '-------------' + '\n'
    #開盤
    resultString += key[2]+ '\n' + val[2] + '\n'
    resultString += '-------------' + '\n'
    #範圍
    resultString += key[0] + '\n' + val[0] + '\n'
    resultString += '-------------' + '\n'
    #52週
    resultString += key[1] + '\n' + val[1] + '\n'
    resultString += '-------------' + '\n'
    #股息/收益
    resultString += key[6] + '\n' + val[6] + '\n' + '-------------' + '\n' + 'From Google stock'
   
    return resultString
   
@app.route('/weather', methods=['GET'])
def weather(ChooseCity):
    cityDict = dict()
    cityDict = {'台北': 'Taipei_City', '新北': 'New_Taipei_City', '桃園': 'Taoyuan_City',
          '台中': 'Taichung_City', '台南': 'Tainan_City', '高雄': 'Kaohsiung_City',
          '基隆': 'Keelung_City', '新竹市': 'Hsinchu_City', '新竹縣': 'Hsinchu_County',
          '苗栗市': 'Miaoli_County', '苗栗縣': 'Changhua_County', '南投': 'Nantou_County',
          '雲林': 'Yunlin_County', '嘉義市': 'Chiayi_City', '嘉義縣': 'Chiayi_County',
          '屏東': 'Pingtung_County', '宜蘭': 'Yilan_County', '花蓮': 'Hualien_County',
          '台東': 'Taitung_County', '澎湖': 'Penghu_County','金門': 'Kinmen_County',
          '連江': 'Lienchiang_County'}

    url = 'http://www.cwb.gov.tw/V7/forecast/taiwan/{}.htm'.format(cityDict[ChooseCity])
    #print(url)
    #header = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36'}
    #res = requests.get(url,headers=header,verify=False)
    res = requests.get(url,verify=False)
    res.encoding = 'utf-8'
    soup = BeautifulSoup(res.text,'html.parser')
    #print soup
    city = soup.select('.currentPage')[0].text
    #print(city)
    time = soup.select('.Issued')[0].text
    time = time.split(': ')[1]
    time = time.split(' ')[0]
    #print(time)

    imgTitle = soup.find_all('img')

    title = []
    for i in imgTitle: 
        i = str(i).split('title="')[1]
        i = str(i).split('"/>')[0]
        #print i
        title.append(i)

    content = soup.select('td')
    data = []
    for c in content:
        c = c.text.strip('\n')
        #print(c.encode('utf8'))
        data.append(c)
    
    resultString = ''
    resultString += '🌤 ' + city + '  '  + time + '\n\n' 

    resultString += '今晚至明晨 ' + str(data[0])  + '度\n' 
    resultString += title[0] + '  下雨機率 ' + str(data[3]) + '\n\n' 

    resultString += '明日白天' + str(data[4]) + ' 度\n'
    resultString += title[1] + '  下雨機率 ' + str(data[7]) + '\n\n' 

    resultString += '明日晚上' + str(data[8]) + ' 度\n'
    resultString += title[2] + '  下雨機率 ' + str(data[11]) + '\n'
    resultString += '-交通部氣象局'
    return resultString


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    msg = event.message.text
    
    #if event.source.user_id is not None:
        #profile = line_bot_api.get_profile(event.source.user_id)
        #n = profile.display_name
        #p = profile.picture_url
        #m = profile.status_message
        #p = n + '\n \n' + p + '\n \n' + m
 
    if msg == '安安':
        menulist = 'Hello 我是安安 你可以 \n' + '\n' + '1. 教我說話 \n' + '安 你好=Hello World! \n1.1 查詢教過的關鍵字 \n查 AA\n1.2 刪除 教過的字 \n遺忘 AA \n\n'
        menulist += '2. 輸入 天氣 台北 \n\n'
        menulist += '3. 輸入 股 2330 \n' + '顯示該股票代碼的即時查詢 \n'
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text=menulist))
        
    if msg == 'id':
        profile = line_bot_api.get_profile(event.source.user_id)
        n = profile.display_name
        p = profile.picture_url
        m = profile.status_message
        p = n + '\n \n' + p + '\n \n' + m
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text=p))    
        
    if msg[0] == '股' and msg[1] == ' ' and len(msg) == 6:
        stockNumber = msg.split()[1]
        result = stock(stockNumber)
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text=result))
        
    #if len(msg) > 50:
    #    line_bot_api.reply_message(event.reply_token,TextSendMessage(text='有些文章自己看看就好 廢文就不用再轉發了吧'))
    
    if msg[0] == '安' and msg[1] == ' ':
        msg =  msg.strip('~!@#$%^&*()|"')
        String = msg.split('安 ')[1]
        #print(String)
        key = String.split('=')[0]
        key = key.split()
        #print(key[0])
        #如果第一個字是空白則去除
        value = String.split('=')[1]
        if value[0] == ' ':
            #從第二個字開始算 再裝回去
            value = value[1:]
            if value == '':
                line_bot_api.reply_message(event.reply_token,TextSendMessage(text='不好意思 特殊字元會記不住呢'))
    
        insertFirebase = firebaseInsert(key[0],value)   
        
        #if event.source.user_id is not None:
        
            #insertResult = n + '說的是: \n' + key[0]+ ' = ' + value + ' 嗎? \n' + insertFirebase + ' !'
            #line_bot_api.reply_message(event.reply_token,TextSendMessage(text=insertResult))
        #else:
        insertResult = key[0]+ ' = ' + value + ' 嗎? \n' + insertFirebase + ' !'
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text=insertResult))
        
    if msg[0] == '遺' and msg[1] == '忘' and msg[2] ==' ':
        string = msg.split('遺忘 ')[1]
        print(string)
        deleteFirebase = firebaseDelete(string)
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text=deleteFirebase))
        
    if msg[0] == '查' and msg[1] == ' ':
        string = msg.split('查 ')[1]   
        fetchResult = firebaseFetch(string)
        result = '關鍵字 ' + string + ' 結果為: \n' + fetchResult
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text=result))
    
    if msg[0] == '天' and msg[1] == '氣' and msg[2] == ' ':
        ChooseCity = msg.split('天氣 ')[1]
        weatherResult = weather(ChooseCity)
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text=weatherResult))
        
    if msg == 'temp':
        buttons_template_message = TemplateSendMessage(
            alt_text='Buttons template',
            template=ButtonsTemplate(
                thumbnail_image_url='https://example.com/image.jpg',
                title='Menu',
                text='Please select',
                actions=[
                    PostbackTemplateAction(
                        label='postback',
                        text='postback text',
                        data='action=buy&itemid=1'
                    ),
                    MessageTemplateAction(
                        label='message',
                        text='message text'
                    ),
                    URITemplateAction(
                        label='uri',
                        uri='http://example.com/'
                    )
                ]
            )
        )
        line_bot_api.reply_message(event.reply_token, buttons_template_message)
        
    
    dbResult = firebaseQuery(msg)
    if dbResult != "":
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text=dbResult))
    
    line_bot_api.reply_message(event.reply_token,TextSendMessage(text=msg))
        
  

if __name__ == "__main__":
    app.run()
