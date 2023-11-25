<template>
  <el-form
      ref="ruleFormRef"
      :model="ruleForm"
      :rules="rules"
      label-width="120px"
      class="demo-ruleForm"
      :size="formSize"
      status-icon
  >

    <el-form-item label="用户名:" prop="username">
      <el-input v-model="ruleForm.username" placeholder="请输入昵称"/>
    </el-form-item>

    <el-form-item label="邮箱:" prop="email">
      <el-input v-model="ruleForm.email" placeholder="请输入邮箱" clearable="true"/>
    </el-form-item>

    <el-form-item label="密码" prop="password">
      <el-input v-model="ruleForm.password" placeholder="请输入密码" type="password" show-password="true"/>
    </el-form-item>

    <el-form-item label="确认密码" prop="password_confirm">
      <el-input v-model="ruleForm.password_confirm" placeholder="请确认密码" type="password" show-password="true"/>
    </el-form-item>

    <el-form-item label="Instant delivery" prop="delivery">
      <el-switch v-model="ruleForm.delivery"/>
    </el-form-item>

    <el-form-item>
      <el-button type="primary" @click="submitForm(ruleFormRef)">Create</el-button>
      <el-button @click="resetForm(ruleFormRef)">Reset</el-button>
    </el-form-item>
  </el-form>

  <el-upload
      class="avatar-uploader"
      action="http://127.0.0.1:8000/upload_avatar/"
      :show-file-list="false"
      :data="{ email: ruleForm.email, customField2: '22222' }"
      :on-success="handleAvatarSuccess"
      :before-upload="beforeAvatarUpload"
  >
    <img v-if="imageUrl" :src="imageUrl" class="avatar"/>
    <el-icon v-else class="avatar-uploader-icon">
      <Plus/>
    </el-icon>
  </el-upload>

  <!-- <img :src="imageU" alt="My Image"> -->
</template>

<script lang="ts" setup>
import {onMounted, reactive, ref} from 'vue'
import {FormInstance, FormRules} from 'element-plus'
import http from "../utils/http.ts";
import {Plus} from '@element-plus/icons-vue'
import type {UploadProps} from 'element-plus'
import defaultIcon from '../assets/default.jpg'

interface RuleForm {
  username: string
  email: string
  password: string
  password_confirm: string
}

const formSize = ref('default')
const ruleFormRef = ref<FormInstance>()
const ruleForm = reactive<RuleForm>({
  username: '',
  email: '',
  password: '',
  password_confirm: '',
})

import {ElMessage} from 'element-plus'

const imageUrl = ref('')
const imageU = ref('')

const handleAvatarSuccess: UploadProps['onSuccess'] = (
    response,
    uploadFile
) => {
  imageUrl.value = URL.createObjectURL(uploadFile.raw!)
  console.log(response);
  if (response.state === '1') {
    console.log("saving the icon");
    console.log(response.image_data);
    imageU.value = `data:image/png;base64,${response.image_data}`
  }
}

const beforeAvatarUpload: UploadProps['beforeUpload'] = (rawFile) => {
  if (rawFile.type !== 'image/jpeg') {
    ElMessage.error('Avatar picture must be JPG format!')
    return false
  } else if (rawFile.size / 1024 / 1024 > 2) {
    ElMessage.error('Avatar picture size can not exceed 2MB!')
    return false
  } else {
    console.log(ruleForm.email)
    if (ruleForm.email === '') {
      console.log("Please input email")
      return false;
    }
    return true
  }
}

const getData = () => {
  http.post(
      "http://127.0.0.1:8000/user_query/",
      {user_id: localStorage.getItem("user_id")},
  ).then(
      response => {
        console.log(response.data)
        ruleForm.email = response.data.email
        ruleForm.password = response.data.password
        ruleForm.password_confirm = response.data.password
        ruleForm.username = response.data.username
        if (response.data.avatar === 'default') {
          console.log("using default icon");
          imageUrl.value = defaultIcon
        } else {
          console.log("using user's icon");
          imageUrl.value = `data:image/png;base64,${response.data.image_data}`
        }
      }
  )
}
onMounted(getData)
const rules = reactive<FormRules<RuleForm>>({
  username: [
    {required: true, message: 'Please input your username', trigger: 'blur'},
    {min: 4, max: 20, message: 'Name length should be 4 to 20', trigger: 'blur'},
  ],
  email: [
    {required: true, message: 'Please input your email address', trigger: 'change'},
    {type: 'email', message: "Invaild email address formate", trigger: 'change'}
  ],
  password: [
    {required: true, message: 'Please input your password', trigger: 'blur'},
    {min: 5, max: 30, message: 'Password length should be 5 to 30', trigger: 'blur'}
  ],
  password_confirm: [
    {required: true, message: 'Please repeat your password', trigger: 'blur'},
    {min: 5, max: 30, message: 'Password length should be 5 to 30', trigger: 'blur'}
  ],
})

const submitForm = async (formEl: FormInstance | undefined) => {
  if (!formEl) return
  await formEl.validate((valid, fields) => {
    if (valid) {
      if (checkPassword()) {
        console.log('submit!')
        send_post()
      } else {
        ruleForm.password = ''
        ruleForm.password_confirm = ''
      }
    } else {
      console.log('error submit!', fields)
    }
  })
}

const resetForm = (formEl: FormInstance | undefined) => {
  if (!formEl) return
  formEl.resetFields()
}

const checkPassword = () => {
  if (ruleForm.password == ruleForm.password_confirm) {
    console.log("password is the same")
    return true;
  } else {
    alert("the password isn't the same")
    return false;
  }
}

const send_post = () => {
  http.post("http://127.0.0.1:8000/user_register/", {
        username: ruleForm.username,
        password: ruleForm.password,
        email: ruleForm.email,
      },
  )
}
</script>

<style scoped>
.avatar-uploader {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 120px;
  height: 120px;
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