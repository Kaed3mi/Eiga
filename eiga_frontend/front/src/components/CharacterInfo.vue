<template>
  <el-card class="box-card" style="min-width: 90%; width: auto">
    <h2>
      {{ character_name }}
    </h2>
    <el-divider border-style="dashed"></el-divider>
    <el-container>
      <el-aside style="margin-right: 5%">
        <el-card class="characterCard" :body-style="{ padding: '10px', height: 'auto', width: 'auto'}">
          <img :src="imageUrl" class="image"/>
          <div style="margin-top: 5px">
            <span>{{ character_name }}</span>
          </div>
        </el-card>
      </el-aside>
      <el-main>
        <el-descriptions title="角色信息"  :column="1">
          <el-descriptions-item
              v-for="(description, index) in descriptions"
              :key="index"
              :label="description.label"
          >
            {{ description.content }}
          </el-descriptions-item>
          <el-descriptions-item>
            <h3 :style="{ textAlign: 'left' }">简介</h3>
            <div>
              <p v-for="(line, index) in introduce.split('\n')" :key="index"
                 style="text-align: left;white-space: pre-wrap;text-indent: 2em;"
              >
                {{ line }}
              </p>
            </div>
          </el-descriptions-item>
        </el-descriptions>
        <el-divider border-style="dashed"/>
        <h3>出演</h3>
        <!--出演-->
        <el-container class="main_flex_style">
          <el-row
              :gutter="20"
              style="width: 100%"
          >
            <el-col :span="24" v-for="(bangumi, index) in starringBangumis" :key="index">
              <ListItem type="bangumi" :id="bangumi.bangumi_id"
                        :name="bangumi.bangumi_name"
                        :description="bangumi.bangumi_intro"
                        :image="bangumi.image"></ListItem>
            </el-col>
          </el-row>
        </el-container>
        <el-divider border-style="dashed"/>
        <CommentArea object_type="character" :object_id="character_id"></CommentArea>
      </el-main>
    </el-container>
  </el-card>
</template>

<script lang="ts">
// import { ref } from 'vue'
import http from '../utils/http';
import ListItem from "./ListItem.vue";
import CommentArea from "./CommentArea.vue";

export default {
  components: {CommentArea, ListItem},
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
      starringBangumis: [],
    };
  },
  mounted() {
    this.characterQuery();
    this.starringQuery();
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
      })
    },
    starringQuery() {
      http.get(
          "http://127.0.0.1:8000/character_bangumi_query/",
          {
            params: {
              "character_id": this.character_id
            }
          }
      ).then(response => {
        console.log(response.data);
        this.starringBangumis = []
        for (let bangumi of response.data.starring_bangumis) {
          this.starringBangumis.push({
            bangumi_id: bangumi.bangumi_id,
            bangumi_name: bangumi.bangumi_name,
            bangumi_intro: bangumi.bangumi_intro,
            image: `data:image/png;base64,${bangumi.image}`
          })
        }
      })
      console.log('出演番组表：' + this.starringBangumis)
    }
  }
};
</script>

<style>
.time {
  font-size: 12px;
  color: #999;
}

.bottom {
  margin-top: 13px;
  line-height: 12px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.button {
  padding: 0;
  min-height: auto;
}


.image {
  width: 100%;
  height: auto;
  display: block;
}
</style>

{
attributes: [
{
label: "姓名",
content: "黄前久美子",
},
{
label: "生日",
content: "8月21日",
},
{
label: "声优",
content: "黑泽朋世",
},
{
label: "年龄",
content: "16岁（第一季）→17岁（剧场版4）",
},
{
label: "发色",
content: "棕发",
},
{
label: "身高",
content: "162cm",
},
],
image: "",
introduce: "北宇治高中一年级新生，吹奏乐部成员，负责吹奏上低音号(Euphonium)，目前所用乐器型号为YEP-621。
平时是章鱼头，在重要的比赛会梳单马尾。
小时候在欣赏了姐姐黄前麻美子的演出后，对吹奏乐产生兴趣。希望有朝一日可以和姐姐一同演奏。
小学时原本想和姐姐一样选择长号，由于学校空缺上低音号手，在老师的劝导下选择了上低音号。
初中就读于大吉山北中学校（简称北中），同样担任上低音号手，在吹奏乐部中被自认关系很好的学姐欺凌，留下了阴影。"
}