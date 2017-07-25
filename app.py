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
    
    if event.message.text == 'stock':
        result = stock()

    line_bot_api.reply_message(
                               event.reply_token,
                               TextSendMessage(text=result))




def stock():
    stockNumber = '2330'
    url = 'https://tw.finance.yahoo.com/q/q?s='
    url += stockNumber
    print(url)
    
    #寫header偽裝成瀏覽器瀏覽
    header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:46.0) Gecko/20100101 Firefox/46.0'}
    resp = requests.get(url, headers=header ,verify=False)
    soup = BeautifulSoup(resp.text, 'html.parser')
    
    #撈出那支股票的標題
    stockTitle = soup.find('td', width='105').text
    #print(stockTitle)
    stockTitle = stockTitle.replace('加到投資組合'.decode('utf8'),'')
    #print(stockTitle)

    #把欄位撈出來
    title = []
    for t in soup.find_all('th', align='center'):
        #print(t.text)
        title.append(t.text.encode('utf8'))
    #最後一個欄位沒用,刪掉    
    del title[11]
    #print(title)

    #欄位對應的內容撈出來
    content = []
    content.append(stockTitle.encode('utf8'))
    for info in soup.find_all('td', bgcolor='#FFFfff'): 
        #print(info.text[0:6].encode('utf8'))
        #content.append(info.text.replace('\n                ','').replace('成交明細技術　新聞基本　籌碼個股健診'.decode('utf8'),'').encode('utf8'))
        content.append(info.text.strip()[0:6].encode('utf8'))
    
    #print(content)

    dictionary = dict(zip(title,content))
    #print json.dumps(dictionary, ensure_ascii=False)

    resutString = ''
    for key,value in dictionary.iteritems():
        resutString += key + ' ' + value + '\n'
        #print(key,value)

    print(resutString)
    return resutString

if __name__ == "__main__":
    app.run()
