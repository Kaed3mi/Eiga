<template>
  <VerticalMenu></VerticalMenu>
  <BlogCreateItem></BlogCreateItem>
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