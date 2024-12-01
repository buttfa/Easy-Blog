<template>
    <h3> 标题 </h3>
    <el-input v-model="title" clearable placeholder="请输入标题" />
    <h3> 作者 </h3>
    <el-input v-model="author" clearable placeholder="请输入作者" />
    <h3> 内容 </h3>
    <el-input v-model="content" placeholder="请输入内容" />
    <button @click="add_post"> 添加 </button>
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

    methods: {
        add_post() {
            axios.post('http://127.0.0.1:5000/add_post', {
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
