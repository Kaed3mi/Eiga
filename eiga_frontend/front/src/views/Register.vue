<template>

    <el-container>
      <el-container>
        <el-aside width="200px"><VerticalMenu></VerticalMenu></el-aside>
        <el-main>
          <el-row >
            <el-col :span="6"></el-col>
            <el-col :span="12"><UserInfoInput></UserInfoInput></el-col>
            <el-col :span="6"></el-col>
          </el-row>
        </el-main>
      </el-container>
    </el-container>
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