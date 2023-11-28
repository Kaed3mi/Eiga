<template>
  <div class="common-layout">
    <el-container>
      <el-container>
        <el-aside width="200px"><VerticalMenu></VerticalMenu></el-aside>
        <el-main><BangumiCreate></BangumiCreate></el-main>
      </el-container>
    </el-container>
  </div>
</template>
<script lang="ts">
import VerticalMenu from '../components/VerticalMenu.vue';
import BangumiCreate from '../components/BangumiCreate.vue';
export default {
  name: "Bangumi_create",
  components: {
    VerticalMenu,
    BangumiCreate
  }
}
</script>
   
   
<style scoped>
.container {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.inputBar {
  width: 300px;
}
span {
  color: red;
}
</style>