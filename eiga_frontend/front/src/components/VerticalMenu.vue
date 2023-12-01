<template>
  <div class="vertical-menu">
    <el-row class="tac">
      <el-col>
        <el-link href="/home/">
          <el-image src="/src/assets/mukamuka.svg" style="width: 24px">
          </el-image>
          <h3 class="mb-2">Eiga映画计划</h3>
        </el-link>
        <el-menu
            active-text-color="#007f7f"
            background-color="#ffffff"
            class="el-menu-vertical-demo"
            :default-active="activate"
            :default-openeds="openeds"
            text-color="#000"
            @open="handleOpen"
            @close="handleClose"
            @select="handleActivate"
            :unique-opened="true"
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

          <router-link :to="{ name: 'bangumi-subject_search'}">
            <el-menu-item index="2">
              <el-icon>
                <Search/>
              </el-icon>
              <span>搜索</span>
            </el-menu-item>
          </router-link>
          <router-link :to="{name: 'rank', params:{page: 1}}">
            <el-menu-item index="3">
              <el-icon>
                <icon-menu/>
              </el-icon>
              <span>排行榜</span>
            </el-menu-item>
          </router-link>
          <el-menu-item index="4" @click="handleUserPage">
            <el-icon>
              <document/>
            </el-icon>
            <span>个人站</span>
          </el-menu-item>
          <el-menu-item index="5" @click="handleBlog">
            <el-icon>
              <Notebook/>
            </el-icon>
            <span>日志</span>
          </el-menu-item>

          <el-sub-menu
              index="6"
              v-if="isAdmin"
          >
            <template #title>
              <el-icon>
                <location/>
              </el-icon>
              <span>控制台</span>
            </template>

            <el-menu-item index="6-1" v-bind:disabled="!isAdmin || !isEditable" @click="routeToModify">修改当前页面
            </el-menu-item>

            <el-menu-item index="6-2" v-bind:disabled="!isAdmin" @click="routeToCreateCharacter">新建角色
            </el-menu-item>

            <el-menu-item index="6-3" v-bind:disabled="!isAdmin" @click="routeToCreateBangumi">新建番剧
            </el-menu-item>

          </el-sub-menu>

          <el-sub-menu
              index="7"
              active-text-color="#007f7f"
              background-color="#ffffff"
              v-if="user_id!=null &&String(user_id)!==''"
              class="el-menu-vertical-demo"
              text-color="#000"
          >
            <template #title>
              <el-avatar :src="avatar_url" :size="24" style="margin-left: -0px;" class="avatar"/>
              <span style="padding: 5px; font-size:14px">{{ username }}</span>
            </template>
            <el-menu-item index="7-1" @click="logOut">
              <el-icon>
                <ArrowLeft/>
              </el-icon>
              <span style="padding: 5px; ">登出</span>
            </el-menu-item>
            <el-menu-item index="7-2" @click="switchAccount">
              <el-icon>
                <Sort/>
              </el-icon>
              <span>切换账号</span>
            </el-menu-item>
          </el-sub-menu>
          <el-menu-item v-else @click="logIn" index="7">
            <el-icon>
              <User/>
            </el-icon>
            <span>请登录</span>
          </el-menu-item>

        </el-menu>
      </el-col>
    </el-row>
  </div>
  <!-- <div class="fixed-user">
    <el-row class="row-with-divider">
      <el-col v-if="user_id!=null &&String(user_id)!==''" :span="24">
        <el-menu
            active-text-color="#007f7f"
            background-color="#ffffff"
            class="el-menu-vertical-demo"
            text-color="#000"
        >
          <el-menu-item index="1">
            <el-avatar :src="avatar_url" :size="24" style="margin-left: -0px;" class="avatar"/>
            <span style="padding: 5px; font-size:14px">{{ username }}</span>
          </el-menu-item>
          <el-menu-item index="2" @click="logOut">
            <el-icon>
              <ArrowLeft/>
            </el-icon>
            <span style="padding: 5px; ">登出</span>
          </el-menu-item>
          <el-menu-item index="3" @click="switchAccount">
            <el-icon>
              <Sort/>
            </el-icon>
            <span>切换账号</span>
          </el-menu-item>
        </el-menu>
      </el-col>
      <el-col v-else :span="24">
        <el-menu
            active-text-color="#007f7f"
            background-color="#ffffff"
            class="el-menu-vertical-demo"
            text-color="#000"
        >
          <el-menu-item @click="logIn" index="1">
            <el-icon>
              <User/>
            </el-icon>
            <span>请登录</span>
          </el-menu-item>
        </el-menu>
      </el-col>
    </el-row>
  </div> -->
