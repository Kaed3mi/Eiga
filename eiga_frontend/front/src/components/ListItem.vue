<template>
  <div style="padding: 1%"></div>
  <el-card :body-style="{ padding: '1.5%' }" style="position: relative">
    <div v-if="rank" class="tag">
      <el-tag size="large" round plain type="primary">
        <p style="font-size: 13px"> Rank {{ rank }}</p>
      </el-tag>
    </div>
    <div class="main_left_style">
      <el-container>
        <el-aside width="120px">
          <el-card v-if="image" :body-style="{ padding: '3px' }" style="width: 110px">
            <el-image :src="image" fit="cover" style="width: 100px; height: auto;;margin-bottom: -5px"/>
          </el-card>

        </el-aside>
        <el-main>
          <el-row>
            <div class="main_left_style">
              <el-icon style="margin-top:2px;margin-right: 5px">
                <Component :is="getIcon(type)"></Component>
              </el-icon>
              <router-link :to="'/'+type +'/'+ id">
                <el-button link plain type="primary" class="button">

                  {{ name }}

                </el-button>
              </router-link>
            </div>
          </el-row>
          <div v-if="description">
            <div style="padding: 3px"></div>
            <el-row>
              <div class="main_left_style" style="width: 250px;">
                <el-text truncated>{{ description }}</el-text>
              </div>
            </el-row>
          </div>
          <div v-if="relation">
            <div style="padding: 3px"></div>
            <el-row>
              <div class="main_left_style" style="width: 250px;">
                <el-icon style="margin-top:2px;margin-right: 5px">
                  <Connection/>
                </el-icon>
                <el-text truncated>{{ relation }}</el-text>
              </div>
            </el-row>
          </div>
          <div v-if="score">
            <div style="padding: 3px"></div>
            <el-row>
              <div class="main_left_style" style="width: 250px;">
                <el-rate
                    v-model="score_model"
                    size="small"
                    disabled
                    show-score
                    text-color="#ff9900"
                    score-template="{value} 分"
                />
                <el-text> &nbsp;({{ rater_cnt }}人)</el-text>
              </div>
            </el-row>
          </div>
        </el-main>
      </el-container>

    </div>
  </el-card>
</template>

<script lang="ts" setup>
import {
  Connection, Calendar

} from '@element-plus/icons-vue'
</script>

<script lang="ts">
import {
  User, Film, Avatar, Notebook

} from '@element-plus/icons-vue'
import axios from "axios";
import http from "../utils/http";

export default {
  props: ['type', 'id', 'name', 'image', 'description', 'rank', 'score', 'rater_cnt', 'relation', 'date'],
  data() {
    return {
      score_model: this.score,
      characters: []
    }
  },
  methods: {
    getIcon(type: String) {
      if (type === "user") {
        return Avatar;
      } else if (type === "bangumi") {
        return Film;
      } else if (type === "character") {
        return User;
      } else if (type === "blog") {
        return Notebook;
      }
    }
  },
  name: "ListItem",
}

</script>

<style>
.item-card {
  max-height: 150px;
  min-width: 700px;
}

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

.tag {
  position: absolute;
  z-index: 100;
  right: 20px; /* Adjust the top position as needed */
  top: 20px; /* Adjust the right position as needed */
  width: 15%
}
</style>
