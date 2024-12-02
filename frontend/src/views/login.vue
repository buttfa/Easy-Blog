<template>
  <div class="login-container">
    <el-card class="box-card">
      <template #header>
        <div class="card-header">
          <h3> 登录 </h3>
        </div>
      </template>
      <div class="form-item">
        <el-input v-model="email" clearable placeholder="请输入邮箱" />
      </div>
      <div class="form-item">
        <el-input v-model="password" show-password clearable placeholder="请输入密码" />
      </div>
      <div class="form-item">
        <el-button type="primary" @click="login">登录</el-button>
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
      email: '',
      password: ''
    }
  },

  methods: {
    login() { 
      console.log(this.email, this.password)
      axios.post('http://127.0.0.1:5000/login', {
        email: this.email,
        password: this.password
      })
        .then(res => {

          // If login fails, display 'login failure' and clear the content of the login input box.
          if (res.data['status'] == "fail") {
            this.email = '',
            this.password = '',
            this.login_fail()
          }

          // If the login is successful, it will display 'login successfully' and return to the main page.
          if (res.data['status'] == "success") {
            this.login_success()
            window.location.href = "/";
          }
        })
    },

    login_success () {
      ElMessage({
        type: 'success',
        message: '登录成功',
        showClose: true
      })  
    },

    login_fail () {
      ElMessage({
        type: 'error', // Corrected the type from 'fail' to 'error'
        message: '登录失败',
        showClose: true
      })
    }
  }
}
</script>

<style scoped>
.login-container {
  position: relative;
  top: 0;
  left: 0;
  bottom: 0;
  right: 0;
  margin: auto auto;
  width: 30%;
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