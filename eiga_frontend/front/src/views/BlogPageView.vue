<template>
  <VerticalMenu></VerticalMenu>
  <BlogItem :blog_id="this.$route.params.blogId"></BlogItem>
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