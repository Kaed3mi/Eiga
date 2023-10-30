<template>
    <button><router-link to="/reg">register</router-link></button>
    <button><router-link to="/login">login</router-link></button>
    <h3 @click="log">{{ message }}</h3>
    <span>{{ login_message }}</span>
  </template>
   
   
  <!-- 以下为选项API格式 -->
  <script>
  export default {
    name: "Index",
    data() {
      return {
        message: "welcome to INDEX",
        login_message: '登录成功！！！',
      }
    },
    methods: {
      log() {
        console.log(this.message)
      },
    },
  }
  </script>
   
   
  <style scoped>
   
  </style>