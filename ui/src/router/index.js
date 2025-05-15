import { createRouter, createWebHistory } from 'vue-router';
import { AuthService } from '../services/auth';
import Login from '../components/Login.vue';
import Curator from '../views/Curator.vue';

const routes = [
  {
    path: '/',
    redirect: '/curator'
  },
  {
    path: '/login',
    name: 'Login',
    component: Login
  },
  {
    path: '/callback',
    name: 'Callback',
    component: Login  // Reuse Login component for handling callback
  },
  {
    path: '/curator',
    name: 'Curator',
    component: Curator,
    meta: { requiresAuth: true }
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
    component: () => import('../components/Ping.vue')
  }
]
const router = createRouter({
  history: createWebHistory(),
  routes: routes
})

// Navigation guard to check authentication
router.beforeEach((to, from, next) => {
  if (to.matched.some(record => record.meta.requiresAuth)) {
    if (!AuthService.isAuthenticated()) {
      next({
        path: '/login',
        query: { redirect: to.fullPath }
      })
    } else {
      next()
    }
  } else {
    next()
  }
})

export default router
