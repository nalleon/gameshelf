<template>
    <nav
        class="bg-gsoscuro text-gsblanco px-6 py-4 flex items-center justify-between shadow-lg sticky top-0 z-50 border-b border-white/5">

        <!-- LOGO -->
        <router-link :to="auth.isLogged ? '/games' : '/'"
            class="flex items-center hover:opacity-90 transition-all duration-300">
            <img src="../assets/cover-logo-cut.png" alt="" class="h-10 w-auto object-contain" />

            <span class="ml-3 font-bold text-xl tracking-tight hidden md:block">
                Game<span class="text-gsmenta">Shelf</span>
            </span>
        </router-link>

        <!-- RIGHT -->
        <div class="flex items-center gap-4 md:gap-7 flex-1 justify-end">

            <!-- SEARCH -->
            <div class="hidden lg:flex items-center gap-3 w-full max-w-3xl">

                <!-- SEARCH TYPE -->
                <div class="relative">

                    <select v-model="searchType"
                        class="appearance-none bg-[#161a21] border border-white/8 rounded-2xl px-4 py-2.5 pr-10 text-sm font-medium text-gsblanco focus:outline-none focus:border-gsmenta transition-all">
                        <option value="games">Games</option>
                        <option value="users">Users</option>
                    </select>

                    <i class="pi pi-chevron-down absolute right-3 top-3 text-xs text-gsgris pointer-events-none"></i>

                </div>

                <!-- SEARCH INPUT -->
                <div class="relative flex-1 group">

                    <input v-model="searchQuery" type="text" :placeholder="searchType === 'games'
                        ? 'Search games...'
                        : 'Search users...'"
                        class="w-full bg-[#161a21] border border-white/8 rounded-2xl py-2.5 pl-11 pr-14 text-sm text-gsblanco placeholder-gsgris/60 focus:outline-none focus:border-gsmenta focus:ring-2 focus:ring-gsmenta/20 transition-all"
                        @keyup.enter="handleSearch" />

                    <!-- SEARCH ICON -->
                    <svg xmlns="http://www.w3.org/2000/svg"
                        class="h-4 w-4 absolute left-4 top-[13px] text-gsgris group-focus-within:text-gsmenta transition-colors"
                        fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                            d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
                    </svg>

                    <!-- FILTER BUTTON -->
                    <button v-if="searchType === 'games'" @click="showFilters = true"
                        class="absolute right-4 top-[10px] text-gsgris hover:text-gsmenta transition-colors">
                        <i class="pi pi-sliders-h text-sm"></i>
                    </button>

                </div>

            </div> 

            <!-- BROWSE -->
            <router-link to="/games"
                class="text-sm font-semibold uppercase tracking-[0.15em] hover:text-gsmenta transition-colors">
                Browse Games
            </router-link>

            <!-- DIVIDER -->
            <div class="h-7 w-px bg-white/10"></div>

            <!-- AUTH -->
            <template v-if="auth.isLogged">

                <router-link to="/profile" class="text-sm font-medium hover:text-gsmenta transition-colors">
                    Profile
                </router-link>

                <button @click="handleLogout"
                    class="text-sm font-medium text-gsgris hover:text-red-400 transition-colors">
                    Logout
                </button>

            </template>

            <template v-else>

                <router-link to="/login"
                    class="bg-gsmenta hover:bg-gsbosque text-gsoscuro px-5 py-2.5 rounded-full font-bold transition-all duration-300 hover:scale-105 active:scale-95 shadow-lg shadow-gsmenta/10">
                    Login
                </router-link>

            </template>

        </div>
    </nav>

    <!-- FILTER MODAL -->
    <div v-if="showFilters"
        class="fixed inset-0 bg-black/70 backdrop-blur-sm flex items-center justify-center z-50 px-4">

        <div class="relative w-full max-w-xl bg-gsoscuro border border-white/10 rounded-3xl overflow-hidden shadow-2xl">

            <!-- TOP BAR -->
            <div class="absolute top-0 left-0 w-full h-1 bg-linear-to-r from-gsmenta via-gsblanco/70 to-gsbosque"></div>

            <div class="p-7">
                <!-- HEADER -->
                <div class="flex items-center justify-between mb-8">
                    <div>
                        <h2 class="text-xl font-bold text-gsblanco">
                            Search Filters
                        </h2>
                        <p class="text-sm text-gsgris mt-1">
                            Refine your game search
                        </p>
                    </div>

                    <button @click="showFilters = false"
                        class="w-9 h-9 rounded-full bg-white/5 hover:bg-white/10 transition-all flex items-center justify-center text-gsgris hover:text-gsblanco">
                        ✕
                    </button>
                </div>

                <!-- FIELDS -->
                <div class="space-y-5">

                    <div>
                        <label class="block text-sm text-gsgris mb-2">
                            Developer
                        </label>
                        <input v-model="filters.developer" type="text" placeholder="Nintendo..."
                            class="w-full bg-[#161a21] border border-white/8 rounded-2xl px-4 py-3 text-sm text-gsblanco placeholder-gsgris/50 focus:outline-none focus:border-gsmenta transition-all" />
                    </div>

                    <div>
                        <label class="block text-sm text-gsgris mb-2">
                            Publisher
                        </label>
                        <input v-model="filters.publisher" type="text" placeholder="Sony..."
                            class="w-full bg-[#161a21] border border-white/8 rounded-2xl px-4 py-3 text-sm text-gsblanco placeholder-gsgris/50 focus:outline-none focus:border-gsmenta transition-all" />
                    </div>

                    <div>
                        <label class="block text-sm text-gsgris mb-2">
                            Genre
                        </label>
                        <input v-model="genreInput" type="text" placeholder="Press enter..." @keyup.enter="addGenre"
                            class="w-full bg-[#161a21] border border-white/8 rounded-2xl px-4 py-3 text-sm text-gsblanco placeholder-gsgris/50 focus:outline-none focus:border-gsmenta transition-all" />
                    </div>
                    <div class="flex flex-wrap gap-2 mt-3">

                        <div v-for="genre in filters.genres" :key="genre"
                            class="px-3 py-1 rounded-full bg-gsmenta/20 border border-gsmenta/30 text-xs text-gsmenta flex items-center gap-2">
                            {{ genre }}

                            <button @click="removeGenre(genre)">
                                ✕
                            </button>
                        </div>

                    </div>

                    <div>
                        <label class="block text-sm text-gsgris mb-2">
                            Release Year
                        </label>

                        <input v-model="filters.year" type="number" placeholder="2025"
                            class="w-full bg-[#161a21] border border-white/8 rounded-2xl px-4 py-3 text-sm text-gsblanco placeholder-gsgris/50 focus:outline-none focus:border-gsmenta transition-all" />
                    </div>

                    <div>
                        <label class="block text-sm text-gsgris mb-2">
                            Region
                        </label>

                        <input v-model="filters.region" type="text" placeholder="EU..."
                            class="w-full bg-[#161a21] border border-white/8 rounded-2xl px-4 py-3 text-sm text-gsblanco placeholder-gsgris/50 focus:outline-none focus:border-gsmenta transition-all" />
                    </div>

                    <div>
                        <label class="block text-sm text-gsgris mb-2">
                            Region
                        </label>

                        <input v-model="filters.region" type="text" placeholder="EU..."
                            class="w-full bg-[#161a21] border border-white/8 rounded-2xl px-4 py-3 text-sm text-gsblanco placeholder-gsgris/50 focus:outline-none focus:border-gsmenta transition-all" />
                    </div>
                </div>

                <!-- ACTIONS -->
                <div class="flex justify-end gap-3 mt-8">

                    <button @click="resetFilters"
                        class="px-5 py-2.5 rounded-full border border-white/10 text-gsgris hover:bg-white/5 transition-all">
                        Reset
                    </button>

                    <button @click="applyFilters"
                        class="bg-gsmenta hover:bg-gsbosque text-gsoscuro px-6 py-2.5 rounded-full font-bold transition-all shadow-lg shadow-gsmenta/10">
                        Apply Filters
                    </button>

                </div>

            </div>

        </div>

    </div>
