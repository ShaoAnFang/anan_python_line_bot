#!/usr/bin/env python3 
# -*- coding: utf-8 -*-
import re
import time
import json
import pytz 
import random
import gspread
import requests
import datetime

from firebase import firebase
from bs4 import BeautifulSoup
from imgurpython import ImgurClient
from flask import Flask, request, abort

from oauth2client.service_account import ServiceAccountCredentials
from Module import Aime, Constellation, Weather, Movies, GoogleSheet, TemplateSend, Sticker

sendTime = time.time()

firebase = firebase.FirebaseApplication('https://python-f5763.firebaseio.com/',None)
queryAllKeyAndValues = firebase.get('/data',None)
quiet = firebase.get('/QuietGroup',None)
quietArr = quiet['group_id']

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *
#from linebot.models import (
#    MessageEvent, TextMessage, TextSendMessage,TemplateSendMessage
#)

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
    #queryAllKeyAndValues = firebase.get('/data',None)
    global queryAllKeyAndValues
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
    
    return 'GG'

@app.route('/insertDB/<string:key>/<string:value>', methods=['GET'])
def firebaseInsert(key,value):
    #key = '冠宏'
    #value = 'OC之神'
    getValues = firebase.get('/data',key)
    if getValues is None:
        new = dict()
        new['0'] = value
        firebase.put('data',key,new)
    else:    
        getValues.append(value)
        firebase.put('data',key,getValues)
    #寫完 停兩秒 再讀取DB一次
    time.sleep(2)
    global queryAllKeyAndValues
    queryAllKeyAndValues.clear()
    queryAllKeyAndValues = firebase.get('/data',None)
    #queryAllKeyAndValues[key] = value
    return "好的 記住了"

@app.route('/deleteDB', methods=['GET'])
def firebaseDelete(deleteKey):
    firebase.delete('/data', deleteKey)
    time.sleep(2)
    #刪除完再重新讀取一次DB
    global queryAllKeyAndValues
    queryAllKeyAndValues.clear()
    queryAllKeyAndValues = firebase.get('/data',None)
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

def firebaseChatLog(content, name='', userID = ''):
    tz = pytz.timezone('Asia/Taipei')
    dd = datetime.datetime.now(tz).date()
    inputDate = "{}-{}-{}".format(dd.year,dd.month,dd.day)
    getChatLog = firebase.get('/ChatLog',inputDate)
    
    if name != '' and userID != '':
        content = name + ':' + content + '.' + userID
        
    if getChatLog is None:
        arr = []
        arr.append(content)
        firebase.put('/ChatLog',inputDate,arr)
    else:    
        getChatLog.append(content)
        firebase.put('/ChatLog',inputDate,getChatLog)


# def stock(stockNumber):
#     url = 'https://www.google.com.hk/finance?q='
#     url += stockNumber
#     header = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36'}
#     res = requests.get(url,headers=header,verify=False)
#     res.encoding = 'utf-8'
#     soup = BeautifulSoup(res.text,'html.parser')
#     title = soup.find('div', class_='PyJv1b kno-fb-ctx')
#     #print(title.text)
#     resultString = '{}'.format(title.text) + '\n'
#     info = soup.find_all('td', class_='iyjjgb')
#     #print(info)
#     for index, element in enumerate(info):
#         if index == 0:
#             resultString+= '-------------' + '\n'
#             resultString+= '開盤: '+ element.text + '\n'
#         if index == 1:
#             resultString+= '最高: '+ element.text + '\n'
#         if index == 2:
#             resultString+= '最低: '+ element.text + '\n'
#         if index == 3:
#             resultString+= '本益比: '+ element.text + '\n'
#         if index == 7:
#             resultString+= '上次收盤價: '+ element.text + '\n'
#             resultString+= 'From Google'
#     return resultString


@app.route('/star/<string:star>', methods=['GET'])
def getConstellation(star):
    resultString = Constellation.constellation(star)
    return resultString

@app.route('/weather', methods=['GET'])
def weather(ChooseCity):
    resultString = Weather.weather(ChooseCity)
    return resultString

@app.route('/movie', methods=['GET'])
def get_movies():
    movies = Movies.get_movies()
    return movies

