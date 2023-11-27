<template>
  <div class="eiga-avatar">
    <el-avatar :src="avatar_url" class="avatar"
               @mouseover="showChange = true"
               @mouseleave="showChange = false"
               @click="this.dialogVisible = true"
    />

    <div class="update-user-avatar">
      <el-dialog
          v-model="this.dialogVisible"
          width="50%"
      >
        <span>请上传您的头像</span>
        <el-upload
            list-type="picture-card"
            action="http://127.0.0.1:8000/upload_avatar/"
            :limit="1"
            :show-file-list="true"
            :on-success="handleSuccess"
            :before-upload="beforeUpload"
        >
          <i class="el-icon-plus"></i>
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
      uploadDisabled: false
    }
  },
  props: {
    avatar_url: {
      type: String,
      required: true,
    },
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