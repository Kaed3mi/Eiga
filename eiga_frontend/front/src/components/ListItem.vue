<template>
  <el-card :body-style="{ padding: '0px' }">
    <img
        :src="image"
        class="image"
    />
    <div style="padding: 14px">
      <span>{{ type }},{{ name }}</span>
      <div class="bottom">
        <el-button text class="button">
          <router-link :to="'/'+type +'/'+ id">Check</router-link>
        </el-button>
      </div>
    </div>
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
