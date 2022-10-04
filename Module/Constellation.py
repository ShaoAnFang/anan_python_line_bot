import requests
from bs4 import BeautifulSoup

#@app.route('/star/<string:star>', methods=['GET'])
def constellation(star):
#     constellationDict = dict()
#     constellationDict = {'牡羊': 'Aries', '金牛': 'Taurus', '雙子': 'Gemini','巨蟹': 'Cancer',
#                             '獅子': 'Leo', '處女': 'Virgo', '天秤': 'Libra','天蠍': 'Scorpio', 
#                             '射手': 'Sagittarius', '魔羯': 'Capricorn', '摩羯':'Capricorn','水瓶': 'Aquarius', '雙魚': 'Pisces'}

#     url = 'http://www.daily-zodiac.com/mobile/zodiac/{}'.format(constellationDict[star])
#     res = requests.get(url,verify=False)
#     res.encoding = 'utf-8'
#     soup = BeautifulSoup(res.text,'html.parser')
#     #print(soup)
#     name = soup.find_all('p')
#     #print(name)
#     starAndDate = []
#     for n in name:
#         #print n.text.encode('utf8')
#         starAndDate.append(n.text)
#         #print(starAndDate)
#     today = soup.select('.today')[0].text.strip('\n')
#     today = today.split('\n\n')[0]
#     #print today
#     title = soup.find('li').text.strip()
#     #print(title)
#     content = soup.find('article').text.strip()
#     #print content

#     resultString = ''
#     resultString += starAndDate[0] + ' ' + starAndDate[1] + '\n'
#     resultString += today + '\n'
#     resultString += content + '\n\n'
#     resultString += 'from 唐立淇每日星座運勢' + '\n\n'
    resultString += '-以下內容來自小歐星座網站-' + '\n'

    urlOrz= 'https://horoscope.dice4rich.com/?sign={}'.format(constellationDict[star])
    urlOrz = urlOrz.lower()
    res = requests.get(urlOrz)
    soup = BeautifulSoup(res.text,'html.parser')

    title = soup.select('.current .title')
    content = soup.select('.current .content')
    for i in range(len(title)+len(content)):
        if i%2 == 0:
            print(title[int(i/2)].text.strip())
            resultString += title[int(i/2)].text.strip() + '\n'
        else:
            print(content[int(i/2)].text)
            resultString += content[int(i/2)].text + '\n\n'

    return resultString
