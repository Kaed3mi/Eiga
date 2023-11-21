<template>
    <hr>
    <h1>登录页面</h1>
    <hr>
    <UserLogin></UserLogin>
</template>
   
<script lang="ts">
  import http from "../utils/http";
  import UserLogin from '../components/UserLogin.vue'
  export default {
    name: "Login",
    components: {
      UserLogin
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