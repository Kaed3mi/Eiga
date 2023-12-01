<template>

  <el-container style="height: 100vh;">
    <el-container>
      <el-aside width="200px">
        <VerticalMenu></VerticalMenu>
      </el-aside>
      <el-main>
        <div class="main_full_flex_style">
          <div style="width: var(--main-width)">
            <UserInfoInput></UserInfoInput>
          </div>
        </div>
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