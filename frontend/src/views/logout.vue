<template>
</template>

<script>
import axios from 'axios';
axios.defaults.withCredentials = true;
axios.defaults.baseURL = import.meta.env.VITE_EBLOG_API_URL;

export default {
    mounted() {
        this.logout()
    },

    methods: {
        logout() {
            axios.post('/logout')
                .then(res => {
                    window.location.href = "/";
                })
        }
    }
}
</script>
