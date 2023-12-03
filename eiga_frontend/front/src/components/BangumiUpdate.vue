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
              <el-header><h2>更改番组：{{ bangumi_name }}</h2></el-header>
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
                  <h3 style="text-align: left;"> 番组名：</h3>
                  <el-input v-model="bangumi_name"
                            placeholder="请输入番组名"></el-input>
                  <el-divider border-style="dashed"/>

                  <h3 style="text-align: left;"> 简介：</h3>
                  <el-input v-model="bangumi_intro" :autosize="{ minRows: 2, maxRows: 20 }" type="textarea"
                            placeholder="请输入简介"></el-input>
                  <el-divider border-style="dashed"/>

                  <h3>角色</h3>

                  <el-table :data="characterTable" style="width: auto" max-height="250">
                    <el-table-column prop="character_id" label="ID"/>
                    <el-table-column prop="character_name" label="Name"/>
                    <el-table-column label="Operations">
                      <template #default="scope">
                        <el-button
                            round
                            plain
                            type="warning"
                            @click.prevent="deleteCharacterRow(scope.$index)">
                          <el-icon>
                            <Delete/>
                          </el-icon>
                          &nbsp;
                          移除
                        </el-button>
                      </template>
                    </el-table-column>
                  </el-table>

                  <div class="input-row-bc">
                    <el-autocomplete
                        v-model="selectedResultCharacter"
                        :fetch-suggestions="querySearchCharacter"
                        placeholder="请输入角色名"
                        :trigger-on-focus="false"
                        clearable
                        @select="onSelectCharacter">
                    </el-autocomplete>

                    <el-button plain class="mt-4" type="primary" @click="onAddCharacter">
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
                        <el-table-column prop="bangumi_name" label="番组名"/>
                        <el-table-column prop="bangumi_relation" label="关系"/>
                        <el-table-column label="操作">
                          <template #default="scope">
                            <el-button
                                round
                                plain
                                type="warning"
                                @click.prevent="deleteBangumiRow(scope.$index)">
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
                        placeholder="请输入番组名"
                        :trigger-on-focus="false"
                        clearable
                        @select="onSelectBangumi">
                    </el-autocomplete>
                    <el-input v-model="newRelation" placeholder="请输入关系"></el-input>

                    <el-button plain class="mt-4" @click="onAddBangumi" type="primary">
                      <el-icon>
                        <Plus/>
                      </el-icon>
                      添加番组关系
                    </el-button>


                  </div>

                </el-main>
              </el-container>
            </el-container>
            <el-divider border-style="dashed"/>
            <div class="main_flex_style">
              <el-row>
                <el-button :icon="Select" type="primary" @click="submitUpdate">
                  提交更改
                </el-button>
                <el-popover :visible="delete_visible" placement="top" :width="160">
                  <div class="main_flex_style">
                    <p>确定要删除吗?</p>
                  </div>
                  <div class="main_flex_style">
                    <el-button size="small" text @click="delete_visible = false">取消</el-button>
                    <el-button size="small" type="primary" @click="delete_visible = false; bangumiDelete()"
                    >确认
                    </el-button
                    >
                  </div>
                  <template #reference>
                    <el-button :icon="Delete" type="danger" @click="delete_visible = true">
                      删除条目
                    </el-button>
                  </template>
                </el-popover>

              </el-row>
            </div>
          </el-card>
          <Footer/>
        </div>
      </div>
    </el-main>
  </el-container>
</template>
<script lang="ts" setup>
import {Plus, Delete, Select} from '@element-plus/icons-vue'
</script>
<script lang="ts">
import VerticalMenu from '../components/VerticalMenu.vue'
import CharacterCard from '../components/CharacterCard.vue'
import http from "../utils/http";
import ListItem from '../components/ListItem.vue'
import CommentItem from "../components/CommentItem.vue";
import {ref} from 'vue'
import {ElMessage, ElNotification} from 'element-plus'
import Footer from "./Footer.vue";

export default {
  components: {
    Footer,
    CommentItem,
    VerticalMenu,
    CharacterCard,
    ListItem
  },
  data() {
    return {
      delete_visible: false,
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
      imageUrl: '',
      isEditing: false,
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
    bangumiDelete() {
      http.delete(
          "http://127.0.0.1:8000/bangumi_delete/",
          {
            params: {
              "bangumi_id": this.bangumi_id,
            }
          }
      ).then(response => {
        ElNotification({
          title: '删除成功',
          message: '已删除番组\"' + this.bangumi_name + '\"',
          type: 'success',
        })
        this.$router.push("/home")
      }).catch(error => {
        ElMessage.error('操作失败')
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
                  bangumi_name: this.bangumi_name,
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
      ElNotification({
        title: '更新成功',
        message: '已更改番组\"' + this.bangumi_name + '\"',
        type: 'success',
      })
      setTimeout(() => {
        this.$router.push({name: 'bangumi-view', params: {bangumiId: this.bangumi_id}}).then(() => {
          window.location.reload();
        });
      }, 500);
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

.input-row-bc {
  display: grid;
  margin-top: 10px;
  grid-template-columns: 80% 20%;
  grid-gap: 8px;
}

.input-row-bb {
  display: grid;
  margin-top: 10px;
  grid-template-columns: 40% 40% 20%;
  grid-gap: 8px;
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