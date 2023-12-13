<template>
  <el-container class="container_style">
    <el-aside width="200px">
      <VerticalMenu></VerticalMenu>
    </el-aside>
    <el-main>
      <div class="main_full_flex_style">
        <div class="main_width">
          <el-card class="box-card" style="position: relative">
            <div v-if="checkUserIdentity" class="user-info-container">
              <UpdateUserInfo/>
            </div>
            <el-container>
              <el-header></el-header>
              <el-main>
                <!-- <CharacterInfo></CharacterInfo> -->
                <div class="user-profile">
                  <!-- 左侧导航栏 -->
                  <!-- 用户信息弹窗组件 -->

                  <!-- 用户头像/修改组件 -->
                  <div class='avatar-container'>
                    <UserAvatar :avatar_url="avatar_url" :editable="checkUserIdentity"/>
                  </div>

                  <h2>{{ username }}</h2>
                  <p>{{ bio }}</p>
                  <div class="stat">
                    <strong>{{ email }}</strong>
                  </div>
                  <el-divider/>
                  <div class="my-bangumis">

                    <h3></h3>
                    <el-text size="large">{{ username }}的番组</el-text>
                    <MyBangumis :user_id="user_id"/>
                  </div>
                  <div>
                    <el-divider></el-divider>
                    <el-text size="large">{{ username }}的日志</el-text>
                    <div style="padding: 10px;"></div>
                    <div v-if="blogs.length > 0">
                      <el-row
                          :gutter="20"
                          class="main_flex_style"
                      >
                        <el-col :span="12" v-for="(result, index) in blogs" :key="index">
                          <ListItem type="blog" :id="result.blog_id.blog_id"
                                    :text_only="true"
                                    :name="result.blog_id.blog_title"
                                    :description="result.blog_id.content"
                                    :date="result.date"
                                    :author_name="result.user_name"
                                    :author_id="result.blog_id.user_id"
                          ></ListItem>
                        </el-col>
                      </el-row>
                    </div>
                    <div v-else>
                      <el-text size="small">暂时没有日志...</el-text>
                    </div>
                  </div>
                </div>
              </el-main>
            </el-container>
          </el-card>
          <Footer/>
        </div>
      </div>
    </el-main>
  </el-container>
</template>

<script setup>
import {
  User, Film, Avatar, Notebook
} from '@element-plus/icons-vue'
</script>
<script>
import VerticalMenu from "../components/VerticalMenu.vue";
import ListItem from "../components/ListItem.vue";
import UpdateUserInfo from "../user_page_components/UpdateUserInfo.vue";
import http from "../utils/http";
import UserAvatar from "../user_page_components/UserAvatar.vue";
import MyBangumis from "../user_page_components/MyBangumis.vue";
import Footer from "../components/Footer.vue";
import {addHours, format} from "date-fns";

export default {
  name: 'UserPage',
  components: {Footer, MyBangumis, UserAvatar, VerticalMenu, UpdateUserInfo, ListItem},
  data() {
    return {
      blogs: [],
      user_id: this.$route.params.userId,
      avatar_url: '',
      username: '',
      email: '',
      bio: '我是Eiga映画计划的一员',
      bangumis: [],
      avatarUrl: 'https://encrypted-tbn1.gstatic.com/images?q=tbn:ANd9GcQ8n9J70Q6vFkV5jzTigNeNGXSFvgzB9SOxHr_zAKWXi8KJRnsF'
    }
  },
  // 用户同路由跳转更新，不能删。
  beforeRouteUpdate(to, from, next) {
    this.user_id = to.params.userId; // 更新 user_id
    console.log("refresh" + this.user_id)
    // this.getUserScores();
    // this.userQuery();
    next();
  },
  mounted() {
    this.getUserScores();
    this.userQuery();
    this.userBlogQuery();
  },
  computed: {
    checkUserIdentity() {
      console.log("is: "+localStorage.getItem('user_id') == this.user_id);
      return localStorage.getItem('user_id') == this.user_id
    }
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
        this.email = response.data.email
        // console.log(response.data.image_data);
        // this.avatarUrl = `data:image/png;base64,${response.data.image_data}`
        // console.log(this.avatarUrl);
        this.avatar_url = `data:image/png;base64,${response.data.image_data}`
        // console.log("avatar_url: " + this.avatar);
      }).catch(error => {
        console.error('Error fetching data:', error);
      });
    },
    userBlogQuery() {
      this.blogs = []
      http.get(
          "http://127.0.0.1:8000/user_blog_query/",
          {
            params: {
              "user_id": this.user_id,
            }
          }
      ).then(response => {
        for (let item of response.data.blogs) {
          let beijing = addHours(item.blog_id.time, -8)
          this.blogs.push({
            'blog_id': item.blog_id,
            'avatar': item.avatar,
            'date': format(beijing, 'yyyy-MM-dd HH:mm'),
            'user_name': item.user_name,
          })
        }
      }).catch(error => {
        console.error('Error fetching data:', error);
      });
    },
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
  z-index: 100;
  position: absolute;
  top: 20px; /* Adjust the top position as needed */
  right: 20px; /* Adjust the right position as needed */
}

.stat {
  margin: 0 10px;
}
</style>