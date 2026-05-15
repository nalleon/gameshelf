import GameListView from '@/views/GameListView.vue';
import HomeView from '@/views/HomeView.vue';
import LoginView from '@/views/LoginView.vue';
import ProfileView from '@/views/ProfileView.vue';
import RegisterView from '@/views/RegisterView.vue';
import GameDetails from '@/views/GameDetails.vue';
import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/authStore'
import EditProfile from '@/views/EditProfile.vue';
import Wishlist from '@/views/Wishlist.vue';
import UserSearch from '@/views/UserSearch.vue';
import Favorites from '@/views/Favorites.vue';
import LibraryList from '@/views/LibraryList.vue';
import CompletedList from '@/views/CompletedList.vue';
import Collections from '@/views/Collections.vue';
import CollectionDetails from '@/views/CollectionDetails.vue';

const routes = [
  { path: '/', component: HomeView },
  { path: '/login', component: LoginView },
  { path: '/register', component: RegisterView },
  { 
    path: '/games', 
    component: GameListView
  },
  {
    path: '/games/:id',
    component: GameDetails
  },
  { 
    path: '/profile', 
    component: ProfileView,
    meta: { requiresAuth: true }
  },
  { 
    path: '/profile/:id', 
    component: ProfileView,
    meta: { requiresAuth: true }
  },
  { 
    path: '/profile/edit', 
    component: EditProfile,
    meta: { requiresAuth: true }
  },
  { 
    path: '/collections/:user_id', 
    component: Collections,
    meta: { requiresAuth: true }
  },
  { 
    path: '/collections/:user_id/:collection_id', 
    component: CollectionDetails,
    meta: { requiresAuth: true }
  },
  // { 
  //   path: '/wishlist/:wishlist_id', 
  //   component: Wishlist,
  //   meta: { requiresAuth: true }
  // },
  { 
    path: '/wishlist/:user_id/:wishlist_id', 
    component: Wishlist,
    meta: { requiresAuth: true }
  },
  { 
    path: '/favorites/:user_id', 
    component: Favorites,
    meta: { requiresAuth: true }
  },
  { 
    path: '/library/:user_id', 
    component: LibraryList,
    meta: { requiresAuth: true }
  },
  { 
    path: '/completed/:user_id', 
    component: CompletedList,
    meta: { requiresAuth: true }
  },
  { 
    path: '/users', 
    component: UserSearch,
  },
];

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes,
})

router.beforeEach((to) => {
  const authStore = useAuthStore();
  const isProtected = to.matched.some(record => record.meta.requiresAuth);

  // Vue 3 prefiere retornar la ruta en vez de invocar next()
  if (isProtected && !authStore.isLogged) {
    return '/login'; 
  }
  // Si no se retorna nada, la navegación continúa normalmente
});

export default router
