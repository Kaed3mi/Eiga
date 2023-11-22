<template>
  <el-row>
    <el-col
      v-for="(o, index) in 1"
      :key="o"
      :span="8"
      :offset="index > 0 ? 2 : 0"
    >
      <el-card :body-style="{ padding: '0px' }">
        <img
          src="https://lain.bgm.tv/r/400/pic/crt/l/e3/2f/18101_crt_343At.jpg?r=1410320023"
          class="image"
        />
        <div style="padding: 14px">
          <span>My character_id is {{id}}</span>
          <div class="bottom">
            <el-button text class="button">
              <router-link :to="'/character/'+ id" >Check</router-link>
            </el-button>
          </div>
        </div>
      </el-card>
    </el-col>
  </el-row>
</template>

<script lang="ts" >
export default {
  props: ['id'],
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
  display: block;
}
</style>
