<template>
  <div class="UpdateInfo">
    <button @click="showModal = true">修改信息</button>

    <!-- Modal for editing user info -->
    <div v-if="showModal" class="modal">
      <div class="modal-content">
        <span class="close" @click="showModal = false">&times;</span>
        <h2>修改用户信息</h2>
        <p>不需修改则留空</p>
        <!-- Form for editing user info -->

        <form @submit.prevent="updateUserInfo">
          <!-- Input fields for user info -->
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
          <!-- Submit button -->
          <button type="submit">保存</button>
        </form>
      </div>
    </div>
  </div>
</template>

<script>

import http from "../utils/http";

export default {
  data() {
    return {
      showModal: false,
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
      console.log('Updated user info:', this.editedUserInfo);
      http.post(
          "http://127.0.0.1:8000/user_info_update/", {
            user_id: localStorage.getItem('user_id'),
            username: this.username,
            email: this.email,
            password: this.password
          })
      this.showModal = false; // 临时关闭模态框（在实际应用中应在请求成功后关闭）
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
