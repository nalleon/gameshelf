<template>
    <nav
        class="bg-gsoscuro text-gsblanco px-4 sm:px-6 py-4 flex items-center justify-between shadow-lg sticky top-0 z-50 border-b border-white/5">

        <router-link :to="auth.isLogged ? '/games' : '/'"
            class="flex items-center hover:opacity-90 transition-all duration-300 z-50">
            <img src="../assets/logo-navbar.png" alt="" class="h-9 sm:h-10 w-auto object-contain" />

            <span class="ml-3 font-bold text-xl tracking-tight hidden sm:block">
                Game<span class="text-gsmenta">Shelf</span>
            </span>
        </router-link>

        <div class="hidden lg:flex items-center w-full max-w-xl xl:max-w-2xl mx-8 bg-[#161a21] border border-white/8 rounded-full focus-within:border-gsmenta focus-within:ring-2 focus-within:ring-gsmenta/20 transition-all duration-300 group pl-4 pr-2 py-1.5">
            
            <div class="relative flex items-center shrink-0">
                <select v-model="searchType"
                    class="appearance-none bg-transparent pr-8 w-25 text-xs uppercase tracking-wider font-bold text-gsgris hover:text-gsblanco focus:outline-none transition-colors cursor-pointer z-10 py-2">
                    <option value="games" class="bg-gsoscuro text-gsblanco normal-case tracking-normal">Games</option>
                    <option value="users" class="bg-gsoscuro text-gsblanco normal-case tracking-normal">Users</option>
                </select>
                <i class="pi pi-chevron-down absolute right-3 text-[10px] text-gsgris pointer-events-none"></i>
            </div>

            <div class="h-4 w-px bg-white/10 mx-2"></div>

            <div class="relative flex-1 flex items-center">
                <svg xmlns="http://www.w3.org/2000/svg"
                    class="h-4 w-4 absolute left-0 text-gsgris group-focus-within:text-gsmenta transition-colors"
                    fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                        d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
                </svg>

                <input v-model="searchQuery" type="text" :placeholder="searchType === 'games'
                    ? 'Search games...'
                    : 'Search users...'"
                    class="w-full bg-transparent pl-6 pr-10 text-sm text-gsblanco placeholder-gsgris/50 focus:outline-none"
                    @keyup.enter="handleSearch" />

                <button v-if="searchType === 'games'" @click="showFilters = true"
                    class="absolute right-2 text-gsgris hover:text-gsmenta transition-colors p-1 rounded-full hover:bg-white/5">
                    <i class="pi pi-sliders-h text-sm"></i>
                </button>
            </div>

        </div> 

        <div class="flex items-center gap-2 sm:gap-4 flex-1 lg:flex-none justify-end z-50">

            <button @click="showMobileSearch = !showMobileSearch" 
                class="lg:hidden p-2 text-gsgris hover:text-gsmenta transition-colors rounded-full hover:bg-white/5">
                <i class="pi text-lg" :class="showMobileSearch ? 'pi-times' : 'pi-search'"></i>
            </button>

            <div class="hidden lg:flex items-center gap-4 md:gap-7">
                <router-link to="/games"
                    class="text-sm font-semibold uppercase tracking-[0.15em] hover:text-gsmenta transition-colors">
                    Browse Games
                </router-link>

                <div class="h-7 w-px bg-white/10"></div>

                <template v-if="auth.isLogged">
                    <router-link to="/profile" class="text-sm font-medium hover:text-gsmenta transition-colors">
                        Profile
                    </router-link>

                    <button @click="handleLogout"
                        class="text-sm font-medium text-gsgris hover:text-red-400 transition-colors cursor-pointer">
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

            <button @click="showMobileMenu = !showMobileMenu" 
                class="lg:hidden p-2 text-gsgris hover:text-gsmenta transition-colors focus:outline-none rounded-full hover:bg-white/5">
                <i class="pi text-xl" :class="showMobileMenu ? 'pi-times' : 'pi-bars'"></i>
            </button>

        </div>

        <div v-if="showMobileSearch" 
            class="absolute top-full left-0 w-full bg-[#0e121a]/95 backdrop-blur-md p-4 border-b border-white/10 flex flex-col gap-3 lg:hidden shadow-xl animate-fade-in">
            <div class="flex items-center bg-[#161a21] border border-white/8 rounded-full px-4 py-2 w-full focus-within:border-gsmenta transition-all">
                
                <div class="relative flex items-center shrink-0">
                    <select v-model="searchType"
                        class="appearance-none bg-transparent pr-6 w-25 text-xs uppercase tracking-wider font-bold text-gsgris focus:outline-none">
                        <option value="games" class="bg-gsoscuro text-gsblanco normal-case tracking-normal">Games</option>
                        <option value="users" class="bg-gsoscuro text-gsblanco normal-case tracking-normal">Users</option>
                    </select>
                    <i class="pi pi-chevron-down absolute right-0 text-[9px] text-gsgris pointer-events-none"></i>
                </div>

                <div class="h-4 w-px bg-white/10 mx-3"></div>

                <div class="relative flex-1 flex items-center">
                    <input v-model="searchQuery" type="text" :placeholder="searchType === 'games' ? 'Search games...' : 'Search users...'"
                        class="w-full bg-transparent pr-8 text-sm text-gsblanco placeholder-gsgris/50 focus:outline-none"
                        @keyup.enter="handleSearch(); showMobileSearch = false;" />
                    
                    <button v-if="searchType === 'games'" @click="showFilters = true"
                        class="absolute right-0 text-gsgris hover:text-gsmenta p-1">
                        <i class="pi pi-sliders-h text-sm"></i>
                    </button>
                </div>

            </div>
        </div>

        <Transition name="slide">
            <div v-if="showMobileMenu" class="fixed inset-y-0 right-0 w-64 bg-[#121620] border-l border-white/10 z-40 pt-20 px-6 flex flex-col gap-5 lg:hidden shadow-2xl">
                <router-link to="/games" @click="showMobileMenu = false" 
                    class="text-md font-semibold uppercase tracking-wider hover:text-gsmenta transition-colors py-2 border-b border-white/5">
                    Browse Games
                </router-link>

                <template v-if="auth.isLogged">
                    <router-link to="/profile" @click="showMobileMenu = false" 
                        class="text-md font-medium hover:text-gsmenta transition-colors py-2 border-b border-white/5">
                        Profile
                    </router-link>
                    <button @click="handleLogout(); showMobileMenu = false;" 
                        class="text-left text-md font-medium text-gsgris hover:text-red-400 transition-colors py-2">
                        Logout
                    </button>
                </template>
                
                <template v-else>
                    <router-link to="/login" @click="showMobileMenu = false" 
                        class="text-center bg-gsmenta text-gsoscuro py-3 rounded-full font-bold transition-all mt-4">
                        Login
                    </router-link>
                </template>
            </div>
        </Transition>

        <div v-if="showMobileMenu" @click="showMobileMenu = false" class="fixed inset-0 bg-black/40 backdrop-blur-xs z-35 lg:hidden"></div>

    </nav>

    <div v-if="showFilters"
        class="fixed inset-0 bg-black/70 backdrop-blur-sm flex items-center justify-center z-50 px-4">

        <div class="relative w-full max-w-xl bg-gsoscuro border border-white/10 rounded-3xl overflow-hidden shadow-2xl">

            <div class="absolute top-0 left-0 w-full h-1 bg-linear-to-r from-gsmenta via-gsblanco/70 to-gsbosque"></div>

            <div class="p-5 sm:p-7">
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

                <div class="space-y-4 max-h-[60vh] overflow-y-auto pr-1">

                    <div>
                        <label class="block text-sm text-gsgris mb-2">
                            Developer
                        </label>
                        <input v-model="filters.developer" type="text" placeholder="Nintendo..."
                            class="w-full bg-[#161a21] border border-white/8 rounded-full px-5 py-3 text-sm text-gsblanco placeholder-gsgris/50 focus:outline-none focus:border-gsmenta transition-all" />
                    </div>

                    <div>
                        <label class="block text-sm text-gsgris mb-2">
                            Publisher
                        </label>
                        <input v-model="filters.publisher" type="text" placeholder="Sony..."
                            class="w-full bg-[#161a21] border border-white/8 rounded-full px-5 py-3 text-sm text-gsblanco placeholder-gsgris/50 focus:outline-none focus:border-gsmenta transition-all" />
                    </div>

                    <div>
                        <label class="block text-sm text-gsgris mb-2">
                            Genre
                        </label>
                        <input v-model="genreInput" type="text" placeholder="Press enter..." @keyup.enter="addGenre"
                            class="w-full bg-[#161a21] border border-white/8 rounded-full px-5 py-3 text-sm text-gsblanco placeholder-gsgris/50 focus:outline-none focus:border-gsmenta transition-all" />
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
                            class="w-full bg-[#161a21] border border-white/8 rounded-full px-5 py-3 text-sm text-gsblanco placeholder-gsgris/50 focus:outline-none focus:border-gsmenta transition-all" />
                    </div>

                    <div>
                        <label class="block text-sm text-gsgris mb-2">
                            Region
                        </label>

                        <input v-model="filters.region" type="text" placeholder="EU..."
                            class="w-full bg-[#161a21] border border-white/8 rounded-full px-5 py-3 text-sm text-gsblanco placeholder-gsgris/50 focus:outline-none focus:border-gsmenta transition-all" />
                    </div>
                </div>

                <div class="flex justify-end gap-3 mt-8 pt-4 border-t border-white/5">

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
const showMobileMenu = ref(false)   
const showMobileSearch = ref(false) 
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

<style scoped>
.slide-enter-active,
.slide-leave-active {
    transition: transform 0.3s ease;
}
.slide-enter-from,
.slide-leave-to {
    transform: translateX(100%);
}

@keyframes fadeIn {
    from { opacity: 0; transform: translateY(-10px); }
    to { opacity: 1; transform: translateY(0); }
}
.animate-fade-in {
    animation: fadeIn 0.2s ease-out forwards;
}
</style>