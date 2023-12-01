<template>
  <el-container class="container_style">
    <el-aside width="200px">
      <VerticalMenu></VerticalMenu>
    </el-aside>
    <el-main>
      <div class="main_full_flex_style">
        <div style="width: var(--main-width)">
          <CharacterCreate></CharacterCreate>
        </div>
      </div>
    </el-main>
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