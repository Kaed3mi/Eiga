<template>
  <el-card class="box-card">
    <el-container>
      <el-main>
        <h2>新日志</h2>
        <el-divider></el-divider>
        <div class="center-container">

          <el-container>
            <el-main :style="{ width: '60%' }">
              <h3>标题</h3>
              <el-input
                  v-model="new_title_area"
                  maxlength="20"
                  placeholder="您的标题..."
                  show-word-limit
                  rows="3"
                  clearable
              >
              </el-input>
              <h3>正文</h3>
              <el-input
                  v-model="new_blog_area"
                  maxlength="2000"
                  :autosize="{ minRows: 16, maxRows: 20 }"
                  placeholder="畅所欲言..."
                  show-word-limit
                  type="textarea"
                  rows="3"
                  clearable
              >
              </el-input>

            </el-main>
            <el-main :style="{ width: '40%' }">
              <h3>关联番组</h3>
              <el-row :gutter="20">
                <el-col :span="24">
                  <el-table :data="bangumiTable" style="width: auto" max-height="250">
                    <el-table-column prop="bangumi_id" label="ID"/>
                    <el-table-column prop="bangumi_name" label="番组名"/>
                    <el-table-column label="操作">
                      <template #default="scope">
                        <el-button
                            round
                            plain
                            type="warning"
                            @click.prevent="deleteBangumiRow(scope.$index)">
                          <el-icon>
                            <Delete/>
                          </el-icon>
                          &nbsp;
                          移除
                        </el-button>
                      </template>
                    </el-table-column>
                  </el-table>
                </el-col>
              </el-row>
              <div
                  style="
                    display: grid;
                    margin-top: 10px;
                    grid-template-columns: 60% 40%;
                    grid-gap: 8px;
                  "
              >

                <el-autocomplete
                    v-model="selectedResultBangumi"
                    :fetch-suggestions="querySearchBangumi"
                    placeholder="请输入内容"
                    :trigger-on-focus="false"
                    clearable
                    @select="onSelectBangumi">
                </el-autocomplete>
                <el-button plain class="mt-4" type="primary" @click="onAddBangumi">
                  <el-icon>
                    <Plus/>
                  </el-icon>
                  添加番组
                </el-button>
              </div>
              <el-divider border-style="dashed"/>

            </el-main>
          </el-container>
        </div>
        <div class="submit_button">
          <el-button :icon="Finished" type="success" @click="submitUpdate">
            创建条目
          </el-button>
        </div>
      </el-main>
    </el-container>
  </el-card>
</template>

<script lang="ts" setup>
import {Plus, Delete, Finished} from '@element-plus/icons-vue'
</script>

<script lang="ts">
import {ref} from "vue";
import http from "../utils/http.js";
import {ElMessage, ElNotification} from "element-plus";

export default {
  name: "BlogCreateItem",
  data() {
    return {
      new_blog_area: ref(''),
      new_title_area: ref(''),
      selectedResultBangumi: null,
      bangumiTable: [],
      bangumiObject: {
        bangumi_id: null,
        bangumi_name: null,
        intro: ""
      },
      searchResults: [],
      searchBangumiResults: []
    }
  },
  methods: {
    blogInsert() {

    },
    querySearchBangumi(query: string, cb: any) {
      console.log(query);
      console.log(this.searchResults);
      if (query) {
        http.get(
            "http://127.0.0.1:8000/bangumi_select/",
            {
              params: {
                "keyword": query
              }
            }
        ).then(response => {
          console.log("response: " + response.data);
          this.searchBangumiResults = response.data
          console.log("searchResults" + this.searchResults);
          cb(this.searchBangumiResults);
        })
      }
    },
    deleteBangumiRow(index) {
      this.bangumiTable.splice(index, 1);
    },
    onAddBangumi() {
      if (this.bangumiObject) {
        console.log({"bangumi_id": this.bangumiObject.bangumi_id, "bangumi_name": this.bangumiObject.value});
        this.bangumiTable.push({"bangumi_id": this.bangumiObject.bangumi_id, "bangumi_name": this.bangumiObject.value})
      }
    },
    onSelectBangumi(bangumi: any) {
      this.bangumiObject = bangumi
      this.selectedResultBangumi = bangumi.value
      if (this.selectedResultBangumi != null) {
        console.log(this.selectedResultBangumi);
      }
    },
    submitUpdate() {
      if (String(this.new_title_area) === '') {
        ElNotification({
          title: '格式错误',
          message: '标题不可为空',
          type: 'warning',
        })
        return
      }
      if (String(this.new_blog_area) === '') {
        ElNotification({
          title: '格式错误',
          message: '正文不可为空',
          type: 'warning',
        })
        return
      }
      let bangumi_id_list = []
      for (let item of this.bangumiTable) {
        bangumi_id_list.push(item.bangumi_id)
      }
      http.post(
          "http://127.0.0.1:8000/blog_insert/", {
            blog_title: this.new_title_area,
            content: this.new_blog_area,
            time: new Date().getTime(),
            user_id: localStorage.getItem("user_id"),
            bangumis: bangumi_id_list
          }
      ).then(response => {
        ElNotification.success({
          title: '创建成功',
          message: '已创建日志\"' + this.new_title_area + '\"',
          type: 'success',
        })
        this.$router.push("/blog/"+response.data.blog_id)
      })
    }
  }
}
</script>

<style scoped>
.center-container {
  display: flex;
  width: 100%;
  justify-content: center;
  align-items: center;
}

.submit_button {
  display: flex;
  flex-direction: column;
  align-items: center;
}
</style>