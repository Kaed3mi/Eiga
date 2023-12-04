<template>
  <div class="eiga-avatar">
    <el-avatar shape="circle" :fit="fit" :src="avatar_url" alt="User avatar" class="avatar"
               @mouseover="showChange = true"
               @mouseleave="showChange = false"
               @click="this.dialogVisible = editable"/>
    <div class="update-user-avatar">
      <el-dialog
          v-model="this.dialogVisible"
          width="50%"
      >
        <span>请上传您的头像</span>
        <el-upload
            class="avatar-uploader"
            list-type="picture-card"
            action="http://127.0.0.1:8000/upload_avatar/"
            :limit="1"
            :data="{user_id: this.user_id }"
            :show-file-list="true"
            :on-success="handleSuccess"
            :before-upload="beforeUpload"
        >
          <el-avatar shape="circle" :fit="fit" v-if="edited_url" :src="edited_url" class="avatar"/>
          <el-icon v-else class="avatar-uploader-icon">
            <Plus/>
          </el-icon>
        </el-upload>

      </el-dialog>
    </div>

  </div>
</template>

<script>


import {ElMessage} from "element-plus";

export default {
  name: "userAvatar",
  data() {
    return {
      showChange: false,
      dialogVisible: false,
      uploadDisabled: false,
      user_id: localStorage.getItem("user_id"),
      edited_url: ''
    }
  },
  props: {
    avatar_url: {
      type: String,
      required: true,
    },
    editable:{}
  },
  methods: {
    handleSuccess() {
      ElMessage.success('上传成功！')
    },
    beforeUpload(rawFile) {
      // 限制上传的文件类型和大小
      if (rawFile.type !== 'image/jpeg') {
        ElMessage.error('Avatar picture must be JPG format!')
        return false
      } else if (rawFile.size / 1024 / 1024 > 2) {
        ElMessage.error('Avatar picture size can not exceed 2MB!')
        return false
      }
      this.edited_url = URL.createObjectURL(rawFile)
      return true
    },
  },
}

</script>

<style scoped>

.avatar {
  width: 100px;
  height: 100px;
  border-radius: 50%;
  transition: filter 0.3s ease;
  cursor: pointer;
}

.avatar:hover {
  filter: blur(5px); /* 图像悬停时应用虚化效果 */
}
</style>