<template>
    <el-menu mode="horizontal" :default-active="1" background-color="#545c64" text-color="#fff" active-text-color="#ffd04b">
        <el-menu-item index="1">
            {{ blogger_info['name'] }}的博客
        </el-menu-item>
        <el-menu-item index="2" v-if="user_info.length == 0">
            <a href="/login"> 登录 </a>
        </el-menu-item>
        <el-menu-item index="3">
            <a href="/about"> 关于 </a>
        </el-menu-item>
    </el-menu>
    
    
    <li v-for="post in post_list" :key="post['id']">{{ post['title'] }} {{ post['author'] }} {{ post['content'] }}</li>
</template>

<script>
import axios from 'axios'

export default {
    data () {
        return {
            msg: 'Hello Easy-Blog!',
            blogger_info: [],
            user_info: [],
            post_list: []
        }
    },

    created() {
        // this.get_blogger_info()
    },

    mounted() {
        this.get_blogger_info(),
        this.get_user_info(),
        this.get_post_list()
    },

    methods: {
        get_blogger_info() {
            axios.post('http://127.0.0.1:5000/get_blogger_info')
            .then(res => {
                this.blogger_info = res.data['blogger_info']
                console.log(res.data['blogger_info'])
            })
        },
        get_user_info() {
            axios.post('http://127.0.0.1:5000/get_user_info')
            .then(res => {
                user_info = res.data['user_info']
                console.log(res.data['user_info'])
            })
        },
        get_post_list() {
            axios.post('http://127.0.0.1:5000/get_post_list')
            .then(res => {
                this.post_list = res.data['post_list']
                console.log(res.data['post_list'])
            })
        }
    }
}
</script>