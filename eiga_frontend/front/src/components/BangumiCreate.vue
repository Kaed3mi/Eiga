<template>
  <el-card class="box-card" style="">
    <h2>新番组</h2>
    <el-divider></el-divider>
    <el-input v-model="bangumi_name" placeholder="Please input" label="Name" clearable>
      <template #prepend>
        <span>番组名</span>
      </template>
    </el-input>
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
                  placeholder="Please input">
        </el-input>

        <el-divider border-style="dashed"/>
        角色

        <el-table :data="characterTable" style="width: auto" max-height="250">
          <el-table-column prop="character_id" label="ID"/>
          <el-table-column prop="character_name" label="Name"/>
          <el-table-column label="Operations">
            <template #default="scope">
              <el-button
                  round
                  plain
                  type="warning"
                  @click.prevent="deleteCharacterRow(scope.$index)"
              >
                <el-icon>
                  <Delete/>
                </el-icon>
                移除
              </el-button>
            </template>
          </el-table-column>
        </el-table>

        <div class="input-row-bc">
          <el-autocomplete
              v-model="selectedResultCharacter"
              :fetch-suggestions="querySearchCharacter"
              placeholder="请输入内容"
              :trigger-on-focus="false"
              clearable
              @select="onSelectCharacter">
          </el-autocomplete>

          <el-button
              plain
              class="mt-4"
              type="primary"
              @click="onAddCharacter"
          >
            <el-icon>
              <Plus/>
            </el-icon>
            添加角色
          </el-button>
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
                      round
                      plain
                      type="warning"
                      @click.prevent="deleteBangumiRow(scope.$index)"
                  >
                    <el-icon>
                      <Delete/>
                    </el-icon>
                    &nbsp;
                    移除
                  </el-button>
                </template>
              </el-table-column>
            </el-table>
          </el-col>
        </el-row>

        <div class="input-row-bb">
          <el-autocomplete
              v-model="selectedResultBangumi"
              :fetch-suggestions="querySearchBangumi"
              placeholder="请输入名称"
              :trigger-on-focus="false"
              clearable
              @select="onSelectBangumi">
          </el-autocomplete>
          <el-input v-model="newRelation" placeholder="请输入关系"></el-input>
          <el-button plain class="mt-4" type="primary" @click="onAddBangumi">
            <el-icon>
              <Plus/>
            </el-icon>
            添加番组关系
          </el-button>

        </div>

        <el-divider border-style="dashed"/>

        <el-button type="primary" @click="submitUpdate">提交</el-button>
      </el-main>
    </el-container>
  </el-card>
</template>

<script lang="ts" setup>
import {Plus, Delete} from '@element-plus/icons-vue'
</script>
<script lang="ts">
import VerticalMenu from '../components/VerticalMenu.vue'
import http from "../utils/http";
import ListItem from '../components/ListItem.vue'
import CommentItem from "../components/CommentItem.vue";

import {ElMessage} from 'element-plus'
import defaultImage from '../assets/bangumi_default.jpg'

export default {
  components: {
    CommentItem,
    VerticalMenu,
    ListItem
  },
  data() {
    return {
      bangumi_image: '',
      bangumi_intro: "",
      bangumi_name: "",
      bangumi_relationships: [],
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
    this.imageUrl = defaultImage
  },
  methods: {
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
      if (this.imageUrl !== defaultImage) {

        this.urlToBase64(this.imageUrl)
            .then((base64) => {
              console.log(this.bangumi_intro);
              console.log(this.$route.params.bangumiId);
              http.post(
                  "http://127.0.0.1:8000/bangumi_create/", {
                    bangumi_name: this.bangumi_name,
                    bangumi_intro: this.bangumi_intro,
                    image: base64
                  }
              ).then(response => {
                console.log(response.data.bangumi_id);
                http.post(
                    "http://127.0.0.1:8000/bangumi_charater_update/", {
                      bangumi_id: response.data.bangumi_id,
                      characters: this.characterTable
                    }
                )
                http.post(
                    "http://127.0.0.1:8000/bangumi_bangumi_update/", {
                      bangumi_id: response.data.bangumi_id,
                      bangumis: this.bangumiTable
                    }
                )
              })
            })
            .catch((error) => {
              console.error('Error converting URL to Base64:', error);
            });
      } else {
        ElMessage.error("请上传图片")
      }
    }
  },
}
</script>

<style scoped>
.full-screen-layout {
  height: 80vh; /* 设置高度为视口高度，以填充整个屏幕 */
  width: 100%
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

.input-row-bc > * {
  flex: 1;
  margin-right: 8px;
}

.input-row-bc {
  display: grid;
  margin-top: 10px;
  grid-template-columns: 80% 20%;
  grid-gap: 8px;
}

.input-row-bb > * {
  flex: 1;
  margin-right: 8px;
}

.input-row-bb {

  display: grid;
  margin-top: 10px;
  grid-template-columns: 40% 40% 20%;
  grid-gap: 8px;
}
</style>