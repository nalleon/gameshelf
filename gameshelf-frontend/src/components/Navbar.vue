<template>
    <nav class="bg-gsoscuro text-gsblanco px-6 py-4 flex items-center justify-between shadow-lg sticky top-0 z-50">
        
        <!-- Logo Izquierda -->
        <router-link to="/" class="flex items-center hover:opacity-80 transition-opacity">
            <img src="../assets/cover-logo-cut.png" alt="" class="h-10 w-auto object-contain" />
            
            <span class="ml-3 font-bold text-xl tracking-tight hidden md:block">
                Game<span class="text-gsmenta">Shelf</span>
            </span>
        </router-link>

        <!-- Contenedor Derecha (Buscador + Cuenta) -->
        <div class="flex items-center gap-4 md:gap-8 flex-1 justify-end">
        
            <!-- Buscador de Juegos -->
            <div class="relative hidden sm:block w-full max-w-xs group">
                <input 
                    v-model="searchQuery"
                    type="text" 
                    placeholder="Buscar juegos..." 
                    class="w-full bg-[#1a1e26] border border-gsgris/30 rounded-full py-2 pl-10 pr-4 text-sm focus:outline-none focus:border-gsmenta focus:ring-1 focus:ring-gsmenta transition-all placeholder-gsgris/60"
                    @keyup.enter="handleSearch"
                />
                <svg xmlns="http://w3.org" class="h-4 w-4 absolute left-3 top-2.5 text-gsgris group-focus-within:text-gsmenta transition-colors" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
                </svg>
            </div>

            <!-- Botón Game List -->
            <router-link 
                to="/gamelist" 
                class="text-sm font-semibold uppercase tracking-wider hover:text-gsmenta transition-colors">
            Colección
            </router-link>

            <!-- Divisor visual -->
            <div class="h-6 w-[1px] bg-gsgris/30"></div>

        <!-- Cuenta -->
            
            <!-- Estado: Autenticado -->
            <template v-if="auth.isLogged">
                <router-link to="/profile" class="flex items-center gap-2 hover:text-gsmenta transition-colors font-medium">
                Mi Perfil
                </router-link>

                <button @click="handleLogout" class="list-none cursor-pointer text-gsgris hover:text-red-400 transition-colors font-medium">
                Cerrar Sesión
                </button>
            </template>

            <!-- Estado: No Autenticado -->
            <template v-else>
                <router-link to="/login" class="bg-gsmenta hover:bg-gsbosque text-gsoscuro px-5 py-2 rounded-md font-bold transition-all transform hover:scale-105 active:scale-95 text-md">
                Login
                </router-link>
            </template>

        </div>
    </nav>
</template>

<script setup lang="ts">
    import {ref} from 'vue'
    import { useAuthStore } from '@/stores/authStore'

    let searchQuery = ref('')

    const auth = useAuthStore()

    function handleLogout() {
        auth.logout()
    }

    function handleSearch(){

    }

</script>

<style scoped>

</style>