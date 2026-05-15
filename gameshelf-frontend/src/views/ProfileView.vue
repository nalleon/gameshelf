<template>
    <Navbar />
    <transition name="toast-modern">
        <div
            v-if="showSuccessMessage"
            class="fixed top-6 right-6 z-50 flex items-center gap-4 p-4 rounded-2xl border border-gsmenta/30 bg-gsoscuro/80 backdrop-blur-md shadow-[0_20px_50px_rgba(0,0,0,0.5)] min-w-[320px] overflow-hidden"
        >
            <div class="flex-shrink-0 w-10 h-10 bg-gsmenta/20 rounded-xl flex items-center justify-center text-gsmenta shadow-[0_0_15px_rgba(104,211,145,0.2)]">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="3">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M5 13l4 4L19 7" />
                </svg>
            </div>

            <div class="flex-grow">
                <p class="text-gsblanco font-bold text-sm leading-tight">Success!</p>
                <p class="text-gsgris text-xs mt-0.5">Profile updated successfully</p>
            </div>

            <button @click="showSuccessMessage = false" class="text-gsgris hover:text-gsblanco transition-colors p-1">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
                </svg>
            </button>

            <div class="absolute bottom-0 left-0 h-[3px] bg-gsmenta shadow-[0_0_10px_#68d391] progress-bar"></div>
        </div>
    </transition>
    <div class="min-h-screen bg-gsoscuro text-gsblanco font-sans pb-20">
        <!-- Header / Banner -->
        <header class="relative bg-[#1a1e26]">
            <!-- Banner con degradado -->
            <div class="h-48 md:h-55" :style="{ backgroundColor: profile?.color_bg || '#79a998' }" />

            <div class="max-w-5xl mx-auto px-6">
                <div class="flex flex-col md:flex-row items-end -mt-12 md:-mt-10 gap-6 pb-6">
                    <!-- Avatar -->
                    <div class="w-32 h-32 md:w-40 md:h-40 rounded-full bg-gsoscuro border-4 overflow-hidden shadow-xl"
                        :style="{ border: `2px solid ${profile?.color_bg || '#79a998'}` }">
                        <img v-if="profile?.avatar" :src="profile.avatar" alt="User Avatar"
                            class="w-full h-full rounded-full object-cover" />
                    </div>

                    <!-- User Details -->
                    <div class="flex-1">
                        <h1 class="text-2xl sm:text-3xl font-bold">
                            {{ fullName }}
                        </h1>
                        <p class="text-gsmenta font-medium">@{{ profile?.user.username }}</p>

                        <div class="flex flex-wrap gap-2 mt-3" v-if="profile">
                            <Badge nombre="role" :role="profile.role ?? 'unknown'" />
                            <Badge nombre="completionist" :completedQuantity="completed" />
                            <Badge nombre="collectionist"
                                :collectionsQuantity="profile.user.collections?.length ?? 0" />
                            <Badge nombre="wisher" :wishlistQuantity="profile.user.wishlist.items?.length ?? 0" />
                            <Badge nombre="player" :libraryQuantity="profile.user.library.items?.length ?? 0" />
                        </div>
                    </div>

                    <router-link v-if="isOwnProfile" to="/profile/edit"
                        class="mb-2 px-6 py-2 border border-gsmenta text-gsmenta rounded-full hover:bg-gsmenta hover:text-gsoscuro transition-all duration-300 font-semibold">
                        Edit profile
                    </router-link>
                </div>
            </div>
        </header>

        <!-- Stats Bar -->
        <section class="bg-[#161a21] border-y border-gsgris/10 py-8" v-if="profile">
            <div class="max-w-5xl mx-auto px-6 flex justify-around md:justify-center md:gap-24">
                <router-link :to="`/collections/${profile.user.id}`" class="text-center">
                    <span class="block text-2xl md:text-3xl font-bold text-gsmenta">{{ profile.user.collections?.length
                        ?? 0 }}</span>
                    <span class="text-gsgris text-xs uppercase tracking-wider font-semibold">Collections</span>
                </router-link>
                <router-link
                    v-if="!profile.user.library.is_private || isOwnProfile"
                    :to="`/library/${profile.user.id}`" class="text-center">
                    <span class="block text-2xl md:text-3xl font-bold text-gsmenta">{{
                        profile.user.library.items?.length ?? 0 }}</span>
                    <span class="text-gsgris text-xs uppercase tracking-wider font-semibold">Library</span>
                </router-link>
                <router-link
                    :to="`/favorites/${profile.user.id}`" class="text-center">
                    <span class="block text-2xl md:text-3xl font-bold text-gsmenta">{{ profile.user.favorites?.length ??
                        0 }}</span>
                    <span class="text-gsgris text-xs uppercase tracking-wider font-semibold">Favorites</span>
                </router-link>
                <router-link 
                    v-if="!profile.user.wishlist.is_private || isOwnProfile"
                    :to="`/wishlist/${profile.user.id}/${profile.user.wishlist.id}`" class="text-center">
                    <span class="block text-2xl md:text-3xl font-bold text-gsmenta">{{
                        profile.user.wishlist.items?.length ?? 0 }}</span>
                    <span class="text-gsgris text-xs uppercase tracking-wider font-semibold">Wishlist</span>
                </router-link>
                <router-link
                    v-if="!profile.user.library.is_private || isOwnProfile"
                    :to="`/completed/${profile.user.wishlist.id}`" class="text-center">
                    <span class="block text-2xl md:text-3xl font-bold text-gsmenta">{{ completed }}</span>
                    <span class="text-gsgris text-xs uppercase tracking-wider font-semibold">Completed</span>
                </router-link>
            </div>
        </section>

        <!-- Main Content -->
        <main class="max-w-5xl mx-auto px-6 mt-12">
            <!-- Biografía -->
            <section class="mb-12">
                <h3 class="text-xs uppercase tracking-[0.2em] text-gsmenta font-bold mb-3">Biography</h3>
                <div class="bg-[#1a1e26] border border-gsgris/10 p-5 rounded-2xl relative overflow-hidden group">
                    <div
                        class="absolute top-0 right-0 w-16 h-16 bg-gsmenta/5 rounded-bl-full transition-all group-hover:bg-gsmenta/10">
                    </div>
                    <p class="text-gsblanco/80 leading-relaxed text-sm md:text-base">
                        {{ profile?.bio || defaultBio }}
                    </p>
                </div>
            </section>

            <div class="flex justify-between items-center mb-8">
                <h2 class="text-2xl font-bold border-l-4 border-gsmenta pl-4">Favorites</h2>
                <router-link
                    :to="`/favorites/${profile?.user.id}`" class="text-gsmenta hover:text-gsbosque text-sm font-medium transition-colors">
                    View all →
                </router-link>
            </div>

            <!-- Game Grid -->
            <div class="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-4 gap-6">
                <template v-if="profile && limitedFavorites.length > 0">
                    <div v-for="game in limitedFavorites" :key="game.id"
                        class="group cursor-pointer flex flex-col bg-[#161a21] rounded-xl border border-gsgris/20 hover:border-gsmenta/50 transition-all duration-300 shadow-lg">
                        <GameCard :game="game.game" />
                    </div>
                </template>
                <div v-else class="col-span-full flex justify-center items-center">
                    <img alt="no recent games" src="@/assets/Empty-cuate.svg" class="w-sm" />
                </div>
            </div>
        </main>
    </div>
