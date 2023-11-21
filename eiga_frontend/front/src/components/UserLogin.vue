<template>
    <el-form ref="ruleFormRef" :model="ruleForm" status-icon :rules="rules" class="ruleForm">
      <el-form-item label="用户邮箱" prop="pass">
        <el-input v-model="email" class="inputBar" width autocomplete="off" placeholder="Please input" clearable/>
      </el-form-item>
      <el-form-item label="登录密码" prop="checkPass">
        <el-input v-model="password" class="inputBar" width type="password" autocomplete="off" placeholder="Please input password" show-password/>
      </el-form-item>
      <el-form-item>
        <el-button type="primary" @click="submitForm(ruleFormRef)">
          <a href="/" @click.prevent="send_post">login</a>
        </el-button>
        <el-button><router-link to="/reg">register</router-link></el-button>
      </el-form-item>
    </el-form>
</template>
   
  <script>
  import http from "../utils/http.ts";
   
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
          if (response.data.state == '1') {
            console.log('登录成功')
            this.exception = ''
            this.tip = response.data.tip
            window.location.href = "/index"
          } else {
            console.log('登录失败')
            this.exception = response.data.exception
            this.tip = response.data.tip
            if (this.exception == "user_not_exist") {
                alert("用户不存在")
            } else if (this.exception == "password_wrong") {
                alert("密码错误")
            } else {
                alert("其他错误")
            }
          }
        }).catch(error => {
          console.log('请求错误!error=', error)
        })
      },
    }
  }
  </script>
   
   
  <style scoped>
  .inputBar {
    width: 300px;
  }
  span {
    color: red;
  }
  </style>