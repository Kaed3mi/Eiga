<template>
  <el-container class="container_style">
    <el-aside width="200px">
      <VerticalMenu></VerticalMenu>
    </el-aside>
    <el-main>
      <div class="main_full_flex_style">
        <div style="width: var(--bangumi-width) ">
      <BangumiCreate></BangumiCreate>
        </div>
      </div>
    </el-main>
  </el-container>
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