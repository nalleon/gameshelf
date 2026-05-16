<template>
  <div class="h-screen flex flex-col bg-[#0b0e14]">
    <!-- NAVBAR -->
    <div class="flex-shrink-0 sticky top-0 z-50">
      <Navbar />
    </div>

    <!-- SCROLL AREA -->
    <section
      ref="scrollContainer"
      class="flex-1 overflow-y-auto p-6 sm:p-8 pb-28 text-gsblanco relative"
    >
      <div class="max-w-[1600px] mx-auto pb-20">
        
        <!-- HEADER -->
        <div class="mb-8 flex items-center justify-between text-gsmenta">
          <h2 class="text-2xl font-semibold border-l-4 border-gsmenta/50 pl-4">
            Game Catalog
          </h2>

          <button
            @click="showSettings = true"
            class="flex items-center gap-2 text-sm px-3 py-2 rounded-full border border-gsgris/30 hover:border-gsmenta hover:text-gsmenta transition"
          >
            <i class="pi pi-cog"></i>
            Settings
          </button>
        </div>

        <!-- GRID -->
        <main class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-5 gap-y-10 gap-x-6">
          <div
            v-for="game in games"
            :key="game.id"
            class="group flex flex-col bg-[#161a21] rounded-xl border border-gsgris/20 hover:border-gsmenta/50 transition-all duration-300 shadow-lg"
          >
            <GameCard :game="game" />
          </div>
        </main>

        <!-- PAGINATION -->
        <Pagination
          :current-page="currentPage"
          :total-pages="totalPages"
          @change="goToPage"
        />
      </div>

      <!-- FLOAT BUTTON -->
      <ScrollTopButton
        :target="scrollContainer"
        :threshold="300"
      />
    </section>
  </div>

  <!-- SETTINGS -->
  <Transition name="fade">
    <div
      v-if="showSettings"
      class="fixed inset-0 z-50 flex items-center justify-center bg-black/60"
      @click.self="showSettings = false"
    >
      <div class="bg-[#161a21] p-6 rounded-xl border border-gsgris/30 w-[90%] max-w-md text-gsblanco">
        
        <div class="flex items-center justify-between mb-4">
          <h3 class="text-lg font-semibold text-gsmenta flex items-center gap-2">
            <i class="pi pi-cog"></i>
            Settings
          </h3>

          <button @click="showSettings = false" class="text-gsgris hover:text-gsblanco transition">
            <ion-icon name="close-outline"></ion-icon>
          </button>
        </div>

        <label class="flex items-center justify-between gap-4">
          <span class="text-sm">Show mature content</span>

          <input
            type="checkbox"
            v-model="matureContent"
            class="w-5 h-5 accent-gsmenta"
          />
        </label>

        <p class="text-xs text-gsgris mt-3 leading-relaxed">
          Enabling this option includes adult-rated games as well as titles without an assigned age rating.
        </p>
      </div>
    </div>
  </Transition>
</template>

<script setup lang="ts">
import { computed, onMounted, ref, watch } from 'vue';
import { useRoute } from 'vue-router';
import ScrollTopButton from '@/components/ScrollTopButton.vue'
import axios from 'axios';

import GameCard from '@/components/GameCard.vue';
import Navbar from '@/components/Navbar.vue';
import type { Game } from '@/types/gameListTypes';
import { useAuthStore } from '@/stores/authStore';
import api from "@/api/client";
import Pagination from '@/components/Pagination.vue'

const games = ref<Game[] | null>([])
const loading = ref(true)
const route = useRoute()
const authStore = useAuthStore()
const scrollContainer = ref<HTMLElement | null>(null)
const showSettings = ref(false)

const matureContent = ref(false)

const STORAGE_KEY = computed(() => {
    const userId = authStore.getSelfId()

    return userId
        ? `games_preferences_user_${userId}`
        : 'games_preferences_guest'
})
onMounted(() => {
    const saved = localStorage.getItem(STORAGE_KEY.value)

    if (saved) {
        const parsed = JSON.parse(saved)
        matureContent.value = parsed.matureContent ?? false
    }

    loadPage(1)
    loading.value = false
})

watch(matureContent, (val) => {
    localStorage.setItem(
        STORAGE_KEY.value,
        JSON.stringify({ matureContent: val })
    )

    loadPage(1)
})


// --- VARIABLES DE PAGINACIÓN ---
const currentPage = ref(1);
const totalPages = ref(1);
const totalCount = ref(0);
const hasNext = ref(false);
const hasPrevious = ref(false);

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

const goToPage = (page: number) => {
    if (page < 1 || page > totalPages.value) return

    loadPage(page)
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