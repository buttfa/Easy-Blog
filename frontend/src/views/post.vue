<template>
    <h3> {{ post_info['title'] }} </h3>
    <h3> {{ post_info['author'] }} </h3>
    <h3> {{ post_info['content'] }} </h3>
    <hr>

    <li v-for="comment in comment_list" :key="comment['comment_id']">
        {{ comment['name'] }} {{ comment['user_id'] }} : {{ comment['content'] }}
    </li>

    <el-input v-model="post_comment" clearable placeholder="评论" /> 
    <button @click="add_comment"> 提交评论 </button>
</template>

<script>
import axios from 'axios';
axios.defaults.withCredentials = true;

import { ElMessage, ElMessageBox, ElNotification } from 'element-plus'

export default {
    data() {
        return {
            post_info: {},
            comment_list: [],
            post_comment: ""
        }
    },

    mounted() {
        this.get_post_info(),
        this.get_comment_list()
    },

    methods: {
        get_post_info() {
            axios.post('http://127.0.0.1:5000/get_post_info', {
                post_id: this.$route.query.post_id
            })
                .then(res => {
                this.post_info = res.data['post_info'];
            })
        },

        get_comment_list() {
            axios.post('http://127.0.0.1:5000/get_comment_list', {
                post_id: this.$route.query.post_id
            })
                .then(res => {
                this.comment_list = res.data['comment_list']; 
            })
        },
        add_comment() {
            axios.post('http://127.0.0.1:5000/add_comment', {
                post_id: this.$route.query.post_id,
                content: this.post_comment
            })
                .then(res => {
                    if (res.data['status'] == "fail") {
                        ElMessage({
                            type: 'fail',
                            message: '评论失败',
                            showClose: true
                        }) 
                    }

                    if (res.data['status'] == "success") {
                        ElMessage({
                            type: 'success',
                            message: '评论成功',
                            showClose: true
                        });
                        this.get_comment_list();
                    }
                })
        }
    }
}

</script>