def sticker(key):
    searchResult = Sticker.sticker(key)
    return searchResult

#AVgle API
def darkAnan():
    AVGLE_LIST_COLLECTIONS_API_URL = 'https://api.avgle.com/v1/videos/{}'

    randomPagesNumber = random.randint(0,1195)
    #page 1195,有60片,其他都50
    #print randomPageNumber
    if randomPagesNumber != 1195:
        #0~49選不重複的7個數字
        randomVideoNumbers = random.sample(range(0, 49), 5)
    else:
        randomVideoNumbers = random.sample(range(0, 59), 5)

    res = requests.get(AVGLE_LIST_COLLECTIONS_API_URL.format(randomPagesNumber))
    res.encoding='utf8'
    #print(res.json())
    videos = []
    videos = res.json()['response']['videos']
    
    videoRandom = []
    for x in randomVideoNumbers:
        videoRandom.append(videos[x])
    
    return videoRandom

def darkAnanQuery(name):
    url = 'https://api.avgle.com/v1/search/{}/{}'
    res = requests.get(url.format(name,'0'))
    videos = res.json()['response']['videos']
    randomVideoNumbers = random.sample(range(0, len(videos)), 5)
    
    videoRandom = []
    for x in randomVideoNumbers:
        videoRandom.append(videos[x])
    
    return videoRandom

#存取imgur
def aime(key):
    imgurResult = Aime.aime(key)
    return imgurResult

def handsome():
    client_id = 'c3e767d450a401e'
    client_secret = 'cdf5fb70e82bc00e65c0d1d1a4eed318ae82024c'
    client = ImgurClient(client_id,client_secret)
    images = client.get_album_images('hjCtM')
    index = random.randint(0, len(images) - 1)
    
    return images[index].link

@app.route('/wine', methods=['GET'])
def wine():
    notYet = GoogleSheet.wine()
    return notYet

@app.route('/birthday/<string:date>', methods=['GET'])
def birthday(date):
    result = GoogleSheet.birthday(date)
    return result

# LocationMessage
@handler.add(MessageEvent, message=LocationMessage)
def handle_message(event): 
    locationInfo = '地區:' + event.message.address[:20] + '\n\n'
    locationInfo += '經緯度: ' '(' + str(event.message.longitude)[:10] +' ,'+ str(event.message.latitude)[:10] + ' )'+ '\n\n'
    locationInfo += '向阿寶請示雄三發射許可' + '\n' +'請稍候'
    #line_bot_api.reply_message(event.reply_token,TextSendMessage(text=str(event))) 
    line_bot_api.reply_message(event.reply_token,TextSendMessage(text=locationInfo)) 
    
#@handler.add(MessageEvent, message=ImageMessage)
#def handle_message(event): 
    #image_message = ImageSendMessage(
    #    original_content_url='https://i.imgur.com/uPhBqLK.jpg',
    #    preview_image_url='https://i.imgur.com/uPhBqLK.jpg'
    #)
    #line_bot_api.reply_message(event.reply_token, image_message)
    
    #line_bot_api.reply_message(event.reply_token,TextSendMessage(text=str(event.message)))
    
@handler.add(MessageEvent, message=StickerMessage)
def handle_message(event): 
    sticker_message = StickerSendMessage(
        package_id = event.message.package_id,
        sticker_id = event.message.sticker_id
    )
    line_bot_api.reply_message(event.reply_token, sticker_message)


