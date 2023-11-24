<template>
    <VerticalMenu></VerticalMenu>
    <CharacterInfo></CharacterInfo>
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

<style>

</style>
