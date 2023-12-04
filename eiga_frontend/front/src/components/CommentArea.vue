<template>
  <div v-if="comments.length > 0">
    <h3>评论</h3>
    <el-row
        :gutter="20"
    >
      <el-col :span="24" v-for="(result, index) in comments" :key="index">
        <CommentItem :comment_id="result.comment_id" @delete-comment = refresh></CommentItem>
      </el-col>
    </el-row>
    <el-divider border-style="dashed"/>
  </div>
  <div v-else>
    <el-text size="small">评论区空空如也~</el-text>
    <el-divider border-style="dashed"/>
  </div>
  <div v-if="user_id!=null &&String(user_id)!==''">
    <el-card>
      <el-row>
        <div class="main_left_style">
          <el-avatar :src="avatar" :size="32" style="margin-left: -0px;" class="avatar"/>
        </div>
      </el-row>
      <div style="padding: 8px"></div>
      <el-input
          v-model="new_comment_area"
          maxlength="400"
          :autosize="{ minRows: 4, maxRows: 6 }"
          placeholder="畅所欲言..."
          show-word-limit
          type="textarea"
          rows="3"
          clearable
      >
      </el-input>
      <div style="padding: 8px"></div>
      <el-button :icon="Position" type="primary" @click=commentInsert>
        发送评论
      </el-button>
    </el-card>
  </div>
  <div v-else>
    <p>登录后即可发表评论</p>
  </div>
</template>
<script lang="ts" setup>
import {
  Position
} from '@element-plus/icons-vue'
</script>

<script lang="ts">
import CommentItem from "../components/CommentItem.vue";
import {ref} from "vue";
import http from "../utils/http.js";
import {ElNotification} from "element-plus";

export default {
  name: "CommentArea",
  data() {
    return {
      comments: [],
      new_comment_area: ref(''),
      user_name: '',
      avatar: '',
      user_id: ref(''),
    }
  },
  props: {
    object_type: {
      type: String,
      required: true
    },
    object_id: {
      type: Number,
      required: true
    }
  },
  components: {CommentItem},
  mounted() {
    this.commentSearch();
    this.user_id = ref(localStorage.getItem('user_id'))
    if (this.user_id != null) {
      this.userQuery();
    }
  },
  methods: {
    userQuery() {
      http.post(
          "http://127.0.0.1:8000/user_query/",
          {'user_id': localStorage.getItem("user_id")}
      ).then(response => {
        this.user_name = response.data.username
        this.avatar = `data:image/png;base64,${response.data.image_data}`
      }).catch(error => {
        console.error('Error fetching data:', error);
      });
    },
    refresh(){
      this.commentSearch()
    },
    commentInsert() {
      http.post(
          'http://127.0.0.1:8000/comment_insert/',
          {
            content: this.new_comment_area,
            time: new Date().getTime(),
            user_id: localStorage.getItem("user_id"),
            bangumi_id: this.object_type === "bangumi" ? this.object_id : '',
            blog_id: this.object_type === "blog" ? this.object_id : '',
            character_id: this.object_type === "character" ? this.object_id : '',
          },
      ).then(response => {
        console.log("submitted comment")
        ElNotification({
          title: '操作成功',
          message: '已发送评论',
          type: 'success',
        })
        this.new_comment_area = ref('')
        this.commentSearch()
      }).catch(error => {
        alert("评论失败")
        console.error('Error posting data:', error);
      });
    },
    commentSearch() {
      this.comments = []
      http.get(
          "http://127.0.0.1:8000/comment_search/",
          {
            params: {
              bangumi_id: this.object_type === "bangumi" ? this.object_id : null,
              blog_id: this.object_type === "blog" ? this.object_id : null,
              character_id: this.object_type === "character" ? this.object_id : null,
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
          }
      ).catch(error => {
        console.error('Error fetching data:', error);
      });
    }
  }
}
</script>

<style scoped>

</style>