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
    {
        path: '/user_info',
        component: () => import("../views/user_info.vue")
    }
]

const router = createRouter({
    history: createWebHistory(),
    routes
})

export default router