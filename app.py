#!/usr/bin/env python3 
# -*- coding: utf-8 -*-
import requests
import json
from bs4 import BeautifulSoup
from flask import Flask, request, abort

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


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):

    #line_bot_api.reply_message(
    #    event.reply_token,
    #    TextSendMessage(text=event.message.text))

    if event.message.text == '股':
        result = stock()
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text=result))
    else:  
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text=event.message.text))

    
def stock():
    url = 'https://www.google.com.hk/finance?q=TPE:2330'
    header = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36'}
    res = requests.get(url,headers=header,verify=False)
    res.encoding = 'utf-8'
    soup = BeautifulSoup(res.text,'html.parser')
    title = soup.find('h3')
    title = title.text.strip()
    #print(title)
    
    resultString = ''
    resultString += title
    
    upDown = soup.select('.chr')
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
    
    resultString += k[2] + '' + val[2]
    
    
    dictionary = dict(zip(key,val))
    dictionary['漲跌'] = uString
    #resultString += dictionary['漲跌']
    
    #del dictionary['啤打系數']
    #del dictionary['機構持股率：']
    #print(json.dumps(dictionary, ensure_ascii=False))

    
    resultString += title + '\n'

    #for key, value in dictionary.items():
        #print key, value
    #    resultString += key + ' ' + value + '\n'
        #print resultString
   
    

    return resultString
    

if __name__ == "__main__":
    app.run()
