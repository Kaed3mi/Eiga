<template>
  <el-card class="box-card" style="min-width: 800px;">
    <h2>修改角色: {{ character_name }}</h2>
    <el-divider></el-divider>
    <el-row :gutter="10">
      <el-col :span="9">
        <el-upload class="avatar-uploader" :show-file-list="false" :data="{}" :before-upload="beforeImageUpload">
          <img v-if="imageUrl" :src="imageUrl" class="avatar"/>
          <el-icon v-else class="avatar-uploader-icon">
            <Plus/>
          </el-icon>
        </el-upload>


      </el-col>
      <el-col :span="15">
        <h4 style="text-align: left;">角色属性</h4>
        <el-table :data="tableData" @cell-click="editCell">
          <el-table-column
              v-for="(column, index) in tableColumns"
              :key="index"
              :prop="column.prop"
              :label="column.label"
          >
            <template #default="scope">
              <div v-if="scope.row.editing === scope.column.property" class="editable-cell">
                <el-input v-model="scope.row[scope.column.property]" @blur="updateValue(scope)"/>
              </div>
              <div v-else>
                {{ scope.row[column.prop] }}
              </div>
            </template>
          </el-table-column>
          <el-table-column fixed="right" label="操作" width="120">
            <template #default="scope">
              <el-button
                  round
                  plain
                  type="warning"
                  @click.prevent="deleteRow(scope.$index)"
              >
                <el-icon>
                  <Delete/>
                </el-icon>
                移除
              </el-button>
            </template>
          </el-table-column>
        </el-table>
        <el-button plain type="primary" @click="addRow">
          <el-icon>
            <Plus/>
          </el-icon>
          &nbsp;
          添加属性
        </el-button>
        <h4 style="text-align: left;">简介</h4>
        <el-input v-model="intoduction" :autosize="{ minRows: 2, maxRows: 20 }" type="textarea"
                  placeholder="请输入简介">
        </el-input>
      </el-col>
    </el-row>
    <el-divider border-style="dashed"/>
    <div class="main_flex_style">
      <el-row>
        <el-button :icon="Select" type="primary" @click.prevent="submit">
          提交更改
        </el-button>
        <el-popover :visible="delete_visible" placement="top" :width="160">
          <div class="main_flex_style">
            <p>确定要删除吗?</p>
          </div>
          <div class="main_flex_style">
            <el-button size="small" text @click="delete_visible = false">取消</el-button>
            <el-button size="small" type="primary" @click="delete_visible = false; characterDelete()"
            >确认
            </el-button
            >
          </div>
          <template #reference>
            <el-button :icon="Delete" type="danger" @click="delete_visible = true">
              删除条目
            </el-button>
          </template>
        </el-popover>
      </el-row>
    </div>
  </el-card>

</template>

<script lang="ts" setup>
import {onMounted, ref} from 'vue'
import {useRoute} from 'vue-router'
import http from "../utils/http.ts";
import {Plus, Delete, Select} from '@element-plus/icons-vue'
import type {UploadProps} from 'element-plus'
import {ElMessage, ElNotification} from 'element-plus'
import router from "../utils/router";

const delete_visible = ref(false)
const intoduction = ref('')
const route = useRoute()
const imageUrl = ref('')
const character_name = ref('')
const tableData = ref([])
const tableColumns = ref([
  {label: '属性名', prop: 'label'},
  {label: '属性内容', prop: 'content'},
])

const beforeImageUpload: UploadProps['beforeUpload'] = (rawFile) => {
  if (rawFile.type !== 'image/jpeg') {
    ElMessage.error('Avatar picture must be JPG format!')
    return false
  } else if (rawFile.size / 1024 / 1024 > 2) {
    ElMessage.error('Avatar picture size can not exceed 2MB!')
    return false
  } else {
    imageUrl.value = URL.createObjectURL(rawFile)
  }
}

const fetchData = () => {
  console.log(route.params.characterId);
  http.get(
      "http://127.0.0.1:8000/character_query/",
      {
        params: {
          "character_id": route.params.characterId
        }
      }
  ).then(
      response => {
        console.log(response.data);
        console.log(response.data.introduce);
        imageUrl.value = `data:image/png;base64,${response.data.image}`
        intoduction.value = response.data.introduce
        character_name.value = response.data.character_name
        tableData.value = response.data.attributes
      }
  )
}
onMounted(fetchData)

const editCell = (row, column) => {
  row.editing = column.property;
}
const updateValue = (scope) => {
  scope.row.editing = '';
}

const addRow = () => {
  const newRow = {id: tableData.value.length + 1, name: '', age: '', editing: 'name'};
  tableData.value.push(newRow);
}

const deleteRow = (index) => {
  tableData.value.splice(index, 1);
}

const submit = () => {
  console.log(tableData.value);
  console.log(intoduction.value);
  console.log(imageUrl.value);
  urlToBase64(imageUrl.value)
      .then((base64) => {
        console.log('Base64 encoded image:', base64);
        http.post(
            "http://127.0.0.1:8000/character_update/", {
              character_id: route.params.characterId,
              attributes: tableData.value,
              introduction: intoduction.value,
              image: base64
            }
        ).then(response => {
          ElNotification({
            title: '更新成功',
            message: '已更改角色\"' + character_name.value + '\"',
            type: 'success',
          })
          router.push("/character/" + route.params.characterId)
        })
      })
      .catch((error) => {
        console.error('Error converting URL to Base64:', error);
      });
}

const characterDelete = () => {
  http.delete(
      "http://127.0.0.1:8000/character_delete/",
      {
        params: {
          "character_id": route.params.characterId,
        }
      }
  ).then(response => {
    ElNotification({
      title: '删除成功',
      message: '已删除角色\"' + character_name.value + '\"',
      type: 'success',
    })
    router.push("/home")
  }).catch(error => {
    ElMessage.error('操作失败')
    console.error('Error fetching data:', error);
  });
}

async function urlToBase64(url) {
  try {
    const response = await fetch(url);
    const blob = await response.blob();
    const reader = new FileReader();
    reader.readAsDataURL(blob);
    reader.onload = () => {
      const base64 = reader.result;
      console.log(base64);
    };
    return new Promise((resolve, reject) => {
      reader.onload = () => {
        const base64 = reader.result;
        // console.log(base64);

        resolve(base64);
      };
      reader.onerror = (error) => {
        reject(error);
      };
    });
  } catch (error) {
    console.error('Error converting URL to Base64:', error);
  }
}
</script>

<style scoped>
.avatar-uploader {
  display: flex;
  align-items: center;
  justify-content: center;
  width: auto;
  height: auto;
  border: 1px dashed #d9d9d9;
  border-radius: 6px;
  overflow: hidden;
}

.avatar {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.avatar-uploader-icon {
  font-size: 28px;
  color: #8c939d;
}
</style>