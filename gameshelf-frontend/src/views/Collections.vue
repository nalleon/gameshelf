<template>
    <div class="h-screen flex flex-col bg-[#0b0e14]"> 
        <div class="flex-shrink-0 sticky top-0 z-50">
            <Navbar/>
        </div>

        <section ref="scrollContainer" class="flex-1 overflow-y-auto p-4 sm:p-6 md:p-8 text-gsblanco relative">            
            <div class="max-w-[1600px] mx-auto">
                
                <div class="mb-6 md:mb-8 flex flex-col sm:flex-row sm:items-center justify-between border-b border-gsgris/10 pb-4 md:pb-6 text-gsmenta gap-4">
                    <div class="flex items-center gap-3">
                        <i class="pi pi-tags text-xl md:text-2xl"></i>
                        <h2 class="text-xl md:text-2xl font-semibold border-l-4 border-gsmenta/50 pl-3 md:pl-4">
                            Collections
                        </h2>
                    </div>
                    <span class="self-start sm:self-auto text-gsgris text-xs md:text-sm bg-[#161a21] px-3 py-1.5 rounded-xl border border-gsgris/10">
                        Total Collections: <span class="text-gsblanco font-semibold">{{ visibleCollections.length }}</span>
                    </span>
                </div>

                <div v-if="visibleCollections.length > 0" class="space-y-4 md:space-y-6">
                    <details
                        v-for="collection in visibleCollections"
                        :key="collection.id" 
                        class="group bg-[#161a21] rounded-xl border border-gsgris/10 overflow-hidden transition-all duration-300 open:border-gsmenta/30 shadow-md"
                        open
                    >
                        <summary class="flex flex-col sm:flex-row sm:items-center justify-between p-4 md:p-5 cursor-pointer list-none hover:bg-[#1c222c] transition-colors gap-3 sm:gap-4 select-none">
                            <div class="flex items-center gap-2 sm:gap-4 w-full sm:w-auto">
                                <i class="pi pi-chevron-right text-[10px] sm:text-xs text-gsgris group-open:rotate-90 group-open:text-gsmenta transition-all duration-200 flex-shrink-0"></i>
                                <h3 class="text-lg md:text-xl font-bold tracking-tight text-gsblanco group-hover:text-gsmenta transition-colors truncate max-w-[180px] xs:max-w-xs sm:max-w-none">
                                    {{ collection.name }}
                                </h3>
                                <span class="text-gsgris text-[10px] sm:text-xs font-semibold bg-[#0b0e14] px-2 py-0.5 sm:py-1 rounded-full border border-gsgris/10 flex-shrink-0">
                                    {{ collection.items.length }} {{ collection.items.length === 1 ? 'game' : 'games' }}
                                </span>
                            </div>

                            <div class="flex items-center justify-between sm:justify-end gap-3 w-full sm:w-auto border-t border-gsgris/5 pt-2 sm:pt-0 sm:border-0" @click.stop>
                                <button
                                    v-if="authStore.isOwnProfile(userId)"
                                    @click="toggleCollectionPrivacy(collection)"
                                    class="text-[11px] sm:text-xs px-2.5 py-1 sm:py-1.5 rounded-xl border transition-all duration-300 flex items-center gap-1.5 font-medium"
                                    :class="collection.is_private
                                        ? 'border-red-500/30 text-red-400 bg-red-500/5 hover:bg-red-500/20'
                                        : 'border-gsmenta/30 text-gsmenta bg-gsmenta/5 hover:bg-gsmenta/20'"
                                >
                                    <i :class="collection.is_private ? 'pi pi-eye-slash' : 'pi pi-eye'" class="text-[9px] sm:text-[10px]"></i>
                                    {{ collection.is_private ? 'Private' : 'Public' }}
                                </button>

                                <router-link 
                                    :to="`/collections/${userId}/${collection.id}/`" 
                                    class="text-xs sm:text-sm text-gsgris hover:text-gsmenta font-medium flex items-center gap-1.5 group/link transition-colors ml-auto sm:ml-0"
                                >
                                    <span>View full</span>
                                    <i class="pi pi-arrow-right text-[10px] sm:text-xs group-hover/link:translate-x-1 transition-transform"></i>
                                </router-link>
                            </div>
                        </summary>

                        <div class="p-4 md:p-5 border-t border-gsgris/10 bg-[#0f1217]/50">
                            <div class="flex gap-4 md:gap-6 overflow-x-auto pb-3 md:pb-4 scrollbar-hide snap-x">
                                <div 
                                    v-for="item in collection.items.slice(0, 10)" 
                                    :key="item.id"
                                    class="min-w-[160px] max-w-[160px] sm:min-w-[200px] sm:max-w-[200px] snap-start transition-transform duration-300 hover:-translate-y-1"
                                >
                                    <GameCard 
                                        v-if="!item.is_private || authStore.isOwnProfile(userId)" 
                                        :game="item.game" :platform="item.platform"
                                    />
                                </div>
                                
                                <div v-if="collection.items.length > 10" class="min-w-[130px] sm:min-w-[160px] flex items-center justify-center snap-start pr-1">
                                    <router-link 
                                        :to="`/collections/${userId}/${collection.id}`"
                                        class="flex flex-col items-center gap-2 group/more text-gsgris hover:text-gsmenta transition-colors"
                                    >
                                        <div class="w-12 h-12 sm:w-14 sm:h-14 rounded-full border border-dashed border-gsgris/30 bg-[#161a21] flex items-center justify-center group-hover/more:border-gsmenta group-hover/more:bg-gsmenta/5 transition-all duration-300 shadow-inner">
                                            <span class="text-xs font-bold text-gsblanco group-hover/more:text-gsmenta transition-colors">
                                                +{{ collection.items.length - 10 }}
                                            </span>
                                        </div>
                                        <span class="text-[10px] sm:text-xs font-semibold tracking-wide uppercase">See all</span>
                                    </router-link>
                                </div>
                            </div>
                        </div>
                    </details>
                </div>

                <div v-else class="flex flex-col items-center justify-center py-20 md:py-28 text-gsgris border border-dashed border-gsgris/10 rounded-2xl bg-[#161a21]/30 backdrop-blur-sm">
                    <i class="pi pi-folder-open text-4xl md:text-5xl mb-3 md:mb-4 text-gsmenta/30 animate-pulse"></i>
                    <p class="text-sm md:text-base font-semibold text-gsblanco mb-1">No collections found</p>
                    <p class="text-xs md:text-sm text-gsgris text-center max-w-xs px-4">There are no custom collections created or visible for this profile yet.</p>
                </div>
            </div>

            <ScrollTopButton :target="scrollContainer" :threshold="300" />
        </section>
    </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue';
