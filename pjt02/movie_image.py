import requests, csv
import time
from pprint import pprint
from decouple import config

BASE_URL = 'https://openapi.naver.com/v1/search/movie.json'
CLIENT_ID = config('CLIENT_ID')
CLIENT_SECRET = config('CLIENT_SECRET')
HEADER = {
    'X-Naver-Client-Id': CLIENT_ID,
    'X-Naver-Client-Secret': CLIENT_SECRET,
}

with open('movie_naver.csv', 'r', newline='', encoding='utf-8') as f:
    reader = csv.DictReader(f)

    movies_naver_list = []

    for row in reader:
        movies_naver_list.append([row['썸네일 이미지 URL'], row['영화 대표코드']])

for movie in movies_naver_list:

    with open(f'images/{movie[1]}.jpg', 'wb') as f:
        response = requests.get(movie[0])
        f.write(response.content)
