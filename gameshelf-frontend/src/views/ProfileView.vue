<template>
    <Navbar />
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
                        <h1 class="text-3xl md:text-4xl font-bold">{{ fullName }}</h1>
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
                        Editar Perfil
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
                <router-link :to="`/library/${profile.user.id}`" class="text-center">
                    <span class="block text-2xl md:text-3xl font-bold text-gsmenta">{{
                        profile.user.library.items?.length ?? 0 }}</span>
                    <span class="text-gsgris text-xs uppercase tracking-wider font-semibold">Library</span>
                </router-link>
                <router-link :to="`/favorites/${profile.user.id}`" class="text-center">
                    <span class="block text-2xl md:text-3xl font-bold text-gsmenta">{{ profile.user.favorites?.length ??
                        0 }}</span>
                    <span class="text-gsgris text-xs uppercase tracking-wider font-semibold">Favorites</span>
                </router-link>
                <router-link :to="`/wishlist/${profile.user.wishlist.id}`" class="text-center">
                    <span class="block text-2xl md:text-3xl font-bold text-gsmenta">{{
                        profile.user.wishlist.items?.length ?? 0 }}</span>
                    <span class="text-gsgris text-xs uppercase tracking-wider font-semibold">Wishlist</span>
                </router-link>
                <router-link :to="`/completed/${profile.user.wishlist.id}`" class="text-center">
                    <span class="block text-2xl md:text-3xl font-bold text-gsmenta">{{ completed }}</span>
                    <span class="text-gsgris text-xs uppercase tracking-wider font-semibold">Completed</span>
                </router-link>
            </div>
        </section>

        <!-- Main Content -->
        <main class="max-w-5xl mx-auto px-6 mt-12">
            <!-- Biografía -->
            <section class="mb-12">
                <h3 class="text-xs uppercase tracking-[0.2em] text-gsmenta font-bold mb-3">Biografía</h3>
                <div class="bg-[#1a1e26] border border-gsgris/10 p-5 rounded-2xl relative overflow-hidden group">
                    <div
                        class="absolute top-0 right-0 w-16 h-16 bg-gsmenta/5 rounded-bl-full transition-all group-hover:bg-gsmenta/10">
                    </div>
                    <p class="text-gsblanco/80 leading-relaxed text-sm md:text-base">
                        {{ profile?.bio || 'Este coleccionista aún no ha escrito su historia... ¡Pero su estantería habla por sí sola!' }}
                    </p>
                </div>
            </section>

            <div class="flex justify-between items-center mb-8">
                <h2 class="text-2xl font-bold border-l-4 border-gsmenta pl-4">Favoritos</h2>
                <a href="#" class="text-gsmenta hover:text-gsbosque text-sm font-medium transition-colors">Ver todos los
                    favoritos →</a>
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
import axios from 'axios';

import type { Profile } from '@/types/profileTypes';
import { useAuthStore } from '@/stores/authStore';
import Navbar from '@/components/Navbar.vue';
import Badge from '@/components/Badge.vue';
import GameCard from '@/components/GameCard.vue';

const authStore = useAuthStore()
const profile = ref<Profile | null>(null);
const loading = ref(true)

const route = useRoute()

const isOwnProfile = computed(() => {

    if (!route.params.id) return true

    return authStore.isOwnProfile(
        Number(route.params.id)
    )
})

watch(
    () => route.params.id,
    fetchProfile,
    { immediate: true } // Hace inecesario un onMounted
)


// onMounted(async () => {
//     try {
//         const data = await apiProfileMe()
//         profile.value = data
//    } catch (error: any) {
//         console.error('Error cargando el perfil:', error)
//     } finally {
//         loading.value = false
//     }
// });

async function fetchProfile() {

    loading.value = true

    try {

        // MI PERFIL
        if (!route.params.id) {

            const data = await apiProfileMe()
            profile.value = data

            return
        }

        // PERFIL PUBLICO
        const data = await apiProfileById(route.params.id as string)
        profile.value = data

    } catch (error: any) {

        console.error(error)

    } finally {

        loading.value = false
    }
}

async function apiProfileById(id: string) {

    const response = await axios.get(
        `http://127.0.0.1:8000/api/users/${id}/`
    )

    return response.data
}

const fullName = computed(() => {
    const first = profile.value?.user.first_name?.trim()
    const last = profile.value?.user.last_name?.trim()

    if (!first && !last) return 'noname'
    return `${first || ''} ${last || ''}`.trim()
})

const completed = computed(() => {
    if (!profile.value?.user.library.items) return 0

    // Devuelve la longitud de un array creado a partir de los items completed
    return profile.value.user.library.items.filter(item => item.status === "Completed").length
})

const limitedFavorites = computed(() => {
    return profile.value?.user.favorites?.slice(0, 4) || []
})

async function apiProfileMe() {
    const webhookUrl = `http://127.0.0.1:8000/api/users/me/`
    const headers = {
        'Authorization': `Bearer ${authStore.token}`,
        'Content-Type': 'application/json'
    }

    const response = await axios.get(webhookUrl, { headers })
    return response.data
}
</script>
