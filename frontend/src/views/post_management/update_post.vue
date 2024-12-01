<template>
    <h3> 标题 </h3>
    <el-input v-model="title" clearable placeholder="请输入标题" />
    <h3> 作者 </h3>
    <el-input v-model="author" clearable placeholder="请输入作者" />
    <h3> 内容 </h3>
    <el-input v-model="content" placeholder="请输入内容" />
    <button @click="update_post_info"> 修改 </button>
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
        this.get_post_info()
    },

    methods: {
        get_post_info() {
            axios.post('http://127.0.0.1:5000/get_post_info', {
                post_id: this.$route.query.post_id
            }).then(res => {
                this.title = res.data['post_info']['title'];        
                this.author = res.data['post_info']['author'];
                this.content = res.data['post_info']['content'];
            })
        },

        update_post_info() {
            axios.post('http://127.0.0.1:5000/update_post_info', {
                post_id: this.$route.query.post_id,
                title: this.title,
                author: this.author,
                content: this.content
            }).then(res=>{
                window.location.href = "/post_management";
            })
        }   
    }
}


</script>
