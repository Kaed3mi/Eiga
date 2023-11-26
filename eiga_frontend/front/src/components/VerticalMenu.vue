<template>
  <div class="vertical-menu">
    <el-row class="tac">
      <el-col :span="24">
        <h5 class="mb-2">Mukamuka</h5>
        <el-menu
            active-text-color="#007f7f"
            background-color="#ffffff"
            class="el-menu-vertical-demo"
            default-active="2"
            text-color="#000"
            @open="handleOpen"
            @close="handleClose"
        >
          <el-sub-menu index="1">
            <template #title>
              <el-icon>
                <location/>
              </el-icon>
              <span>探索</span>
            </template>
            <router-link :to="{ name: 'bangumi-view', params: { bangumiId: 1 }}">
              <el-menu-item index="1-1">番组
              </el-menu-item>
            </router-link>
            <el-menu-item index="1-2">人物</el-menu-item>
            <el-menu-item index="1-3">标签</el-menu-item>
          </el-sub-menu>

          <el-menu-item index="2">
            <el-icon>
              <icon-menu/>
            </el-icon>
            <span>排行榜</span>
          </el-menu-item>

          <router-link :to="{ name: 'UserPage', params: { userId: userId }}">
            <el-menu-item>
              <el-icon>
                <document/>
              </el-icon>
              <span>个人站</span>
            </el-menu-item>
          </router-link>

          <el-menu-item index="4">
            <el-icon>
              <setting/>
            </el-icon>
            <span>设置</span>
          </el-menu-item>
        </el-menu>
      </el-col>
    </el-row>
  </div>
</template>

<script lang="ts" setup>

import router from '../utils/router';
import {
  Document,
  Menu as IconMenu,
  Location,
  Setting,
} from '@element-plus/icons-vue'
import {watch, ref} from "vue";

const handleOpen = (key: string, keyPath: string[]) => {
  console.log(key, keyPath)
}

const handleClose = (key: string, keyPath: string[]) => {
  console.log(key, keyPath)
}

const userId = localStorage.getItem('user_id');

</script>


<style scoped>
.vertical-menu {
  position: absolute;
  top: 0;
  left: 0;
}
</style>