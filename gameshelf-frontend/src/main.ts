import './style.css'

import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import { createPinia } from 'pinia'
import PrimeVue from 'primevue/config';

import { useAuthStore } from '@/stores/authStore';
import 'primeicons/primeicons.css'
import 'flag-icons/css/flag-icons.min.css'

const app = createApp(App)

// Registrar Pinia (obligatorio antes de usar cualquier store)
const pinia = createPinia()
app.use(pinia)

// Registrar PrimeVue
app.use(PrimeVue);

// Inicializar el store de auth para cargar token desde localStorage
useAuthStore().init()

// Registrar router
app.use(router)

// Montar la app
app.mount('#app')