@handler.add(MessageEvent, message=AudioMessage)
def handle_message(event): 
    msgType = event.message.type
    id = event.message.id
    m = 'msgType:' + msgType + '\n' + 'id:' + id
    url = 'https://api.line.me/v2/bot/message/{}/content'.format(id)
    headers =  {'Authorization':'Bearer E3V1P2J74V3qQ5VQsR0Au27E+NwBBlnh8r24mpP5vbkrogwj7PFroxNAKS9MU2iBeDMJiEFiaqe0SvKypYsoPcr70wVac/v4FJfXa1TwGPo0QeI1fkZcaejhJSz09aetC0TaMsblhNOorJaG4J/RlwdB04t89/1O/w1cDnyilFU=' }
    response = requests.get(url, headers=headers)
    #print(response)
    with open('{}.m4a'.format(id), 'wb') as f:
        f.write(response.content)
    line_bot_api.reply_message(event.reply_token,TextSendMessage(text=m))


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    msg = event.message.text

    #if event.source.group_id is not None:
    #    groupID = event.source.group_id 

    if msg == '沒填生日':
        m = birthday(msg)
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text=m))

    if msg.find('生日') != -1:
        string = msg.split('生日')[1]
        m = birthday(string)
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text=m))

    if msg == '重抓':
        global queryAllKeyAndValues
        queryAllKeyAndValues.clear()
        queryAllKeyAndValues = firebase.get('/data',None)

    if msg == '抽':
        result = handsome()
        image_message = ImageSendMessage(
            original_content_url=result,
            preview_image_url=result)
        line_bot_api.reply_message(event.reply_token, image_message)
    
    if msg.find('哪喝') != -1:
        w = wine()
        w += '\n\n這家如何呢!?'
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text=w))

    if msg == '籃球':
        video_message = VideoSendMessage(
            original_content_url='https://firebasestorage.googleapis.com/v0/b/python-f5763.appspot.com/o/Hollaback%20Girl.mp4?alt=media&token=e46a3d98-6e51-4c18-b903-61ff45f19f2a',
            preview_image_url='https://imgur.com/tCtYGfK.jpg')
        line_bot_api.reply_message(event.reply_token, video_message) 
        
    if msg == '上車':
        video_message = VideoSendMessage(
            original_content_url='https://firebasestorage.googleapis.com/v0/b/python-f5763.appspot.com/o/89.mp4?alt=media&token=4a20b5ca-d129-496a-a0b3-1d820204a3c1',
            preview_image_url='https://firebasestorage.googleapis.com/v0/b/python-f5763.appspot.com/o/89.png?alt=media&token=c3238c0d-3207-4d6d-9867-0bfa80381263')
        line_bot_api.reply_message(event.reply_token, video_message)
        
    if msg.find('吃懶') != -1 :
        image_message = ImageSendMessage(
            original_content_url='https://imgur.com/5XILKP5.jpg',
            preview_image_url='https://imgur.com/5XILKP5.jpg')
        line_bot_api.reply_message(event.reply_token, image_message)  
        
    if msg == '好朋友' :
        image_message = ImageSendMessage(
            original_content_url='https://imgur.com/2jB4sV1.jpg',
            preview_image_url='https://imgur.com/2jB4sV1.jpg')
        line_bot_api.reply_message(event.reply_token, image_message)
        
    if msg.find('珍惜') != -1 :
        image_message = ImageSendMessage(
            #https://imgur.com/syKgMMa.jpg
            original_content_url='https://imgur.com/Htn9qxf.jpg',
            preview_image_url='https://imgur.com/Htn9qxf.jpg')
        line_bot_api.reply_message(event.reply_token, image_message)
    
    if msg.find('珍奶') != -1 :
        image_message = ImageSendMessage(
            original_content_url='https://imgur.com/3XBTU2t.jpg',
            preview_image_url='https://imgur.com/3XBTU2t.jpg')
        line_bot_api.reply_message(event.reply_token, image_message)
    
    if msg.find('葡萄') != -1 :
        hua = ["https://i.imgur.com/NxG5gdO.jpg", "https://i.imgur.com/Th8j0Qu.jpg", "https://i.imgur.com/5EouecF.jpg"]
        url = hua[random.randint(0,2)]
        image_message = ImageSendMessage(
            original_content_url = url,
            preview_image_url= url)
        line_bot_api.reply_message(event.reply_token, image_message)
        
    global quiet
    global quietArr
    if msg == '安靜':
        if event.source.group_id in quietArr :
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text='已經安靜哩'))       
        else:    
