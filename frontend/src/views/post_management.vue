<template>
    <button @click="add_post"> 添加博文 </button>
    
    <li v-for="post in post_list" :key="post['[post_id']">
        {{ post['post_id'] }} {{ post['title'] }} {{ post['author'] }} {{ post['content'] }}
        <button @click="update_post(post['post_id'])"> 修改博文 </button>
        <button @click="delete_post(post['post_id'])"> 删除博文 </button>
    </li>
</template>

<script>
import axios from 'axios';
axios.defaults.withCredentials = true;

import { ElMessage, ElMessageBox, ElNotification } from 'element-plus'

export default {
    data() {
        return {
            post_list: []
        }
    },
 
    mounted() {
        this.get_post_list()
    },

    methods: {
        get_post_list() {
            axios.post('http://127.0.0.1:5000/get_post_list')
                .then(res => {
                    this.post_list = res.data['post_list']
                })
        },

        add_post() {
            window.location.href = "/post_management/add_post";
        },
       
        update_post(target_post_id) {
            window.location.href = "/post_management/update_post?post_id=" + target_post_id;
        },

        delete_post(target_post_id) {
            axios.post('http://127.0.0.1:5000/delete_post', {
                post_id: target_post_id
            })
                .then(res => {
                    //  If the deletion of the blog post fails, it will display 'delete blog post failed'.
                    if (res.data['status'] == 'fail') {
                        ElMessage({
                            type: 'fail',
                            message: '删除博文失败',
                            showClose: true
                        })
                    }

                    // If the deletion of the blog post is successful, it will display 'delete blog post successfully' and update the blog post list.
                    if (res.data['status'] == 'success') {
                        ElMessage({
                            type: 'success',
                            message: '删除博文成功',
                            showClose: true
                        })

                        this.get_post_list()
                    }
                })
        }
    }
}

</script>
