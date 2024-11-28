<template>
    <li v-for="post in post_list" :key="post['[post_id']">{{ post['title'] }} {{ post['author'] }} {{ post['content'] }}
    </li>
</template>

<script>
import axios from 'axios';
axios.defaults.withCredentials = true;
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
        }
    }
}
</script>
