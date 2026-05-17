<template>
  <div class="h-screen flex flex-col bg-[#0b0e14]">
    <div class="flex-shrink-0 sticky top-0 z-50">
      <Navbar />
    </div>

    <section ref="scrollContainer" class="flex-1 overflow-y-auto p-4 sm:p-6 md:p-8 pb-28 text-gsblanco relative">
      <div class="max-w-[1600px] mx-auto pb-20">

        <div class="mb-6 md:mb-8 flex flex-col sm:flex-row sm:items-center justify-between border-b border-gsgris/10 pb-4 md:pb-6 gap-4">
          <div class="flex flex-col md:flex-row md:items-center gap-3 md:gap-6">
            <div class="flex items-center gap-3 text-gsmenta">
              <i class="pi pi-th-large text-xl md:text-2xl"></i>
              <h2 class="text-xl md:text-2xl font-semibold border-l-4 border-gsmenta/50 pl-3 md:pl-4">
                Catalog
              </h2>
            </div>

            <div v-if="activeFilters.length > 0" class="flex flex-wrap items-center gap-2">
              <div v-for="(filter, index) in activeFilters" :key="index"
                class="flex items-center gap-2 text-xs md:text-sm text-gsgris bg-[#161a21]/60 px-3 py-1.5 rounded-xl border border-gsgris/10 w-fit">
                <i class="pi pi-tag text-[10px] md:text-xs text-gsmenta/70"></i>
                <span>{{ filter.label }}:</span>
                <span class="text-gsmenta font-bold tracking-wide">
                  {{ filter.value }}
                </span>
              </div>
            </div>
          </div>

          <button @click="showSettings = true"
            class="flex items-center gap-2 text-sm px-4 py-2 rounded-full border border-gsgris/30 hover:border-gsmenta hover:text-gsmenta bg-[#161a21]/50 transition self-start sm:self-auto shadow-sm">
            <i class="pi pi-cog"></i>
            Settings
          </button>
        </div>

        <div v-if="loading" class="flex flex-col items-center justify-center py-32 text-gsmenta">
          <i class="pi pi-spin pi-spinner text-4xl mb-4"></i>
          <span class="text-sm tracking-wider uppercase font-medium text-gsgris animate-pulse">Loading catalog...</span>
        </div>

        <main v-else-if="games && games.length > 0"
          class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-5 gap-y-10 gap-x-6">
          <div v-for="game in games" :key="game.id"
            class="group flex flex-col bg-[#161a21] rounded-xl border border-gsgris/20 hover:border-gsmenta/50 transition-all duration-300 shadow-lg">
            <GameCard :game="game" />
          </div>
        </main>

        <div v-else
          class="flex flex-col items-center justify-center py-16 md:py-24 text-gsgris border border-dashed border-gsgris/10 rounded-2xl bg-[#161a21]/30 backdrop-blur-sm px-4">
          <div class="bg-[#161a21] border border-gsgris/10 p-5 rounded-full shadow-md mb-4 flex items-center justify-center">
            <i class="pi pi-search-minus text-3xl text-gsmenta/40"></i>
          </div>
          
          <h3 class="text-base md:text-lg font-semibold text-gsblanco mb-1 text-center">No results found</h3>
          <p class="text-xs md:text-sm text-gsgris text-center max-w-sm">
            We couldn't find any games matching your search criteria. Try checking your spelling or using different keywords.
          </p>
        </div>

        <Pagination v-if="!loading && games && games.length > 0" :current-page="currentPage" :total-pages="totalPages"
          @change="goToPage" />
      </div>

      <ScrollTopButton :target="scrollContainer" :threshold="300" />
    </section>
  </div>

  <Transition name="fade">
    <div v-if="showSettings" class="fixed inset-0 z-50 flex items-center justify-center bg-black/60"
      @click.self="showSettings = false">
      <div class="bg-[#161a21] p-6 rounded-xl border border-gsgris/30 w-[90%] max-w-md text-gsblanco">

        <div class="flex items-center justify-between mb-4">
          <h3 class="text-lg font-semibold text-gsmenta flex items-center gap-2">
            <i class="pi pi-cog"></i>
            Settings
          </h3>

          <button @click="showSettings = false" class="text-gsgris hover:text-red-400 transition">
            <i class="pi pi-times"></i>
          </button>
        </div>

        <label class="flex items-center justify-between gap-4 cursor-pointer">
          <span class="text-sm">Show mature content</span>
          <input type="checkbox" v-model="matureContent" class="w-5 h-5 accent-gsmenta cursor-pointer" />
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
  return userId ? `games_preferences_user_${userId}` : 'games_preferences_guest'
})

// Mapea dinámicamente los queries activos para renderizar las etiquetas en la cabecera
const activeFilters = computed(() => {
  const filters: Array<{ label: string; value: string }> = []
  
  if (route.query.q) filters.push({ label: 'Results for', value: route.query.q as string })
  if (route.query.developer) filters.push({ label: 'Developer', value: route.query.developer as string })
  if (route.query.publisher) filters.push({ label: 'Publisher', value: route.query.publisher as string })
  if (route.query.year) filters.push({ label: 'Year', value: route.query.year as string })
  if (route.query.region) filters.push({ label: 'Region', value: route.query.region as string })
  
  if (route.query.genres) {
    const genres = Array.isArray(route.query.genres) ? route.query.genres : [route.query.genres]
    genres.forEach(g => {
      if (g) filters.push({ label: 'Genre', value: g as string })
    })
  }
  
  return filters
})

// --- VARIABLES DE PAGINACIÓN ---
const currentPage = ref(1);
const totalPages = ref(1);
const totalCount = ref(0);
const hasNext = ref(false);
const hasPrevious = ref(false);

const loadPage = async (page: number) => {
  loading.value = true
  try {
    const data = await getGames(page)
    games.value = data.results
    currentPage.value = data.current_page
    totalPages.value = data.total_pages
    hasNext.value = data.has_next
    hasPrevious.value = data.has_previous
    totalCount.value = data.count
  } catch (error: any) {
    console.error("Error fetching games:", error)
    games.value = []
  } finally {
    loading.value = false
  }
}

async function getGames(page: number) {
  const params = new URLSearchParams()

  params.append('page', page.toString())
  params.append('page_size', '20')
  params.append('mature_content', matureContent.value ? 'true' : 'false')

  if (route.query.q) params.append('q', route.query.q as string)
  if (route.query.developer) params.append('developer', route.query.developer as string)
  if (route.query.publisher) params.append('publisher', route.query.publisher as string)
  if (route.query.year) params.append('year', route.query.year as string)
  if (route.query.region) params.append('region', route.query.region as string)

  if (route.query.genres) {
    const genres = Array.isArray(route.query.genres) ? route.query.genres : [route.query.genres]
    genres.forEach(g => {
      if (g) params.append('genres', g)
    })
  }

  const response = await api.get('/api/games/search/', {
    params: Object.fromEntries(params)
  })

  return response.data
}

onMounted(() => {
  const saved = localStorage.getItem(STORAGE_KEY.value)
  if (saved) {
    const parsed = JSON.parse(saved)
    matureContent.value = parsed.matureContent ?? false
  }
  
  if (Object.keys(route.query).length === 0) {
    loadPage(1)
  }
})

watch(matureContent, (val) => {
  localStorage.setItem(STORAGE_KEY.value, JSON.stringify({ matureContent: val }))
  loadPage(1)
})

watch(
  () => route.query,
  async () => {
    await loadPage(1)
  },
  { immediate: true }
)

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