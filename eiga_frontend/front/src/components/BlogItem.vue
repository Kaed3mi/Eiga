<template>
  <el-card :body-style="{ padding: '0px' }">
    <div style="padding: 14px">
      <span>标题：{{ blog_title }}<br/>内容：{{ content }}</span>
      <div class="bottom">
        <el-button text class="button">
          <router-link :to="'/user/'+ user_id.user_id">Check User(user_id:{{ user_id.user_id }})</router-link>
        </el-button>
      </div>
    </div>
  </el-card>
  <div v-if="bangumis.length > 0">
    <h3>关联番组</h3>
    <el-row
        :gutter="20"
    >
      <el-col :span="24" v-for="(result, index) in bangumis" :key="index">
        <ListItem type="bangumi" :id="result.id" :name="result.bangumi_name" :description="0" :image="''"></ListItem>
      </el-col>
    </el-row>
  </div>
</template>

<script lang="ts">
import http from "../utils/http";
import ListItem from "./ListItem.vue";

export default {
  props: ['blog_id'],
  data() {
    return {
      content: '',
      time: '',
      user_id: '',
      blog_title: '',
      bangumis: []
    }
  },
  mounted() {
    this.blogQuery();
    this.blogBangumiQuery();
  },
  methods: {
    blogQuery() {
      console.log("i'm blog#" + this.blog_id)
      http.get(
          "http://127.0.0.1:8000/blog_query/",
          {
            params: {
              "blog_id": this.blog_id,
            }
          }
      ).then(response => {
        this.content = response.data.content;
        this.time = response.data.time;
        this.user_id = response.data.user_id;
        this.blog_title = response.data.blog_title;
      }).catch(error => {
        console.error('Error fetching data:', error);
      });
    },
    blogBangumiQuery() {
      this.bangumis = []
      http.get(
          "http://127.0.0.1:8000/blog_bangumi_query/",
          {
            params: {
              "blog_id": this.blog_id,
            }
          }
      ).then(response => {
        for (let item of response.data.bangumis) {
          this.bangumis.push({
            'bangumi_name': item.bangumi_id.bangumi_name,
            'bangumi_intro': item.bangumi_id.bangumi_intro,
            'bangumi_id': item.bangumi_id.bangumi_id,
            'image': item.bangumi_id.image,
          })
        }
        console.log("this.bangumis")
        console.log(this.bangumis)
      }).catch(error => {
        console.error('Error fetching data:', error);
      });
    },
  },
  name: "BlogItem",
  components: {
    ListItem
  },
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
