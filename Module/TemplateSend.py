#from linebot.models import TemplateSendMessage
from linebot.models import *
import json
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

def chloeBlogParser():
    url = "https://aifun01.com"
    header = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36"}
    res = requests.get(url, headers=header)
    res.encoding = 'utf-8'
    soup = BeautifulSoup(res.text,'html.parser')
    articles = []
    
    for (index, article) in enumerate(soup.select('.thumbnail-link')):
        articleDict = {}
        #print(soup.select('.meta-cat')[index].a.string)
        articleDict['classification'] = soup.select('.meta-cat')[index].a.string
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
                articleDict['title'] = image['alt'][:20]
                articleDict['image'] = 'https://' + urllib.parse.quote(image['src'].split('https://')[1])
        articles.append(articleDict)
    return articles

def chloeStyleOne():
    articles = chloeBlogParser()
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

def chloeStyleTwo():
    articles = chloeBlogParser()
    contentResult = []
    for article in articles[:5]:
        contentDict = {
            "type": "bubble",
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                  {
                    "type": "image",
                    "url": article['image'],
                    "size": "full",
                    "aspectRatio": "1:1",
                    "aspectMode": "cover",
                    "position": "relative"
                  },
                  {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                      {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                          {
                            "type": "text",
                            "text": article['title'],
                            "size": "sm",
                            "color": "#ffffff",
                            "weight": "bold",
                            "margin": "none"
                          }
                        ]
                      }
                    ],
                    "position": "absolute",
                    "offsetBottom": "0px",
                    "offsetStart": "0px",
                    "offsetEnd": "0px",
                    "backgroundColor": "#03303Acc",
                    "paddingAll": "5px",
                    "paddingTop": "5px"
                  }
                ],
                "paddingAll": "0px"
              },
              "footer": {
                "type": "box",
                "layout": "horizontal",
                "contents": [
                  {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                      {
                        "type": "image",
                        "url": "https://i2.wp.com/aifun01.com/wp-content/uploads/2020/05/IMG_8525_meitu_1-e1589029321532.jpg",
                        "aspectMode": "cover",
                        "position": "relative",
                        "size": "xs"
                      }
                    ],
                    "flex": 1,
                    "justifyContent": "center"
                  },
                  {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                      {
                        "type": "text",
                        "text": article['classification'],
                        "align": "start",
                        "flex": 2,
                        "weight": "bold"
                      },
                      {
                        "type": "text",
                        "text": "啾比 Joli",
                        "maxLines": 1
                      }
                    ],
                    "flex": 3
                  }
                ],
                "position": "relative"
              },
              "action": {
                "type": "uri",
                "label": "action",
                "uri": article['url']
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

def smzb():
    host = "https://smzb.cn"
    # https://smzb.cn/api/more/live?live_type_id=2
    url = f'{host}/hot/top'

    liveDataList = []

    res = requests.get(url)
    # print(json.loads(res.text))
    responseJson = json.loads(res.text)
    # print(responseJson['data']['rooms'])
    if len(responseJson['result']) > 0:
        # print(responseJson['data']['rooms']['1']['data'])
        dataList = responseJson['result']
        for data in dataList:
            liveDataDict = {}
            liveDataDict['title'] = data['title']
            liveDataDict['nickname'] = data['nickname']
            liveDataDict['user_icon'] = data['icon']
            liveDataDict['image_url'] = 'https:' + data['image_url']
            liveDataDict['url'] = host + '/room/' + data['room_num']
            # print(liveDataDict['url'])
            liveDataList.append(liveDataDict)
    else:
        # 沒有直播中的
        print("data empty")
    
    contentResult = []
    for liveData in liveDataList:
        contentDict = {
            "type": "bubble",
              "body": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                  {
                    "type": "image",
                    "url": liveData['image_url'],
                    "size": "full",
                    "aspectRatio": "16:9",
                    "gravity": "center",
                    "aspectMode": "cover",
                    "position": "relative"
                  },
                  {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                      {
                        "type": "text",
                        "text": "Live",
                        "color": "#ffffff",
                        "align": "center",
                        "size": "xs",
                        "offsetTop": "3px"
                      }
                    ],
                    "position": "absolute",
                    "cornerRadius": "20px",
                    "offsetTop": "18px",
                    "backgroundColor": "#ff334b",
                    "offsetStart": "18px",
                    "height": "25px",
                    "width": "53px"
                  },
                  {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                      {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                          {
                            "type": "text",
                            "text": liveData['title'],
                            "size": "sm",
                            "color": "#ffffff",
                            "weight": "bold",
                            "margin": "none"
                          }
                        ]
                      }
                    ],
                    "position": "absolute",
                    "offsetBottom": "0px",
                    "offsetStart": "0px",
                    "offsetEnd": "0px",
                    "backgroundColor": "#03303Acc",
                    "paddingAll": "5px",
                    "paddingTop": "5px"
                  }
                ],
                "paddingAll": "0px"
              },
              "footer": {
                "type": "box",
                "layout": "horizontal",
                "contents": [
                  {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                      {
                        "type": "image",
                        "url": liveData['user_icon'],
                        "aspectMode": "cover",
                        "position": "relative",
                        "size": "xs"
                      }
                    ],
                    "flex": 1,
                    "justifyContent": "center"
                  },
                  {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                      {
                        "type": "text",
                        "text": liveData['title'],
                        "align": "start",
                        "flex": 2,
                        "weight": "bold",
                        "maxLines": 1
                      },
                      {
                        "type": "text",
                        "text": liveData['nickname'],
                        "maxLines": 1
                      }
                    ],
                    "flex": 3
                  }
                ],
                "position": "relative"
              },
              "action": {
                "type": "uri",
                "label": "action",
                "uri":  liveData['url']
              }
        }
        contentResult.append(contentDict)
    
    flex_message = FlexSendMessage(
        alt_text='直播中',
        contents={
            "type": "carousel",
            "contents": contentResult
        }
    )
    return flex_message

