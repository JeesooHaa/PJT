import requests, csv
from pprint import pprint
from datetime import datetime, timedelta
from decouple import config

with open('boxoffice.csv', 'w', newline='', encoding='utf-8') as f:

    fieldnames = ('영화 대표코드', '영화명', '누적관객수')
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()

    movieCd_list = []

    for i in range(50):

        targetDt = datetime(2019, 7, 13) - timedelta(weeks=(i))
        targetDt = targetDt.strftime('%Y%m%d')

        key = config('API_KEY')
        base_url = 'http://www.kobis.or.kr/kobisopenapi/webservice/rest/boxoffice/searchWeeklyBoxOfficeList.json'
        api_url = f'{base_url}?key={key}&targetDt={targetDt}&weekGb=0'

        response = requests.get(api_url)
        datas = response.json()

        datas = datas['boxOfficeResult']['weeklyBoxOfficeList']

        for data in datas:
            data_dict = {
                '영화 대표코드': data['movieCd'], 
                '영화명': data['movieNm'], 
                '누적관객수': data['audiAcc'],
                }
            if data['movieCd'] in movieCd_list:
                continue
            else:   
                writer.writerow(data_dict)    
            movieCd_list.append(data['movieCd'])       
