<template>
  <el-card class="item-card" :body-style="{ padding: '0px' }">
    <el-row :gutter="20">
      <el-col :span="9">
        <el-image :src="image" :fit="cover" style="width: auto; height: 150px;"/>
      </el-col>
      <el-col :span="15">
        <span>{{ type }},{{ name }}</span>
      <div class="bottom">
        <el-button text class="button">
          <router-link :to="'/'+type +'/'+ id">Check</router-link>
        </el-button>
      </div>
      </el-col>
    </el-row>
  </el-card>
</template>

<script lang="ts">
import axios from "axios";
import http from "../utils/http";

export default {
  props: ['type', 'id', 'name', 'image', 'description'],
  data() {
    return {
      characters: []
    }
  },
  methods: {},
  name: "ListItem",
}

</script>

<style>
.item-card {
  max-height: 150px;
  min-width: 700px;
}
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
