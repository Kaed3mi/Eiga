<template>
  <div class="full-screen-layout">
    <el-container>
      <el-aside width="200px">
        <VerticalMenu/>
      </el-aside>
      <el-container>
        <el-header><p :style="{ fontSize: '24px' }">搜索内容</p></el-header>
        <el-divider border-style="dashed"/>
        <el-container>
          <el-main>
            <div class="mt-4">
              <el-input
                  v-model="search_input"
                  placeholder="Please input"
                  class="input-with-select"
                  size="large"
                  clearable style="width: 700px"
              >
                <template #prepend>
                  <el-select v-model="search_type" placeholder="Select" style="width: 115px">
                    <el-option label="全部" value="1"/>
                    <el-option label="番组" value="2"/>
                    <el-option label="角色" value="3"/>
                    <el-option label="用户" value="4"/>
                  </el-select>
                </template>
                <template #append>
                  <el-button :icon="search_icon" @click="search"/>
                </template>
              </el-input>
            </div>
            <div v-if="search_results.length > 0">
              <h3>搜索结果：</h3>
              <el-row
                  :gutter="20"
              >
                <el-col :span="24" v-for="(result, index) in search_results" :key="index">
                  <ListItem :type="result.type" :id="result.id" :name="result.name" :description="0" :image="''"></ListItem>
                </el-col>
              </el-row>
            </div>
          </el-main>
        </el-container>
        <el-footer>
          Footer
        </el-footer>
      </el-container>
    </el-container>
  </div>
</template>

<script lang="ts">
import VerticalMenu from '../components/VerticalMenu.vue'
import ListItem from '../components/ListItem.vue'
import {ref} from 'vue'
import {Search} from '@element-plus/icons-vue'
import http from "../utils/http";

export default {
  data() {
    return {
      search_type: null,
      search_input: ref(''),
      search_icon: Search,
      search_results: [],
    }
  },
  name: "DiscoveringPageView",
  components: {
    VerticalMenu,
    ListItem
  },
  methods: {
    search() {
      this.search_results = []
      if (this.search_type == 2) {
        this.bangumi_search()
      } else if (this.search_type == 3) {
        this.character_search()
      } else if (this.search_type == 4) {
        this.user_search()
      } else if (this.search_type == 1) {
        this.user_search()
        this.character_search()
        this.bangumi_search()
      }

    },
    bangumi_search() {
      http.get(
          "http://127.0.0.1:8000/bangumi_search/",
          {
            params: {
              "pattern": this.search_input,
            }
          }
      ).then(response => {
        for (let item of response.data.bangumis) {
          this.search_results.push({type: "bangumi",id: item.id, name: item.name})
        }
      })
          .catch(error => {
            console.error('Error fetching data:', error);
          });
    },
    character_search() {
      http.get(
          "http://127.0.0.1:8000/character_search/",
          {
            params: {
              "pattern": this.search_input,
            }
          }
      ).then(response => {
        for (let item of response.data.characters) {
          this.search_results.push({type: "character",id: item.id, name: item.name})
        }
        console.log(this.search_results)
      })
          .catch(error => {
            console.error('Error fetching data:', error);
          });
    },
    user_search() {
      http.get(
          "http://127.0.0.1:8000/user_search/",
          {
            params: {
              "pattern": this.search_input,
            }
          }
      ).then(response => {
        for (let item of response.data.users) {
          this.search_results.push({type: "user",id: item.id, name: item.name})
        }
        console.log(this.search_results)
      })
          .catch(error => {
            console.error('Error fetching data:', error);
          });
    }
  },
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