def nba_data():
    league_board_route_url = "https://smzb.cn/get_League_Board_Json"
    res = requests.get(league_board_route_url)
    # print(res.text)
    json_obj = json.loads(res.text)
    # print('https:' + json_obj['data'])
    league_board_data_url = 'https:' + json_obj['data']
    res = requests.get(league_board_data_url)
    resClean = res.text.replace("gameStatus(", "").replace("})", "}")
    json_obj = json.loads(resClean)
    # print(json_obj['data'])
    nba_group_list = []
    contentResult = []
    for data in json_obj['data']:
        if data['name'] == "NBA":
            # print(data)
            # print(data['group'])
            nba_group_list = data

            for nba_data in nba_group_list['data']:
                teamDataList = []
                # print(nba_data['group'])
                for team in nba_data['rows']:
                    # print(team['team_name'])
                    # print(team['won'])
                    # print(team['loss'])
                    won = int(team['won'])
                    loss = int(team['loss'])
                    total_game = won + loss
                    rate = "0%"
                    if total_game > 0:
                        rateFloat = float('{:.3f}'.format(won / total_game)) * 100
                        rate = f'{ rateFloat }%'.replace(".0", "")
                    teamDict = {
                        "type": "box",
                        "layout": "horizontal",
                        "contents": [
                            {
                                "type": "text",
                                "text": team['team_name'],
                                "size": "sm",
                                "color": "#555555",
                                "flex": 2
                            },
                            {
                                "type": "text",
                                "text": f"{ total_game }",
                                "size": "sm",
                                "color": "#111111",
                                "align": "center",
                                "flex": 1
                            },
                            {
                                "type": "text",
                                "text": f"{won}/{loss}",
                                "size": "sm",
                                "color": "#111111",
                                "flex": 1,
                                "align": "center"
                            },
                            {
                                "type": "text",
                                "text": rate,
                                "flex": 1,
                                "align": "center"
                            }
                        ]}
                    teamDataList.append(teamDict)

                # print(teamDataList)
                print(nba_data['group'])
                contentDict = {
                    "type": "bubble",
                    "body": {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                            {
                                "type": "text",
                                "text": nba_data['group'],
                                "weight": "bold",
                                "size": "lg"
                            },
                            {
                                "type": "separator"
                            },
                            {
                                "type": "box",
                                "layout": "horizontal",
                                "contents": [
                                    {
                                        "type": "text",
                                        "text": "Team",
                                        "size": "sm",
                                        "color": "#555555",
                                        "flex": 2
                                    },
                                    {
                                        "type": "text",
                                        "text": "Total",
                                        "size": "sm",
                                        "color": "#111111",
                                        "align": "center",
                                        "flex": 1
                                    },
                                    {
                                        "type": "text",
                                        "text": "W/L",
                                        "size": "sm",
                                        "color": "#111111",
                                        "flex": 1,
                                        "align": "center"
                                    },
                                    {
                                        "type": "text",
                                        "text": "Rate",
                                        "flex": 1,
                                        "align": "center"
                                    }
                                ],
                                "paddingTop": "3px",
                                "paddingBottom": "3px"
                            },
                            {
                                "type": "separator",
                            },
                            {
                                "type": "box",
                                "layout": "vertical",
                                "contents": teamDataList
                            }
                        ]
                    }
                }
                contentResult.append(contentDict)

    flex_message = FlexSendMessage(
        alt_text='NBA',
        contents={
            "type": "carousel",
            "contents": contentResult
        }
    )
    return flex_message
