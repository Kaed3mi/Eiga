<template>
    <el-container>
      <el-container>
        <el-aside width="200px"><VerticalMenu></VerticalMenu></el-aside>
        <el-main><CharacterUpdate></CharacterUpdate></el-main>
      </el-container>
    </el-container>
</template>
   
<script lang="ts">
import VerticalMenu from '../components/VerticalMenu.vue';
import CharacterUpdate from '../components/CharacterUpdate.vue';
export default {
  name: "Character_update",
  components: {
    CharacterUpdate,
      VerticalMenu
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