import { useRoute } from 'vue-router';

import { useAuthStore } from '@/stores/authStore';
import GameCard from '@/components/GameCard.vue';
import Navbar from '@/components/Navbar.vue';
import ScrollTopButton from '@/components/ScrollTopButton.vue'; 
import type { Collection } from '@/types/profileTypes';
import api from "@/api/client";

const collections = ref<Collection[]>([]);
const authStore = useAuthStore();
const route = useRoute();
const userId = Number(route.params.user_id);

const scrollContainer = ref<HTMLElement | null>(null);

onMounted(async () => {
    await loadCollections();
});

async function loadCollections() {
    try {
        const response = await api.get(`/api/users/${userId}/`);
        collections.value = response.data.user.collections || [];
    } catch (error: any) {
        console.error('Error loading collections:', error);
    }
}

const visibleCollections = computed(() => {
    if (!collections.value) return [];
    if (authStore.isOwnProfile(userId)) {
        return collections.value;
    }
    return collections.value.filter(c => !c.is_private);
});

async function toggleCollectionPrivacy(collection: Collection) {
    const previousValue = collection.is_private;
    collection.is_private = !collection.is_private;

    try {
        await api.patch(
            `/api/collections/${collection.id}/`,
            {
                name: collection.name,
                is_private: collection.is_private
            }
        );
    } catch (error) {
        collection.is_private = previousValue;
        console.error('Error updating collection privacy', error);
    }
}
</script>

<style scoped>
.scrollbar-hide::-webkit-scrollbar {
    display: none;
}
.scrollbar-hide {
    -ms-overflow-style: none;
    scrollbar-width: none;
}

summary::-webkit-details-marker {
    display: none;
}
summary {
    list-style: none;
}
</style>