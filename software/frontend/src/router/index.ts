import { createRouter, createWebHistory } from 'vue-router'
import LandingView from '@/views/LandingView.vue'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    { path: '/', component: LandingView },
    {
      path: '/mapa',
      component: () => import('@/views/MapView.vue'),
    },
    {
      path: '/mock',
      component: () => import('@/views/MockView.vue'),
    },
    {
      path: '/simulador',
      component: () => import('@/views/SimulatorView.vue'),
    },
  ],
})

export default router
