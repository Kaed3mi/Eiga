<template>
  <el-card :body-style="{ padding: '0px' }">
    <img
        :src="avatar"
        class="image"
    />
    <div style="padding: 14px">
      <span>{{ user_id.user_name }}:{{ content }}</span>
      <div class="bottom">
        <el-button text class="button">
          <router-link :to="'/user/'+ user_id.user_id">Check</router-link>
        </el-button>
      </div>
    </div>
  </el-card>
</template>

<script lang="ts">
import axios from "axios";
import http from "../utils/http";

export default {
  props: ['comment_id'],
  data() {
    return {
      content: '',
      time: '',
      user_id: '',
      bangumi_id: '',
      blog_id: '',
      character_id: ''
    }
  },
  mounted() {
    this.commentQuery(); // 在组件挂载后调用 fetchData 方法
  },
  methods: {
    commentQuery() {
      console.log("i'm " + this.comment_id)
      http.get(
          "http://127.0.0.1:8000/comment_query/",
          {
            params: {
              "comment_id": this.comment_id,
            }
          }
      ).then(response => {
        this.content = response.data.content;
        this.time = response.data.time;
        this.user_id = response.data.user_id;
        this.bangumi_id = response.data.bangumi_id;
        this.blog_id = response.data.blog_id;
        this.character_id = response.data.character_id;
      })
          .catch(error => {
            console.error('Error fetching data:', error);
          });
    }
  },
  name: "CommentItem",
}

</script>

<style>
.time {
  font-size: 12px;
  color: #999;
}

.bottom {
  margin-top: 13px;
  line-height: 12px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.button {
  padding: 0;
  min-height: auto;
}

.image {
  width: 100%;
  display: block;
}
</style>
