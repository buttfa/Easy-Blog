<template>
    <button @click="getPosts">Get Posts</button>
    <p> Hello Easy-Blog! </p>
    <li v-for="post in post_list" :key="post['id']">{{ post['title'] }} {{ post['author'] }} {{ post['content'] }}</li>
</template>

<script>
import axios from 'axios'

export default {
    data () {
        return {
            msg: 'Hello Easy-Blog!',
            post_list: []       
        }
    },

    methods: {
        getPosts() {
            axios.get('http://127.0.0.1:5000/get_post_list')
            .then(res => {
                this.post_list = res.data['post_list']
                console.log(res.data['post_list'])
            })
        }
    }
}
</script>