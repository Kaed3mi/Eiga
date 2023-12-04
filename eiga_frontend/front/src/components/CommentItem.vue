<template>
  <div style="padding: 1%"></div>
  <el-card :body-style="{ padding: '20px' }" style="position: relative">
    <div v-if="isEditable()">
      <el-button :icon="Delete" size="small" plain type="danger" class="delete_button" @click="commentDelete">
      </el-button>
    </div>
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
<script lang="ts" setup>
import {Delete} from '@element-plus/icons-vue'
</script>
<script lang="ts">
import axios from "axios";
import http from "../utils/http";
import {format} from 'date-fns';
import {ElMessage, ElNotification} from "element-plus";

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
      avatar: '',
      deleted: false
    }
  },
  mounted() {
    this.commentQuery(); // 在组件挂载后调用 fetchData 方法
  },
  computed: {

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
    },
    commentDelete() {
      http.delete(
          "http://127.0.0.1:8000/comment_delete/",
          {
            params: {
              "comment_id": this.comment_id,
            }
          }
      ).then(response => {
        ElNotification({
          title: '删除成功',
          message: '已删除用户\"' + this.user_id.user_name + '的评论\"',
          type: 'success',
        })
        this.$emit('delete-comment', this.comment_id)
      }).catch(error => {
        ElMessage.error('操作失败')
        console.error('Error fetching data:', error);
      });
    },
    isEditable() {
      let user_id = localStorage.getItem("user_id")
      let permission = localStorage.getItem("permission")
      return (
        user_id && (permission === "admin" || user_id == this.user_id.user_id)
      );
    },
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

.delete_button {
  z-index: 100;
  position: absolute;
  top: 15px; /* Adjust the top position as needed */
  right: 20px; /* Adjust the right position as needed */
}
</style>
