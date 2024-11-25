import {createRouter, createWebHistory} from 'vue-router'

const routes = [
    {
        path: '/',
        component: () => import("../views/index.vue")
    },
    {
        path: '/about',
        component: () => import("../views/about.vue")
    },
    {
        path: '/login',
        component: () => import("../views/login.vue")
    },
]

const router = createRouter({
    history: createWebHistory(),
    routes
})

export default router