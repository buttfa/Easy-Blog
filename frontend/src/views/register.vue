<template>
    <div class="register-container">
        <h3> 注册 </h3>
        <el-input v-model="name" clearable placeholder="请输入用户名" />
        <el-input v-model="email" clearable placeholder="请输入邮箱" />
        <el-input v-model="password" show-password clearable placeholder="请输入密码" />
        <el-button type="primary" @click="register">注册</el-button>
    </div>
</template>

<script>
import axios from 'axios';
axios.defaults.withCredentials = true;

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
            axios.post('http://127.0.0.1:5000/register', {
                name: this.name,
                email: this.email,
                password: this.password
            })
                .then(res => {

                    // If register fails, display 'register failure' and clear the content of the login input box.
                    if (res.data['status'] == "fail") {
                        this.email = '',
                        this.password = '',
                        this.login_fail()
                    }

                    // If the register is successful, it will display 'register successfully' and return to the main page.
                    if (res.data['status'] == "success") {
                        this.login_success()
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
                type: 'fail',
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
    width: 30%;
}
</style>
