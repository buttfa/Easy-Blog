<template>
    <main_navigation_bar />
    <router-view />
</template>


<script>
import main_navigation_bar from './components/main_navigation_bar.vue'

export default {
    components: {
        main_navigation_bar
    }
}
</script>
