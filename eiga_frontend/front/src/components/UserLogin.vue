<template>
  <el-container>
    <el-main>
      <el-image src="src/assets/eiga_title.png" style="width: 600px">
      </el-image>
      <el-divider/>
      <div class="main_flex_style">
        <div style="width: 500px">
          <el-card class="login-content" shadow="always">
            <h3>登录至Eiga</h3>
            <el-form ref="ruleFormRef" :model="ruleForm" status-icon :rules="rules" class="ruleForm">
              <el-form-item label="用户邮箱" prop="pass">
                <el-input v-model="email" class="inputBar" width autocomplete="off" placeholder="请输入您的邮箱"
                          clearable :prefix-icon="Message"/>
              </el-form-item>
              <el-form-item label="登录密码" prop="checkPass">
                <el-input v-model="password" class="inputBar" width type="password" autocomplete="off"
                          placeholder="请输入您的密码" show-password :prefix-icon="Key"/>
              </el-form-item>
              <el-button type="primary" @click.prevent="send_post">
                登录
              </el-button>
              <el-button>
                <router-link :to="{name : 'Register'}">注册</router-link>
              </el-button>
            </el-form>
          </el-card>
        </div>
      </div>
    </el-main>
  </el-container>
</template>

<script>
import http from "../utils/http.ts";
import {ElMessage} from "element-plus";

export default {
  name: "Login",
  data() {
    return {
      email: '',
      password: '',
      tip: '',
      exception: '',
    }
  },
  methods: {
    send_post() {
      http.post("http://127.0.0.1:8000/user_login/", {
            email: this.email,
            password: this.password,
          },
      ).then(response => {
        if (response.data.state === '1') {
          console.log('登录成功')
          this.exception = ''
          this.tip = response.data.tip
          console.log(response.data.user_id)
          console.log(response.data.username)
          console.log(response.data.permission)
          localStorage.setItem("login_status", true);
          localStorage.setItem("user_id", response.data.user_id);
          localStorage.setItem("username", response.data.username);
          localStorage.setItem("permission", response.data.permission);
          window.location.href = "/home"
        } else {
          console.log('登录失败')
          this.exception = response.data.exception
          this.tip = response.data.tip
          if (this.exception === "user_not_exist") {
            alert("用户不存在")
          } else if (this.exception === "password_wrong") {
            alert("密码错误")
          } else {
            alert("其他错误")
          }
        }
      }).catch(error => {
        ElMessage.error('邮箱和密码不匹配！')
        console.log('请求错误!error=', error)
      })
    },
  }
}
</script>
<script setup>
import {
  Message, Key
} from '@element-plus/icons-vue'
</script>

<style scoped>
.login-content {

  display: flex;
  justify-content: center;
  align-items: center;
}

.ruleForm {
  /* max-width: 70%; */
}

span {
  color: red;
}
</style>