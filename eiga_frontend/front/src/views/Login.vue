<template>
    <hr>
    <h1>登录页面</h1>
    <hr>
    账号：<input type="text" v-model="username"><span>{{ info3 }}</span><br>
    密码：<input :type="password" v-model="passwd">
    <button @click="pwd">{{ tip }}</button>
    <span>{{ info4 }}</span>
    <br>
    <button>
      <a href="/" @click.prevent="send_post">login</a>
    </button>
    <button>
      <router-link to="/reg">register</router-link>
    </button>
  </template>
   
  <script>
  import http from "../utils/http.ts";
   
  export default {
    name: "Login",
    data() {
      return {
        username: '请输入用户名',
        passwd: '请输入密码',
        password: 'password',
        tip: '显示密码',
        num: 0,
        info3: '',
        info4: '',
      }
    },
    methods: {
      pwd() {
        if (this.num === 0) {
          this.password = 'text'
          this.tip = '隐藏密码'
          this.num = 1
        } else {
          this.password = 'password'
          this.tip = '显示密码'
          this.num = 0
        }
      },
      send_post() {
        console.log("hahaha")
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
   
  span {
    color: red;
  }
  </style>