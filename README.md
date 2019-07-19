# Project 01

##  목차

1. [API](#1.-API)

2. [01.py](#2.-01.py)

3. [boxoffice.csv](#3.-boxoffice.csv)

4. [02.py](#4.-02.py)

5. [movie.csv](#5.-movie.csv)

6. [03.py](#6.-03.py)

7. [director.csv](#7.-director.csv)

   

### 1. API

[영화진흥위원회 오픈API](http://www.kobis.or.kr/kobisopenapi/homepg/main/main.do)

영화진흥위원회에서 지원하는 '주간/주말 박스오피스', '영화 상세정보', '영화인목록' API 사용.



###  2. 01.py

##### '주간/주말 박스오피스'API 에서 박스오피스 정보 수집, boxoffice.csv 생성

* boxoffice.csv 의 머리말 만들기
```python
with open('boxoffice.csv', 'w', newline='', encoding='utf-8') as f:

    fieldnames = ('영화 대표코드', '영화명', '누적관객수')
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
```

* 50주간 박스오피스 기록 수집 
```python
    for i in range(50):

        targetDt = datetime(2019, 7, 13) - timedelta(weeks=(i))
        targetDt = targetDt.strftime('%Y%m%d')

        key = config('API_KEY')
        base_url = 'http://www.kobis.or.kr/kobisopenapi/webservice/rest/boxoffice/searchWeeklyBoxOfficeList.json'
        api_url = f'{base_url}?key={key}&targetDt={targetDt}&weekGb=0'

        response = requests.get(api_url)
        datas = response.json()
```

* 영화가 중복되지 않게 'movieCd' 를 확인하면서 boxoffice.csv 작성 
* writer.writerow 안에 ditctionray 형식이 들어가야 하므로 data_dict 를 미리 생성
```python
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
```



###  3. boxoffice.csv

#####  기준일 역순으로 '영화 대표코드', ' 영화명', '누적관객수' 기록

```python
영화 대표코드,영화명,누적관객수
20196309,스파이더맨: 파 프롬 홈,6685160
20183867,알라딘,10161238
20184047,토이 스토리 4,3151062
20185353,기방도령,220182
20183782,기생충,9919835
20185986,진범,106756
```



###  4. 02.py

##### boxoffice.csv 의 '영화 대표코드'와 '영화 상세정보'API를 이용해 수집한 영화의 상세정보 작성

* boxoffice.cvs 에서 '영화 대표코드' 받기 
```python
with open('boxoffice.csv', 'r', newline='', encoding='utf-8') as f:
    reader = csv.DictReader(f)

    movieCd_list = []

    for row in reader:
        movieCd_list.append(row['영화 대표코드'])
```

* '장르'는 복수의 장르가 존재하는 경우가 있어 list 처리 
* '관람등급'과 '감독명'이 없는 경우에 공란 처리 
```python
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
```



### 5. movie.csv

##### '영화 대표코드', '영화명(국문)', '영화명(영문)', '영화명(원문)', '관람등급', '개봉연도', '상영시간', '장르', '감독명' 기록

```python
영화 대표코드,영화명(국문),영화명(영문),영화명(원문),관람등급,개봉연도,상영시간,장르,감독명
20196309,스파이더맨: 파 프롬 홈,Spider-Man: Far From Home,,12세이상관람가,20190702,129,"['액션', '어드벤처', '코미디', 'SF']",존 왓츠
20183867,알라딘,Aladdin,,전체관람가,20190523,127,"['어드벤처', '가족', '판타지']",가이 리치
20184047,토이 스토리 4,Toy Story 4,,전체관람가,20190620,99,"['애니메이션', '어드벤처', '코미디']",조시 쿨리
20185353,기방도령,HOMME FATALE,,15세이상관람가,20190710,110,"['코미디', '사극']",남대중
20183782,기생충,PARASITE,,15세이상관람가,20190530,131,['드라마'],봉준호
20185986,진범,The Culprit,,15세이상관람가,20190710,100,['스릴러'],고정욱
```



### 6. 03.py

##### movies.csv 의 '감독명', '영화명(국문)'과 '영화인정보'API를 이용해 수집한 영화의 상세정보 작성

* 감독명은 중복되거나 단어가 포함된 경우 여러 리스트가 나오는 경우 발생 ex :) 봉준
* 이를 해결하기 위해 영화명을 감독의 필모그래피에서 확인
* 분야가 감독이 아닌 경우는 제외함

```python
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
```



### 7. director.csv

##### '영화인 코드', '영화인명', '분야', '필모리스트' 기록

```python
영화인 코드,영화인명,분야,필모리스트
10038689,존 왓츠,감독,스파이더맨: 파 프롬 홈|스파이더맨: 홈 커밍|캅카
10000296,가이 리치,감독,알라딘|킹 아서: 제왕의 검|맨 프롬 UNCLE|셜록홈즈 : 그림자 게임|셜록 홈즈|락큰롤라|리볼버|스웹트 어웨이|스내치|록 스탁 앤 2 스모킹 배럴즈
10023314,조시 쿨리,감독,토이 스토리 4
20209287,남대중,감독,기방도령|위대한 소원
10031641,봉준호,감독,"기생충|옥자|해무(海霧)|설국열차|토니 레인즈의 한국영화 25년|마더|감독들, 김기영을 말하다|괴물|남극일기|살인의 추억|이공|피도 눈물도 없이|플란다스의 개|유령|모텔 선인장|인플루엔자|싱크 & 라이즈|백색인|지리멸렬|프레임 속의 기억들|인디포럼2014 필름1|도쿄!"
10090941,히라야마 미호,감독,극장판 엉덩이 탐정: 화려한 사건 수첩
```

