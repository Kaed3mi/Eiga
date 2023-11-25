<template>
    <VerticalMenu></VerticalMenu>
    <CharacterUpdate></CharacterUpdate>
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