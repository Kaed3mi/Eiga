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
            :src="character.image"
            class="image"
        />
        <div style="padding: 14px">
          <span>{{ character.character_name}}</span>
          <div class="bottom">
            <el-button text class="button">
              <router-link :to="'/character/'+ character.character_id">Check</router-link>
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
</style>
