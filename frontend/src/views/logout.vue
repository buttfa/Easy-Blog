<template>
</template>

<script>
import axios from 'axios';
axios.defaults.withCredentials = true;

export default {
    mounted() {
        this.logout()
    },

    methods: {
        logout() {
            axios.post('http://127.0.0.1:5000/logout')
                .then(res => {
                    window.location.href = "/";
                })
        }
    }
}
</script>
