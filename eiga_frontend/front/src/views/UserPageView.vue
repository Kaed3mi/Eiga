<template>
  <div class="user-profile">

    <div class="vertical-menu">
      <!-- 左侧导航栏 -->
      <VerticalMenu/>
    </div>
    <div class="user-info-container">
      <!-- 用户信息弹窗组件 -->
      <UpdateUserInfo/>
    </div>
    
    <img :src="avatarUrl" alt="User avatar" class="avatar"/>
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
import UpdateUserInfo from "../components/UpdateUserInfo.vue";
import http from "../utils/http";
import {watch} from "vue";

export default {
  name: 'UserPage',
  components: {VerticalMenu, UpdateUserInfo},
  data() {
    return {
      user_id: this.$route.params.userId,
      username: '',
      bio: '大家好啊我是膜蛤',
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
      }).catch(error => {
        console.error('Error fetching data:', error);
      });
    }
  },
  props: {
    // 头像
    avatarUrl: {
      type: String,
      default: 'https://encrypted-tbn1.gstatic.com/images?q=tbn:ANd9GcQ8n9J70Q6vFkV5jzTigNeNGXSFvgzB9SOxHr_zAKWXi8KJRnsF',
      required: true,
    },
  },
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