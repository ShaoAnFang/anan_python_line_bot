#from linebot.models import TemplateSendMessage
from linebot.models import *
import hashlib 
import requests
from datetime import datetime

def moive(g):
    carousel_template_message = TemplateSendMessage(
    alt_text='電影',
    template=CarouselTemplate(
        columns=[
            CarouselColumn(
                thumbnail_image_url=g[0]['poster_url'],
                title=g[0]['ch_name'],
                text= g[0]['intro'],
                actions=[URITemplateAction(label='查看', uri=g[0]['info_url'])]
            ),
            CarouselColumn(
                thumbnail_image_url=g[1]['poster_url'],
                title=g[1]['ch_name'],
                text= g[1]['intro'],
                actions=[URITemplateAction(label='查看', uri=g[1]['info_url'])]
            ),
            CarouselColumn(
                thumbnail_image_url=g[2]['poster_url'],
                title=g[2]['ch_name'],
                text= g[2]['intro'],
                actions=[URITemplateAction(label='查看', uri=g[2]['info_url'])]
            ),
            CarouselColumn(
                thumbnail_image_url=g[3]['poster_url'],
                title=g[3]['ch_name'],
                text= g[3]['intro'],
                actions=[URITemplateAction(label='查看', uri=g[3]['info_url'])]
            ),
            CarouselColumn(
                thumbnail_image_url=g[4]['poster_url'],
                title=g[4]['ch_name'],
                text= g[4]['intro'],
                actions=[URITemplateAction(label='查看', uri=g[4]['info_url'])]
            )
        ]
        )
    )
    return carousel_template_message

def avgleSearch(avgleResult,titleText='小電影'):
    #asd = avgleResult[4]['title'][:10] + '\n' + avgleResult[4]['preview_url'] +'\n'+ avgleResult[4]['keyword'][:10] +'\n'+ avgleResult[4]['video_url']
    #line_bot_api.reply_message(event.reply_token,TextSendMessage(text=asd))
    carousel_template_message = TemplateSendMessage(
    alt_text=titleText,
    template=CarouselTemplate(
        columns=[
            CarouselColumn(
                thumbnail_image_url=avgleResult[0]['preview_url'],
                title=avgleResult[0]['keyword'][:10],
                text= avgleResult[0]['title'][:10],
                actions=[URITemplateAction(label='查看', uri=avgleResult[0]['video_url'])]
            ),
            CarouselColumn(
                thumbnail_image_url=avgleResult[1]['preview_url'],
                title=avgleResult[1]['keyword'][:10],
                text= avgleResult[1]['title'][:10],
                actions=[URITemplateAction(label='查看', uri=avgleResult[1]['video_url'])]
            ),
            CarouselColumn(
                thumbnail_image_url=avgleResult[2]['preview_url'],
                title=avgleResult[2]['keyword'][:10],
                text= avgleResult[2]['title'][:10],
                actions=[URITemplateAction(label='查看', uri=avgleResult[2]['video_url'])]
            ),
            CarouselColumn(
                thumbnail_image_url=avgleResult[3]['preview_url'],
                title=avgleResult[3]['keyword'][:10],
                text= avgleResult[3]['title'][:10],
                actions=[URITemplateAction(label='查看', uri=avgleResult[3]['video_url'])]
            ),
            CarouselColumn(
                thumbnail_image_url=avgleResult[4]['preview_url'],
                title=avgleResult[4]['keyword'][:10],
                text= avgleResult[4]['title'][:10],
                actions=[URITemplateAction(label='查看', uri=avgleResult[4]['video_url'])]
            )
        ]
        )
    )
    return carousel_template_message

def sportsChannel():
    carousel_template_message = TemplateSendMessage(
    alt_text='體育台',
    template=CarouselTemplate(
        columns=[
            CarouselColumn(
                thumbnail_image_url="https://i.imgur.com/YvY2ttl.jpg",
                title="緯來體育台",
                text ="緯來體育台",
                actions=[URITemplateAction(label='查看', uri="http://60.250.69.26:8080/live/vlpor0714.m3u8")]
            ),
            CarouselColumn(
                thumbnail_image_url="https://i.imgur.com/YvY2ttl.jpg",
                title="緯來日本台",
                text= "緯來日本台",
                actions=[URITemplateAction(label='查看', uri="http://60.250.69.26:8080/live/vxlxjxp0714.m3u8")]
            ),
            CarouselColumn(
                thumbnail_image_url="https://i.imgur.com/YvY2ttl.jpg",
                title="壹電視新聞",
                text= "壹電視新聞",
                actions=[URITemplateAction(label='查看', uri="http://www.bouosu.com/dvr/mt9txb8x/cggmv7m5/index.m3u8")]
            ),
            CarouselColumn(
                thumbnail_image_url="https://i.imgur.com/YvY2ttl.jpg",
                title="愛爾達體育1台",
                text= "愛爾達體育1台",
                actions=[URITemplateAction(label='查看', uri=redir("http://pcb.myds.me/token/MOD/04.m3u8?CH=200"))]
            ),
            CarouselColumn(
                thumbnail_image_url="https://i.imgur.com/YvY2ttl.jpg",
                title="ANIMAX",
                text= "ANIMAX",
                actions=[URITemplateAction(label='查看', uri="http://59.125.101.122:8080/live/anxax0714.m3u8"))]
            )
        ]
        )
    )
    return carousel_template_message

def redir(urlString):
    #print(int(datetime.now().timestamp()))
    nowTimestamp = int(datetime.now().timestamp())
    token = "CA0670498B2C9B1C" + str(nowTimestamp + 5)
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