</template>


<script lang="ts" setup>
import {
  Document,
  Menu as IconMenu,
  Location,
  Setting,
  Notebook,
  Sort,
  ArrowLeft,
  Search
} from '@element-plus/icons-vue'
</script>

<script lang="ts">
import {ElNotification, ElMessage} from 'element-plus'
import {ref} from 'vue'
import router from '../utils/router';
import {
  Document,
  Menu as IconMenu,
  Location,
  Setting,

  User
} from '@element-plus/icons-vue'
import http from "../utils/http";
import UserAvatar from "../user_page_components/UserAvatar.vue";
import {defaults} from "axios";

export default {
  data() {
    return {
      user_id: ref(''),
      username: '',
      avatar_url: '',
      activate: '1',
      openeds :[''],
      activate2: '1'
    }
  },
  computed: {
    isAdmin() {
      console.log("permission:"+localStorage.getItem("permission"))
      return (
          localStorage.getItem("user_id") && localStorage.getItem("permission") === "admin"
      );
    },
    isEditable() {
      return (
          this.$route.path.startsWith("/bangumi/") ||
          this.$route.path.startsWith("/character/") ||
              this.$route.path.startsWith("/blog/")
      );
    }
  },
  components: {
    UserAvatar
  },
  mounted() {
    this.user_id = ref(localStorage.getItem('user_id'))
    if (this.user_id != null) {
      this.userQuery();
    }
    this.defaultActivate();

  },
  methods: {
    handleUserPage() {
      let user_id = localStorage.getItem('user_id');
      console.log(user_id)
      if (user_id == null) {
        ElMessage({
          message: '请先登录',
          type: 'warning',
        })
        this.$router.push('/login')
      } else {
        this.$router.push('/user/' + user_id)
      }
    },
    handleBlog() {
      this.$router.push('/blog_create')
    },
    defaultActivate() {
      this.activate = localStorage.getItem("default-active")
      this.openeds =['6']
      console.log("opened:"+this.openeds)
      console.log("opened2:"+['4'])
      this.activate2 = localStorage.getItem("default-active2")
      if (this.activate == null) {
        localStorage.setItem("default-active", '')
        this.activate = ''
      }
      if (this.activate2 == null) {
        localStorage.setItem("default-active2", '')
        this.activate2 = ''
      }
    },
    handleActivate(index,indexPath) {
      localStorage.setItem("default-active", indexPath[0])
      if (indexPath.length == 2) {
        localStorage.setItem("default-active2", indexPath[1])
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
      this.user_id = ref('')
      ElMessage({
        message: '已登出',
        type: 'success',
      })
    },
    logIn() {
      console.log("click login");

      this.$router.push('/login')
    },
    switchAccount() {
      ElMessage({
        message: '已登出',
        type: 'success',
      })
      localStorage.removeItem('user_id');
      this.$router.push('/login')
    },
    routeToModify() {
      if (this.$route.path.startsWith("/bangumi/")) {
        console.log("/bangumi/" + this.$route.params.bangumiId);
        this.$router.push("/bangumi_update/" + this.$route.params.bangumiId);
      }
      if (this.$route.path.startsWith("/character/")) {
        console.log("/character/" + this.$route.params.characterId);
        this.$router.push("/character_update/" + this.$route.params.characterId);
      }
      if (this.$route.path.startsWith("/blog/")) {
        console.log("/blog/" + this.$route.params.blogId);
        this.$router.push("/blog_update/" + this.$route.params.blogId);
      }
    },
    routeToCreateCharacter() {
      this.$router.push('/character_create')
    },
    routeToCreateBangumi() {
      this.$router.push('/bangumi_create')
    },
  }
}

</script>


<style scoped>
.vertical-menu {
  top: 0;
  left: 0;
  height: 100%;
  width: 200px;
  position: fixed;
}

.fixed-user {
  position: fixed;
  width: 150px;
  height: 20%;
  bottom: 10px; /* 距离底部的位置 */
  left: 00px; /* 距离左侧的位置 */
}

.row-with-divider::after {
  content: '';
  position: absolute;
  top: 0;
  bottom: 0;
  right: 0px;
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