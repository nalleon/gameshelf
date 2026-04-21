import GameListView from '@/views/GameListView.vue';
import HomeView from '@/views/HomeView.vue';
import LoginView from '@/views/LoginView.vue';
import ProfileView from '@/views/ProfileView.vue';
import RegisterView from '@/views/RegisterView.vue';
import GameDetails from '@/views/GameDetails.vue';
import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/authStore'

const routes = [
  { path: '/', component: HomeView },
  { path: '/login', component: LoginView },
  { path: '/register', component: RegisterView },
  { 
    path: '/game-list', 
    component: GameListView
  },
  {
    path: '/game-list/detail/:slug',
    component: GameDetails
  },
  { 
    path: '/profile', 
    component: ProfileView,
    meta: { requiresAuth: true } // Indica que esta ruta es privada
  },
];

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes,
})

router.beforeEach((to, from, next) => {
  const authStore = useAuthStore();
  const isProtected = to.matched.some(record => record.meta.requiresAuth); // Si la ruta contiene el meta.requiresAuth o alguno de sus anidados

  if (isProtected && !authStore.isLogged) {
    next('/login'); // Bloquea y manda al login
  } else {
    next(); // Permite el paso
  }
});

export default router
