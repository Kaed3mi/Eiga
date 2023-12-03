<template>
  <el-container class="container_style">
    <el-aside width="200px">
      <VerticalMenu></VerticalMenu>
    </el-aside>
    <el-main>
      <div class="main_full_flex_style">
        <div class="main_width">
          <BlogUpdateItem :blog_id="this.$route.params.blogId"></BlogUpdateItem>
        </div>
      </div>
    </el-main>
  </el-container>
</template>

<script>
import VerticalMenu from "../components/VerticalMenu.vue";
import BlogUpdateItem from "../components/BlogUpdateItem.vue";

export default {
  name: "BlogUpdateView",
  components: {
    VerticalMenu,
    BlogUpdateItem
  }
}
</script>

<style scoped>

</style>