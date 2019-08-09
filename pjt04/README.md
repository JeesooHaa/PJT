# Project 04

## 목차

1. [01_layout.html](https://github.com/JeesooHaa/PJT/blob/master/pjt04#1-01_layouthtml)
2. [02_movie.html](https://github.com/JeesooHaa/PJT/blob/master/pjt04#2-02_moviehtml)
3. [03_detail_view.html](https://github.com/JeesooHaa/PJT/blob/master/pjt04#3-03_detail_viewhtml)



### 1. 01_layout.html

##### 영화 추천 사이트를 위한 레이아웃 구성

```html
  <!-- Navigation Bar -->
  <nav class="navbar navbar-expand-lg navbar-light bg-light fixed-top">
    <a class="navbar-brand" href="#">영화추천시스템</a>
    <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarNav"
      aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
      <span class="navbar-toggler-icon"></span>
    </button>
    <div class="collapse navbar-collapse" id="navbarNav">
      <ul class="navbar-nav ml-auto">
        <li class="nav-item active">
          <a class="nav-link" href="#">Home<span class="sr-only">(current)</span></a>
        </li>
        <li class="nav-item">
          <a class="nav-link disabled" href="#">친구평점보러가기</a>
        </li>
        <li class="nav-item">
          <a class="nav-link disabled" href="#">Login</a>
        </li>
      </ul>
    </div>
  </nav>
  
   <!-- Footer --> 
    <footer class="d-flex justify-content-between bg-light fixed-bottom">
    <a>
      JeesooHaa
    </a>
    <a href="#go_top">
      <i class="fas fa-arrow-alt-circle-up icon-black"></i>
    </a>
  </footer>
```



### 2. 02_movie.html

##### 영화 추천 사이트를 위한 리스트 구성 

```html
<!-- 영화 박스 구성 -->
      <div class="px-0.5">
        <div class="card_box col-xs-12 col-sm-6 col-md-4 col-lg-3">
          <div class="card" style="width: 15rem;">
            <img src="images/20175771.jpg" class="card-img-top" alt="라이온 킹">
            <div class="card-body">
              <h4 class="card-title">라이온 킹,The Lion King</h4>
              <button type="button" class="btn btn-secondary">8.7</button>
              <hr />
              <p class="card-text">모험</p>
              <p class="card-text">개봉일: 2019-07-17</p>
              <a href="https://movie.naver.com/movie/bi/mi/basic.nhn?code=169637" target="_blank"
                class="btn btn-primary">영화정보 보러가기</a>
            </div>
          </div>
        </div>
      </div>
```



### 3. 03_detail_view.html

##### 영화 상세 보기 

```html
<!-- Modal 만들기 -->
  <div class="modal fade" id="modal_20175771" tabindex="-1" role="dialog" aria-labelledby="exampleModalCenterTitle"
    aria-hidden="true">
    <div class="modal-dialog modal-dialog-centered" role="document">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title" id="exampleModalCenterTitle">라이온 킹,The Lion King</h5>
          <button type="button" class="close" data-dismiss="modal" aria-label="Close">
            <span aria-hidden="true">&times;</span>
          </button>
        </div>
        <div id="carouselcontrol_20175771" class="carousel slide" data-ride="carousel">
          <div class="carousel-inner">
            <div class="carousel-item active">
              <img src="images/20175771-01.jpg" class="d-block w-100" alt="...">
            </div>
            <div class="carousel-item">
              <img src="images/20175771-02.jpg" class="d-block w-100" alt="...">
            </div>
            <div class="carousel-item">
              <img src="images/20175771-03.jpg" class="d-block w-100" alt="...">
            </div>
          </div>
          <a class="carousel-control-prev" href="#carouselcontrol_20175771" role="button" data-slide="prev">
            <span class="carousel-control-prev-icon" aria-hidden="true"></span>
            <span class="sr-only">Previous</span>
          </a>
          <a class="carousel-control-next" href="#carouselcontrol_20175771" role="button" data-slide="next">
            <span class="carousel-control-next-icon" aria-hidden="true"></span>
            <span class="sr-only">Next</span>
          </a>
        </div>
        <div class="modal-body">
          "새로운 세상, 너의 시대가 올 것이다!
          어린 사자 ‘심바’는 프라이드 랜드의 왕인 아버지 ‘무파사’를   야심과 욕망이 가득한 삼촌 ‘스카’의 음모로 잃고 왕국에서도 쫓겨난다.      기억해라! 네가 누군지.      아버지의 죽음에
          대한 죄책감에 시달리던 ‘심바’는   의욕 충만한 친구들 ‘품바’와 ‘티몬’의 도움으로 희망을 되찾는다.   어느 날 우연히 옛 친구 ‘날라’를 만난 ‘심바’는 과거를 마주할 용기를
          얻고,   진정한 자신의 모습을 찾아 위대하고도 험난한 도전을 떠나게 되는데…
        </div>
        <div class="modal-footer">
          <button type="button" class="btn btn-secondary" data-dismiss="modal">Close</button>
        </div>
      </div>
    </div>
  </div>
```