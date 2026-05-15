<template>
    <div class="h-screen flex flex-col bg-[#0b0e14]">
        <div class="flex-shrink-0 sticky top-0 z-50">
            <Navbar />
        </div>
        <section ref="scrollContainer" @scroll="handleScroll"
            class="flex-1 overflow-y-auto p-6 sm:p-8 text-gsblanco relative">
            <div class="max-w-[1600px] mx-auto">
                <div class="mb-8 flex items-center justify-between text-gsmenta">
                    <h2 class="text-2xl font-semibold border-l-4 border-gsmenta/50 pl-4">
                        Game Catalog
                    </h2>

                    <button @click="showSettings = true"
                        class="flex items-center gap-2 text-sm px-3 py-2 rounded-lg border border-gsgris/30 hover:border-gsmenta hover:text-gsmenta transition">
                        <i class="pi pi-cog"></i>
                        Settings
                    </button>
                </div>

                <main class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-5 gap-y-10 gap-x-6">
                    <div v-for="game in games" :key="game.id"
                        class="group flex flex-col bg-[#161a21] rounded-xl border border-gsgris/20 hover:border-gsmenta/50 transition-all duration-300 shadow-lg">
                        <GameCard :game="game" />
                    </div>
                </main>

                <nav v-if="totalPages > 1" class="mt-16 flex justify-center items-center gap-2 text-gsblanco">
                    <button @click="prevPage" :disabled="!hasPrevious" :class="[
                        'w-10 h-10 flex items-center justify-center rounded-lg border transition-colors',
                        currentPage === 1 ? 'border-gsgris/30 text-gsgris/30 cursor-not-allowed' : 'border-gsblanco hover:text-gsmenta hover:border-gsmenta'
                    ]">
                        <svg xmlns="http://w3.org" class="h-5 w-5" fill="none" viewBox="0 0 24 24"
                            stroke="currentColor">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" />
                        </svg>
                    </button>

                    <div class="flex items-center bg-[#161a21] rounded-lg border border-gsblanco p-1 gap-1">
                        <template v-for="page in visiblePages" :key="page">
                            <button v-if="typeof page === 'number'" @click="goToPage(page)" :class="[
                                'w-9 h-9 flex items-center justify-center rounded-md transition-colors',
                                currentPage === page ? 'bg-gsmenta font-bold text-[#161a21]' : 'hover:bg-gsblanco/20'
                            ]">
                                {{ page }}
                            </button>

                            <span v-else class="w-9 h-9 flex items-center justify-center text-gsgris/60">
                                {{ page }}
                            </span>
                        </template>
                    </div>

                    <button @click="nextPage" :disabled="!hasNext" :class="[
                        'w-10 h-10 flex items-center justify-center rounded-lg border transition-colors',
                        currentPage === totalPages ? 'border-gsgris/30 text-gsgris/30 cursor-not-allowed' : 'border-gsblanco hover:text-gsmenta hover:border-gsmenta'
                    ]">
                        <svg xmlns="http://w3.org" class="h-5 w-5" fill="none" viewBox="0 0 24 24"
                            stroke="currentColor">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
                        </svg>
                    </button>
                </nav>
            </div>
            <Transition name="fade">
                <button v-show="showButton" @click="scrollTop"
                    class="fixed bottom-8 right-8 z-50 p-3 rounded-md bg-gsmenta text-gsoscuro shadow-xl hover:bg-gsbosque hover:scale-110 transition-all duration-300 group">
                    <svg xmlns="http://www.w3.org/2000/svg"
                        class="h-6 w-6 group-hover:-translate-y-1 transition-transform" fill="none" viewBox="0 0 24 24"
                        stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 15l7-7 7 7" />
                    </svg>
                </button>
            </Transition>
        </section>
    </div>

    <Transition name="fade">
        <div v-if="showSettings" class="fixed inset-0 z-50 flex items-center justify-center bg-black/60"
            @click.self="showSettings = false">
            <div class="bg-[#161a21] p-6 rounded-xl border border-gsgris/30 w-[90%] max-w-md text-gsblanco">

                <div class="flex items-center justify-between mb-4">
                    <h3 class="text-lg font-semibold text-gsmenta flex items-center gap-2">
                        <ion-icon name="settings-outline"></ion-icon>
                        Settings
                    </h3>

                    <button @click="showSettings = false" class="text-gsgris hover:text-gsblanco transition">
                        <ion-icon name="close-outline"></ion-icon>
                    </button>
                </div>

                <label class="flex items-center justify-between gap-4">
                    <span class="text-sm">
                        Show mature content
                    </span>

                    <input type="checkbox" v-model="matureContent" class="w-5 h-5 accent-gsmenta" />
                </label>

                <p class="text-xs text-gsgris mt-3 leading-relaxed">
                    Enabling this option includes adult-rated games as well as titles without an assigned age rating.
                    Due to current data limitations, unrated content cannot be reliably classified and is therefore
                    treated
                    as mature content.
                </p>

            </div>
        </div>
    </Transition>
