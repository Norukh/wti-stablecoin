import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import CoinView from '../views/CoinView.vue'
import WTIView from "@/views/WTIView.vue";

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView
    },
    {
      path: '/about',
      name: 'about',
      // route level code-splitting
      // this generates a separate chunk (About.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      component: () => import('../views/AboutView.vue')
    },
    {
      path: '/coin',
      name: 'coin',
      component: () => CoinView
    },
    {
      path: '/WTI',
      name: 'WTI',
      component: () => WTIView
    }
  ]
})

export default router
