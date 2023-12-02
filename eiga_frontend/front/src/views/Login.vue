<template>
  <el-container class="container_style">
    <el-aside width="200px">
      <VerticalMenu></VerticalMenu>
    </el-aside>
    <el-main>
      <div class="main_full_flex_style">
        <div style="width: var(--main-width)">
          <UserLogin></UserLogin>
          <Footer/>
        </div>
      </div>
    </el-main>
  </el-container>
</template>

<script lang="ts">
import UserLogin from '../components/UserLogin.vue'
import VerticalMenu from "../components/VerticalMenu.vue";
import Footer from "../components/Footer.vue";

export default {
  name: "Login",
  components: {
    UserLogin,
    VerticalMenu,
    Footer
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