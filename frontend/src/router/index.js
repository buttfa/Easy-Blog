import {createRouter, createWebHistory} from 'vue-router'

const routes = [
    {
        path: '/',
        component: () => import("../views/index.vue")
    },
    {
        path: '/about',
        component: () => import("../views/about.vue")
    }
]

const router = createRouter({
    history: createWebHistory(),
    routes
})

export default router