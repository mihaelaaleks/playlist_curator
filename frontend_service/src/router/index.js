import { createRouter, createWebHistory } from 'vue-router';
import Ping from '@/components/Ping.vue';

const routes = [
  {
    path: '/',
    name: 'Home',
    component: () => import('../views/Home.vue')
  },
  {
    path: '/curator',
    name: 'curator',
    component: () => import('../views/Curator.vue')
  },
  {
    path: '/stats',
    name: 'stats',
    // route level code-splitting
    // this generates a separate chunk (About.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: () => import('../views/Stats.vue')
  },
  {
    path: '/ping',
    name: 'ping', 
    component: Ping
  }
]

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: routes
})

export default router
