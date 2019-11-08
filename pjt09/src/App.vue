<template>
  <div id="app">
    <div class="container">
      <!-- 1-3. 호출하시오. 
        필요한 경우 props를 데이터를 보내줍니다.
      -->
      <MovieList v-bind:movies="movies" v-bind:genres="genres"/>
    </div>
  </div>
</template>

<script>
const axios = require('axios');
// 1-1. 저장되어 있는 MovieList 컴포넌트를 불러오고,
import MovieList from './components/movies/MovieList.vue'

export default {
  name: 'app',
  // 1-2. 아래에 등록 후
  components: {
    MovieList: MovieList, 
  },
  data() {
    return {
      // 활용할 데이터를 정의하시오.
      movies: [],
      genres: [],
    }
  },
  mounted() {
    // 0. mounted 되었을 때, 
    // 1) 제시된 URL로 요청을 통해 data의 movies 배열에 해당 하는 데이터를 넣으시오. 
    // 2) 제시된 URL로 요청을 통해 data의 genres 배열에 해당 하는 데이터를 넣으시오.
    // axios는 위에 호출되어 있으며, node 설치도 완료되어 있습니다.
    const MOVIE_URL = 'https://gist.githubusercontent.com/edujason-hphk/f57d4cb915fcec433ece535b2f08a10f/raw/612fd3f00468722ead2cfe809f14e38230b47686/movie.json'
    axios.get(MOVIE_URL)
      .then((movieResponse) => {
        this.movies = movieResponse.data
        // for (const movie of movieResponse.data) {
        //   this.movies.push({
        //     id: movie.id,
        //     name: movie.name,
        //     rating: movie.rating,
        //     genre_id: movie.genre_id,
        //     director: movie.director,
        //     user_rating: movie.user_rating,
        //     poster_url: movie.poster_url,
        //     description: movie.description,
        //   })
        // }
      })
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

<style>
#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>
