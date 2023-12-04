<template>
  <div class="bangumi_rank" v-if="valid()">

    <el-carousel

        style=""
        indicator-position="none"
        :autoplay='false'>
      <el-carousel-item
          v-for="fourGroup in bangumiGroupList"
          :key="fourGroup">
        <el-row>
          <!--:span="6"是为了一行展示4个-->
          <el-col
              :span="6"
              v-for="bangumi in fourGroup"
              :key="bangumi">
            <el-container class="row-content">
              <el-card
                  style="width: 140px; height: 230px; margin: 30px"
              >
                <el-col>
                  <el-row>
                    <el-card :body-style="{padding: '3px'}">
                      <el-image
                          style="width: 100px; height: 134px;margin-bottom: -5px;margin-left: -3px"
                          :src="bangumi.image"/>
                    </el-card>
                  </el-row>
                  <div style="padding: 3px"></div>
                  <el-row>
                    <router-link :to="{ name: 'bangumi-view', params: { bangumiId: bangumi.bangumi_id }}">
                      <el-text class="w-80px" type="primary" truncated>{{ bangumi.bangumi_name }}</el-text>
                      <el-text type="info">用户评分：</el-text>
                      <el-text type="success"> {{ bangumi.my_score }}</el-text>
                    </router-link>
                  </el-row>
                </el-col>
              </el-card>
            </el-container>
          </el-col>
        </el-row>
      </el-carousel-item>
    </el-carousel>

  </div>
  <div v-else>
    <p>
      ta还没有评价过番组哦~
    </p>
  </div>
</template>

<script>
import http from "../utils/http";
import {ElMessage} from "element-plus";

export default {
  name: "MyBangumis",
  data() {
    return {
      bangumiGroupList: [],
    };
  },
  mounted() {
    this.myBangumiQuery();
  },
  props: {
    user_id: {}
  },
  methods: {
    myBangumiQuery() {
      this.bangumiGroupList = []
      http.get(
          "http://127.0.0.1:8000/my_bangumi_query/",
          {
            params: {
              'user_id': this.user_id,
            }
          }
      ).then(response => {
        console.log(response.data.bangumis)
        let counter = 0; // 将番组分成4个一组
        let bangumiGroup = []
        for (let bangumi of response.data.bangumis) {
          counter++
          if (counter === 5) {
            this.bangumiGroupList.push(bangumiGroup)
            bangumiGroup = []
            counter = counter % 4
          }
          bangumiGroup.push({
            'bangumi_id': bangumi.bangumi_id,
            'bangumi_name': bangumi.bangumi_name,
            'my_score': bangumi.my_score,
            'image': `data:image/png;base64,${bangumi.image}`,
          })
        }
        if (bangumiGroup.length > 0) {
          this.bangumiGroupList.push(bangumiGroup) // 最后加上省下的番组
        }
        console.log(this.bangumiGroupList);
      }).catch(error => {
        ElMessage.error('怎么出错了')
      });
      console.log("len=" + this.bangumiGroupList.length)
      console.log(">0? :" + String(this.bangumiGroupList.length > 0))
    },
    valid() {
      console.log("list ::" + this.bangumiGroupList)
      console.log("len ::" + String(this.bangumiGroupList.length))
      console.log(">0? ::" + String(this.bangumiGroupList.length > 0))
      console.log("false::" + String(false))
      return this.bangumiGroupList.length > 0
    }
  }
}
</script>

<style scoped>
.w-80px {
  width: 110px;
}

.row-content {
  display: flex;
  align-items: center;
  justify-content: center;
}

</style>