</template>

<script setup lang="ts">
import { computed, onMounted, ref, watch } from 'vue';
import { useRoute } from 'vue-router';

import axios from 'axios';

import GameCard from '@/components/GameCard.vue';
import Navbar from '@/components/Navbar.vue';
import type { Game } from '@/types/gameListTypes';

import api from "@/api/client";

const games = ref<Game[] | null>([])
const loading = ref(true)
const route = useRoute()

const showSettings = ref(false)

const matureContent = ref(false)

const STORAGE_KEY = 'games_preferences'

onMounted(() => {
    const saved = localStorage.getItem(STORAGE_KEY)
    if (saved) {
        const parsed = JSON.parse(saved)
        matureContent.value = parsed.matureContent ?? false
    }

    loadPage(1)
    loading.value = false
})

watch(matureContent, (val) => {
    localStorage.setItem(
        STORAGE_KEY,
        JSON.stringify({ matureContent: val })
    )

    // recargar juegos cuando cambie el filtro
    loadPage(1)
})

// --- VARIABLES DE PAGINACIÓN ---
const currentPage = ref(1);
const totalPages = ref(1);
const totalCount = ref(0);
const hasNext = ref(false);
const hasPrevious = ref(false);

// Load Games
onMounted(async () => {
    await loadPage(1)
    loading.value = false
});

// Detecta cambios en la URL (filtros, búsqueda, etc.) y recarga la página
watch(
    () => route.query,
    async () => {
        await loadPage(1)
    }
)

const loadPage = async (page: number) => {
    try {
        const data = await getGames(page)

        games.value = data.results
        currentPage.value = data.current_page
        totalPages.value = data.total_pages
        hasNext.value = data.has_next
        hasPrevious.value = data.has_previous
        totalCount.value = data.count

    } catch (error: any) {
        console.error(error)
    }
}

async function getGames(page: number) {

    const params = new URLSearchParams()

    params.append('page', page.toString())
    params.append('page_size', '15')
    params.append('mature_content', matureContent.value ? 'true' : 'false')

    if (route.query.q) {
        params.append('q', route.query.q as string)
    }

    if (route.query.developer) {
        params.append('developer', route.query.developer as string)
    }

    if (route.query.publisher) {
        params.append('publisher', route.query.publisher as string)
    }

    if (route.query.year) {
        params.append('year', route.query.year as string)
    }

    if (route.query.genres) {
        const genres = Array.isArray(route.query.genres)
            ? route.query.genres
            : [route.query.genres]

        genres.forEach(g => {
            if (g) params.append('genres', g)
        })
    }

    const response = await api.get('/api/games/search/', {
        params: Object.fromEntries(params)
    })

    return response.data
}

// --- FUNCIONES DE NAVEGACIÓN ---
const nextPage = () => {
    if (hasNext.value) loadPage(currentPage.value + 1);
};

const prevPage = () => {
    if (hasPrevious.value) loadPage(currentPage.value - 1);
};

const goToPage = (page: number) => {
    loadPage(page);
};

// Lógica para calcular qué números de página mostrar
const visiblePages = computed(() => {
    const total = totalPages.value;
    const current = currentPage.value;
    const delta = 2; // Páginas a mostrar a la izquierda y derecha de la actual
    const range = [];
    const rangeWithDots = [];
    let l;

    for (let i = 1; i <= total; i++) {
        if (i === 1 || i === total || (i >= current - delta && i <= current + delta)) {
            range.push(i);
        }
    }

    for (let i of range) {
        if (l) {
            if (i - l === 2) {
                rangeWithDots.push(l + 1);
            } else if (i - l !== 1) {
                rangeWithDots.push('...');
            }
        }
        rangeWithDots.push(i);
        l = i;
    }

    return rangeWithDots;
});

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