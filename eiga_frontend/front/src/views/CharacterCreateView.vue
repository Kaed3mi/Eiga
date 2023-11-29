<template>
    <el-container>
      <el-container>
        <el-aside width="200px"><VerticalMenu></VerticalMenu></el-aside>
        <el-main><CharacterCreate></CharacterCreate></el-main>
      </el-container>
    </el-container>
</template>
   
<script lang="ts">
import VerticalMenu from '../components/VerticalMenu.vue';
import CharacterCreate from '../components/CharacterCreate.vue'
export default {
  name: "Character_create",
  components: {
    VerticalMenu,
    CharacterCreate
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