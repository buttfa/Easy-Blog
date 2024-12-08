<template>
  <el-card class="box-card">
    <template #header>
      <div class="card-header">
        <h3> 用户信息 </h3>
      </div>
    </template>
    <div class="user-info-item">
      <h3> 用户编号：{{ user_info['user_id'] }} </h3>
    </div>
    <div class="user-info-item">
      <h3> 用户名称：{{ user_info['name'] }} </h3>
    </div>
    <div class="user-info-item">
      <h3> 邮箱：{{ user_info['email'] }} </h3>
    </div>
    <div class="user-info-item">
      <h3> 身份：{{ user_info['role'] }} </h3>
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
      user_info: {}
    }
  },

  mounted() {
    this.get_user_info()
  },

  methods: {
    get_user_info() {
      axios.post('/get_user_info')
        .then(res => {
          if (res.data['status'] == 'success') {
            this.user_info = res.data['user_info']
          }
        })
    }
  }
}
</script>

<style scoped>
.box-card {
  width: 100%;
  max-width: 400px;
  margin: 20px auto;
}

.card-header {
  text-align: center;
}

.user-info-item {
  margin-bottom: 10px;
}
</style>