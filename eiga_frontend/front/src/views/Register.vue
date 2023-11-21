<template>
    <hr>
    <h1>注册页面</h1>
    <hr>
    <UserInfoInput></UserInfoInput>
    <!-- <el-form ref="ruleFormRef" :model="ruleForm" status-icon :rules="rules"  class="ruleForm">
      <el-form-item label="用户账号" prop="pass">
        <el-input v-model="username" class="inputBar" placeholder="Please input" clearable></el-input>
      </el-form-item>
      <el-form-item label="设置密码" prop="checkPass">
        <el-input v-model="passwd1" class="inputBar" type="password" placeholder="Please input password" show-password/>
      </el-form-item>
      <el-form-item label="确认密码" prop="checkPass">
        <el-input v-model="passwd2" class="inputBar" type="password" placeholder="Please input password again" show-password/>
      </el-form-item>
      <el-form-item>
        <el-button type="primary" @click="submitForm(ruleFormRef)">
          <a href="/login" @click.prevent="send_post">register</a>
        </el-button>
        <el-button><router-link to="/login">login</router-link></el-button>
      </el-form-item>
    </el-form> -->
  </template>
   
  <script>
  import http from "../utils/http";
  import UserInfoInput from '../components/UserInfoInput.vue'
  export default {
    name: "Register",
    components: {
      UserInfoInput
    },
    data() {
      return {
        username: '',
        passwd1: '',
        passwd2: '',
        info1: '',
        info2: ''
      }
    },
    methods: {
      send_post() {
        http.post("http://127.0.0.1:8000/vue/", {
              username: this.username,
              passwd: this.passwd1,
              passwd2: this.passwd2,
            },
        ).then(response => {
          //console.log(response.data); // 服务端响应的响应体
          if (response.data.state == 'fail1') {
            console.log('注册失败')
            this.info1 = response.data.tip
            this.info2 = ''
            alert("用户名已存在")
          } else if (response.data.state == 'fail2') {
            this.info1 = ''
            this.info2 = response.data.tip
          } else {
            window.location.href = "/login"
          }
        }).catch(error => {
          console.log('请求错误！error=', error)
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