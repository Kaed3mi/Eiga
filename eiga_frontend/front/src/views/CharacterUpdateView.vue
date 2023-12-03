<template>
  <el-container class="container_style">
    <el-aside width="200px">
      <VerticalMenu></VerticalMenu>
    </el-aside>
    <el-main>
      <div class="main_full_flex_style">
        <div class="main_width">
          <CharacterUpdate></CharacterUpdate>
          <Footer/>
        </div>
      </div>
    </el-main>
  </el-container>
</template>

<script lang="ts">
import VerticalMenu from '../components/VerticalMenu.vue';
import CharacterUpdate from '../components/CharacterUpdate.vue';
import Footer from "../components/Footer.vue";

export default {
  name: "Character_update",
  components: {
    Footer,
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