</template>

<script setup lang="ts">
import { computed, onMounted, ref, watch } from 'vue';
import { useRoute } from 'vue-router'
import type { Profile } from '@/types/profileTypes';
import { useAuthStore } from '@/stores/authStore';
import Navbar from '@/components/Navbar.vue';
import Badge from '@/components/Badge.vue';
import GameCard from '@/components/GameCard.vue';
import api from "@/api/client";

const authStore = useAuthStore()
const profile = ref<Profile | null>(null);
const loading = ref(true)
const showSuccessMessage = ref(false)

const route = useRoute()
const defaultBio = 'This collector has not yet written their story... But their shelf speaks for itself!'

const isOwnProfile = computed(() => {

    if (!route.params.id){
        return true
    }

    return authStore.isOwnProfile(
        Number(route.params.id)
    )
})

watch(
    () => route.params.id,
    fetchProfile,
    { immediate: true } // Hace inecesario un onMounted
)

onMounted(() => {
    if (route.query.updated === 'true') {

        showSuccessMessage.value = true

        // Elimina el query param de la URL
        window.history.replaceState(
            {},
            '',
            route.path
        )

        setTimeout(() => {
            showSuccessMessage.value = false
        }, 3000)
    }
})

async function fetchProfile() {
    loading.value = true;

    try {
        profile.value = route.params.id
            ? (await api.get(`/api/users/${route.params.id}/`)).data
            : (await api.get('/api/users/me/')).data;

    } catch (error: unknown) {
        console.error(error);

    } finally {
        loading.value = false;
    }
}
const fullName = computed(() => {
    const first = profile.value?.user.first_name?.trim()
    const last = profile.value?.user.last_name?.trim()

    if (!first && !last) return 'noname'
    return `${first || ''} ${last || ''}`.trim()
})

const completed = computed(() => {
    if (!profile.value?.user.library.items) return 0
    return profile.value.user.library.items.filter(item => item.status === "Completed").length
})

const limitedFavorites = computed(() => {
    return profile.value?.user.favorites?.slice(0, 4) || []
})
</script>

<style scoped>
.toast-enter-active,
.toast-leave-active {
    transition: all 0.3s ease;
}

.toast-enter-from,
.toast-leave-to {
    opacity: 0;
    transform: translateY(-10px);
}
</style>
