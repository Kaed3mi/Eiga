<template>
  <el-row>
    <el-col
        v-for="(character, index) in characters"
        :key="index"
        :span="4"
        :offset="index > 0 ? 2 : 0"
    >
      <el-card :body-style="{ padding: '0px' }">
        <img
            src="https://lain.bgm.tv/r/400/pic/crt/l/e3/2f/18101_crt_343At.jpg?r=1410320023"
            class="image"
        />
        <div style="padding: 14px">
          <span>{{ character.character_name}}</span>
          <div class="bottom">
            <el-button text class="button">
              <router-link :to="'/character/'+ character.id">Check</router-link>
            </el-button>
          </div>
        </div>
      </el-card>
    </el-col>
  </el-row>
</template>

<script lang="ts">
import axios from "axios";
import http from "../utils/http";

export default {
  props: ['id'],
  data() {
    return {
      characters: []
    }
  },
  mounted() {
    this.bangumiQuery(); // 在组件挂载后调用 fetchData 方法
  },
  methods: {
    bangumiQuery() {
      http.get(
          "http://127.0.0.1:8000/bangumi_character_query/",
          {
            params: {
              "bangumi_id": this.id,
            }
          }
      ).then(response => {
        this.characters = response.data.characters;
      })
          .catch(error => {
            console.error('Error fetching data:', error);
          });
    }
  },
  name: "Login",
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
