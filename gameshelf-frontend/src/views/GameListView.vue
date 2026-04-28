<template>
    <div class="h-screen flex flex-col bg-[#0b0e14]"> 
        <div class="flex-shrink-0 sticky top-0 z-50">
            <Navbar/>
        </div>
        <section ref="scrollContainer" @scroll="handleScroll" class="flex-1 overflow-y-auto p-6 sm:p-8 text-gsblanco relative">            
            <div class="max-w-[1600px] mx-auto">
                <div class="mb-8 flex items-center justify-between text-gsmenta">
                    <h2 class="text-2xl font-semibold border-l-4 border-gsmenta/50 pl-4">
                        Catálogo de Juegos
                    </h2>
                    <span class="text-gsgris text-sm">Mostrando {{ games?.length }} resultados</span>
                </div>

                <main class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-5 gap-y-10 gap-x-6">
                    <div v-for="game in paginatedGames" :key="game.id"
                        class="group flex flex-col bg-[#161a21] rounded-xl border border-gsgris/20 hover:border-gsmenta/50 transition-all duration-300 shadow-lg"
                    >
                        <GameCard :game="game"/>
                    </div>
                </main>

                <nav v-if="totalPages > 1" class="mt-16 flex justify-center items-center gap-2 text-gsblanco">
                    <button 
                        @click="prevPage" 
                        :disabled="currentPage === 1"
                        :class="[
                            'w-10 h-10 flex items-center justify-center rounded-lg border transition-colors',
                            currentPage === 1 ? 'border-gsgris/30 text-gsgris/30 cursor-not-allowed' : 'border-gsblanco hover:text-gsmenta hover:border-gsmenta'
                        ]"
                    >
                        <svg xmlns="http://w3.org" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" />
                        </svg>
                    </button>

                    <div class="flex items-center bg-[#161a21] rounded-lg border border-gsblanco p-1 gap-1">
                        <button 
                            v-for="page in totalPages" 
                            :key="page"
                            @click="goToPage(page)"
                            :class="[
                                'w-9 h-9 flex items-center justify-center rounded-md transition-colors',
                                currentPage === page ? 'bg-gsmenta font-bold text-[#161a21]' : 'hover:bg-gsblanco/20'
                            ]"
                        >
                            {{ page }}
                        </button>
                    </div>

                    <button 
                        @click="nextPage" 
                        :disabled="currentPage === totalPages"
                        :class="[
                            'w-10 h-10 flex items-center justify-center rounded-lg border transition-colors',
                            currentPage === totalPages ? 'border-gsgris/30 text-gsgris/30 cursor-not-allowed' : 'border-gsblanco hover:text-gsmenta hover:border-gsmenta'
                        ]"
                    >
                        <svg xmlns="http://w3.org" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
                        </svg>
                    </button>
                </nav>
            </div>
            <Transition name="fade">
                <button 
                    v-show="showButton"
                    @click="scrollTop"
                    class="fixed bottom-8 right-8 z-50 p-3 rounded-md bg-gsmenta text-gsoscuro shadow-xl hover:bg-gsbosque hover:scale-110 transition-all duration-300 group"
                >
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 group-hover:-translate-y-1 transition-transform" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 15l7-7 7 7" />
                    </svg>
                </button>
            </Transition>
        </section>
    </div>
</template>

<script setup lang="ts">
import GameCard from '@/components/GameCard.vue';
import Navbar from '@/components/Navbar.vue';
import type { Game } from '@/types/gameListTypes';
import { computed, onMounted, ref } from 'vue';
import { useGameStore } from '@/stores/gameStore';

const gameStore = useGameStore()

let games = ref<Game[] | null>([])

// Load Games
onMounted(async () => {

    if(gameStore.gamesLoaded){
        games.value = gameStore.games;
    } else {
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
            // console.log(data);
            gameStore.setGamesCache(data);

        } catch (err) {
            console.error(err);
        }
    }

});

// --- VARIABLES DE PAGINACIÓN ---
const currentPage = ref(1);
const itemsPerPage = 15; // Numero de items por página

const totalPages = computed(() => {
    return Math.ceil(games.value?.length || 0 / itemsPerPage);
});

// Calcula qué juegos mostrar en la página actual
const paginatedGames = computed(() => {
    const start = (currentPage.value - 1) * itemsPerPage;
    const end = start + itemsPerPage;
    return games.value?.slice(start, end);
});

// --- FUNCIONES DE NAVEGACIÓN ---
const nextPage = () => {
    if (currentPage.value < totalPages.value) currentPage.value++;
};

const prevPage = () => {
    if (currentPage.value > 1) currentPage.value--;
};

const goToPage = (page: number) => {
    currentPage.value = page;
};

// Botón de scroll hasta arriba
const scrollContainer = ref<HTMLElement | null>(null);
const showButton = ref(false);

const handleScroll = () => {
    if (scrollContainer.value) {
        showButton.value = scrollContainer.value.scrollTop > 300;
    }
};

function scrollTop() {
    scrollContainer.value?.scrollTo({ top: 0, behavior: 'smooth' });
}

</script>

<style scoped>
.fade-enter-active,
.fade-leave-active {
    transition: opacity 0.3s ease, transform 0.3s ease;
}
.fade-enter-from,
.fade-leave-to {
    opacity: 0;
    transform: translateY(20px);
}
</style>