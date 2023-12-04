<template>
  <el-container class="container_style">
    <el-aside width="200px">
      <VerticalMenu/>
    </el-aside>
    <el-main>
      <div class="main_full_flex_style">
        <div class="bangumi_width">
          <el-card class="box-card" style="">
            <el-container class="content-container">
              <el-header><h2>{{ bangumi_name }}</h2></el-header>
              <el-divider border-style="dashed"/>
              <el-main>
                <el-container>
                  <el-aside style="margin-right: 5%">
                    <el-card :body-style="{ padding: '8px'}" shadow="always">
                      <el-image
                          style="width: 300px; height: 400px"
                          :src="bangumi_image"
                          :fit="cover"
                      />
                    </el-card>
                    <el-divider></el-divider>
                    <el-card :body-style="{padding:'8px'}">
                      <h4>Eiga评分</h4>
                      <el-rate
                          style="margin-top: -20px"
                          v-model="bangumi_score"
                          disabled
                          show-score
                          text-color="#ff9900"
                          :score-template="Number(bangumi_score) !== -1 ? Number(bangumi_score).toFixed(1)+ '分' : ''"
                          :colors="rate_colors"
                      />
                      <br/>
                      <div style="padding: 20px;"></div>
                      你的评分:&nbsp;&nbsp;
                      <br/>
                      <el-rate
                          v-model="user_score"
                          allow-half
                          show-score
                          text-color="#ff9900"
                          :score-template="Number(user_score) !== -1 ? Number(user_score).toFixed(1)+ '分' : ''"
                          :colors="rate_colors"
                          @click="handleScoring"
                      />
                      <div style="padding: 8px;"></div>
                    </el-card>
                    <div>
                      <el-divider border-style="dashed"/>
                      <div v-if="blogs.length > 0">
                        <h3>关联日志</h3>
                        <el-row
                            :gutter="20"
                        >
                          <el-col :span="24" v-for="(result, index) in blogs" :key="index">
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
                  </el-aside>

                  <el-main>
                    <h3>简介</h3>
                    <el-descriptions>
                      <el-descriptions-item>
                        <p v-for="(line, index) in bangumi_intro.split('\n')" :key="index"
                           style="text-align: left;white-space: pre-wrap;text-indent: 2em;"
                        >
                          {{ line }}
                        </p>
                      </el-descriptions-item>
                    </el-descriptions>
                    <el-divider border-style="dashed"/>
                    <h3>角色</h3>
                    <CharacterCard :id=bangumi_id></CharacterCard>
                    <el-divider border-style="dashed"/>
                    <div v-if="bangumi_relationships.length > 0">
                      <h3>关联番组</h3>
                      <el-row
                          :gutter="20"
                      >
                        <el-col :span="24" v-for="(result, index) in bangumi_relationships" :key="index">
                          <ListItem type="bangumi" :id="result.bangumi_id.bangumi_id"
                                    :name="result.bangumi_id.bangumi_name"
                                    :relation="result.relation"
                                    :image="result.image"></ListItem>
                        </el-col>
                      </el-row>
                      <el-divider border-style="dashed"/>
                    </div>
                    <CommentArea object_type="bangumi" :object_id="bangumi_id"></CommentArea>
                  </el-main>

                </el-container>
              </el-main>

            </el-container>
          </el-card>
          <Footer/>
        </div>
      </div>

    </el-main>

  </el-container>
</template>
<script lang="ts">
import VerticalMenu from '../components/VerticalMenu.vue'
import Footer from '../components/Footer.vue'
import CharacterCard from '../components/CharacterCard.vue'
import http from "../utils/http";
import ListItem from '../components/ListItem.vue'
import CommentItem from "../components/CommentItem.vue";
import CommentArea from "../components/CommentArea.vue";
import {ref} from 'vue'
import {format} from "date-fns";
import {ElNotification} from "element-plus";

