<template>
  <el-container>
        <el-aside width="200px"><VerticalMenu></VerticalMenu></el-aside>
        <el-container>
          <el-header></el-header>
          <el-main>
          <!-- <CharacterInfo></CharacterInfo> -->
          <div class="user-profile">
            <!-- 左侧导航栏 -->
            <!-- 用户信息弹窗组件 -->
            <div class="user-info-container">
              <UpdateUserInfo/>
            </div>

            <!-- 用户头像/修改组件 -->
            <div class='avatar-container'>
              <UserAvatar :avatar_url="avatar_url"/>
            </div>

            <h2>{{ username }}</h2>
            <p>{{ bio }}</p>
            <div class="stat">
              <strong>@{{ username }}</strong>
            </div>

            <div class="my-bangumis">
              <h3></h3>
              <el-text type="primary" size="large">{{ username }}的番组</el-text>
              <MyBangumis :user_id="user_id"/>
            </div>

          </div>
        </el-main>
        </el-container>
      </el-container>
</template>
<script>
import VerticalMenu from "../components/VerticalMenu.vue";
import UpdateUserInfo from "../user_page_components/UpdateUserInfo.vue";
import http from "../utils/http";
import UserAvatar from "../user_page_components/UserAvatar.vue";
import MyBangumis from "../user_page_components/MyBangumis.vue";

export default {
  name: 'UserPage',
  components: {MyBangumis, UserAvatar, VerticalMenu, UpdateUserInfo},
  data() {
    return {
      user_id: this.$route.params.userId,
      avatar_url: '',
      username: '',
      bio: '好',
      bangumis: [],
      avatarUrl: 'https://encrypted-tbn1.gstatic.com/images?q=tbn:ANd9GcQ8n9J70Q6vFkV5jzTigNeNGXSFvgzB9SOxHr_zAKWXi8KJRnsF'
    }
  },
  // 用户同路由跳转更新，不能删。
  beforeRouteUpdate(to, from, next) {
    this.user_id = to.params.user_id; // 更新 user_id
    this.getUserScores();
    this.userQuery();
    next();
  },
  mounted() {
    this.getUserScores();
    this.userQuery();
  },
  methods: {
    getUserScores() {
      this.bangumis = []
      http.get(
          "http://127.0.0.1:8000/get_user_scores/",
          {
            params: {'user_id': this.user_id,}
          }
      ).then(response => {
        console.log(response.data.length);
        for (let item of response.data.bangumis) {
          this.bangumis.push({
            'bangumi': item.bangumi,
            'score': item.score,
          })
        }
      }).catch(error => {
        console.error('Error fetching data:', error);
      });
    },
    userQuery() {
      console.log("I'm user#" + this.user_id)
      http.post(
          "http://127.0.0.1:8000/user_query/",
          {'user_id': this.user_id}
      ).then(response => {
        this.username = response.data.username
        // console.log(response.data.image_data);
        // this.avatarUrl = `data:image/png;base64,${response.data.image_data}`
        // console.log(this.avatarUrl);
        this.avatar_url = `data:image/png;base64,${response.data.image_data}`
        // console.log("avatar_url: " + this.avatar);
      }).catch(error => {
        console.error('Error fetching data:', error);
      });
    }
  },
  props: {},
};
</script>
<style scoped>
.user-profile {
  text-align: center;
}

.avatar {
  width: 100px;
  height: 100px;
  border-radius: 50%;
  margin-bottom: 20px;
}

.user-info-container {
  position: fixed;
  top: 20px; /* 距离顶部的距离 */
  right: 20px; /* 距离右侧的距离 */
}

.stat {
  margin: 0 10px;
}
</style>