#             quietArr.append(event.source.group_id)
#             firebase.put('QuietGroup','group_id',quietArr)
#             #寫完讓DB重讀一次
#             time.sleep(2)
#             quiet.clear()
#             quietArr.clear()
#             quiet = firebase.get('/QuietGroup',None)
#             quietArr = quiet['group_id']
#             line_bot_api.reply_message(event.reply_token,TextSendMessage(text='好的 安靜哩'))
            quietArr.append(event.source.group_id)
            firebase.put('QuietGroup','group_id',quietArr)
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text='好的 安靜哩'))
        
    if msg == '講話':
        if event.source.group_id in quietArr :
            quietArr.remove(event.source.group_id)
            firebase.put('QuietGroup','group_id',quietArr)
            #寫完讓DB重讀一次
            time.sleep(2)
            quiet.clear()
            quietArr.clear()
            quiet = firebase.get('/QuietGroup',None)
            quietArr = quiet['group_id']
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text='好 我會好好講話'))

    if msg == '安安':
        menulist = 'Hello 我是安安 你可以 \n' + '\n' + '1. 教我說話 \n' + '安 你好=Hello World! \n1.1 查詢教過的關鍵字 \n查 AA\n1.2 刪除 教過的字 \n遺忘 AA \n\n'
        menulist += '2. 輸入 天氣 台北 \n\n'
        menulist += '3. 輸入 星座 天蠍\n\n'
        menulist += '4. 輸入 電影\n\n'
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text=menulist))
       
    # if msg[0] == '股' and msg[1] == ' ' and len(msg) == 6:
    #     stockNumber = msg.split()[1]
    #     result = stock(stockNumber)
    #     line_bot_api.reply_message(event.reply_token,TextSendMessage(text=result))
        
    #if len(msg) > 200:
    #    line_bot_api.reply_message(event.reply_token,TextSendMessage(text='未看先猜 __文'))
    
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
        
        insertResult = key[0]+ ' = ' + value + ' 嗎? \n' + insertFirebase + ' !'
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text=insertResult))
        
        #if event.source.user_id != "" :
            #profile = line_bot_api.get_profile(event.source.user_id)
            #n = profile.display_name
            #insertResult = '嗨! ' + n + '說的是: \n' + key[0]+ ' = ' + value + ' 嗎? \n' + insertFirebase + ' !'
            #line_bot_api.reply_message(event.reply_token,TextSendMessage(text=insertResult))
            
        #else:
        #insertResult = key[0]+ ' = ' + value + ' 嗎? \n' + insertFirebase + ' !'
        #line_bot_api.reply_message(event.reply_token,TextSendMessage(text=insertResult))
        
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
    
    if msg[0] == '星' and msg[1] == '座' and msg[2] == ' ':
        star = msg.split('星座 ')[1]
        constellationResult = getConstellation(star)
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text=constellationResult))
        
    if msg[0] == '天' and msg[1] == '氣' and msg[2] == ' ':
        ChooseCity = msg.split('天氣 ')[1]
        weatherResult = weather(ChooseCity)
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text=weatherResult))
        
    if msg == '時間':
        tz = pytz.timezone('Asia/Taipei')
        dd = datetime.datetime.now(tz).date()
        dt = datetime.datetime.now(tz).time()
        queryTime = "{}-{}-{} {}:{}".format(dd.year,dd.month,dd.day,dt.hour,dt.minute)
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text=queryTime))
    
    if msg== 'Id' or msg== 'id':
        #if event.source.type =='group':
        #    line_bot_api.reply_message(event.reply_token,TextSendMessage(text=event.source.group_id))
        #else: 

        profile = line_bot_api.get_profile(event.source.user_id)
        n = profile.display_name
        p = profile.picture_url
        i = profile.user_id
        m = profile.status_message
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text= n))

        if not m:
            z = n + '\n \n' + p + '\n \n' + '\n \n' + event.source.user_id
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text= z))
        else: 
            z = n + '\n \n' + p + '\n \n' + m + '\n \n' + event.source.user_id
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text= z))

    if msg == '電視' or msg == 'Tv' or msg == 'TV' or msg == 'tv':
        carousel_template_message = TemplateSend.sportsChannel()
        line_bot_api.reply_message(event.reply_token, carousel_template_message)

    if msg == '電影':
        if event.source.type == 'group' :
            if event.source.group_id == 'C54f882fec4c5b8dc538b6d1cee5fc31f' :
                line_bot_api.reply_message(event.reply_token,TextSendMessage(text=''))
        g = get_movies()
        carousel_template_message = TemplateSend.moive(g)
        line_bot_api.reply_message(event.reply_token, carousel_template_message)
    
    if msg == '小電影' or msg == 'AV':
        if event.source.type == 'group' and event.source.group_id == 'C54f882fec4c5b8dc538b6d1cee5fc31f':
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text=''))
        elif event.source.user_id == 'U2e046844ad61d32e4e091b2db7dbc53f':
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text='GG WP'))
            
        avgleResult = darkAnan()
        carousel_template_message = TemplateSend.avgleSearch(avgleResult)
        line_bot_api.reply_message(event.reply_token, carousel_template_message)         
    
    
    if msg[0] == 'A' and msg[1] == 'V' and msg[2] == ' ' and len(msg) >= 4:
        #帶有人名的查詢 'AV XXXX'
        if event.source.type == 'group' and event.source.group_id == 'C54f882fec4c5b8dc538b6d1cee5fc31f':
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text=''))
        elif event.source.user_id == 'U2e046844ad61d32e4e091b2db7dbc53f':
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text='GG WP'))
        # event.source.group_id == 'C54f882fec4c5b8dc538b6d1cee5fc31f'
        name = msg.split('AV ')[1]
        avgleResult = darkAnanQuery(name)
        #asd = avgleResult[4]['title'][:10] + '\n' + avgleResult[4]['preview_url'] +'\n'+ avgleResult[4]['keyword'][:10] +'\n'+ avgleResult[4]['video_url']
        #line_bot_api.reply_message(event.reply_token,TextSendMessage(text=asd))
        carousel_template_message = TemplateSend.avgleSearch(avgleResult, titleText=msg)
        line_bot_api.reply_message(event.reply_token, carousel_template_message)
        
    if msg == 'Aime' or msg == 'aime' or msg == 'AlittleSheep' or msg == '小綿羊':
        albumResult = aime(msg)
        #album = albumResult[4]['imageLink'] + '\n' + albumResult[4]['title&price'] +'\n' + albumResult[4]['shopeeLink']
        #line_bot_api.reply_message(event.reply_token,TextSendMessage(text=album))
        carousel_template_message = TemplateSend.aime(albumResult, msg)
        line_bot_api.reply_message(event.reply_token, carousel_template_message)
        
    #firebaseChatLog(msg)
    #profile = line_bot_api.get_profile(event.source.user_id)
    if event.source.type =='user' :
        #直接對機器人講
        z = '單獨(user_id):' + event.source.user_id
        #firebaseChatLog(msg,profile.display_name,z)   
        firebaseChatLog(msg,'',z)
        
    elif event.source.type == 'group':
        #群組裡講
        z = '群組(group_id):' + event.source.group_id
        #firebaseChatLog(msg,profile.display_name,z)
        firebaseChatLog(msg,'',z)    
            
    if sticker(msg) != 'GG':
        if event.source.type !='group':
            sticker_message = StickerSendMessage(
            package_id = sticker(msg)['package_id'],
            sticker_id = sticker(msg)['sticker_id']
            )
            line_bot_api.reply_message(event.reply_token, sticker_message)
        
        elif not event.source.group_id in quietArr :
            sticker_message = StickerSendMessage(
            package_id = sticker(msg)['package_id'],
            sticker_id = sticker(msg)['sticker_id']
            )
            line_bot_api.reply_message(event.reply_token, sticker_message)
            
    dbResult = firebaseQuery(msg)
    if dbResult != 'GG':
        #line_bot_api.reply_message(event.reply_token,TextSendMessage(text=dbResult))
        
        #r = random.random()
        #if r > 0.05 :
        #    line_bot_api.reply_message(event.reply_token,TextSendMessage(text=dbResult))
        #else:
        #    line_bot_api.reply_message(event.reply_token,TextSendMessage(text='如果我之前回過幹話 不要生氣 去怪紹安')) 
        
        global sendTime
        sendTimeStr = str(sendTime).split('.')[0]
        s = int(sendTimeStr)
        
        now = str(time.time()).split('.')[0]
        n = int(now)

        if event.source.type != 'group':
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text=dbResult))
        
        if not event.source.group_id in quietArr and (n - s) > 10:
            sendTime = time.time()
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text=dbResult))

if __name__ == "__main__":
    app.run()
