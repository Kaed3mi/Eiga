<template>
  <div style="padding: 1%"></div>
  <el-card :body-style="{ padding: '20px' }" >
    <el-row>
      <div class="main_left_style">
        <el-avatar :src="avatar" :size="24" style="margin-left: -0px;" class="avatar"/>
        <router-link :to="'/user/'+ user_id.user_id">
          <el-button link plain type="primary" class="button">
            <div style=" margin-left: 2px;margin-bottom: 4px">
              {{ user_id.user_name }}
            </div>
          </el-button>
        </router-link>
        <el-text style="font-size: 10px;color:gray">@{{ time }}</el-text>
        <span style="padding: 5px; font-size:14px">{{}}</span>
      </div>
    </el-row>
    <div style="padding: 5px"></div>
    <el-row>
      <div class="main_left_style">
        <p v-for="(line, index) in content.split('\n')" :key="index"
           style="font-size: 14px;text-align: left;white-space: pre-wrap;text-indent: 2em; margin: 0"
        >
          {{ line }}
        </p>
      </div>
    </el-row>
  </el-card>
</template>

<script lang="ts">
import axios from "axios";
import http from "../utils/http";
import {format} from 'date-fns';

export default {
  props: ['comment_id'],
  data() {
    return {
      content: '',
      time: '',
      user_id: '',
      bangumi_id: '',
      blog_id: '',
      character_id: '',
      avatar: ''
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
        this.time = format(response.data.time, "yyyy-MM-dd HH:mm");
        this.user_id = response.data.user_id;
        this.avatar = `data:image/png;base64,${response.data.avatar}`;
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
