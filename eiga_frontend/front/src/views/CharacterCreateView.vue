<template>
    <VerticalMenu></VerticalMenu>
    <CharacterCreate></CharacterCreate>
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