<template>
    <div class="h-screen flex flex-col bg-[#0b0e14]"> 
        <div class="flex-shrink-0 sticky top-0 z-50">
            <Navbar/>
        </div>

        <section ref="scrollContainer" @scroll="handleScroll" class="flex-1 overflow-y-auto p-6 sm:p-8 text-gsblanco relative">            
            <div class="max-w-[1600px] mx-auto">
                <div class="mb-8 flex items-center justify-between text-gsmenta">
                    <h2 class="text-2xl font-semibold border-l-4 border-gsmenta/50 pl-4">
                        Collections
                    </h2>
                    <span class="text-gsgris text-sm">Total Collections: {{ visibleCollections.length }}</span>
                </div>

                <div class="space-y-6">
                    <details
                        v-for="collection in collections" 
                        :key="collection.id" 
                        class="group bg-[#161a21] rounded-xl border border-gsgris/20 overflow-hidden transition-all duration-300 open:border-gsmenta/30"
                        open
                    >
                        <summary
                            class="flex items-center justify-between p-5 cursor-pointer list-none hover:bg-[#1c222c] transition-colors">
                            <div class="flex items-center gap-4">
                                <span class="text-gsmenta transform group-open:rotate-90 transition-transform duration-200">▶</span>
                                <h3 class="text-xl font-bold">{{ collection.name }}</h3>
                                <span class="text-gsgris text-xs bg-gsoscuro px-2 py-1 rounded-full">
                                    {{ collection.items.length }} games
                                </span>
                            </div>
                            <button
                                v-if="authStore.isOwnProfile(userId)"
                                @click.stop="toggleCollectionPrivacy(collection)"
                                class="text-xs px-3 py-1 rounded-full border transition-all"
                                :class="collection.is_private
                                    ? 'border-red-500/40 text-red-400 hover:bg-red-500/10'
                                    : 'border-gsmenta/40 text-gsmenta hover:bg-gsmenta/10'"
                            >
                                {{ collection.is_private ? 'Private' : 'Public' }}
                            </button>
                            <router-link 
                                :to="`/collections/${userId}/${collection.id}/`" 
                                class="text-sm text-gsmenta hover:underline flex items-center gap-1"
                            >
                                View full collection 
                                <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 7l5 5m0 0l-5 5m5-5H6" />
                                </svg>
                            </router-link>
                        </summary>

                        <div 
                            class="p-5 border-t border-gsgris/10">
                            <div class="flex gap-6 overflow-x-auto pb-4 scrollbar-hide snap-x">
                                <div 
                                    v-for="item in collection.items.slice(0, 10)" 
                                    :key="item.id"
                                    class="min-w-[200px] max-w-[200px] snap-start"
                                >
                                    <GameCard 
                                        v-if="!item.is_private || authStore.isOwnProfile(userId)" 
                                        :game="item.game" :platform="item.platform"
                                    />
                                </div>
                                
                                <div v-if="collection.items.length > 10" class="min-w-[150px] flex items-center justify-center">
                                    <router-link 
                                        :to="`/collections/${userId}/${collection.id}`"
                                        class="flex flex-col items-center gap-2 text-gsgris hover:text-gsmenta transition-colors"
                                    >
                                        <div class="w-12 h-12 rounded-full border-2 border-dashed border-gsgris/40 flex items-center justify-center">
                                            <span>+{{ collection.items.length - 10 }}</span>
                                        </div>
                                        <span class="text-sm font-medium">See all</span>
                                    </router-link>
                                </div>
                            </div>
                        </div>
                    </details>
                </div>
            </div>

            <Transition name="fade">
                <button v-show="showButton" @click="scrollTop" class="fixed bottom-8 right-8 z-50 p-3 rounded-md bg-gsmenta text-gsoscuro shadow-xl hover:bg-gsbosque hover:scale-110 transition-all">
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 15l7-7 7 7" />
                    </svg>
                </button>
            </Transition>
        </section>
    </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue';
import { useRoute } from 'vue-router';

import { useAuthStore } from '@/stores/authStore';
import GameCard from '@/components/GameCard.vue';
import Navbar from '@/components/Navbar.vue';
import type { Collection, Profile } from '@/types/profileTypes';
import api from "@/api/client";

// const profile = ref<Profile>();
const collections = ref<Collection[]>([]);
const authStore = useAuthStore();
const route = useRoute();
const userId = Number(route.params.user_id);

const scrollContainer = ref<HTMLElement | null>(null);
const showButton = ref(false);

onMounted(async () => {
    await loadCollections();
});

async function loadCollections() {
    try {
        const response = await api.get(`/api/users/${userId}/`);
        console.log(response.data)
        collections.value = response.data.user.collections;
    } catch (error: any) {
        console.error('Error loading collections:', error);
    }
}

const visibleCollections = computed(() => {
    // Si es mi propio perfil, las veo todas (públicas y privadas)
    if (authStore.isOwnProfile(userId)) {
        return collections.value;
    }
    // Si no es mi perfil, solo veo las que NO son privadas
    return collections.value.filter(c => !c.is_private);
});

async function toggleCollectionPrivacy(collection: Collection) {

    const previousValue = collection.is_private

    // Optimistic UI
    collection.is_private = !collection.is_private

    try {

        await api.patch(
            `/api/collections/${collection.id}/`,
            {
                name: collection.name,
                is_private: collection.is_private
            }
        )

    } catch (error) {

        // rollback
        collection.is_private = previousValue

        console.error('Error updating collection privacy', error)
    }
}

const handleScroll = () => {
    if (scrollContainer.value) showButton.value = scrollContainer.value.scrollTop > 300;
};

function scrollTop() {
    scrollContainer.value?.scrollTo({ top: 0, behavior: 'smooth' });
}
</script>

<style scoped>
/* Ocultar scrollbar para Chrome, Safari y Opera */
.scrollbar-hide::-webkit-scrollbar {
    display: none;
}
/* Ocultar scrollbar para IE, Edge y Firefox */
.scrollbar-hide {
    -ms-overflow-style: none;
    scrollbar-width: none;
}

summary::-webkit-details-marker {
    display: none;
}
</style>