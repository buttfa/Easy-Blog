<template>
  <div class="update-post-container">
    <el-card class="box-card">
      <template #header>
        <div class="card-header">
          <h3> 更新文章 </h3>
        </div>
      </template>
      <el-form label-width="80px" label-position="top">
        <el-form-item label="标题">
          <el-input v-model="title" clearable placeholder="请输入标题" />
        </el-form-item>
        <el-form-item label="作者">
          <el-input v-model="author" clearable placeholder="请输入作者" />
        </el-form-item>
        <el-form-item label="内容">
          <el-input v-model="content" type="textarea" :rows="5" placeholder="请输入内容" />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="update_post_info"> 修改 </el-button>
        </el-form-item>
      </el-form>
    </el-card>
  </div>
</template>

<script>
import axios from 'axios';
axios.defaults.withCredentials = true;

export default {
  data() {
    return {
      title: "",
      author: "",
      content: ""
    }
  },

  mounted() {
    this.get_post_info();
  },

  methods: {
    get_post_info() {
      axios.post('http://127.0.0.1:5000/get_post_info', {
        post_id: this.$route.query.post_id
      }).then(res => {
        this.title = res.data['post_info']['title'];
        this.author = res.data['post_info']['author'];
        this.content = res.data['post_info']['content'];
      });
    },

    update_post_info() {
      axios.post('http://127.0.0.1:5000/update_post_info', {
        post_id: this.$route.query.post_id,
        title: this.title,
        author: this.author,
        content: this.content
      }).then(res => {
        window.location.href = "/post_management";
      });
    }
  }
}
</script>

<style scoped>
.update-post-container {
  position: relative;
  top: 0;
  left: 0;
  bottom: 0;
  right: 0;
  margin: auto auto;
  width: 60%;
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
}

.box-card {
  width: 100%;
  max-width: 800px;
}

.card-header {
  text-align: center;
}

.el-form-item__label {
  font-size: 16px;
  font-weight: bold;
}

.el-input {
  width: 100%;
}

.el-button {
  margin-top: 20px;
  width: 100%;
}
</style>