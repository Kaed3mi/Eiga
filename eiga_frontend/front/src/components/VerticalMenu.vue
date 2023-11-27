<template>
  <div class="vertical-menu">
    <el-row class="tac" >
      <el-col :span="24" >
        <h5 class="mb-2">Mukamuka</h5>
        <el-menu
            active-text-color="#007f7f"
            background-color="#ffffff"
            class="el-menu-vertical-demo"
            default-active="2"
            text-color="#000"
            @open="handleOpen"
            @close="handleClose"
        >
          <el-sub-menu index="1">
            <template #title>
              <el-icon>
                <location/>
              </el-icon>
              <span>探索</span>
            </template>
            <router-link :to="{ name: 'bangumi-view', params: { bangumiId: 1 }}">
              <el-menu-item index="1-1">番组
              </el-menu-item>
            </router-link>
            <el-menu-item index="1-2">人物</el-menu-item>
            <el-menu-item index="1-3">标签</el-menu-item>
          </el-sub-menu>

          <router-link :to="{ name: 'rank_home_page'}">
            <el-menu-item index="2">
              <el-icon>
                <icon-menu/>
              </el-icon>
              <span>排行榜</span>
            </el-menu-item>
          </router-link>
          <el-menu-item @click="handleUserPage">
            <el-icon>
              <document/>
            </el-icon>
            <span>个人站</span>
          </el-menu-item>
          <el-menu-item index="4">
            <el-icon>
              <setting/>
            </el-icon>
            <span>设置</span>
          </el-menu-item>
        </el-menu>
      </el-col>
    </el-row>
  </div>
  <div class="fixed-user">
    <el-row class="row-with-divider">
      <el-col v-if="user_id!=null" :span="24">
        <div class='avatar-container'>

          <el-avatar :src="avatar_url" class="avatar"/>
          <p style="padding: 3px; font-size:14px">
            {{ username }}
          </p>
          <el-button style="font-size:12px" @click="logOut"> 登出</el-button>
          <br/>
          <el-button style="font-size:12px" @click="switchAccount"> 切换账号</el-button>

        </div>

      </el-col>
      <el-col v-else :span="24">
        <el-button @click="logIn"> 请登录</el-button>
      </el-col>
    </el-row>
  </div>
</template>

<script lang="ts" setup>
import {
  Document,
  Menu as IconMenu,
  Location,
  Setting,
} from '@element-plus/icons-vue'
</script>

<script lang="ts">
import {ElNotification} from 'element-plus'
import router from '../utils/router';
import {
  Document,
  Menu as IconMenu,
  Location,
  Setting,
} from '@element-plus/icons-vue'
import http from "../utils/http";
import UserAvatar from "../user_page_components/UserAvatar.vue";

export default {
  data() {
    return {
      user_id: '',
      username: '',
      avatar_url: ''
    }
  },
  components: {
    UserAvatar
  },
  mounted() {
    this.user_id = localStorage.getItem('user_id')
    if (this.user_id != null) {
      this.userQuery();
    }
  },
  methods: {
    handleUserPage() {
      let user_id = localStorage.getItem('user_id');
      console.log(user_id)
      if (user_id == null) {
        ElNotification({
          title: '警告',
          message: '请先登录',
          type: 'warning',
        })
        this.$router.push('/login')
      } else {
        this.$router.push('/user/' + user_id)
      }
    },
    handleOpen(key, keyPath) {
    },
    handleClose(key, keyPath) {
    },
    userQuery() {
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
    },
    logOut() {
      console.log("removing user_id")
      localStorage.removeItem('user_id');
      console.log("removed user_id")
    },
    logIn() {
      this.$router.push('/login')
    },
    switchAccount() {
      localStorage.removeItem('user_id');
      this.$router.push('/login')
    }
  }
}

</script>


<style scoped>
.vertical-menu {
  position: fixed;
  top: 0;
  left: 0;
}

.fixed-user {
  position: fixed;


  bottom: 10px; /* 距离底部的位置 */
  left: 10px; /* 距离左侧的位置 */
  z-index: 1000; /* 控制图标的层级，确保它在其他元素上面 */
}

.row-with-divider::after {
  content: '';
  position: absolute;
  top: 0;
  bottom: 0;
  right: -20px;
  width: 1px; /* 分割线的宽度 */
  background-color: #eee; /* 分割线的颜色 */
}

.small_avatar {
  align-items: center;
  margin-bottom: 24px;
  margin-left: -5px;
}

.middle-col {
  flex: 1;
  overflow-y: auto; /* 如果内容过多，允许滚动 */
}

.flex-grow {
  bottom: 10px; /* 距离底部的位置 */
  flex-grow: 1;
}
</style>