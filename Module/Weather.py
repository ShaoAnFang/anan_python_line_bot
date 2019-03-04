import requests
from bs4 import BeautifulSoup

#@app.route('/weather', methods=['GET'])
def weather(ChooseCity):
    cityDict = dict()
    cityDict = {'台北': 'Taipei_City', '新北': 'New_Taipei_City', '桃園': 'Taoyuan_City',
            '台中': 'Taichung_City', '台南': 'Tainan_City', '高雄': 'Kaohsiung_City',
            '基隆': 'Keelung_City', '新竹市': 'Hsinchu_City', '新竹縣': 'Hsinchu_County',
            '苗栗': 'Miaoli_County', '彰化': 'Changhua_County', '南投': 'Nantou_County',
            '雲林': 'Yunlin_County', '嘉義市': 'Chiayi_City', '嘉義縣': 'Chiayi_County',
            '屏東': 'Pingtung_County', '宜蘭': 'Yilan_County', '花蓮': 'Hualien_County',
            '台東': 'Taitung_County', '澎湖': 'Penghu_County','金門': 'Kinmen_County','連江': 'Lienchiang_County'}

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

    return resultString