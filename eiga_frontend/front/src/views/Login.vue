<template>
    <hr>
    <h1>登录页面</h1>
    <hr>
    <el-form ref="ruleFormRef" :model="ruleForm" status-icon :rules="rules"  class="ruleForm">
      <el-form-item label="用户账号" prop="pass">
        <el-input v-model="username" class="inputBar" width autocomplete="off" placeholder="Please input" clearable/>
      </el-form-item>
      <el-form-item label="登录密码" prop="checkPass">
        <el-input v-model="passwd" class="inputBar" width type="password" autocomplete="off" placeholder="Please input password" show-password/>
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
        username: '',
        passwd: '',
        tip: '',
        info3: '',
        info4: '',
      }
    },
    methods: {
      send_post() {
        http.post("http://127.0.0.1:8000/vue/", {
              username: this.username,
              passwd: this.passwd,
            },
        ).then(response => {
          //console.log(response.data); // 服务端响应的响应体
          if (response.data.state == 'fail3') {
            //console.log('注册失败')
            this.info3 = ''
            this.info4 = response.data.tip
          } else if (response.data.state == 'fail4') {
            this.info3 = response.data.tip
            this.info4 = ''
          } else {
            window.location.href = "/index"
          }
        }).catch(error => {
          console.log('请求错误！error=', error)
        })
      },
    }
  }
  </script>
   
   
  <style scoped>
  * {
    margin: 10px;
  }
  .inputBar {
    width: 300px;
  }
  span {
    color: red;
  }
  </style>