</template>
<script setup lang="ts">
import { ref } from 'vue'
import { useAuthStore } from '@/stores/authStore'
import router from '@/router'
import axios from 'axios'

const auth = useAuthStore()

const searchQuery = ref('')

const searchType = ref<'games' | 'users'>('games')

const showFilters = ref(false)
const genreInput = ref('')

const filters = ref({
    developer: '',
    publisher: '',
    genres: [] as string[],
    year: '',
    region: '',
    mature_content: false
})



function addGenre() {

    const value = genreInput.value.trim()

    if (!value) return

    if (!filters.value.genres.includes(value)) {
        filters.value.genres.push(value)
    }

    genreInput.value = ''
}

function removeGenre(genre: string) {

    filters.value.genres =
        filters.value.genres.filter(
            g => g !== genre
        )
}

function handleSearch() {

    // USERS
    if (searchType.value === 'users') {

        router.push({
            path: '/users',
            query: {
                q: searchQuery.value
            }
        })

        return
    }

    // GAMES
    router.push({
        path: '/games',
        query: {
            ...(searchQuery.value && { q: searchQuery.value }),
            ...(filters.value.developer && { developer: filters.value.developer }),
            ...(filters.value.publisher && { publisher: filters.value.publisher }),
            ...(filters.value.genres.length > 0 && { genres: filters.value.genres }),
            ...(filters.value.year && { year: filters.value.year })
        }
    })
}
function applyFilters() {
    showFilters.value = false
    handleSearch()
}

function resetFilters() {

    filters.value = {
    developer: '',
        publisher: '',
        genres: [] as string[],
        year: '',
        region: '',
        mature_content: false
    }
}

function handleLogout() {
    auth.removeUserSesion()
    router.replace('/login')
}
</script>

<style scoped></style>