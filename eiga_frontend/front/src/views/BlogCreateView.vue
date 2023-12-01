<template>
  <el-container style="height: 100vh;">
    <el-aside width="200px">
      <VerticalMenu></VerticalMenu>
    </el-aside>
    <el-main>
      <div class="main_full_flex_style">
        <div style="width: var(--main-width)">
          <BlogCreateItem></BlogCreateItem>
        </div>
      </div>
    </el-main>
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