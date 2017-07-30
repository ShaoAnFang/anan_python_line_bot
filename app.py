#!/usr/bin/env python3 
# -*- coding: utf-8 -*-

import random
import requests
import json
from bs4 import BeautifulSoup
from flask import Flask, request, abort

from firebase import firebase
firebase = firebase.FirebaseApplication('https://python-f5763.firebaseio.com/',None)
    
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

@app.route('/queryDB', methods=['GET'])
def firebaseQuery(message):
    
    #只撈DB的Key做比對,如果沒有則全撈下來和整句比對
    queryAllValues = []
    queryAllValues = firebase.get('/data',message)
    if queryAllValues is not None:
        #print(getResult)
        #取個數
        count = len(queryAllValues) - 1
        #抽亂數
        randomNumber = random.randint(0,count)
        #print(queryAllValues[randomNumber])
        result = queryAllValues[randomNumber]
    else:
        #全撈下,和整句比對
        queryAllKeyAndValues = firebase.get('/data',None)
        #把Key丟進allKeys[]
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

@app.route('/insertDB', methods=['GET'])
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
   
  
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    msg = event.message.text
 
    if msg == '安安':
        menulist = 'Hello 我是安安 你可以 \n' + '\n' + '1. 教我說話 \n' + '安 你好=Hello World! \n \n'
        menulist += '2. 輸入 股 2330 \n' + '顯示該股票代碼的即時查詢 \n'
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text=menulist))
        
    if msg == 'id':
        
        profile = line_bot_api.get_profile(event.source.user_id)
        
        n = profile.display_name
        p = profile.picture_url
        m = profile.status_message
        
        p = n + '\n' + p + '\n' + m
        
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
        insertResult = key[0]+ ' = ' + value + ' 嗎? \n' + insertFirebase + ' !'
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text=insertResult))
        
    
    if msg == '開始玩':
        buttons_template = TemplateSendMessage(
            type = 'template',
            alt_text='開始玩 template',
            template=ButtonsTemplate(
                title='選擇服務',
                text='請選擇',
                thumbnail_image_url='https://i.imgur.com/xQF5dZT.jpg',
                actions=[
                    MessageTemplateAction(
                        label='新聞',
                        text='新聞'
                    ),
                    MessageTemplateAction(
                        label='電影',
                        text='電影'
                    )
                ]
            )
        )
        line_bot_api.reply_message(event.reply_token, buttons_template)
        return 0
    
    dbResult = firebaseQuery(msg)
    if dbResult != "":
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text=dbResult))
    
    line_bot_api.reply_message(event.reply_token,TextSendMessage(text=msg))
        
  

if __name__ == "__main__":
    app.run()
