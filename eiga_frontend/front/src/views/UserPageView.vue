<template>
  <div class="user-profile">
    <!-- 左侧导航栏 -->
    <div class="vertical-menu">
      <VerticalMenu/>
    </div>

    <!-- 用户信息弹窗组件 -->
    <div class="user-info-container">
      <UpdateUserInfo/>
    </div>

    <!-- 用户头像/修改组件 -->
    <div class='avatar-container'>
      <UserAvatar :avatar_url="this.avatar_url"/>
    </div>

    <h2>{{ username }}</h2>
    <p>{{ bio }}</p>
    <div class="stat">
      <strong>@{{ username }}</strong>
    </div>

    <div v-if="bangumis.length >= 0">
      <h3>{{ username }}的Bangumi</h3>
      <el-row :gutter="20">
        <el-col :span="24" v-for="(item, index) in bangumis" :key="index">
          {{ item.bangumi.bangumi_name }} : {{ item.score }}
        </el-col>
      </el-row>
      <el-divider border-style="dashed"/>
    </div>

  </div>
</template>
<script>
import VerticalMenu from "../components/VerticalMenu.vue";
import UpdateUserInfo from "../user_page_components/UpdateUserInfo.vue";
import http from "../utils/http";
import UserAvatar from "../user_page_components/UserAvatar.vue";

export default {
  name: 'UserPage',
  components: {UserAvatar, VerticalMenu, UpdateUserInfo},
  data() {
    return {
      avatar_url: '',
      user_id: this.$route.params.userId,
      username: '',
      bio: '好',
      bangumis: [],
    }
  },
  // 用户同路由跳转更新，不能删。
  beforeRouteUpdate(to, from, next) {
    this.user_id = to.params.userId; // 更新 user_id
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
      http.post(
          "http://127.0.0.1:8000/user_query/",
          {'user_id': this.user_id}
      ).then(response => {
        this.username = response.data.username
        this.avatar_url = response.data.avatar
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