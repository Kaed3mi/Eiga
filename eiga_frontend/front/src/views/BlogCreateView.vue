<template>
  <el-container class="container_style">
    <el-aside width="200px">
      <VerticalMenu></VerticalMenu>
    </el-aside>
    <el-main>
      <div class="main_full_flex_style">
        <div class="main_width">
          <BlogCreateItem></BlogCreateItem>
          <Footer/>
        </div>
      </div>
    </el-main>
  </el-container>
</template>

<script>
import VerticalMenu from "../components/VerticalMenu.vue";
import BlogCreateItem from "../components/BlogCreateItem.vue";
import Footer from "../components/Footer.vue";

export default {
  name: "BlogCreateView",
  components: {
    Footer,
    VerticalMenu,
    BlogCreateItem
  }
}
</script>

<style scoped>
</style>