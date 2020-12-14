#from linebot.models import TemplateSendMessage
from linebot.models import *
import urllib
import hashlib 
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from firebase import firebase

firebase = firebase.FirebaseApplication('https://python-f5763.firebaseio.com/',None)

# def moive(g):
#     carousel_template_message = TemplateSendMessage(
#     alt_text='電影',
#     template=CarouselTemplate(
#         columns=[
#             CarouselColumn(
#                 thumbnail_image_url=g[0]['poster_url'],
#                 title=g[0]['ch_name'],
#                 text= g[0]['intro'],
#                 actions=[URITemplateAction(label='查看', uri=g[0]['info_url'])]
#             ),
#             CarouselColumn(
#                 thumbnail_image_url=g[1]['poster_url'],
#                 title=g[1]['ch_name'],
#                 text= g[1]['intro'],
#                 actions=[URITemplateAction(label='查看', uri=g[1]['info_url'])]
#             ),
#             CarouselColumn(
#                 thumbnail_image_url=g[2]['poster_url'],
#                 title=g[2]['ch_name'],
#                 text= g[2]['intro'],
#                 actions=[URITemplateAction(label='查看', uri=g[2]['info_url'])]
#             ),
#             CarouselColumn(
#                 thumbnail_image_url=g[3]['poster_url'],
#                 title=g[3]['ch_name'],
#                 text= g[3]['intro'],
#                 actions=[URITemplateAction(label='查看', uri=g[3]['info_url'])]
#             ),
#             CarouselColumn(
#                 thumbnail_image_url=g[4]['poster_url'],
#                 title=g[4]['ch_name'],
#                 text= g[4]['intro'],
#                 actions=[URITemplateAction(label='查看', uri=g[4]['info_url'])]
#             )
#         ]
#         )
#     )
#     return carousel_template_message

def moive(datas):
    contentResult = []
    for data in datas:
        contentDict = {
            "type": "bubble",
              "hero": {
                "type": "image",
                "size": "full",
                "aspectMode": "cover",
                "url": data['poster_url']
              },
              "body": {
                "type": "box",
                "layout": "vertical",
                "spacing": "sm",
                "contents": [
                  {
                    "type": "text",
                    "text": data['intro'],
                    "wrap": True,
                    "weight": "bold",
                    "size": "xl"
                  }
                ]
              },
              "footer": {
                "type": "box",
                "layout": "vertical",
                "spacing": "sm",
                "contents": [
                  {
                    "type": "button",
                    "style": "primary",
                    "action": {
                      "type": "uri",
                      "label": "查看",
                      "uri": data['info_url']
                    }
                  }
                ]
              }
        }
        contentResult.append(contentDict)
    flex_message = FlexSendMessage(
        alt_text='FlexMessage',
        contents={
            "type": "carousel",
            "contents": contentResult
        }
    )
    return flex_message

def avgleSearch(avgleResult,titleText='小電影'):
    #asd = avgleResult[4]['title'][:10] + '\n' + avgleResult[4]['preview_url'] +'\n'+ avgleResult[4]['keyword'][:10] +'\n'+ avgleResult[4]['video_url']
    #line_bot_api.reply_message(event.reply_token,TextSendMessage(text=asd))
    carousel_template_message = TemplateSendMessage(
    alt_text=titleText,
    template=CarouselTemplate(
        columns=[
            CarouselColumn(
                thumbnail_image_url=avgleResult[0]['preview_url'],
                #thumbnail_image_url="https://i.imgur.com/YvY2ttl.jpg",
                title=avgleResult[0]['keyword'][:10],
                text= avgleResult[0]['title'][:10],
                actions=[URITemplateAction(label='查看', uri=avgleResult[0]['video_url'])]
            ),
            CarouselColumn(
                thumbnail_image_url=avgleResult[1]['preview_url'],
                #thumbnail_image_url="https://i.imgur.com/YvY2ttl.jpg",
                title=avgleResult[1]['keyword'][:10],
                text= avgleResult[1]['title'][:10],
                actions=[URITemplateAction(label='查看', uri=avgleResult[1]['video_url'])]
            ),
            CarouselColumn(
                thumbnail_image_url=avgleResult[2]['preview_url'],
                #thumbnail_image_url="https://i.imgur.com/YvY2ttl.jpg",
                title=avgleResult[2]['keyword'][:10],
                text= avgleResult[2]['title'][:10],
                actions=[URITemplateAction(label='查看', uri=avgleResult[2]['video_url'])]
            ),
            CarouselColumn(
                thumbnail_image_url=avgleResult[3]['preview_url'],
                #thumbnail_image_url="https://i.imgur.com/YvY2ttl.jpg",
                title=avgleResult[3]['keyword'][:10],
                text= avgleResult[3]['title'][:10],
                actions=[URITemplateAction(label='查看', uri=avgleResult[3]['video_url'])]
            ),
            CarouselColumn(
                thumbnail_image_url=avgleResult[4]['preview_url'],
                #thumbnail_image_url="https://i.imgur.com/YvY2ttl.jpg",
                title=avgleResult[4]['keyword'][:10],
                text= avgleResult[4]['title'][:10],
                actions=[URITemplateAction(label='查看', uri=avgleResult[4]['video_url'])]
            )
        ]
        )
    )
    return carousel_template_message

