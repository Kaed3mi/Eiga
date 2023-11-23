<template>
    <hr>
    <h1>信息修改页面</h1>
    <hr>
    <UserInfoUpdate></UserInfoUpdate>
</template>
   
<script lang="ts">
  import UserInfoUpdate from '../components/UserInfoUpdate.vue'
  export default {
    name: "Login",
    components: {
        UserInfoUpdate
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