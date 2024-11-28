<template>
    <main_menu />
    <router-view />
</template>


<script>
import main_menu from './components/main_menu.vue'
export default {
    components: {
        main_menu
    }
}
</script>
