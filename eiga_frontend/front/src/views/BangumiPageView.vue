<template>
  <div class="full-screen-layout">
    <el-container>
      <el-aside width="200px">
        <VerticalMenu/>
      </el-aside>
      <el-container>
        <el-header><p :style="{ fontSize: '24px' }">{{ bangumi_name }}</p></el-header>
        <el-divider border-style="dashed"/>
        <el-container>
          <el-aside>
            <div class="demo-image">
              <el-image
                  style="width: 300px; height: 400px"
                  :src="'https://lain.bgm.tv/r/400/pic/cover/l/78/c9/55770_HsJfh.jpg'"
                  :fit="cover"
              />
            </div>
            <el-rate
                v-model="bangumi_score"
                disabled
                show-score
                text-color="#ff9900"
                score-template="{value} points"
                :colors="rate_colors"
            />
            <br/>
            你的评分：
            <br/>
            <el-rate
                v-model="user_score"
                allow-half
                show-score
                text-color="#ff9900"
                :score-template="Number(user_score) !== -1 ? Number(user_score).toFixed(1)+ 'points' : ''"
                :colors="rate_colors"
            />
          </el-aside>

          <el-main>
            简介：
            {{ bangumi_intro }}
            <el-divider border-style="dashed"/>
            角色
            <CharacterCard :id=bangumi_id></CharacterCard>
            <el-divider border-style="dashed"/>
            <div v-if="bangumi_relationships.length > 0">
              <h3>关联番组</h3>
              <el-row
                  :gutter="20"
              >
                <el-col :span="24" v-for="(result, index) in bangumi_relationships" :key="index">
                  <ListItem type="bangumi" :id="result.bangumi_id.bangumi_id" :name="result.bangumi_id.bangumi_name"
                            :description="0"
                            :image="''"></ListItem>
                </el-col>
              </el-row>
              <el-divider border-style="dashed"/>
            </div>
            <div v-if="comments.length > 0">
              <h3>评论</h3>
              <el-row
                  :gutter="20"
              >
                <el-col :span="24" v-for="(result, index) in comments" :key="index">
                  <CommentItem :comment_id="result.comment_id"></CommentItem>
                </el-col>
              </el-row>
              <el-divider border-style="dashed"/>
            </div>
          </el-main>

        </el-container>

        <el-footer>Footer</el-footer>
      </el-container>
    </el-container>
  </div>
</template>

<script lang="ts">
import VerticalMenu from '../components/VerticalMenu.vue'
import CharacterCard from '../components/CharacterCard.vue'
import http from "../utils/http";
import ListItem from '../components/ListItem.vue'
import CommentItem from "../components/CommentItem.vue";
import {ref} from 'vue'

export default {
  data() {
    return {
      bangumi_id: this.$route.params.bangumiId,
      bangumi_intro: "No introduction",
      bangumi_name: "Untitled",
      bangumi_score: 0,
      user_score: ref(-1),
      rate_colors: ref(['#99A9BF', '#F7BA2A', '#FF9900']),
      bangumi_relationships: [],
      comments: []
    }
  },
  mounted() {
    this.bangumiQuery(); // 在组件挂载后调用 fetchData 方法
    this.bangumiCommentQuery();
    this.bangumiRelationShipQuery();
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
        this.bangumi_score = response.data.bangumi_score;
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
            'bangumi_id': item.bangumi_id,
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
      })
          .catch(error => {
            console.error('Error fetching data:', error);
          });
    }
  },
  name: "Login",
  components: {
    CommentItem,
    VerticalMenu,
    CharacterCard,
    ListItem
  }
}
</script>

<style scoped>
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