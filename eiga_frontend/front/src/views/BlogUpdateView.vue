<template>
  <VerticalMenu></VerticalMenu>
  <BlogUpdateItem :blog_id="this.$route.params.blogId"></BlogUpdateItem>
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