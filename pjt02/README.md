# Project 02

## 목차

1. API
2. movie_naver.py
3. movie_naver.csv
4. movie_image.py
5. images



### 1. API

[네이버 개발자 센터 오픈API](https://developers.naver.com/main/)

네이버 개발자 센터에서 지원하는 서비스API 중 영화검색 API 사용.



### 2. movie_naver.py

##### movie.csv 의 영화명으로 검색해서 하이퍼텍스트 link, 영화 썸네일 이미지 URL, 유저 평점 수집

* Naver API에서 json 정보 받기
* header를 만들어야 한다.

```python
BASE_URL = 'https://openapi.naver.com/v1/search/movie.json'
CLIENT_ID = config('CLIENT_ID')
CLIENT_SECRET = config('CLIENT_SECRET')
HEADER = {
    'X-Naver-Client-Id': CLIENT_ID,
    'X-Naver-Client-Secret': CLIENT_SECRET,
}
API_URL = f'{BASE_URL}?query={query}'
response = requests.get(API_URL, headers=HEADER).json()
```

* movie.csv 에서 필요한 정보 받기
* 영화 대표코드, 영화명(국문), 감독명을 받는다.

```python
with open('movie.csv', 'r', newline='', encoding='utf-8') as f:
    reader = csv.DictReader(f)

    movies_list = []

    for row in reader:
        movies_list.append([row['영화 대표코드'], row['영화명(국문)'], row['감독명']])
```

##### movie_practice.csv 작성 과정

* 검색 결과가 하나인 경우 바로 작성

```python
        movie_director = response['items']

        if len(movie_director) == 1:
            movie_naver_dict = {
                '영화 대표코드': movie[0],
                '하이퍼텍스트 link': movie_director[0]['link'],
                '썸네일 이미지 URL': movie_director[0]['image'],
                '유저평점': movie_director[0]['userRating'],
                }
            writer.writerow(movie_naver_dict)
```

* 검색 결과가 여러개인 경우 movie.csv 의 감독명과 검색 리스트의 감독명이 movie.csv 감독명의 글자수 - 1 보다 많이 같을 경우 작성 
* 영화진흥위원회와 네이버의 외국인 감독 표기가 다른 경우가 발생하기 때문에 이와 같이 처리함

```python
        else:
            for i in range(len(movie_director)):
                director = movie[2]
                list_str = movie_director[i]['director'].split('|')
                for j in list_str:
                    count = 0
                    if abs(len(director)-len(j)) <= 1:
                        for m in director:
                            for n in j:                                
                                if m == n:
                                    count += 1
                    if (len(director)-count) <= 1:
                        movie_naver_dict = {
                            '영화 대표코드': movie[0],
                            '하이퍼텍스트 link': movie_director[i]['link'],
                            '썸네일 이미지 URL': movie_director[i]['image'],
                            '유저평점': movie_director[i]['userRating'],
                            }
                        writer.writerow(movie_naver_dict) 
```



### 3. movie_naver.csv

##### '영화 대표코드', '하이퍼텍스트 link', '썸네일 이미지 URL',  '유저평점' 을 기록

```python
영화 대표코드,하이퍼텍스트 link,썸네일 이미지 URL,유저평점
20196309,https://movie.naver.com/movie/bi/mi/basic.nhn?code=173123,https://ssl.pstatic.net/imgmovie/mdi/mit110/1731/173123_P06_135928.jpg,8.37
20183867,https://movie.naver.com/movie/bi/mi/basic.nhn?code=163788,https://ssl.pstatic.net/imgmovie/mdi/mit110/1637/163788_P18_105943.jpg,9.43
20184047,https://movie.naver.com/movie/bi/mi/basic.nhn?code=101966,https://ssl.pstatic.net/imgmovie/mdi/mit110/1019/101966_P09_114632.jpg,9.09
20185353,https://movie.naver.com/movie/bi/mi/basic.nhn?code=180209,https://ssl.pstatic.net/imgmovie/mdi/mit110/1802/180209_P42_134851.jpg,5.90
20183782,https://movie.naver.com/movie/bi/mi/basic.nhn?code=161967,https://ssl.pstatic.net/imgmovie/mdi/mit110/1619/161967_P80_151640.jpg,8.50
```



### 4. movie_image.py

##### movie_naver.csv 의 '썸네일 이미지 URL' 을 이용해 영화 포스터 이미지 수집

* '영화 대표코드'.jpg 로 images 폴더에 저장

```python
for movie in movies_naver_list:

    with open(f'images/{movie[1]}.jpg', 'wb') as f:
        response = requests.get(movie[0])
        f.write(response.content)
```



### 5. images

##### '영화 대표코드'.jpg 저장

* '이웃집 토토로' 는 포스터가 없습니다...
![poster](./img/poster.png)
