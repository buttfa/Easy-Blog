<template>
    <h3> 用户编号：{{ user_info['id'] }} </h3>
    <h3> 用户名称：{{ user_info['name'] }} </h3>
    <h3> 邮箱：{{ user_info['email'] }} </h3>
    <h3> 身份：{{ user_info['role'] }} </h3>
</template>

<script>
import axios from 'axios';
axios.defaults.withCredentials = true;

export default {
    data() {
        return {
            user_info: {}
        }
    },

    mounted() {
        this.get_user_info()
    },

    methods: {
        get_user_info() {
            axios.post('http://127.0.0.1:5000/get_user_info')
                .then(res => {
                    if (res.data['status'] == 'success') {
                        this.user_info = res.data['user_info']
                    }
                })
        }
    },
}
</script>