export default {
  data() {
    return {
      bangumi_id: this.$route.params.bangumiId,
      bangumi_image: '',
      bangumi_intro: "No introduction",
      bangumi_name: "Untitled",
      bangumi_score: 0,
      user_scored: ref(false),
      user_score: ref(-1),
      rate_colors: ref(['#99A9BF', '#F7BA2A', '#FF9900']),
      bangumi_relationships: [],
      comments: [],
      blogs: [],
      new_comment_area: ref(''),
      user_name: '',
      avatar: '',
      user_id: ref(''),
    }
  },
  mounted() {
    this.bangumiQuery(); // 在组件挂载后调用 fetchData 方法
    this.bangumiCommentQuery();
    this.bangumiRelationShipQuery();
    this.userScoreQuery();
    this.bangumiScoreQuery();
    this.bangumiBlogQuery();
    this.user_id = ref(localStorage.getItem('user_id'))
    if (this.user_id != null) {
      this.userQuery();
    }

  },
  methods: {
    bangumiQuery() {
      http.get(
          "http://127.0.0.1:8000/bangumi_query/",
          {
            params: {
              "bangumi_id": this.bangumi_id,
            }
          }
      ).then(response => {
        this.bangumi_intro = response.data.bangumi_intro;
        this.bangumi_name = response.data.bangumi_name;
        // this.bangumi_score = response.data.bangumi_score;
        this.bangumi_image = `data:image/png;base64,${response.data.image}`;
        console.log(this.bangumi_image);

      })
          .catch(error => {
            console.error('Error fetching data:', error);
          });
    },
    bangumiRelationShipQuery() {
      http.get(
          "http://127.0.0.1:8000/bangumi_relationship_query/",
          {
            params: {
              "bangumi_id": this.bangumi_id,
            }
          }
      ).then(response => {
        for (let item of response.data.bangumis) {
          this.bangumi_relationships.push({
            "relation": item.relation,
            'bangumi_id': item.bangumi_id,
            'image': `data:image/png;base64,${item.image}`
          })
        }
        console.log("this.bangumi_relationships")
        console.log(this.bangumi_relationships)
      })
          .catch(error => {
            console.error('Error fetching data:', error);
          });
    },
    bangumiCommentQuery() {
      console.log("i'm called")
      this.comments = []
      http.get(
          "http://127.0.0.1:8000/comment_search/",
          {
            params: {
              "bangumi_id": this.bangumi_id,
            }
          }
      ).then(response => {
        for (let item of response.data.comments) {
          this.comments.push({
            'comment_id': item.comment_id,
            'content': item.content,
            'time': item.time,
            'user_id': item.user_id,
            'bangumi_id': item.bangumi_id,
            'blog_id': item.blog_id,
            'character_id': item.character_id,
          })
        }
        console.log("this.comments")
        console.log(this.comments)
      }).catch(error => {
        console.error('Error fetching data:', error);
      });
    },
    bangumiBlogQuery() {
      this.blogs = []
      http.get(
          "http://127.0.0.1:8000/bangumi_blog_query/",
          {
            params: {
              "bangumi_id": this.bangumi_id,
            }
          }
      ).then(response => {
        for (let item of response.data.blogs) {
          this.blogs.push({
            'blog_id': item.blog_id,
            'avatar': item.avatar,
            'date': format(item.blog_id.time, 'yyyy-MM-dd HH:mm'),
            'user_name': item.user_name,
          })
        }
      }).catch(error => {
        console.error('Error fetching data:', error);
      });
    },
    commentInsert() {
      http.post(
          'http://127.0.0.1:8000/comment_insert/',
          {
            content: this.new_comment_area,
            time: new Date().getTime(),
            user_id: localStorage.getItem("user_id"),
            bangumi_id: this.bangumi_id,
            blog_id: '',
            character_id: '',
          },
      ).then(response => {
        console.log("submitted comment")
        this.new_comment_area = ref('')
        this.bangumiCommentQuery()
      }).catch(error => {
        alert("评论失败")
        console.error('Error posting data:', error);
      });
    },
    bangumiScoreQuery() {
      http.get(
          'http://127.0.0.1:8000/bangumi_score_query/',
          {
            params: {
              bangumi_id: this.bangumi_id,
            }
          }
      ).then(response => {
        console.log("submitted score")
        this.bangumi_score = response.data.score
      }).catch(error => {
        alert("评论失败")
        console.error('Error posting data:', error);
      });
    },
    userQuery() {
      http.post(
          "http://127.0.0.1:8000/user_query/",
          {'user_id': localStorage.getItem("user_id")}
      ).then(response => {
        this.user_name = response.data.username
        // console.log(response.data.image_data);
        // this.avatarUrl = `data:image/png;base64,${response.data.image_data}`
        // console.log(this.avatarUrl);
        this.avatar = `data:image/png;base64,${response.data.image_data}`
        // console.log("avatar_url: " + this.avatar);
      }).catch(error => {
        console.error('Error fetching data:', error);
      });
    },
    userScoreQuery() {
      http.get(
          'http://127.0.0.1:8000/score_query/',
          {
            params: {
              user_id: localStorage.getItem("user_id"),
              bangumi_id: this.bangumi_id,
            }
          }
      ).then(response => {
        if (response.data == 1) {
          this.user_score = ref(-1)
        } else {
          this.user_score = response.data.score
          this.user_scored = ref(true)
        }
      }).catch(error => {
        alert("评论失败")
        console.error('Error posting data:', error);
      });
    },
    handleScoring() {
      if (Boolean(this.user_scored)) {
        this.scoreUpdate();
      } else {
        this.scoreInsert();
      }
    },
    scoreInsert() {
      http.post(
          'http://127.0.0.1:8000/score_insert/',
          {
            user_id: localStorage.getItem("user_id"),
            bangumi_id: this.bangumi_id,
            score: this.user_score
          },
      ).then(response => {
        console.log("submitted score")
        ElNotification({
          title: '操作成功',
          message: '已为番组"'+this.bangumi_name+'"评分',
          type: 'success',
        })
      }).catch(error => {
        alert("新增评分失败")
        console.error('Error posting data:', error);
      });
    },
    scoreUpdate() {
      http.put(
          'http://127.0.0.1:8000/score_update/',
          {
            user_id: localStorage.getItem("user_id"),
            bangumi_id: this.bangumi_id,
            score: this.user_score
          },
      ).then(response => {
        console.log("updated score")
        ElNotification({
          title: '操作成功',
          message: '已为番组"'+this.bangumi_name+'"评分',
          type: 'success',
        })
      }).catch(error => {
        alert("修改评分失败")
        console.error('Error posting data:', error);
      });
    }
  },
  name: "Login",
  components: {
    CommentItem,
    VerticalMenu,
    CharacterCard,
    ListItem,
    Footer,
    CommentArea
  }
}
</script>

<style scoped>
.content-container {
  margin: 20px;
}

.full-screen-layout {
  height: 80vh; /* 设置高度为视口高度，以填充整个屏幕 */
}

.demo-image .block {
  padding: 70px 0;
  text-align: center;
  border-right: solid 1px var(--el-border-color);
  display: inline-block;
  width: 40%;
  box-sizing: border-box;
  vertical-align: top;
}
</style>