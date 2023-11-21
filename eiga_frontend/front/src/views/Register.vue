<template>
    <hr>
    <h1>注册页面</h1>
    <hr>
    <UserInfoInput></UserInfoInput>
    <VerticalMenu></VerticalMenu>

</template>
   
<script>
  import http from "../utils/http";
  import UserInfoInput from '../components/UserInfoInput.vue'
  import VerticalMenu from '../components/VerticalMenu.vue'
  export default {
    name: "Register",
    components: {
      UserInfoInput,
      VerticalMenu
    },
  }
</script>
   
<style scoped></style>