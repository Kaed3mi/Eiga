<template>

  <el-card class="box-card" style="">
    <h2>创建角色</h2>
    <el-divider></el-divider>
    <el-row :gutter="10">
      <el-col :span="9">
        <div class="main_flex_style">
          <el-upload class="avatar-uploader" :show-file-list="false" :data="{}" :before-upload="beforeImageUpload">
            <el-image v-if="imageUrl" :src="imageUrl" class="avatar"/>
            <el-icon v-else class="avatar-uploader-icon">
              <Plus/>
            </el-icon>
          </el-upload>
        </div>

      </el-col>
      <el-col :span="15">
        <h4 style="text-align: left;">角色名</h4>
        <el-input v-model="character_name" placeholder="请输入角色名" clearable/>
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
                &nbsp;
                移除
              </el-button>
            </template>
          </el-table-column>
        </el-table>
        <el-button plain type="primary" @click="addRow" style="margin: 12px">
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
    <el-button @click.prevent="submit" :icon="Finished" type="success" style="margin-top: 20px">
      创建条目
    </el-button>
  </el-card>

</template>

<script lang="ts" setup>
import {onMounted, ref} from 'vue'
import http from "../utils/http.ts";
import {Plus, Delete, Finished} from '@element-plus/icons-vue'
import type {UploadProps} from 'element-plus'
import {ElMessage, ElNotification} from 'element-plus'
import defaultImage from '../assets/character_default.jpg'
import {useRoute} from 'vue-router'
import router from "../utils/router";

const route = useRoute()
const intoduction = ref('')
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
  imageUrl.value = defaultImage
  // console.log(route.params.characterId);
  // http.get(
  //     "http://127.0.0.1:8000/character_query/",
  //     {
  //         params: {
  //             "character_id": route.params.characterId
  //         }
  //     }
  // ).then(
  //     response => {
  //         console.log(response.data);
  //         console.log(response.data.introduce);
  //         imageUrl.value = `data:image/png;base64,${response.data.image}`
  //         intoduction.value = response.data.introduce
  //         tableData.value = response.data.attributes
  //     }
  // )
}
onMounted(fetchData)

const editCell = (row, column) => {
  row.editing = column.property;
}
const updateValue = (scope) => {
  scope.row.editing = '';
}

const addRow = () => {
  const newRow = {};
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
        console.log('正在创建');
        http.post(
            "http://127.0.0.1:8000/character_create/", {
              character_name: character_name.value,
              attributes: tableData.value,
              introduction: intoduction.value,
              image: base64
            }
        ).then((response) => {
          console.log('创建成功');
          ElNotification({
            title: '创建成功',
            message: '已创建角色\"' + character_name.value + '\"',
            type: 'success',
          })
          router.push("/character/" + response.data.character_id)
        }).catch((error) => {
          console.log('创建失败');
          ElMessage.error('创建失败！', error)
        })
      }).catch((error) => {
    ElMessage.error('Error converting URL to Base64:', error);
  });
}

async function urlToBase64(url: any) {
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
  width: 250px;
  height: 400px;
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