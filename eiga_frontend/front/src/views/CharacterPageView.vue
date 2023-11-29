<template>
    <el-container>
      <el-container>
        <el-aside width="200px"><VerticalMenu></VerticalMenu></el-aside>
        <el-main><CharacterInfo></CharacterInfo></el-main>
      </el-container>
    </el-container>
</template>

<script lang="ts">
import CharacterInfo from '../components/CharacterInfo.vue';
import VerticalMenu from '../components/VerticalMenu.vue';
export default {
    name: "characterInfo",
    component: {
        VerticalMenu,
        CharacterInfo
    },
    components: { 
        VerticalMenu,
        CharacterInfo 
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