<template>
  <div class="register-container">
    <el-card class="box-card">
      <template #header>
        <div class="card-header">
          <h3> 注册 </h3>
        </div>
      </template>
      <div class="form-item">
        <el-input v-model="name" clearable placeholder="请输入用户名" />
      </div>
      <div class="form-item">
        <el-input v-model="email" clearable placeholder="请输入邮箱" />
      </div>
      <div class="form-item">
        <el-input v-model="password" show-password clearable placeholder="请输入密码" />
      </div>
      <div class="form-item">
        <el-button type="primary" @click="register">注册</el-button>
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
      name: '',
      email: '',
      password: ''
    }
  },

  methods: {
    register() { 
      console.log(this.email, this.password)
      axios.post('/register', {
        name: this.name,
        email: this.email,
        password: this.password
      })
        .then(res => {

          // If register fails, display 'register failure' and clear the content of the login input box.
          if (res.data['status'] == "fail") {
            this.email = '';
            this.password = '';
            this.login_fail();
          }

          // If the register is successful, it will display 'register successfully' and return to the main page.
          if (res.data['status'] == "success") {
            this.login_success();
            window.location.href = "/";
          }
        })
    },

    login_success () {
      ElMessage({
        type: 'success',
        message: '注册成功',
        showClose: true
      })  
    },

    login_fail () {
      ElMessage({
        type: 'error',
        message: '注册失败',
        showClose: true
      })
    }
  }
}
</script>

<style scoped>
.register-container {
  position: relative;
  top: 0;
  left: 0;
  bottom: 0;
  right: 0;
  margin: auto auto;
  width: 70%;
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
}

.box-card {
  width: 100%;
  max-width: 400px;
}

.card-header {
  text-align: center;
}

.form-item {
  margin-bottom: 20px;
}

.el-button {
  width: 100%;
}
</style>