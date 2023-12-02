<template>
  <el-row gutter="20">
    <el-col
        v-for="(character, index) in characters"
        :key="index"
        :span="6"
    >

      <el-card :body-style="{ padding: '8px'}" style="height: 100%;position: relative">
        <el-container style="display: flex;flex-direction: column;">
          <div>
            <el-card :body-style="{ padding: '2px'}">
              <el-image style="width: 100%;margin-bottom: -5px"
                        :src="character.image"
                        class="image"
              />
            </el-card>
          </div>
          <div style="flex-grow: 1;
              display: flex;
              flex-direction: column;
              justify-content: center;
              align-items: center;
              margin-top: 10px;"
          >
          </div>
          <div>
            <el-row>
              <div style="padding: 4px;"></div>
              <div class="main_flex_style" style="width: 100%">
                <el-icon style="margin-top:2px;margin-right: 5px">
                  <User/>
                </el-icon>
                <router-link :to="'/character/'+ character.character_id">
                  <el-button link plain type="primary" class="button">
                    <div>
                      {{ character.character_name }}
                    </div>
                  </el-button>
                </router-link>
              </div>
            </el-row>
          </div>
        </el-container>
      </el-card>

    </el-col>
  </el-row>
</template>

<script lang="ts" setup>
import {
  User
} from '@element-plus/icons-vue'
</script>

<script lang="ts">
import axios from "axios";
import http from "../utils/http";

export default {
  props: ['id'],
  data() {
    return {
      imageUrl: '',
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
        // this.characters = response.data.characters;
        console.log(response.data.characters);
        for (let item of response.data.characters) {
          console.log("item: " + item.id + item.character_name);
          http.get(
              "http://127.0.0.1:8000/character_query/",
              {
                params: {
                  "character_id": item.id
                }
              }
          ).then(
              response => {
                this.characters.push({
                  "character_id": item.id,
                  "character_name": item.character_name,
                  "image": `data:image/png;base64,${response.data.image}`
                })
                // console.log(response.data);
                // console.log(response.data.introduce);
              }
          )
        }
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

.absolute_row {
  position: absolute;
  z-index: 100;
  left: 15%;
  bottom: 20px; /* Adjust the right position as needed */
  width: 15%
}
</style>
