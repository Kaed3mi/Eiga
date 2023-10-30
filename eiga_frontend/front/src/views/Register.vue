<template>
    <hr>
    <h1>注册页面</h1>
    <hr>

    <!-- 用户账号：<input type="text" v-model="username"><span>{{ info1 }}</span><br> -->
    用户账号：
    <el-input v-model="username" class="inputBar" placeholder="Please input" clearable></el-input>
    设置密码：
    <el-input v-model="passwd1" class="inputBar" type="password" placeholder="Please input password" show-password/>
    确认密码：
    <el-input v-model="passwd2" class="inputBar" type="password" placeholder="Please input password again" show-password/>
    <button>
      <a href="/login" @click.prevent="send_post">register</a>
    </button>
    <button>
      <router-link to="/login">login</router-link>
    </button>
  </template>
   
  <script>
  import http from "../utils/http";
  export default {
    name: "Register",
    data() {
      return {
        username: '',
        passwd1: '',
        passwd2: '',
        password1: 'password',
        password2: 'password',
        tip1: '显示密码',
        tip2: '显示密码',
        num1: 0,
        num2: 0,
        info1: '',
        info2: ''
      }
    },
    methods: {
      pwd1() {
        if (this.num1 === 0) {
          this.password1 = 'text'
          this.tip1 = '隐藏密码'
          this.num1 = 1
        } else {
          this.password1 = 'password'
          this.tip1 = '显示密码'
          this.num1 = 0
        }
      },
      pwd2() {
        if (this.num2 === 0) {
          this.password2 = 'text'
          this.tip2 = '隐藏密码'
          this.num2 = 1
        } else {
          this.password2 = 'password'
          this.tip2 = '显示密码'
          this.num2 = 0
        }
      },
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
  * {
    margin: 10px;
  }
  .inputBar {
    max-width: 40%;
  }
  span {
    color: red;
  }
  </style>