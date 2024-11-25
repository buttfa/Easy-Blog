<template>
  <div class="login-container">
    <h3> 登录 </h3>
    <el-input v-model="email" clearable placeholder="请输入邮箱" />
    <el-input v-model="password" show-password clearable placeholder="请输入密码" />
    <el-button type="primary" @click="login">登录</el-button>
  </div>
</template>

<script>
import axios from 'axios';
axios.defaults.withCredentials = true;
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
}
</style>
