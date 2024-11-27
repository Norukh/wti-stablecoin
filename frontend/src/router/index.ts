import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import WTIView from "../views/WTIView.vue";
import AboutView from '@/views/AboutView.vue';
import TransparencyView from '@/views/TransparencyView.vue';

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView
    },
    {
      path: '/transparency',
      name: 'transparency',
      component: () => TransparencyView
    },
    {
      path: '/about',
      name: 'about',
      component: () => AboutView
    },
    {
      path: '/WTI',
      name: 'WTI',
      component: () => WTIView
    }
  ]
})

export default router
