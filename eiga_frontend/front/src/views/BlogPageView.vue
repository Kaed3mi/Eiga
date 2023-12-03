<template>
  <el-container class="container_style">
    <el-aside width="200px">
      <VerticalMenu></VerticalMenu>
    </el-aside>
    <el-main>
      <div class="main_full_flex_style">
        <div class="main_width">
          <BlogItem :blog_id="this.$route.params.blogId"></BlogItem>
        </div>
      </div>
    </el-main>
  </el-container>
</template>

<script>
import VerticalMenu from '../components/VerticalMenu.vue';
import BlogItem from '../components/BlogItem.vue';

export default {
  name: "BlogPageView",
  components: {
    VerticalMenu,
    BlogItem
  }
}
</script>

<style scoped>

</style>