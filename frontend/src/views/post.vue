<template>
  <div class="post-container">
    <h3>{{ post_info['title'] }}</h3>
    <p><strong>作者:</strong> {{ post_info['author'] }}</p>
    <div class="content">{{ post_info['content'] }}</div>
    <hr>

    <el-input v-model="post_comment" clearable placeholder="评论" class="comment-input" />
    <el-button @click="add_comment" type="primary">提交评论</el-button>

    <hr>
    <el-card class="box-card" v-for="comment in comment_list" :key="comment['comment_id']">
      <template #header>
        <div class="card-header">
          <span>{{ comment['name'] }} (ID: {{ comment['user_id'] }})</span>
        </div>
      </template>
      <div class="text item">
        {{ comment['content'] }}
      </div>
    </el-card>
  </div>
</template>

<script>
import axios from 'axios';
axios.defaults.withCredentials = true;
axios.defaults.baseURL = import.meta.env.VITE_EBLOG_API_URL;

import { ElMessage, ElMessageBox, ElNotification } from 'element-plus'

export default {
  data() {
    return {
      post_info: {},
      comment_list: [],
      post_comment: ""
    }
  },

  mounted() {
    this.get_post_info(),
    this.get_comment_list()
  },

  methods: {
    get_post_info() {
      axios.post('/get_post_info', {
        post_id: this.$route.query.post_id
      })
        .then(res => {
        this.post_info = res.data['post_info'];
      })
    },

    get_comment_list() {
      axios.post('/get_comment_list', {
        post_id: this.$route.query.post_id
      })
        .then(res => {
        this.comment_list = res.data['comment_list']; 
      })
    },
    add_comment() {
      axios.post('/add_comment', {
        post_id: this.$route.query.post_id,
        content: this.post_comment
      })
        .then(res => {
          if (res.data['status'] == "fail") {
            ElMessage({
              type: 'error',
              message: '评论失败',
              showClose: true
            }) 
          }

          if (res.data['status'] == "success") {
            ElMessage({
              type: 'success',
              message: '评论成功',
              showClose: true
            });
            this.get_comment_list();
            this.post_comment = "";
          }
        })
    }
  }
}
</script>

<style scoped>
.post-container {
  padding: 20px;
  text-align: center;
}

.content {
  margin-bottom: 20px;
  text-align: left;
}

.box-card {
  margin-bottom: 15px;
  text-align: left;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.text {
  font-size: 14px;
}

.item {
  margin-bottom: 18px;
}

.comment-input {
  margin-top: 20px;
  margin-bottom: 10px;
  text-align: left;
}
</style>