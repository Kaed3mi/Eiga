<template>
  <el-container>
        <el-aside width="200px"><VerticalMenu></VerticalMenu></el-aside>
        <el-main><BlogCreateItem></BlogCreateItem></el-main>
  </el-container>
</template>

<script>
import VerticalMenu from "../components/VerticalMenu.vue";
import BlogCreateItem from "../components/BlogCreateItem.vue";

export default {
  name: "BlogCreateView",
  components: {
    VerticalMenu,
    BlogCreateItem
  }
}
</script>

<style scoped>

</style>