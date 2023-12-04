<template>
  <el-image src="src/assets/eiga_title.png" style="width: 600px">
  </el-image>
  <el-divider/>
  <div class="main_flex_style">
    <div style="width: 600px">
      <el-card class="login-content" shadow="always">
        <h3>注册成为Eiga会员</h3>
        <br/>
        <el-row gutter="30" style="width: 100%">
          <el-col :span="18">
            <el-form
                ref="ruleFormRef"
                :model="ruleForm"
                :rules="rules"
                label-width="120px"
                class="demo-ruleForm"
                :size="formSize"
                status-icon
            >
              <el-form-item label="用户名" prop="username">
                <el-input v-model="ruleForm.username" placeholder="请输入用户名"
                          :prefix-icon="User"/>
              </el-form-item>

              <el-form-item label="邮箱:" prop="email">
                <el-input v-model="ruleForm.email" placeholder="请输入邮箱" clearable="true"
                          :prefix-icon="Message"/>
              </el-form-item>

              <el-form-item label="密码" prop="password">
                <el-input v-model="ruleForm.password" placeholder="请输入密码" type="password" show-password="true"
                          :prefix-icon="Key"/>
              </el-form-item>

              <el-form-item label="确认密码" prop="password_confirm">
                <el-input v-model="ruleForm.password_confirm" placeholder="请确认密码" type="password"
                          show-password="true" :prefix-icon="Key"/>
              </el-form-item>

              <el-form-item label="管理员" prop="Admin">
                <el-switch v-model="ruleForm.Admin"/>
              </el-form-item>
            </el-form>
          </el-col>
          <el-col :span="6">
            <el-upload
                class="avatar-uploader"
                action=""
                :show-file-list="false"
                :on-success="handleAvatarSuccess"
                :before-upload="beforeAvatarUpload"
            >
              <img v-if="imageUrl" :src="imageUrl" class="avatar"/>
              <el-icon v-else class="avatar-uploader-icon">
                <Plus/>
              </el-icon>
            </el-upload>
          </el-col>
        </el-row>
        <div class="main_flex_style">
          <el-form-item>
            <el-button type="primary" @click="submitForm(ruleFormRef)">注册</el-button>
            <el-button @click="resetForm(ruleFormRef)">清空</el-button>
            <el-button @click="this.$router.push({ name: 'Login' });">
              已有账户？
            </el-button>
          </el-form-item>
        </div>
      </el-card>
    </div>
  </div>
</template>

<script lang="ts" setup>
import {getCurrentInstance, reactive, ref} from 'vue'
import { useRouter } from "vue-router"
import type {FormInstance, FormRules} from 'element-plus'
import http from "../utils/http.ts";
import {Plus, Message, Key, User} from '@element-plus/icons-vue'
import type {UploadProps} from 'element-plus'
import { ElMessage } from 'element-plus'

interface RuleForm {
  username: string
  email: string
  password: string
  password_confirm: string
  Admin: boolean
}
const router = useRouter()
const formSize = ref('default')
const ruleFormRef = ref<FormInstance>()
const ruleForm = reactive<RuleForm>({
  username: '',
  email: '',
  password: '',
  password_confirm: '',
  Admin: false
})


const imageUrl = ref('')

// const handleAvatarSuccess: UploadProps['onSuccess'] = (
//   response,
//   uploadFile
// ) => {
//     imageUrl.value = URL.createObjectURL(uploadFile.raw!)
// }

const beforeAvatarUpload: UploadProps['beforeUpload'] = (rawFile) => {
  if (rawFile.type !== 'image/jpeg') {
    ElMessage.error('Avatar picture must be JPG format!')
    return false
  } else if (rawFile.size / 1024 / 1024 > 2) {
    ElMessage.error('Avatar picture size can not exceed 2MB!')
    return false
  } else {
    imageUrl.value = URL.createObjectURL(rawFile)
    return true
  }
}

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
        ElMessage.success("注册成功")
        router.push('/login');
      } else {
        ruleForm.password = ''
        ruleForm.password_confirm = ''
        ElMessage.warning("密码不一致")
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
    console.log("the password isn't the same")
    return false;
  }
}

const send_post = () => {
  if (imageUrl.value === '') {
    http.post("http://127.0.0.1:8000/user_register/", {
          username: ruleForm.username,
          password: ruleForm.password,
          email: ruleForm.email,
          permission: ruleForm.Admin ? "admin" : "user",
          image: "default"
        },
    )
  } else {
    urlToBase64(imageUrl.value).then(
        (base64) => {
          http.post("http://127.0.0.1:8000/user_register/", {
                username: ruleForm.username,
                password: ruleForm.password,
                email: ruleForm.email,
                permission: ruleForm.Admin ? "admin" : "user",
                image: base64
              },
          )
        }
    )
  }
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