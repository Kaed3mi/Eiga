<template>

  <el-container class="container_style">
    <el-aside width="200px">
      <VerticalMenu></VerticalMenu>
    </el-aside>

    <el-main>
      <div class="main_full_flex_style">
        <div class="main_width">
          <!-- 左侧导航栏 -->
          <h2>番组排行</h2>
          <el-divider></el-divider>
          <div class="bangumi_rank">
            <el-row>
              <el-col
                  v-for="key in bangumiList.slice((page-1)*RANK_PAGE_SIZE, page*RANK_PAGE_SIZE)"
                  :key="key"
                  :span="12"
              >

                <el-card
                    style="max-width: 800px;min-height: 50px; margin: 10px;position: relative;"
                >
                  <div v-if="key.bangumi_rank===1" class="medal">
                    <el-image src="/src/assets/medal_gold_icon.png"/>
                  </div>
                  <div v-else-if="key.bangumi_rank===2" class="medal">
                    <el-image src="/src/assets/medal_silver_icon.png"/>
                  </div>
                  <div v-else-if="key.bangumi_rank===3" class="medal">
                    <el-image src="/src/assets/medal_bronze_icon.png"/>
                  </div>
                  <div class="tag">
                    <el-tag size="large" round plain type="primary">
                      <p style="font-size: 13px"> Rank {{ key.bangumi_rank }}</p>
                    </el-tag>
                  </div>
                  <div class="main_flex_style" style="width: 100%;height: 20vh;">
                    <el-row :gutter="15" style="width: 100%;">
                      <el-col :span="9">
                        <div class="main_flex_style" style="height: 100%">

                          <el-image
                              style="width: 100%; height: auto"
                              :src="key.image"
                              fit="cover"
                          />
                        </div>
                      </el-col>
                      <el-col :span="15">
                        <div class="main_flex_style" style="height: 100%">
                          <router-link :to="{ name: 'bangumi-view', params: { bangumiId: key.bangumi_id }}">
                            <el-descriptions :title="key.bangumi_name" width="300px" :column="1">
                              <el-descriptions-item>

                              </el-descriptions-item>
                              <el-descriptions-item>
                                <div class="main_flex_style">
                                  <el-rate
                                      v-model="key.bangumi_score"
                                      disabled
                                      show-score
                                      text-color="#ff9900"
                                      :score-template="Number(key.bangumi_score).toFixed(1)+'分'"
                                  />
                                  &nbsp;({{ key.rater_cnt }}人)
                                </div>
                              </el-descriptions-item>
                            </el-descriptions>
                          </router-link>
                        </div>
                      </el-col>
                    </el-row>
                  </div>
                </el-card>


              </el-col>
            </el-row>
          </div>
          <el-divider></el-divider>
          <!--翻页-->
          <el-row>
            <el-container class="row-content">
              <el-pagination
                  :current-page="Number(page)"
                  background layout="prev, pager, next, jumper, total"
                  :page-size="RANK_PAGE_SIZE"
                  :total="this.total"
                  @current-change="currentChange"/>
            </el-container>
          </el-row>
          <Footer/>
        </div>
      </div>
    </el-main>
  </el-container>
</template>

<script>
import VerticalMenu from "../components/VerticalMenu.vue";
import ListItem from "../components/ListItem.vue";
import http from "../utils/http";
import {ElMessage} from "element-plus";
import Footer from "../components/Footer.vue";

export default {
  components: {ListItem, VerticalMenu, Footer},
  data() {
    return {
      page: this.$route.params.page ? this.$route.params.page : 1,
      RANK_PAGE_SIZE: 8,
      total: 0,
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
  props: {},
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
        for (let bangumi of response.data.bangumis) {
          this.bangumiList.push({
            'bangumi_rank': bangumi.bangumi_rank,
            'bangumi_id': bangumi.bangumi_id,
            'bangumi_name': bangumi.bangumi_name,
            'bangumi_score': bangumi.bangumi_score,
            'rater_cnt': bangumi.bangumi_rater_cnt,
            'image': `data:image/png;base64,${bangumi.image}`,
          })
        }
        this.total = response.data.total
        console.log("response: " + response.data);
      }).catch(error => {
        ElMessage.error('页数过大！')
      });
    },
    currentChange(nextPage) {
      this.$router.push({name: 'rank', params: {page: nextPage}});
    },
  }
};
</script>

<style>
.row-content {
  display: flex;
  align-items: center;
  justify-content: center;
}

.medal {
  position: absolute;
  z-index: 100;
  right: -5px; /* Adjust the top position as needed */
  bottom: -5px; /* Adjust the right position as needed */
  width: 15%
}

.tag {
  position: absolute;
  z-index: 100;
  right: 10px; /* Adjust the top position as needed */
  top: 10px; /* Adjust the right position as needed */
  width: 15%
}
</style>