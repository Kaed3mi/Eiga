<template>
    <BangumiUpdateVue></BangumiUpdateVue>
</template>
   
<script lang="ts">
import BangumiUpdateVue from '../components/BangumiUpdate.vue';
import VerticalMenu from '../components/VerticalMenu.vue';

export default {
  name: "bangumi_update",
  components: {
      VerticalMenu,
      BangumiUpdateVue
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
</style>