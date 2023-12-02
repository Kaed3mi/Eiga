<template>
  <el-container class="container_style">
    <el-aside width="200px">
      <VerticalMenu/>
    </el-aside>
    <el-main>
      <div class="main_full_flex_style">
        <div style="width: var(--bangumi-width) ">
          <el-card class="box-card" style="">
            <el-container>
              <el-header><h2>{{ bangumi_name }}</h2></el-header>
              <el-divider border-style="dashed"/>
              <el-container>
                <el-aside>
                  <div class="demo-image">
                    <el-upload class="avatar-uploader" :show-file-list="false" :data="{}"
                               :before-upload="beforeImageUpload">
                      <el-image
                          style="width: 300px; height: 400px"
                          v-if="imageUrl" :src="imageUrl"
                          :fit="cover"
                      />
                      <el-icon v-else class="avatar-uploader-icon">
                        <Plus/>
                      </el-icon>
                    </el-upload>
                  </div>
                </el-aside>
                <el-main>
                  <h4 style="text-align: left;"> 简介：</h4>
                  <el-input v-model="bangumi_intro" :autosize="{ minRows: 2, maxRows: 20 }" type="textarea"
                            placeholder="Please input"></el-input>
                  <el-divider border-style="dashed"/>
                  <h3>角色</h3>

                  <el-table :data="characterTable" style="width: auto" max-height="250">
                    <el-table-column prop="character_id" label="ID"/>
                    <el-table-column prop="character_name" label="Name"/>
                    <el-table-column label="Operations">
                      <template #default="scope">
                        <el-button
                            link
                            type="primary"
                            size="small"
                            @click.prevent="deleteCharacterRow(scope.$index)">
                          Remove
                        </el-button>
                      </template>
                    </el-table-column>
                  </el-table>

                  <div style="margin:10px">
                    角色:
                    <el-autocomplete
                        v-model="selectedResultCharacter"
                        :fetch-suggestions="querySearchCharacter"
                        placeholder="请输入内容"
                        :trigger-on-focus="false"
                        clearable
                        style="width: 75%;"
                        @select="onSelectCharacter">
                    </el-autocomplete>

                    <el-button class="mt-4" type="primary" @click="onAddCharacter">Add Item</el-button>
                  </div>


                  <el-divider border-style="dashed"/>
                  <h3>关联番组</h3>
                  <el-row :gutter="20">
                    <el-col :span="24">
                      <el-table :data="bangumiTable" style="width: auto" max-height="250">
                        <el-table-column prop="bangumi_id" label="ID"/>
                        <el-table-column prop="bangumi_name" label="Name"/>
                        <el-table-column prop="bangumi_relation" label="Relation"/>
                        <el-table-column label="Operations">
                          <template #default="scope">
                            <el-button
                                link
                                type="primary"
                                size="small"
                                @click.prevent="deleteBangumiRow(scope.$index)">
                              Remove
                            </el-button>
                          </template>
                        </el-table-column>
                      </el-table>
                    </el-col>
                  </el-row>

                  <div style="margin:10px">
                    番组:
                    <el-autocomplete
                        style="width: 35%;"
                        v-model="selectedResultBangumi"
                        :fetch-suggestions="querySearchBangumi"
                        placeholder="请输入内容"
                        :trigger-on-focus="false"
                        clearable
                        @select="onSelectBangumi">
                    </el-autocomplete>

                    关系:
                    <el-input style="width: 35%;" v-model="newRelation" placeholder="Please input"></el-input>

                    <el-button class="mt-4" @click="onAddBangumi" type="primary">Add Item</el-button>

                    <el-divider border-style="dashed"/>

                    <el-button type="primary" @click="submitUpdate">提交</el-button>
                  </div>

                </el-main>
              </el-container>
              <el-footer>Footer</el-footer>
            </el-container>
          </el-card>
        </div>
      </div>
    </el-main>
  </el-container>
</template>

