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
                        Favorites
                    </h2>
                    <span class="text-gsgris text-sm">Fav Games: {{ favorites?.length }}</span>
                </div>

                <main class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-5 gap-y-10 gap-x-6">
                    <div v-for="item in favorites" :key="item.id"
                        class="group flex flex-col bg-[#161a21] rounded-xl border border-gsgris/20 hover:border-gsmenta/50 transition-all duration-300 shadow-lg"
                    >
                        <GameCard :game="item.game" :platform="item.platform"/>
                    </div>
                </main>
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
</template>

<script setup lang="ts">
import { computed, onMounted, ref } from 'vue';
import { useRoute } from 'vue-router'
import type { FavoriteItem } from '@/types/profileTypes';
import GameCard from '@/components/GameCard.vue';
import Navbar from '@/components/Navbar.vue';
import api from "@/api/client";

const favorites = ref<Array<FavoriteItem>>([]);
const route = useRoute()
const userId = route.params.user_id;

onMounted(async () => {
    try {
        const data = await getFavorites()
        favorites.value = data
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