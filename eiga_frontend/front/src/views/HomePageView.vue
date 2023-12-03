<template>
  <el-container class="container_style">
    <el-aside width="200px">
      <VerticalMenu ref="VerticalMenu"></VerticalMenu>
    </el-aside>

    <el-main>
      <div class="main_full_flex_style">
        <div class="main_width">
          <el-header></el-header>
          <el-header style="text-align: left;">
            <h2>Hi! {{ username }}</h2>
          </el-header>
          <el-card shadow="never">
            <el-text>{{ hitokoto.hitokoto }}</el-text>
            <p></p>
            <el-text>—— {{ hitokoto.from_who }}《{{ hitokoto.from }}》</el-text>
          </el-card>
          <el-carousel
              height="500px">
            <el-carousel-item
                v-for="url in urls">
              <el-image
                  style="height: 500px;"
                  :src="url"></el-image>
            </el-carousel-item>
          </el-carousel>
          <Footer/>
        </div>
      </div>
    </el-main>
  </el-container>
</template>

<script lang="ts">


import VerticalMenu from "../components/VerticalMenu.vue";
import http from "../utils/http";
import CharacterUpdate from "../components/CharacterUpdate.vue";
import Footer from "../components/Footer.vue";

export default {
  name: "Character_update",
  components: {
    Footer,
    CharacterUpdate,
    VerticalMenu
  },
  data() {
    return {
      user_id: localStorage.getItem("user_id"),
      hitokoto: [],
      username: '',
      urls: [
        'https://i.postimg.cc/q783HPYV/minami-kotori.jpg'
      ]
    }
  },
  mounted() {
    this.userQuery();
    http.get(
        "https://v1.hitokoto.cn/?c=a"
    ).then(response => {
      this.hitokoto = response.data
      console.log(response.data)
    })
  },
  methods: {
    userQuery() {
      http.post(
          "http://127.0.0.1:8000/user_query/",
          {'user_id': this.user_id}
      ).then(response => {
        this.username = response.data.username
        // console.log(response.data.image_data);
        // this.avatarUrl = `data:image/png;base64,${response.data.image_data}`
        // console.log(this.avatarUrl);
        // this.avatar_url = `data:image/png;base64,${response.data.image_data}`
        // console.log("avatar_url: " + this.avatar);
      }).catch(error => {
        console.error('Error fetching data:', error);
      });
    },
  }
}
</script>
<style scoped>

</style>
