import re
import requests
from bs4 import BeautifulSoup


def get_movie_id(url):
    # e.g. "https://tw.rd.yahoo.com/referurl/movie/thisweek/info/*https://tw.movies.yahoo.com/movieinfo_main.html/id=6707"
    #      -> match.group(0): "/id=6707"
    pattern = '/id=\d+'
    match = re.search(pattern, url)
    if match is None:
        return url
    else:
        return match.group(0).replace('/id=', '')


def get_movies():
    Y_MOVIE_URL = 'https://tw.movies.yahoo.com/movie_thisweek.html'
    dom = requests.get(Y_MOVIE_URL)
    soup = BeautifulSoup(dom.text, 'html.parser')
    movies = []
    rows = soup.select('.release_list li')
    #rows = soup.select('#content_l li')
    Y_INTRO_URL = 'https://tw.movies.yahoo.com/movieinfo_main.html'  # 詳細資訊
    for row in rows:
        movie = dict()
        movie['ch_name'] = row.select('.release_movie_name .gabtn')[0].text.strip()
        movie['eng_name'] = row.select('.en .gabtn')[0].text.strip()
        #movie['movie_id'] = get_movie_id(row.select('.release_movie_name .gabtn')[0]['href'])
        movie['poster_url'] = row.select('img')[0]['data-src']
        #movie['release_date'] = get_date(row.select('.release_movie_time')[0].text)
        movie['intro'] = row.select('.release_text')[0].text.strip().replace(u'...詳全文', '').replace('\n', '')[0:25] + '...'
        #movie['info_url'] = row.select('.release_movie_name .gabtn')[0]['href']
        #movie['info_url'] = Y_INTRO_URL + '/id=' + get_movie_id(row.select('.release_movie_name .gabtn')[0]['href'])
        movie['info_url'] = get_movie_id(row.select('.release_movie_name .gabtn')[0]['href'])
        movies.append(movie)

    return movies
