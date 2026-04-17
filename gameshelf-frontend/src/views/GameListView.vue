<template>
    <Navbar/>
    <section class="min-h-screen bg-[--color-gsoscuro] p-6 sm:p-8 text-[--color-gsblanco]">
        <!-- Contenedor del Grid -->
        <div class="max-w-[1600px] mx-auto">
            <!-- Título de sección opcional / Filtros rápidos -->
            <div class="mb-8 flex items-center justify-between text-gsmenta">
                <h2 class="text-2xl font-semibold border-l-4 border-gsmenta/50 pl-4">
                    Catálogo de Juegos
                </h2>
                <span class="text-gsgris text-sm">Mostrando 30 resultados</span>
            </div>

            <!-- Grid Principal: 5 columnas en escritorio -->
            <main class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-5 gap-y-10 gap-x-6">
                <!-- Card de Juego (Iteración de 30 elementos) -->
                <div v-for="game in games" :key="game.id"
                    class="group flex flex-col bg-[#161a21] rounded-xl border border-gsgris/20 hover:border-gsmenta/50 transition-all duration-300 shadow-lg"
                >
                    <!-- Contenedor de Imagen -->
                    <div class="relative aspect-[3/4] rounded-t-xl overflow-hidden">
                        <img :src="game.title" :alt="game.title" class="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500">
                        <!-- Badge de Plataforma -->
                        <div class="absolute top-2 left-2 bg-gsoscuro/80 backdrop-blur-sm text-gsmenta text-[10px] font-bold px-2 py-0.5 rounded border border-gsmenta/30 uppercase">
                        <!-- {{ game.platform }} -->
                        </div>
                    </div>

                    <!-- Información del Juego -->
                    <div class="p-4 flex flex-col flex-grow">
                        <h3 class="font-bold text-base line-clamp-1 group-hover:text-[--color-gsmenta] transition-colors">
                            {{ game.title }}
                        </h3>
                        <p class="text-[--color-gsgris] text-xs mt-1 mb-4 italic leading-tight">
                            <!-- {{ game.developer }} -->
                        </p>
                    </div>
                </div>
            </main>

            <!-- Paginación Estilo Coleccionista -->
            <nav class="mt-16 flex justify-center items-center gap-2 text-gsblanco">
                <button class="w-10 h-10 flex items-center justify-center rounded-lg border border-gsblanco hover:text-color-gsmenta hover:border-gsmenta transition-colors">
                    <svg xmlns="http://w3.org" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" />
                    </svg>
                </button>

                <!-- Páginas -->
                <div class="flex items-center bg-[#161a21] rounded-lg border border-gsblanco p-1">
                    <button class="w-9 h-9 flex items-center justify-center rounded-md bg-gsmenta font-bold">1</button>
                    <button class="w-9 h-9 flex items-center justify-center rounded-md hover:bg-gsblanco/20 transition-colors">2</button>
                    <button class="w-9 h-9 flex items-center justify-center rounded-md hover:bg-gsblanco/20 transition-colors">3</button>
                    <span class="px-2 text-gsblanco">...</span>
                    <button class="w-9 h-9 flex items-center justify-center rounded-md hover:bg-gsblanco/20 transition-colors">12</button>
                </div>

                <button class="w-10 h-10 flex items-center justify-center rounded-lg border border-gsblanco hover:text-gsmenta hover:border-gsmenta transition-colors">
                <svg xmlns="http://w3.org" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
                </svg>
                </button>
            </nav>
        </div>
    </section>
</template>

<script setup lang="ts">
import Navbar from '@/components/Navbar.vue';
import type { Game } from '@/types/gameListTypes';
import { onMounted, ref } from 'vue';


let games = ref<Game[]>([])

onMounted(async () => {
    try {
        const webhookUrl = 'http://127.0.0.1:8000/api/games/'

        const response = await fetch(webhookUrl, 
            {
                method: "GET",
                headers: {
                    'Content-Type': 'application/json'
                }    
            }
        );

        const data = await response.json();
        games.value = data;
        console.log(data)
    } catch (err) {
        console.error(err);
    }
});


</script>

<style scoped>
    
</style>