<script lang="ts">
import VerticalMenu from '../components/VerticalMenu.vue'
import CharacterCard from '../components/CharacterCard.vue'
import http from "../utils/http";
import ListItem from '../components/ListItem.vue'
import CommentItem from "../components/CommentItem.vue";
import {ref} from 'vue'
import {ElMessage} from 'element-plus'

export default {
  components: {
    CommentItem,
    VerticalMenu,
    CharacterCard,
    ListItem
  },
  data() {
    return {
      bangumi_id: this.$route.params.bangumiId,
      bangumi_image: '',
      bangumi_intro: "No introduction",
      bangumi_name: "Untitled",
      bangumi_score: 0,
      user_scored: ref(false),
      user_score: ref(-1),
      rate_colors: ref(['#99A9BF', '#F7BA2A', '#FF9900']),
      bangumi_relationships: [],
      comments: [],
      new_comment_area: ref(''),
      searchResults: [],
      selectedResultCharacter: null,
      searchBangumiResults: [],
      selectedResultBangumi: null,
      characterObject: null,
      characterTable: [],
      bangumiObject: null,
      bangumiTable: [],
      newRelation: '',
      imageUrl: ''
    }
  },
  mounted() {
    this.bangumiQuery(); // 在组件挂载后调用 fetchData 方法
    this.bangumiRelationShipQuery();
  },
  methods: {
    bangumiQuery() {
      http.get(
          "http://127.0.0.1:8000/bangumi_query/",
          {
            params: {
              "bangumi_id": this.bangumi_id,
            }
          }
      ).then(response => {
        this.bangumi_intro = response.data.bangumi_intro;
        this.bangumi_name = response.data.bangumi_name;
        this.bangumi_score = response.data.bangumi_score;
        this.bangumi_image = `data:image/png;base64,${response.data.image}`;
        this.imageUrl = `data:image/png;base64,${response.data.image}`;
        console.log(this.bangumi_image);
      })
          .catch(error => {
            console.error('Error fetching data:', error);
          });
    },
    bangumiRelationShipQuery() {
      http.get(
          "http://127.0.0.1:8000/bangumi_relationship_query/",
          {
            params: {
              "bangumi_id": this.bangumi_id,
            }
          }
      ).then(response => {
        for (let item of response.data.bangumis) {
          console.log("item");
          console.log(item.relation);

          this.bangumi_relationships.push({
            'bangumi_id': item.bangumi_id,
          })
          this.bangumiTable.push({
            'bangumi_id': item.bangumi_id.bangumi_id,
            'bangumi_name': item.bangumi_id.bangumi_name,
            'bangumi_relation': item.relation
          })
        }
        console.log("this.bangumi_relationships")
        console.log(this.bangumi_relationships)
      })
          .catch(error => {
            console.error('Error fetching data:', error);
          });

      http.get(
          "http://127.0.0.1:8000/bangumi_character_query/",
          {
            params: {
              "bangumi_id": this.bangumi_id,
            }
          }
      ).then(response => {
        for (let item of response.data.characters) {
          console.log("item: " + item.id + item.character_name);
          this.characterTable.push({"character_id": item.id, "character_name": item.character_name})
        }
      })
          .catch(error => {
            console.error('Error fetching data:', error);
          });
    },
    querySearchCharacter(query: string, cb: any) {
      console.log(query);
      console.log(this.searchResults);
      if (query) {
        http.get(
            "http://127.0.0.1:8000/character_select/",
            {
              params: {
                "keyword": query
              }
            }
        ).then(response => {
          console.log("response: " + response.data);
          this.searchResults = response.data
          console.log("searchResults" + this.searchResults);
          cb(this.searchResults);
        })
      }
    },
    onSelectCharacter(character: any) {
      this.characterObject = character
      this.selectedResultCharacter = character.value
      if (this.selectedResultCharacter != null) {
        console.log(this.selectedResultCharacter);
      }
    },
    querySearchBangumi(query: string, cb: any) {
      console.log(query);
      console.log(this.searchResults);
      if (query) {
        http.get(
            "http://127.0.0.1:8000/bangumi_select/",
            {
              params: {
                "keyword": query
              }
            }
        ).then(response => {
          console.log("response: " + response.data);
          this.searchBangumiResults = response.data
          console.log("searchResults" + this.searchResults);
          cb(this.searchBangumiResults);
        })
      }
    },
    onSelectBangumi(bangumi: any) {
      this.bangumiObject = bangumi
      this.selectedResultBangumi = bangumi.value
      if (this.selectedResultBangumi != null) {
        console.log(this.selectedResultBangumi);
      }
    },
    onAddCharacter() {
      if (this.characterObject) {
        console.log({"character_id": this.characterObject.character_id, "character_name": this.characterObject.value});
        this.characterTable.push({
          "character_id": this.characterObject.character_id,
          "character_name": this.characterObject.value
        })
      }
    },
    onAddBangumi() {
      if (this.bangumiObject) {
        console.log({"bangumi_id": this.bangumiObject.bangumi_id, "bangumi_name": this.bangumiObject.value});
        this.bangumiTable.push({
          "bangumi_id": this.bangumiObject.bangumi_id,
          "bangumi_name": this.bangumiObject.value,
          'bangumi_relation': this.newRelation
        })
      }
    },
    deleteCharacterRow(index) {
      this.characterTable.splice(index, 1);
    },
    beforeImageUpload(rawFile: any) {
      if (rawFile.type !== 'image/jpeg') {
        ElMessage.error('Avatar picture must be JPG format!')
        return false
      } else if (rawFile.size / 1024 / 1024 > 2) {
        ElMessage.error('Avatar picture size can not exceed 2MB!')
        return false
      } else {
        this.imageUrl = URL.createObjectURL(rawFile)
      }
    },
    deleteBangumiRow(index) {
      this.bangumiTable.splice(index, 1);
    },
    async urlToBase64(url) {
      try {
        const response = await fetch(url);
        const blob = await response.blob();
        const reader = new FileReader();
        reader.readAsDataURL(blob);
        reader.onload = () => {
          const base64 = reader.result;
          console.log(base64);
        };
        return new Promise((resolve, reject) => {
          reader.onload = () => {
            const base64 = reader.result;
            // console.log(base64);
            resolve(base64);
          };
          reader.onerror = (error) => {
            reject(error);
          };
        });
      } catch (error) {
        console.error('Error converting URL to Base64:', error);
      }
    },
    submitUpdate() {
      this.urlToBase64(this.imageUrl)
          .then((base64) => {
            console.log(this.bangumi_intro);
            console.log(this.$route.params.bangumiId);
            http.post(
                "http://127.0.0.1:8000/bangumi_update/", {
                  bangumi_id: this.$route.params.bangumiId,
                  bangumi_intro: this.bangumi_intro,
                  image: base64
                }
            )
          })
          .catch((error) => {
            console.error('Error converting URL to Base64:', error);
          });
      http.post(
          "http://127.0.0.1:8000/bangumi_charater_update/", {
            bangumi_id: this.$route.params.bangumiId,
            characters: this.characterTable
          }
      )
      http.post(
          "http://127.0.0.1:8000/bangumi_bangumi_update/", {
            bangumi_id: this.$route.params.bangumiId,
            bangumis: this.bangumiTable
          }
      )
      this.$router.push({name: 'bangumi-view', params: {bangumiId: this.bangumi_id}})
    }
  },
}
</script>

<style scoped>
.content-container {
  margin: 20px;
}

.full-screen-layout {
  height: 80vh; /* 设置高度为视口高度，以填充整个屏幕 */
}

.demo-image .block {
  padding: 70px 0;
  text-align: center;
  border-right: solid 1px var(--el-border-color);
  display: inline-block;
  width: 40%;
  box-sizing: border-box;
  vertical-align: top;
}
</style>