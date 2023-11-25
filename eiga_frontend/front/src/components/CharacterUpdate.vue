<template>

    <el-card class="box-card" style="min-width: 800px;">
    <el-row>
      <el-col :span="8">
        <el-upload class="avatar-uploader" :show-file-list="false" :data="{}" :before-upload="beforeImageUpload">
        <img v-if="imageUrl" :src="imageUrl" class="avatar" />
        <el-icon v-else class="avatar-uploader-icon">
            <Plus />
        </el-icon>
    </el-upload>
    <el-button
          @click.prevent="submit"
        >
          submit
        </el-button>
      </el-col>
      <el-col :span="1">
      </el-col>
      <el-col :span="15">
        <el-table :data="tableData" @cell-click="editCell">
    <el-table-column
      v-for="(column, index) in tableColumns"
      :key="index"
      :prop="column.prop"
      :label="column.label"
    >
     <template #default="scope">
        <div v-if="scope.row.editing === scope.column.property" class="editable-cell">
          <el-input v-model="scope.row[scope.column.property]" @blur="updateValue(scope)" />
        </div>
        <div v-else>
          {{ scope.row[column.prop] }}
        </div>
      </template>
    </el-table-column>
    <el-table-column fixed="right" label="Operations" width="120">
      <template #default="scope">
        <el-button
          link
          type="primary"
          size="small"
          @click.prevent="deleteRow(scope.$index)"
        >
          Remove
        </el-button>
      </template>
    </el-table-column>
  </el-table>
  <el-button @click="addRow">Add Row</el-button>
        <h4 style="text-align: left;">introduce</h4>
        <el-input v-model="intoduction" :autosize="{ minRows: 2, maxRows: 20 }" type="textarea" placeholder="Please input" >
    </el-input>
      </el-col>
    </el-row>
  </el-card>

</template>
  
<script lang="ts" setup>
import { onMounted, ref } from 'vue'
import { useRoute } from 'vue-router'
import http from "../utils/http.ts";
import { Plus } from '@element-plus/icons-vue'
import type { UploadProps } from 'element-plus'
import { ElMessage } from 'element-plus'

const intoduction = ref('')
const route = useRoute()
const imageUrl = ref('')
const tableData =  ref([
      ])
const tableColumns = ref([
        { label: 'label', prop: 'label' },
        { label: 'content', prop: 'content' },
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
      const newRow = { id: tableData.value.length + 1, name: '', age: '', editing: 'name' };
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
    )
    })
    .catch((error) => {
      console.error('Error converting URL to Base64:', error);
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