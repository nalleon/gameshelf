<template>
    <div class="h-screen flex flex-col bg-[#0b0e14]"> 
        <div class="flex-shrink-0 sticky top-0 z-50">
            <Navbar/>
        </div>
        <section ref="scrollContainer" class="flex-1 overflow-y-auto p-6 sm:p-8 text-gsblanco relative">            
            <div class="max-w-[1600px] mx-auto">

                <router-link 
                    :to="`/collections/${userId}/`" 
                    class="text-sm text-gsmenta hover:underline flex items-center gap-1 mb-5"
                >
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 7l-5 5m0 0l5 5m-5-5H18" />
                    </svg>
                    Collections
                </router-link>

                <div class="mb-8 flex flex-col sm:flex-row sm:items-center justify-between gap-4 border-b border-gsgris/10 pb-6">
                    <div class="flex items-center gap-4 text-gsmenta">
                        <h2 class="text-2xl font-semibold border-l-4 border-gsmenta/50 pl-4">
                            {{ collection?.name }}
                        </h2>
                        <span class="text-gsgris text-sm">
                            Filtered: {{ filteredItems.length }} / Total: {{ collection?.items.length || 0 }}
                        </span>
                    </div>

                    <div class="relative min-w-[180px]">
                        <label class="block text-[10px] font-bold text-gsgris uppercase tracking-wider mb-1 ml-1">
                            Format
                        </label>
                        <select v-model="currentFormat"
                            class="w-full bg-[#161a21] border border-gsgris/20 rounded-xl px-4 py-2.5 text-sm text-gsblanco focus:outline-none focus:border-gsmenta transition-colors cursor-pointer appearance-none pr-10 font-medium">
                            <option value="ALL">All Formats</option>
                            <option v-for="format in FORMAT_TYPES" :key="format.id" :value="format.id">
                                {{ format.name }}
                            </option>
                        </select>
                        <div class="pointer-events-none absolute inset-y-0 right-0 flex items-center pr-4 pt-4 text-gsgris">
                            <i class="pi pi-chevron-down text-xs"></i>
                        </div>
                    </div>
                </div>

                <main v-if="filteredItems.length > 0" class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-5 gap-y-10 gap-x-6">
                    <div v-for="item in filteredItems" :key="item.id"
                        class="group flex flex-col bg-[#161a21] rounded-xl border border-gsgris/20 hover:border-gsmenta/50 transition-all duration-300 shadow-lg"
                    >
                        <GameCard v-if="!item.is_private" :game="item.game" :platform="item.platform"/>
                    </div>
                </main>

                <div v-else-if="collection?.items.length === 0" class="flex flex-col items-center justify-center py-24 text-gsgris border border-dashed border-gsgris/10 rounded-2xl bg-[#161a21]/30">
                    <i class="pi pi-folder-open text-5xl mb-4 text-gsmenta/40"></i>
                    <p class="text-base font-semibold text-gsblanco mb-1">This collection is empty</p>
                    <p class="text-sm text-gsgris">There are no games added to this collection yet.</p>
                </div>

                <div v-else class="flex flex-col items-center justify-center py-20 text-gsgris border border-dashed border-gsgris/10 rounded-2xl bg-[#161a21]/30">
                    <i class="pi pi-inbox text-4xl mb-3 text-gsgris/40"></i>
                    <p class="text-sm font-medium">No games found for this format.</p>
                </div>
            </div>

            <ScrollTopButton :target="scrollContainer" :threshold="300" />
        </section>
    </div>
</template>


<script setup lang="ts">
import { computed, onMounted, ref } from 'vue';
import { useRoute } from 'vue-router';

import { useAuthStore } from '@/stores/authStore';
import type { Collection } from '@/types/profileTypes';
import GameCard from '@/components/GameCard.vue';
import Navbar from '@/components/Navbar.vue';
import ScrollTopButton from '@/components/ScrollTopButton.vue';

import api from "@/api/client";
import router from '@/router';

const FORMAT_TYPES = [
    { id: 'P', name: 'Physical' },
    { id: 'D', name: 'Digital' }
];

const collection = ref<Collection>();
const authStore = useAuthStore();
const route = useRoute();
const userId = Number(route.params.user_id);
const collectionId = route.params.collection_id;

const currentFormat = ref<string>('ALL');

const filteredItems = computed(() => {
    if (!collection.value || !collection.value.items) return [];

    if (currentFormat.value === 'ALL') {
        return collection.value.items;
    }

    const targetFormat = FORMAT_TYPES.find(f => f.id === currentFormat.value);
    if (!targetFormat) return [];

    return collection.value.items.filter(item => {
        if (!item.type) return false;

        const apiFormat = item.type.toString().toUpperCase().trim();
        return apiFormat === targetFormat.id || apiFormat === targetFormat.name.toUpperCase();
    });
});

onMounted(async () => {
    await loadCollection();
});

async function loadCollection() {
    try {
        const data = await getCollection();
        if(data.is_private && !authStore.isOwnProfile(userId)) router.go(-1);

        collection.value = data;
    } catch (error: any) {
        console.error('Error cargando la collection:', error);
    }
}

async function getCollection() {
    const response = await api.get(
        `api/collections/${collectionId}/user/${userId}/`
    );
    return response.data;
}

// Elemento contenedor que tu SScrollTopButton observará mediante sus props
const scrollContainer = ref<HTMLElement | null>(null);
</script>

<style scoped>
/* Transiciones de opacidad nativas del componente de colección si las necesitas */
.fade-enter-active,
.fade-leave-active {
    transition: opacity 0.25s ease;
}
.fade-enter-from,
.fade-leave-to {
    opacity: 0;
}
</style>