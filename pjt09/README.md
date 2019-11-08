# Project 09

## 목차

1. [App.vue](https://github.com/JeesooHaa/PJT/blob/master/pjt09#1-Appvue)
2. [MovieList.vue](https://github.com/JeesooHaa/PJT/blob/master/pjt09#2-MovieListvue)
3. [MovieListItem.vue, MovieListItemModal.vue](https://github.com/JeesooHaa/PJT/blob/master/pjt09#3-MovieListItemvue-MovieListItemModalvue)



### 1. App.vue

##### - API 에서 영화 정보와 장르 정보를 받는다. 
##### - `MovieList` component 를 불러오고, `props` 에 영화 정보와 장르 정보를 보낸다. 

##### - (하위 항목에서도 같은 동작을 구현하지만 큰 차이가 없으므로 하위 항목에서는 설명을 생략한다.)

```vue
<!-- App.vue -->

<template>
  <div id="app">
    <div class="container">
      <!-- props 에 정보 보내기 --> 
      <MovieList v-bind:movies="movies" v-bind:genres="genres"/>
    </div>
  </div>
</template>

<script>
const axios = require('axios');
import MovieList from './components/movies/MovieList.vue'

export default {
  name: 'app',
  components: {
    MovieList: MovieList, 
  },
  data() {
    return {
      movies: [],
      genres: [],
    }
  },
  // API 정보 받기
  mounted() {
    // 쉬운 방법
    const MOVIE_URL = 'https://gist.githubusercontent.com/edujason-hphk/f57d4cb915fcec433ece535b2f08a10f/raw/612fd3f00468722ead2cfe809f14e38230b47686/movie.json'
    axios.get(MOVIE_URL)
      .then((movieResponse) => {
        this.movies = movieResponse.data
      })
    // 귀찮은 방법 
    const GENRE_URL = 'https://gist.githubusercontent.com/edujason-hphk/eea9c85a937cbf469b8f55fd7f8524df/raw/68bad38a2bc911d3a39bce26d6dd9b68a7efe849/genre.json'
    axios.get(GENRE_URL)
      .then((genreResponse) => {
        for (const genre of genreResponse.data) {
          this.genres.push({
            id: genre.id,
            name: genre.name,
          })
        }
      })
  },
}
</script>

```



### 2. MovieList.vue

##### - 반복을 통해  `MovieListItem` 을 호출한다.
##### - 장르 선택 기능을 구현한다. 이때 `computed` 를 사용할 것을 추천 제발
##### - `watch` 로 구현하면 시작 화면에서 아무런 영화 정보도 볼 수 없다. 


```vue
<!-- MovieList.vue -->

<template>
  <div>
    <h1>영화 목록</h1>
    <h2>장르 선택</h2>
    <!-- v-model 을 이용해 선택한 장르의 id 를 data 에 저장한다. -->
    <select class="form-control" v-model="selectedGenreId">
      <option v-bind:value="0">전체보기</option>
      <option v-for="genre in genres" v-bind:key="genre.id" v-bind:value="genre.id">{{ genre.name }}</option>
    </select>
    <div class="row mt-5">
      <!-- 선택된 영화 목록을 보여준다. for문 component 에 있어야 한다. -->
      <MovieListItem v-for="movie in selectedGenreMovie" v-bind:key="movie.id" v-bind:movie="movie" />
    </div>
  </div>
</template>

<script>
import MovieListItem from "./MovieListItem.vue";

export default {
  name: "MovieList",
  components: {
    MovieListItem: MovieListItem
  },
  data() {
    return {
      selectedGenreId: 0,
    };
  },
  props: {
    movies: Array,
    genres: Array
  },
  // selectedGenreId 의 값이 변할때, 보여줄 영화의 리스트를 바꾼다. 
  computed: {
    selectedGenreMovie: function() {
      if(this.selectedGenreId === 0) {
        return this.movies
      } else {
        return this.movies.filter(movie => movie.genre_id === this.selectedGenreId)
      }
    }
  }
};
</script>
```



### 3. MovieListItem.vue, MovieListItemModal.vue

##### - `MovieListItem` 의 버튼을 눌렀을 때 `modal` 이 나오도록 만든다.

```vue
<!-- MovieListItem.vue -->

<template>
  <div class="col-3 my-3">
    <img class="movie--poster my-3" v-bind:src="movie.poster_url" v-bind:alt="movie.name">
    <h3>{{ movie.name }}</h3>
    <!-- html 에서 id 의 첫글자를 숫자로 받으면 오류가 난다. -->
    <!-- 따라서 'movie' 를 앞에 붙인 id 를 사용할 것! -->
    <button class="btn btn-primary" data-toggle="modal" v-bind:data-target="`#movie-${movie.id}`">영화 정보 상세보기</button>
    <MovieListItemModal v-bind:movie="movie" />
  </div>
</template>

...

<!-- style 은 모든 html 에 같이 적용된다. -->
<!-- 해당 component 에만 사용하려면 scoped 옵션! -->
<style>
.movie--poster {
  width: 200px;
}
</style>
```


```vue
<!-- MovieListItemModal.vue -->

<template>
<!-- 'movie' 를 앞에 붙인 id 를 넘겨준다. -->
<div class="modal fade" tabindex="-1" role="dialog" v-bind:id="`movie-${movie.id}`">
  <div class="modal-dialog" role="document">
    <div class="modal-content">
      <div class="modal-header">
        <h5 class="modal-title">{{ movie.name }}</h5>
        <button type="button" class="close" data-dismiss="modal" aria-label="Close">
          <span aria-hidden="true">&times;</span>
        </button>
      </div>
      <div class="modal-body">
        <img class="movie--poster my-3" v-bind:src="movie.poster_url" v-bind:alt="movie.name">
        <p>{{ movie.description }}</p>
      </div>
      <div class="modal-footer">
        <button type="button" class="btn btn-secondary" data-dismiss="modal">Close</button>
      </div>
    </div>
  </div>
</div>
</template>
```


