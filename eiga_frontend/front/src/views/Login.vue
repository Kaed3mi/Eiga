<template>
  <el-container style="height: 100%">
    <el-aside width="200px"><VerticalMenu></VerticalMenu></el-aside>
    <el-main>
      <el-container class="container">
        <el-header></el-header>
        <el-main>
          <UserLogin></UserLogin>
        </el-main>
      </el-container>
    </el-main>
  </el-container>
</template>
   
<script lang="ts">
import UserLogin from '../components/UserLogin.vue'
import VerticalMenu from "../components/VerticalMenu.vue";
export default {
  name: "Login",
  components: {
    UserLogin,
    VerticalMenu
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
.container {
  display: flex;
  align-items: center;
  justify-content: center;
}
</style>