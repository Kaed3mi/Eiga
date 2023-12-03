<template>
  <el-card class="box-card" style="">
    <h2>更新日志</h2>
    <el-divider></el-divider>
    <div class="main_flex_style">

      <el-row gutter="15" style="width: 90%;">
        <el-col :span="14">
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

        </el-col>
        <el-col :span="10">
          <h3>关联番组</h3>
          <el-row :gutter="20">
            <el-col :span="24">
              <el-table :data="bangumiTable" style="width: auto" max-height="250">
                <el-table-column prop="bangumi_id" label="ID"/>
                <el-table-column prop="bangumi_name" label="Name"/>
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
                      移除
                    </el-button>
                  </template>
                </el-table-column>
              </el-table>
            </el-col>
          </el-row>
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
          <el-divider border-style="dashed"/>

        </el-col>
      </el-row>
    </div>
    <div class="submit_button" style="padding: 24px">
      <el-row>
        <el-button type="primary" @click="submitUpdate">
          更新日志
        </el-button>
        <el-popover :visible="delete_visible" placement="top" :width="160">
          <div class="main_flex_style">
            <p>确定要删除吗?</p>
          </div>
          <div class="main_flex_style">
            <el-button size="small" text @click="delete_visible = false">取消</el-button>
            <el-button size="small" type="primary" @click="delete_visible = false; blogDelete()"
            >确认
            </el-button
            >
          </div>
          <template #reference>
            <el-button type="danger" @click="delete_visible = true">
              删除日志
            </el-button>
          </template>
        </el-popover>

      </el-row>
    </div>
  </el-card>
</template>

<script lang="ts" setup>
import {Plus, Delete} from '@element-plus/icons-vue'
</script>

<script lang="ts">
import {ref} from "vue";
import http from "../utils/http.js";
import {ElNotification,ElMessage} from 'element-plus'

export default {
  props: ['blog_id'],
  name: "BlogCreateItem",
  data() {
    return {
      delete_visible: false,
      new_blog_area: ref(''),
      new_title_area: ref(''),
      time: '',
      user_id: null,
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
  mounted() {
    this.blogQuery();
    this.blogBangumiQuery();
  },
  methods: {
    blogQuery() {
      console.log("i'm blog#" + this.blog_id)
      http.get(
          "http://127.0.0.1:8000/blog_query/",
          {
            params: {
              "blog_id": this.blog_id,
            }
          }
      ).then(response => {
        this.new_blog_area = ref(response.data.content);
        this.time = response.data.time;
        this.user_id = response.data.user_id;
        this.new_title_area = ref(response.data.blog_title);
      }).catch(error => {
        console.error('Error fetching data:', error);
      });
    },
    blogDelete() {
      http.delete(
          "http://127.0.0.1:8000/blog_delete/",
          {
            params: {
              "blog_id": this.blog_id,
            }
          }
      ).then(response => {
        ElMessage.success('已删除日志')
      }).catch(error => {
        ElMessage.error('操作失败')
        console.error('Error fetching data:', error);
      });
    },
    blogBangumiQuery() {
      this.bangumiTable = []
      http.get(
          "http://127.0.0.1:8000/blog_bangumi_query/",
          {
            params: {
              "blog_id": this.blog_id,
            }
          }
      ).then(response => {
        for (let item of response.data.bangumis) {
          this.bangumiTable.push({
            'bangumi_name': item.bangumi_id.bangumi_name,
            'bangumi_intro': item.bangumi_id.bangumi_intro,
            'bangumi_id': item.bangumi_id.bangumi_id,
            'image': item.bangumi_id.image,
          })
        }
        console.log("this.bangumis")
        console.log(this.bangumiTable)
      }).catch(error => {
        console.error('Error fetching data:', error);
      });
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
      http.put(
          "http://127.0.0.1:8000/blog_update/", {
            blog_id: this.blog_id,
            blog_title: this.new_title_area,
            content: this.new_blog_area,
            time: new Date().getTime(),
            user_id: localStorage.getItem("user_id"),
          }
      )
      http.put(
          "http://127.0.0.1:8000/blog_bangumi_update/", {
            blog_id: this.blog_id,
            bangumis: bangumi_id_list
          }
      )
      ElNotification({
        title: '更新成功',
        message: '已提交日志\"' + this.new_title_area + '\"的更新',
        type: 'success',
      })
    }
  }
}
</script>

<style scoped>
.center-container {
  display: flex;
  width: 1000px;
  justify-content: center;
  align-items: center;
}

.submit_button {
  display: flex;
  flex-direction: column;
  align-items: center;
}
</style>