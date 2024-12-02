<template>
  <div class="post-management-container">
    <el-button type="primary" @click="add_post"> 添加博文 </el-button>
    
    <el-card v-for="post in post_list" :key="post['post_id']" class="post-card">
      <div class="post-header">
        <h3>{{ post['title'] }}</h3>
        <span>作者: {{ post['author'] }}</span>
      </div>
      <div class="post-content">
        <p>{{ post['content'] }}</p>
      </div>
      <div class="post-actions">
        <el-button type="warning" @click="update_post(post['post_id'])"> 修改博文 </el-button>
        <el-button type="danger" @click="delete_post(post['post_id'])"> 删除博文 </el-button>
      </div>
    </el-card>
  </div>
</template>

<script>
import axios from 'axios';
axios.defaults.withCredentials = true;

import { ElMessage, ElMessageBox, ElNotification } from 'element-plus'

export default {
  data() {
    return {
      post_list: []
    }
  },
 
  mounted() {
    this.get_post_list()
  },

  methods: {
    get_post_list() {
      axios.post('http://127.0.0.1:5000/get_post_list')
        .then(res => {
          this.post_list = res.data['post_list']
        })
    },

    add_post() {
      window.location.href = "/post_management/add_post";
    },
   
    update_post(target_post_id) {
      window.location.href = "/post_management/update_post?post_id=" + target_post_id;
    },

    delete_post(target_post_id) {
      axios.post('http://127.0.0.1:5000/delete_post', {
        post_id: target_post_id
      })
        .then(res => {
          // If the deletion of the blog post fails, it will display 'delete blog post failed'.
          if (res.data['status'] == 'fail') {
            ElMessage({
              type: 'error', // Corrected the type from 'fail' to 'error'
              message: '删除博文失败',
              showClose: true
            })
          }

          // If the deletion of the blog post is successful, it will display 'delete blog post successfully' and update the blog post list.
          if (res.data['status'] == 'success') {
            ElMessage({
              type: 'success',
              message: '删除博文成功',
              showClose: true
            })

            this.get_post_list()
          }
        })
    }
  }
}
</script>

<style scoped>
.post-management-container {
  padding: 20px;
}

.el-button {
  margin-bottom: 20px;
}

.post-card {
  margin-bottom: 20px;
}

.post-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 10px;
}

.post-content {
  margin-bottom: 10px;
}

.post-actions {
  display: flex;
  justify-content: space-between;
}

.el-button--warning {
  margin-right: 10px;
}
</style>