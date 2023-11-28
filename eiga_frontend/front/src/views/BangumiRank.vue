<template>
  <div>
    <!-- 左侧导航栏 -->
    <div class="vertical-menu">
      <VerticalMenu/>
    </div>
    <el-row
        v-for="(key, index) in bangumiList"
        :key="key"
        :span="8"
    >
      <el-card
          style="width: 450px; height: 240px; margin: 10px"
      >
        <el-row>
          <el-col :span="8">
            <el-image
                style="width: 150px; height: 200px"
                :src="key.image"/>
          </el-col>
          <el-col :span="1"></el-col>
          <el-col :span="15">
            <router-link :to="{ name: 'bangumi-view', params: { bangumiId: key.bangumi_id }}">
              <el-descriptions :title="key.bangumi_name" width="300px" :column="1">
                <el-descriptions-item>
                  Rank {{ key.bangumi_rank }}
                </el-descriptions-item>
                <el-descriptions-item>
                  评分 {{ key.bangumi_score }} ({{ key.rater_cnt }}人评分)
                </el-descriptions-item>
              </el-descriptions>
            </router-link>
          </el-col>
        </el-row>
      </el-card>
    </el-row>

    <!--    <router-link :to="{ name: 'rank', params: { page: page + 1 } }">下一页</router-link>-->

  </div>
</template>

<script>
import VerticalMenu from "../components/VerticalMenu.vue";
import ListItem from "../components/ListItem.vue";
import http from "../utils/http";
import {ElMessage} from "element-plus";

export default {
  components: {ListItem, VerticalMenu},
  data() {
    return {
      page: this.$route.params.page ? this.$route.params.page : 1,
      bangumiList: [],
    };
  },
  mounted() {
    this.bangumi_rank_query();
  },
  // 用户同路由跳转更新，不能删。
  beforeRouteUpdate(to, from, next) {
    this.page = to.params.page; // 更新 user_id
    this.bangumi_rank_query();
    next();
  },
  methods: {
    bangumi_rank_query() {
      this.bangumiList = []
      http.get(
          "http://127.0.0.1:8000/bangumi_rank_query/",
          {
            params: {
              'page': this.page,
            }
          }
      ).then(response => {
        console.log(response.data.bangumis)
        let rank_cnt = this.page * 5 - 4
        for (let bangumi of response.data.bangumis) {
          this.bangumiList.push({
            'bangumi_rank': rank_cnt,
            'bangumi_id': bangumi.bangumi_id,
            'bangumi_name': bangumi.bangumi_name,
            'bangumi_score': bangumi.bangumi_score,
            'rater_cnt': bangumi.bangumi_rater_cnt,
            'image': `data:image/png;base64,${bangumi.image}`,
          })
          rank_cnt = rank_cnt + 1
        }
        console.log("response: " + response.data);
      }).catch(error => {
        ElMessage.error('页数过大！')
      });

    }
  }
};
</script>
