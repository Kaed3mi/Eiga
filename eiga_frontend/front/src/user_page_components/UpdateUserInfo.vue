<template>
  <div class="UpdateInfo">

    <el-button plain type="primary" @click="dialogVisible = true">
      <el-icon><Edit /></el-icon>
      &nbsp;修改信息
    </el-button>
    <el-dialog
        v-model="dialogVisible"
        width="30%"
    >
      <div class="form-container">
        <el-form
            ref="ruleFormRef"
            label-width="120px"
            class="demo-ruleForm"
            status-icon
        >

          <el-form-item label="用户名:" prop="username">
            <el-input v-model="this.editedUserInfo.username" placeholder="请输入昵称"
                      :clearable="true"/>
          </el-form-item>

          <el-form-item label="邮箱:" prop="email">
            <el-input v-model="this.editedUserInfo.email" placeholder="请输入邮箱"
                      :clearable="true"/>
          </el-form-item>

          <el-form-item label="密码" prop="password">
            <el-input v-model="this.editedUserInfo.password" placeholder="请输入密码" type="password"
                      :show-password="true"/>
          </el-form-item>

        </el-form>
      </div>
      <template #footer>
      <span class="dialog-footer">
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="updateUserInfo">确定修改</el-button>
      </span>
      </template>
    </el-dialog>
  </div>
</template>
<script  setup>
import {
  Edit
} from '@element-plus/icons-vue'
</script>
<script>

import http from "../utils/http";
import {ElMessage} from "element-plus";

export default {
  data() {
    return {
      dialogVisible: false,
      editedUserInfo: {
        username: '', // 用户名
        email: '', // 邮箱
        password: '', // 密码（哈哈明文传密码也没啥不好的。）
        // 其他需要修改的用户信息字段
      },
    };
  },
  methods: {
    updateUserInfo() {
      // 在这里处理更新用户信息的逻辑，比如发送请求到后端保存更改等
      // check Email:
      if (this.editedUserInfo.email !== '') {
        const pattern = /^([0-9a-zA-Z_\.\-\])+\@([0-9a-zA-Z_\.\-\])+\.([a-zA-Z]+)$/;
        if (!pattern.test(this.editedUserInfo.email)) {
          ElMessage.error('邮箱格式不正确！')
          return;
        }
      }
      console.log('Updated user info:', localStorage.getItem('user_id'), this.editedUserInfo);
      http.post(
          "http://127.0.0.1:8000/user_info_update/", {
            user_id: localStorage.getItem('user_id'),
            username: this.editedUserInfo.username,
            email: this.editedUserInfo.email,
            password: this.editedUserInfo.password
          })
      this.dialogVisible = false;
    },
  },

};
</script>

<style scoped>
/* 样式可根据需求自行调整 */
.UpdateInfo{
  z-index: 100;
}
.modal {
  display: flex;
  align-items: center;
  justify-content: center;
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
}

.modal-content {
  background-color: #fff;
  padding: 20px;
  flex-direction: column;
}

.form-container {
  display: flex;
  flex-direction: column;
  /* 样式可根据需求自行调整 */
}

.form-input {
  margin-bottom: 10px; /* 设置 input 之间的间距 */
}

.close {
  float: right;
  cursor: pointer;
  font-size: 20px;
}

</style>
