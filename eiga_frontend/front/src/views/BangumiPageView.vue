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
            />
          </el-aside>

          <el-main>
            简介：
            {{ bangumi_intro }}
            <el-divider border-style="dashed"/>
            <CharacterCard :id=1></CharacterCard>
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
import axios from "axios";
import http from "../utils/http";

export default {
  data() {
    return {
      bangumi_id: this.$route.params.bangumiId,
      bangumi_intro: "No introduction",
      bangumi_name: "Untitled",
      bangumi_score: 0
    }
  },
  mounted() {
    this.bangumiQuery(); // 在组件挂载后调用 fetchData 方法
  },
  methods: {
    bangumiQuery() {
      console.log("i'm " + this.bangumi_id)
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
    }
  },
  name: "Login",
  components: {
    VerticalMenu,
    CharacterCard
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