<template>
    <el-menu mode="horizontal" :default-active="main_menu_activate_index" background-color="#545c64" text-color="#fff"
        active-text-color="#ffd04b">
        <el-menu-item index="1">
            <router-link to="/" style="color: white; text-decoration: none"> {{ blogger_info['name'] }}的博客 </router-link>
        </el-menu-item>

        <el-sub-menu index="2" v-if="Object.keys(user_info).length == 0">
            <template #title>
                <router-link to="/login" style="color:white; text-decoration: none"> 登录 </router-link>
            </template>
            
            <el-menu-item index="2-1">
                 <router-link to="/register" style="color:white; text-decoration: none"> 注册 </router-link>
            </el-menu-item>
        </el-sub-menu>

        <el-sub-menu index="2" v-else>
            <template #title> {{ user_info['name'] }} </template>

            <el-menu-item index="2-1">
                <router-link to="/user_info" style="color: white; text-decoration: none"> 用户信息 </router-link>
            </el-menu-item>

            <el-menu-item index="2-3" v-if="blogger_info['user_id'] == user_info['user_id']">
                <router-link to="/post_management" style="color: white; text-decoration: none"> 博文管理 </router-link> 
            </el-menu-item>

            <el-menu-item index="2-2">
                <router-link to="/logout" style="color: white; text-decoration: none"> 登出 </router-link>
            </el-menu-item>
        </el-sub-menu>

        <el-menu-item index="3">
            <router-link to="/about" style="text-decoration: none"> 关于 </router-link>
        </el-menu-item>
    </el-menu>
</template>

<script>
import { reactive, ref } from 'vue'

import axios from 'axios';
axios.defaults.withCredentials = true;
axios.defaults.baseURL = import.meta.env.VITE_EBLOG_API_URL;

export default {
    data() {
        return {
            main_menu_activate_index: ref("1"),
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
            axios.post('/get_blogger_info')
                .then(res => {
                    this.blogger_info = res.data['blogger_info']
                })
        },
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
