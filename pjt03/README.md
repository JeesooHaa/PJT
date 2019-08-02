# Project 03

## 목차

1. [header 고정](https://github.com/JeesooHaa/PJT/blob/master/pjt03#1-header-고정)
2. [navigation 설정](https://github.com/JeesooHaa/PJT/blob/master/pjt03#2-navigation-설정)
3. [title section 설정](https://github.com/JeesooHaa/PJT/blob/master/pjt03#3-title-section-설정)
4. [aside 설정](https://github.com/JeesooHaa/PJT/blob/master/pjt03#4-aside-설정)
5. [footer 설정](https://github.com/JeesooHaa/PJT/blob/master/pjt03#5-footer-설정)



### 1. header 고정

##### header 를 상단에 고정시키며 다른 영역보다 우선하여 볼 수 있도록 함

```html
  position: sticky;
  top: 0;
  z-index: 1000;
```



### 2. navigation 설정

##### navigation 을 오른쪽 위에 한 줄로 고정

```html
  /* navigation 항목을 한 줄로 만들기 */
  display: inline-block;

  /* 좌우 여백 지정 */
  margin: 0 5px;

  /* li 태그의 bullet point를 제거 */
  list-style: none;

.nav-items > li > a:hover {
  /* 마우스 오버시 색 변경 */
  color: rgb(202, 165, 0);

  /* 마우스 오버시 밑줄 제거 */
  text-decoration: none;
}
```



### 3. title section 설정

##### 배경 이미지 적용 및 텍스트 위치 수정

```html
#section-title {
  /* 배경 이미지 적용 */
  height: 320px;
  background-image: url('images/background.jpg');
  background-size: cover;
  background-position: center;

  /* 텍스트를 가운데 정렬 */
  text-align: center;

  /* 텍스트를 수직 가운데 정렬 */
  line-height: 300px;
}

.section-title-heading {
  /* font size 조정 */
  font-size: 3rem;
}
```



### 4. aside 설정

##### aside 를 부모 영역에 위치시킴

```html
  width: 160px;
  padding: 24px;
  position: absolute;
  /* 상단에 위치시킴 */
  top: 0;
```



### 5. footer 설정

##### footer 를 바닥에 고정시키고 텍스트 위치를 수정

```html
  position: sticky;
  bottom: 0;

  text-align: center;
  line-height: 40px;
```