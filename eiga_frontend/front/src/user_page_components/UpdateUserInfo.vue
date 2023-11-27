<template>
  <div class="UpdateInfo">
    <el-button @click="dialogVisible = true">修改信息</el-button>
    <el-dialog
        v-model="dialogVisible"
        title="Tips"
        width="30%"
    >
      <span>请上传您的头像</span>
      <div class="form-container">
        <div class="form-input">
          <label for="name">昵称:</label>
          <input type="text" v-model="editedUserInfo.username" id="name" placeholder="昵称">
        </div>
        <div class="form-input">
          <label for="email">邮箱:</label>
          <input type="email" v-model="editedUserInfo.email" id="email" placeholder="邮箱">
        </div>
        <div class="form-input">
          <label for="email">密码:</label>
          <input type="text" v-model="editedUserInfo.password" id="email" placeholder="密码">
        </div>
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

<script>

import http from "../utils/http";

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
