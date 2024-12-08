<template>
  <el-card class="box-card" v-for="post in post_list" :key="post['post_id']">
    <template #header>
      <div class="card-header">
        <router-link :to="'/post?post_id=' + post['post_id']" class="post-title">{{ post['title'] }}</router-link>
        <span class="post-author">{{ post['author'] }}</span>
      </div>
    </template>
    <div class="post-content">
      {{ post['content'] }}
    </div>
  </el-card>
</template>

<script>
import axios from 'axios';
axios.defaults.withCredentials = true;
axios.defaults.baseURL = import.meta.env.VITE_EBLOG_API_URL;

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
      axios.post('/get_post_list')
        .then(res => {
          this.post_list = res.data['post_list']
        })
    }
  }
}
</script>

<style scoped>
.box-card {
  margin-bottom: 15px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.post-title {
  font-size: 16px;
  font-weight: bold;
  color: #409EFF;
  text-decoration: none;
}

.post-title:hover {
  text-decoration: underline;
}

.post-author {
  font-size: 14px;
  color: #606266;
}

.post-content {
  font-size: 14px;
  color: #303133;
  margin-top: 10px;
}
</style>