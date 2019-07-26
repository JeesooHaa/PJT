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
}  # header : 요청에 대한 정보가 담긴다

with open('movie.csv', 'r', newline='', encoding='utf-8') as f:
    reader = csv.DictReader(f)

    movies_list = []

    for row in reader:
        movies_list.append([row['영화 대표코드'], row['영화명(국문)'], row['감독명']])

with open('movie_naver.csv', 'w', newline='', encoding='utf-8') as f:

    fieldnames = ('영화 대표코드', '하이퍼텍스트 link', '썸네일 이미지 URL', '유저평점')
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()         

    for movie in movies_list:
        query = movie[1]
        API_URL = f'{BASE_URL}?query={query}'
        response = requests.get(API_URL, headers=HEADER).json()

        time.sleep(0.1)

        movie_director = response['items']

        if len(movie_director) == 1:
            movie_naver_dict = {
                '영화 대표코드': movie[0],
                '하이퍼텍스트 link': movie_director[0]['link'],
                '썸네일 이미지 URL': movie_director[0]['image'],
                '유저평점': movie_director[0]['userRating'],
                }
            writer.writerow(movie_naver_dict)
        else:
            for i in range(len(movie_director)):
                director_1 = movie[2][:2]
                director_2 = movie[2][-1:]
                list_str = movie_director[i]['director'].split('|')
                for j in list_str:
                    if director_1 == j[:2] and director_2 == j[-1:]:
                        movie_naver_dict = {
                            '영화 대표코드': movie[0],
                            '하이퍼텍스트 link': movie_director[i]['link'],
                            '썸네일 이미지 URL': movie_director[i]['image'],
                            '유저평점': movie_director[i]['userRating'],
                            }
                        writer.writerow(movie_naver_dict)      
