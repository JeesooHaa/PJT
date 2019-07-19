import requests, csv
from pprint import pprint
from datetime import datetime, timedelta
from decouple import config

with open('movie.csv', 'r', newline='', encoding='utf-8') as f:
    reader = csv.DictReader(f)

    directors_list = []

    for row in reader:
        directors_list.append([row['감독명'], row['영화명(국문)']])


with open('director.csv', 'w', newline='', encoding='utf-8') as f:

    fieldnames = ('영화인 코드', '영화인명', '분야', '필모리스트')
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()

    key = config('API_KEY')
    base_url = 'http://www.kobis.or.kr/kobisopenapi/webservice/rest/people/searchPeopleList.json'

    peopleCd_list = []

    for director in directors_list: 

        api_url = f'{base_url}?key={key}&peopleNm={director[0]}' 

        response = requests.get(api_url)
        director_datas = response.json()

        director_datas = director_datas['peopleListResult']['peopleList']

        for i in range(len(director_datas)):
            director_1 = director[1]
            director_2 = director_datas[i]['filmoNames']
            if (director_1 in director_2):   
                director_data_dict = {
                    '영화인 코드': director_datas[i]['peopleCd'], 
                    '영화인명': director_datas[i]['peopleNm'], 
                    '분야': director_datas[i]['repRoleNm'],
                    '필모리스트': director_datas[i]['filmoNames'],  
                    }
                if director_datas[i]['peopleCd'] in peopleCd_list:
                    continue
                elif director_datas[i]['repRoleNm'] == '감독':   
                    writer.writerow(director_data_dict)    
                peopleCd_list.append(director_datas[i]['peopleCd'])   
