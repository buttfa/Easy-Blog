<template>
    <el-menu mode="horizontal" :default-active="main_menu_activate_index" background-color="#545c64" text-color="#fff"
        active-text-color="#ffd04b">
        <el-menu-item index="1-0">
            {{ blogger_info['name'] }}的博客
        </el-menu-item>

        <el-menu-item index="2-0" v-if="Object.keys(user_info).length == 0">
            <a href="/login"> 登录 </a>
        </el-menu-item>

        <el-sub-menu index="2-0" v-else>
            <template #title> {{ user_info['name'] }} </template>

            <el-menu-item index="2-1">
                <a href="/user_info"> 用户信息 </a>
            </el-menu-item>

            <el-menu-item index="2-2">
                <a href="/logout"> 登出 </a>
            </el-menu-item>
        </el-sub-menu>

        <el-menu-item index="3-0">
            <a href="/about"> 关于 </a>
        </el-menu-item>
    </el-menu>
</template>

<script>
import axios from 'axios';
axios.defaults.withCredentials = true;
export default {
    data() {
        return {
            main_menu_activate_index: '1-0',
            blogger_info: {},
            user_info: {}
        }
    },

    mounted() {
        this.get_blogger_info(),
            this.get_user_info()
    },

    methods: {
        get_blogger_info() {
            axios.post('http://127.0.0.1:5000/get_blogger_info')
                .then(res => {
                    this.blogger_info = res.data['blogger_info']
                })
        },
        get_user_info() {
            axios.post('http://127.0.0.1:5000/get_user_info')
                .then(res => {
                    if (res.data['status'] == 'success') {
                        this.user_info = res.data['user_info']
                    }
                })
        }
    }
}
</script>
