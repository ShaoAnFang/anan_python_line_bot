import random
import requests
from bs4 import BeautifulSoup
from imgurpython import ImgurClient

def aime(key):
    client_id = 'c3e767d450a401e'
    client_secret = 'cdf5fb70e82bc00e65c0d1d1a4eed318ae82024c'
    client = ImgurClient(client_id,client_secret)

    if key == 'Aime' or key == 'aime': 
        album = ['hLZwL','Qt8En']
        i = random.randint(0, len(album) - 1)
        images = client.get_album_images(album[i])
        index = random.sample(range(0, len(images)),5)
    else:
        album = 'hoBxs'
        #i = random.randint(0, len(album) - 1)
        images = client.get_album_images(album)
        index = random.sample(range(0, len(images)),5) 
        
    imgurResult = []
    for i in index:
        imageDict = dict()
        #imageDict['imageLink'] = images[i].link.replace('http', 'https')
        imageDict['imageLink'] = images[i].link
        description = images[i].description.split('http')[0].strip('\n')
        imageDict['title&price'] = description 
        #imageDict['title'] = description.split('$')[0].strip()
        #imageDict['price'] = '$'+ description.split('$')[1].strip()
        imageDict['shopeeLink'] = images[i].description.split('$')[1][3:].strip()
        imgurResult.append(imageDict)
    
    return imgurResult