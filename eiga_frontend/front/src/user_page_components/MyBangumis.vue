<template>
  <div class="bangumi_rank">
    <el-row>
      <el-col
          :span="6"
          v-for="(key, index) in bangumiList"
          :key="key">
        <el-card
            style="width: 140px; height: 240px; margin: 30px"
        >
          <el-col>
            <el-row>
              <el-image
                  style="width: 100px; height: 134px"
                  :src="key.image"/>
            </el-row>
            <el-row>
              <router-link :to="{ name: 'bangumi-view', params: { bangumiId: key.bangumi_id }}">
                <el-text class="w-80px" type="primary" truncated>{{ key.bangumi_name }}</el-text>
                <el-text type="info">用户评分：</el-text>
                <el-text type="success"> {{ key.my_score }}</el-text>
              </router-link>
            </el-row>
          </el-col>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script>
import http from "../utils/http";
import {ElMessage} from "element-plus";

export default {
  name: "MyBangumis",
  data() {
    return {
      bangumiList: [],
    };
  },
  mounted() {
    this.myBangumiQuery();
  },
  props: {
    user_id: {}
  },
  methods: {
    myBangumiQuery() {
      this.bangumiList = []
      http.get(
          "http://127.0.0.1:8000/my_bangumi_query/",
          {
            params: {
              'user_id': this.user_id,
            }
          }
      ).then(response => {
        console.log(response.data.bangumis)
        for (let bangumi of response.data.bangumis) {
          this.bangumiList.push({
            'bangumi_id': bangumi.bangumi_id,
            'bangumi_name': bangumi.bangumi_name,
            'my_score': bangumi.my_score,
            'image': `data:image/png;base64,${bangumi.image}`,
          })
        }
        console.log("response: " + response.data);
      }).catch(error => {
        ElMessage.error('怎么出错了')
      });
    },
  }
}
</script>

<style scoped>
.w-80px {
  width: 110px;
}
</style>