def sportsChannel():
    channelList = firebase.get('/TVChannel','channelList')

    carousel_template_message = TemplateSendMessage(
    alt_text='TV Channel',
    template=CarouselTemplate(
        columns=[
            CarouselColumn(
                thumbnail_image_url="https://i.imgur.com/YvY2ttl.jpg",
                title=channelList[0]["name"],
                text =channelList[0]["name"],
                #actions=[URITemplateAction(label='查看', uri=channelList[0]["url"])]
                actions=[URITemplateAction(label='查看', uri="https://google.com")]
            ),
            CarouselColumn(
                thumbnail_image_url="https://i.imgur.com/YvY2ttl.jpg",
                title=channelList[1]["name"],
                text= channelList[1]["name"],
                #actions=[URITemplateAction(label='查看', uri=channelList[1]["url"])]
                actions=[URITemplateAction(label='查看', uri="https://google.com")]
            ),
            CarouselColumn(
                thumbnail_image_url="https://i.imgur.com/YvY2ttl.jpg",
                title=channelList[2]["name"],
                text= channelList[2]["name"],
                #actions=[URITemplateAction(label='查看', uri=channelList[2]["url"])]
                actions=[URITemplateAction(label='查看', uri="https://google.com")]
            ),
            CarouselColumn(
                thumbnail_image_url="https://i.imgur.com/YvY2ttl.jpg",
                title=channelList[3]["name"],
                text= channelList[3]["name"],
                #actions=[URITemplateAction(label='查看', uri=redir(channelList[3]["url"]))]
                actions=[URITemplateAction(label='查看', uri="https://google.com")]
            ),
            CarouselColumn(
                thumbnail_image_url="https://i.imgur.com/YvY2ttl.jpg",
                title=channelList[4]["name"],
                text= channelList[4]["name"],
                #actions=[URITemplateAction(label='查看', uri=channelList[4]["url"])]
                actions=[URITemplateAction(label='查看', uri="https://google.com")]
            )
        ]
        )
    )
    return carousel_template_message

def redir(urlString):
    #print(int(datetime.now().timestamp()))
    md = firebase.get('/TVChannel',"md")
    nowTimestamp = int(datetime.now().timestamp())
    token = md + str(nowTimestamp + 5)
    result = hashlib.md5(token.encode())
    tokenMD5 = result.hexdigest()
    tokenString = "&st={}&token={}".format(str(nowTimestamp), tokenMD5)
    urlString = urlString + tokenString
    #print(urlString)
    r = requests.get(urlString)
    #print(r.url)
    return r.url

def aime(albumResult,textTitle):
    carousel_template_message = TemplateSendMessage(
    alt_text=textTitle,
    template=CarouselTemplate(
        columns=[
            CarouselColumn(
                thumbnail_image_url=albumResult[0]['imageLink'],
                title=albumResult[0]['title&price'],
                text= ' ',
                actions=[URITemplateAction(label='查看', uri=albumResult[0]['shopeeLink'])]
            ),
            CarouselColumn(
                thumbnail_image_url=albumResult[1]['imageLink'],
                title=albumResult[1]['title&price'],
                text= ' ',
                actions=[URITemplateAction(label='查看', uri=albumResult[1]['shopeeLink'])]
            ),
            CarouselColumn(
                thumbnail_image_url=albumResult[2]['imageLink'],
                title=albumResult[2]['title&price'],
                text= ' ',
                actions=[URITemplateAction(label='查看', uri=albumResult[2]['shopeeLink'])]
            ),
            CarouselColumn(
                thumbnail_image_url=albumResult[3]['imageLink'],
                title=albumResult[3]['title&price'],
                text= ' ',
                actions=[URITemplateAction(label='查看', uri=albumResult[3]['shopeeLink'])]
            ),
            CarouselColumn(
                thumbnail_image_url=albumResult[4]['imageLink'],
                title=albumResult[4]['title&price'],
                text= ' ',
                actions=[URITemplateAction(label='查看', uri=albumResult[4]['shopeeLink'])]
            )
        ]
        )
    )
    return carousel_template_message

def chloeBlog():
    url = "https://aifun01.com"
    header = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36"}
    res = requests.get(url, headers=header)
    res.encoding = 'utf-8'
    soup = BeautifulSoup(res.text,'html.parser')
    articles = []
    
    for (index, article) in enumerate(soup.select('.thumbnail-link')):
        articleDict = {}
        #print(type(article))
        #print(article.get('href'))
        articleDict['url'] = article.get('href')
        #print(type(article.findAll('img')))
        for image in article.findAll('img'):
            if image['src'].find('data:image') == -1:
                #print(type(image['src']))
                #print(image['src'])
                #print(image['src'].split('?')[0])
                #print(image['alt'])
                #print( urllib.parse.quote(image['src'].split('https://')[1]))
                articleDict['title'] = image['alt'][:18]
                articleDict['image'] = 'https://' + urllib.parse.quote(image['src'].split('https://')[1])
    articles.append(articleDict)
        articles.append(articleDict)
        
    contentResult = []
    for article in articles[:5]:
        contentDict = {
            "type": "bubble",
              "hero": {
                "type": "image",
                "size": "full",
                "aspectMode": "cover",
                "url": article['image']
              },
              "body": {
                "type": "box",
                "layout": "vertical",
                "spacing": "sm",
                "contents": [
                  {
                    "type": "text",
                    "text": article['title'],
                    "wrap": True,
                    "weight": "bold",
                    "size": "xl"
                  }
                ]
              },
              "footer": {
                "type": "box",
                "layout": "vertical",
                "spacing": "sm",
                "contents": [
                  {
                    "type": "button",
                    "style": "primary",
                    "action": {
                      "type": "uri",
                      "label": "查看",
                      "uri": article['url']
                    }
                  }
                ]
              }
        }
        contentResult.append(contentDict)
    flex_message = FlexSendMessage(
        alt_text='FlexMessage',
        contents={
            "type": "carousel",
            "contents": contentResult
        }
    )
    return flex_message
