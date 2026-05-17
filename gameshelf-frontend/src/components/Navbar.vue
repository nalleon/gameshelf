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

        <div
            class="hidden lg:flex items-center w-full max-w-xl xl:max-w-2xl mx-8 bg-[#161a21] border border-white/8 rounded-full focus-within:border-gsmenta focus-within:ring-2 focus-within:ring-gsmenta/20 transition-all duration-300 group pl-4 pr-2 py-1.5">

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

            <div class="hidden lg:flex items-center gap-4 md:gap-6">
                <router-link to="/games"
                    class="relative text-xs font-bold uppercase tracking-[0.2em] text-gsgris hover:text-gsblanco py-2 transition-colors duration-300 group mr-2">
                    Browse Games
                    <span
                        class="absolute bottom-0 left-0 w-0 h-[2px] bg-gsmenta transition-all duration-300 group-hover:w-full"></span>
                </router-link>

                <div class="h-7 w-px bg-white/10"></div>

                <template v-if="auth.isLogged">
                    <router-link to="/profile"
                        class="relative text-xs font-bold uppercase tracking-[0.2em] text-gsgris hover:text-gsblanco py-2 transition-colors duration-300 group flex items-center gap-2"
                        title="View Profile">
                        <i class="pi pi-user text-xs"></i>
                        <span>My Profile</span>
                        <span
                            class="absolute bottom-0 left-0 w-0 h-[2px] bg-gsmenta transition-all duration-300 group-hover:w-full"></span>
                    </router-link>

                    <button @click="handleLogout"
                        class="p-2 text-gsgris hover:text-red-400 transition-colors cursor-pointer rounded-full hover:bg-white/5 flex items-center justify-center"
                        title="Logout">
                        <i class="pi pi-power-off text-lg"></i>
                    </button>
                </template>

                <template v-else>
                    <router-link to="/login"
                        class="relative text-xs font-bold uppercase tracking-[0.2em] text-gsgris hover:text-gsblanco py-2 transition-colors duration-300 group flex items-center gap-2"
                        title="Login">
                        <i class="pi pi-sign-in text-xs"></i>
                        <span>Login</span>
                        <span
                            class="absolute bottom-0 left-0 w-0 h-[2px] bg-gsmenta transition-all duration-300 group-hover:w-full"></span>
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
            <div
                class="flex items-center bg-[#161a21] border border-white/8 rounded-full px-4 py-2 w-full focus-within:border-gsmenta transition-all">

                <div class="relative flex items-center shrink-0">
                    <select v-model="searchType"
                        class="appearance-none bg-transparent pr-6 w-25 text-xs uppercase tracking-wider font-bold text-gsgris focus:outline-none">
                        <option value="games" class="bg-gsoscuro text-gsblanco normal-case tracking-normal">Games
                        </option>
                        <option value="users" class="bg-gsoscuro text-gsblanco normal-case tracking-normal">Users
                        </option>
                    </select>
                    <i class="pi pi-chevron-down absolute right-0 text-[9px] text-gsgris pointer-events-none"></i>
                </div>

                <div class="h-4 w-px bg-white/10 mx-3"></div>

                <div class="relative flex-1 flex items-center">
                    <input v-model="searchQuery" type="text"
                        :placeholder="searchType === 'games' ? 'Search games...' : 'Search users...'"
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
            <div v-if="showMobileMenu"
                class="fixed inset-y-0 right-0 w-64 bg-[#121620] border-l border-white/10 z-40 pt-20 px-6 flex flex-col gap-5 lg:hidden shadow-2xl">
                <router-link to="/games" @click="showMobileMenu = false"
                    class="text-md font-semibold uppercase tracking-wider hover:text-gsmenta transition-colors py-2 border-b border-white/5 flex items-center justify-between group">
                    <span>Browse Games</span>
                    <i class="pi pi-chevron-right text-xs text-gsgris group-hover:text-gsmenta transition-colors"></i>
                </router-link>

                <template v-if="auth.isLogged">
                    <router-link to="/profile" @click="showMobileMenu = false"
                        class="text-md font-semibold uppercase tracking-wider hover:text-gsmenta transition-colors py-2 border-b border-white/5 flex items-center justify-between group">
                        <span class="flex items-center gap-3">
                            <i class="pi pi-user text-md"></i>
                            <span>My Profile</span>
                        </span>
                        <i
                            class="pi pi-chevron-right text-xs text-gsgris group-hover:text-gsmenta transition-colors"></i>
                    </router-link>

                    <button @click="handleLogout(); showMobileMenu = false;"
                        class="text-left text-md font-semibold uppercase tracking-wider text-gsgris hover:text-red-400 transition-colors py-2 flex items-center gap-3">
                        <i class="pi pi-power-off text-md"></i>
                        <span>Logout</span>
                    </button>
                </template>

                <template v-else>
                    <router-link to="/login" @click="showMobileMenu = false"
                        class="text-md font-semibold uppercase tracking-wider hover:text-gsmenta transition-colors py-2 border-b border-white/5 flex items-center justify-between group mt-2">
                        <span class="flex items-center gap-3">
                            <i class="pi pi-sign-in text-md"></i>
                            <span>Login</span>
                        </span>
                        <i
                            class="pi pi-chevron-right text-xs text-gsgris group-hover:text-gsmenta transition-colors"></i>
                    </router-link>
                </template>
            </div>
        </Transition>

        <div v-if="showMobileMenu" @click="showMobileMenu = false"
            class="fixed inset-0 bg-black/40 backdrop-blur-xs z-35 lg:hidden"></div>

    </nav>

    <div v-if="showFilters"
        class="fixed inset-0 bg-black/80 backdrop-blur-md flex items-center justify-center z-50 px-4 transition-all duration-300">
        <div
            class="relative w-full max-w-2xl bg-gsoscuro border border-white/10 rounded-2xl overflow-hidden shadow-2xl shadow-gsmenta/5">

            <div
                class="absolute top-0 left-0 w-full h-[3px] bg-gradient-to-r from-gsmenta via-gsmenta/50 to-transparent">
            </div>

            <div class="p-6 sm:p-8">
                <div class="flex items-center justify-between mb-6 border-b border-white/5 pb-4">
                    <div>
                        <h2 class="text-xs uppercase tracking-[0.25em] font-black text-gsmenta">Advanced Filters</h2>
                        <p class="text-xs text-gsgris mt-1">Refine your catalog exploration parameters</p>
                    </div>
                    <button @click="showFilters = false"
                        class="w-8 h-8 rounded-full bg-white/5 hover:bg-gsmenta/20 text-gsgris hover:text-gsmenta transition-all flex items-center justify-center border border-white/10 hover:border-gsmenta/30">
                        <i class="pi pi-times text-xs"></i>
                    </button>
                </div>

                <div class="space-y-5 max-h-[65vh] overflow-y-auto pr-1 custom-scrollbar">
                    <div class="grid grid-cols-1 sm:grid-cols-2 gap-5">
                        <div>
                            <label
                                class="block text-[11px] font-bold uppercase tracking-wider text-gsgris mb-2">Developer</label>
                            <input v-model="filters.developer" type="text" placeholder="e.g. Nintendo, FromSoftware"
                                class="w-full bg-[#141822] border border-white/10 rounded-xl px-4 py-3 text-sm text-gsblanco placeholder-gsgris/40 focus:outline-none focus:border-gsmenta focus:ring-4 focus:ring-gsmenta/10 transition-all duration-200" />
                        </div>
                        <div>
                            <label
                                class="block text-[11px] font-bold uppercase tracking-wider text-gsgris mb-2">Publisher</label>
                            <input v-model="filters.publisher" type="text" placeholder="e.g. Sony, Electronic Arts"
                                class="w-full bg-[#141822] border border-white/10 rounded-xl px-4 py-3 text-sm text-gsblanco placeholder-gsgris/40 focus:outline-none focus:border-gsmenta focus:ring-4 focus:ring-gsmenta/10 transition-all duration-200" />
                        </div>
                    </div>

                    <div class="border-t border-white/5 pt-4">
                        <label class="block text-[11px] font-bold uppercase tracking-wider text-gsgris mb-2">Target
                            Genres</label>
                        <div class="relative flex items-center">
                            <input v-model="genreInput" type="text" placeholder="Type a genre and press Enter..."
                                @keyup.enter="addGenre"
                                class="w-full bg-[#141822] border border-white/10 rounded-xl px-4 py-3 text-sm text-gsblanco placeholder-gsgris/40 focus:outline-none focus:border-gsmenta focus:ring-4 focus:ring-gsmenta/10 transition-all duration-200" />
                            <i class="pi pi-plus absolute right-4 text-xs text-gsgris/60 pointer-events-none"></i>
                        </div>

                        <div v-if="filters.genres.length > 0"
                            class="flex flex-wrap gap-2 mt-3 p-2 bg-[#141822]/50 border border-white/5 rounded-xl">
                            <div v-for="genre in filters.genres" :key="genre"
                                class="pl-3 pr-2 py-1.5 rounded-lg bg-gsmenta/10 border border-gsmenta/20 text-xs font-semibold text-gsmenta flex items-center gap-2 transition-all hover:bg-gsmenta/20">
                                <span>{{ genre }}</span>
                                <button @click="removeGenre(genre)"
                                    class="hover:text-white transition-colors p-0.5 rounded-sm">
                                    <i class="pi pi-times text-[9px]"></i>
                                </button>
                            </div>
                        </div>
                    </div>

                    <div class="grid grid-cols-1 sm:grid-cols-2 gap-5 border-t border-white/5 pt-4">
                        <div>
                            <label class="block text-[11px] font-bold uppercase tracking-wider text-gsgris mb-2">Release
                                Year</label>
                            <input v-model="filters.year" type="number" placeholder="e.g. 2026"
                                class="w-full bg-[#141822] border border-white/10 rounded-xl px-4 py-3 text-sm text-gsblanco placeholder-gsgris/40 focus:outline-none focus:border-gsmenta focus:ring-4 focus:ring-gsmenta/10 transition-all duration-200" />
                        </div>
                        <div>
                            <label
                                class="block text-[11px] font-bold uppercase tracking-wider text-gsgris mb-2">Region</label>
                            <input v-model="filters.region" type="text" placeholder="e.g. EU, US, JP"
                                class="w-full bg-[#141822] border border-white/10 rounded-xl px-4 py-3 text-sm text-gsblanco placeholder-gsgris/40 focus:outline-none focus:border-gsmenta focus:ring-4 focus:ring-gsmenta/10 transition-all duration-200" />
                        </div>
                    </div>
                </div>

                <div class="flex items-center justify-end gap-3 mt-6 pt-4 border-t border-white/5">
                    <button @click="resetFilters"
                        class="border-2 border-white/10 hover:border-white/30 bg-white/5 hover:bg-white/10 text-gsgris hover:text-gsblanco px-5 py-2.5 rounded-full text-xs font-bold uppercase tracking-wider transition-all duration-300 hover:scale-105 active:scale-95">
                        Clear All
                    </button>
                    <button @click="applyFilters"
                        class="border-2 border-gsmenta/30 hover:border-gsmenta bg-gsmenta/5 hover:bg-gsmenta text-gsblanco hover:text-gsoscuro px-6 py-2.5 rounded-full text-xs font-bold uppercase tracking-wider transition-all duration-300 hover:scale-105 active:scale-95 shadow-md shadow-gsmenta/5 hover:shadow-lg hover:shadow-gsmenta/20">
                        Apply Config
                    </button>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useAuthStore } from '@/stores/authStore'
import { useSearchStore } from '@/stores/searchStore'
import { storeToRefs } from 'pinia'
import router from '@/router'

const auth = useAuthStore()
const searchQuery = ref('')

const searchStore = useSearchStore()
const { searchType } = storeToRefs(searchStore)

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
    filters.value.genres = filters.value.genres.filter(g => g !== genre)
}

function handleSearch() {
    if (searchType.value === 'users') {
        router.push({
            path: '/users',
            query: { q: searchQuery.value }
        })
        return
    }

    router.push({
        path: '/games',
        query: {
            ...(searchQuery.value.trim() && { q: searchQuery.value.trim() }),
            ...(filters.value.developer.trim() && { developer: filters.value.developer.trim() }),
            ...(filters.value.publisher.trim() && { publisher: filters.value.publisher.trim() }),
            ...(filters.value.genres.length > 0 && { genres: filters.value.genres }),
            ...(filters.value.year && { year: filters.value.year }),
            ...(filters.value.region.trim() && { region: filters.value.region.trim() })
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
    from {
        opacity: 0;
        transform: translateY(-10px);
    }

    to {
        opacity: 1;
        transform: translateY(0);
    }
}

.animate-fade-in {
    animation: fadeIn 0.2s ease-out forwards;
}
</style>