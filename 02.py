import requests, csv
from pprint import pprint
from datetime import datetime, timedelta
from decouple import config

with open('boxoffice.csv', 'r', newline='', encoding='utf-8') as f:
    reader = csv.DictReader(f)

    movieCd_list = []

    for row in reader:
        movieCd_list.append(row['영화 대표코드'])

with open('movie.csv', 'w', newline='', encoding='utf-8') as f:

    fieldnames = ('영화 대표코드', '영화명(국문)', '영화명(영문)', '영화명(원문)', '관람등급', '개봉연도', '상영시간', '장르', '감독명')
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()

    key = config('API_KEY')
    base_url = 'http://www.kobis.or.kr/kobisopenapi/webservice/rest/movie/searchMovieInfo.json'

    for movieCd in movieCd_list:  

        api_url = f'{base_url}?key={key}&movieCd={movieCd}' 

        response = requests.get(api_url)
        movie_datas = response.json()

        movie_datas = movie_datas['movieInfoResult']['movieInfo']

        movie_data_genre = []
        for data in movie_datas['genres']:
            movie_data_genre.append(data['genreNm'])

        movie_audits = 'a'
        if movie_datas['audits'] == []:
            movie_audits = ''
        else:
            movie_audits = movie_datas['audits'][0]['watchGradeNm']

        movie_directors = 'a'
        if movie_datas['directors'] == []:
            movie_directors = ''
        else: 
            movie_directors = movie_datas['directors'][0]['peopleNm']

        movie_data_dict = {
            '영화 대표코드': movie_datas['movieCd'],
            '영화명(국문)': movie_datas['movieNm'],
            '영화명(영문)': movie_datas['movieNmEn'],
            '영화명(원문)': movie_datas['movieNmOg'],
            '관람등급': movie_audits,
            '개봉연도': movie_datas['openDt'],
            '상영시간': movie_datas['showTm'],
            '장르': movie_data_genre,
            '감독명': movie_directors,
        }

        writer.writerow(movie_data_dict)
  