<template>
  <el-container class="container_style">
    <el-aside width="200px">
      <VerticalMenu></VerticalMenu>
    </el-aside>
    <el-main>
      <div class="main_full_flex_style">
        <div class="bangumi_width">
          <!-- <el-divider border-style="dashed"/> -->
          <el-container class="row-content">
            <CharacterInfo></CharacterInfo>
          </el-container>
          <Footer></Footer>
        </div>
      </div>
    </el-main>
  </el-container>
</template>

<script lang="ts">
import CharacterInfo from '../components/CharacterInfo.vue';
import VerticalMenu from '../components/VerticalMenu.vue';
import http from '../utils/http';
import Footer from "../components/Footer.vue";

export default {
  name: "characterInfo",
  component: {
    VerticalMenu,
    CharacterInfo
  },
  components: {
    Footer,
    VerticalMenu,
    CharacterInfo
  },
  data() {
    return {
      character_id: this.$route.params.characterId,
      character_name: '',
      imageUrl: '',
      descriptions: [],
      jsonData: {
        attributes: [],
        introduce: '',
        image: '',
        character_name: ''
      },
      response: 'attributes',
      introduce: '',
    };
  },
  mounted() {
    this.characterQuery();
  },
  methods: {
    characterQuery() {
      console.log("i'm character" + this.character_id);
      http.get(
          "http://127.0.0.1:8000/character_query/",
          {
            params: {
              "character_id": this.character_id
            }
          }
      ).then(response => {
        console.log(response.data);
        this.jsonData = response.data
        if (this.jsonData != null) {
          this.character_name = this.jsonData.character_name
          if (this.jsonData.attributes != null) {
            this.descriptions = this.jsonData.attributes
          }
          this.introduce = this.jsonData.introduce
          this.imageUrl = `data:image/png;base64,${this.jsonData.image}`
        }
        console.log("my name is " + this.character_name);

      })
    }
  }
}
</script>


<style scoped>
.container {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.row-content {
  display: flex;
  align-items: center;
  justify-content: center;
}

.inputBar {
  width: 300px;
}

span {
  color: red;
}
</style>