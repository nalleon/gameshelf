<template>
    <div class="h-screen flex flex-col bg-[#0b0e14]">
        <div class="flex-shrink-0 sticky top-0 z-50">
            <Navbar />
        </div>

        <section ref="scrollContainer" class="flex-1 overflow-y-auto p-4 sm:p-6 md:p-8 text-gsblanco relative">
            <div class="max-w-400 mx-auto">

                <div
                    class="mb-6 md:mb-8 flex flex-col sm:flex-row sm:items-center justify-between border-b border-gsgris/10 pb-4 md:pb-6 text-gsmenta gap-4">
                    <div class="flex items-center gap-3">
                        <i class="pi pi-heart-fill text-xl md:text-2xl animate-pulse text-gsmenta"></i>
                        <h2 class="text-xl md:text-2xl font-semibold border-l-4 border-gsmenta/50 pl-3 md:pl-4">
                            Favorites
                        </h2>
                    </div>
                    <span
                        class="self-start sm:self-auto text-gsgris text-xs md:text-sm bg-[#161a21] px-3 py-1.5 rounded-xl border border-gsgris/10 flex items-center gap-2">
                        <i class="pi pi-bookmark text-[11px] md:text-xs"></i>
                        Fav Games: <span class="text-gsblanco font-semibold">{{ favorites?.length || 0 }}</span>
                    </span>
                </div>

                <main v-if="favorites.length > 0"
                    class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-5 gap-y-10 gap-x-6">
                    <div v-for="item in favorites" :key="item.id"
                        class="group flex flex-col bg-[#161a21] rounded-xl border border-gsgris/20 hover:border-gsmenta/50 transition-all duration-300 shadow-lg">
                        <GameCard :game="item.game" :platform="item.platform" />
                    </div>
                </main>

                <div v-else
                    class="flex flex-col items-center justify-center py-20 md:py-28 text-gsgris border border-dashed border-gsgris/10 rounded-2xl bg-[#161a21]/30 backdrop-blur-sm">
                    <i class="pi pi-heart text-4xl md:text-5xl mb-3 md:mb-4 text-gsmenta/30"></i>
                    <p class="text-sm md:text-base font-semibold text-gsblanco mb-1">No favorites yet</p>
                    <p class="text-xs md:text-sm text-gsgris text-center max-w-xs px-4">There are no games added to
                        favorites yet.</p>
                </div>
            </div>

            <ScrollTopButton :target="scrollContainer" :threshold="300" />
        </section>
    </div>
</template>

<script setup lang="ts">
import { onMounted, ref } from 'vue';
import { useRoute } from 'vue-router'
import type { FavoriteItem } from '@/types/profileTypes';
import GameCard from '@/components/GameCard.vue';
import Navbar from '@/components/Navbar.vue';
import ScrollTopButton from '@/components/ScrollTopButton.vue';
import api from "@/api/client";

const favorites = ref<Array<FavoriteItem>>([]);
const route = useRoute()
const userId = route.params.user_id;

onMounted(async () => {
    try {
        const data = await getFavorites()
        favorites.value = data || [];
        console.log(data)
    } catch (error: any) {
        console.error('Error cargando los favoritos:', error)
    }
});

async function getFavorites() {
    const response = await api.get(`/api/favorites/user/${userId}/`);
    return response.data;
}

const scrollContainer = ref<HTMLElement | null>(null);
</script>