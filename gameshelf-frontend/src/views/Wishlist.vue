<template>
    <div class="h-screen flex flex-col bg-[#0b0e14]">
        <div class="flex-shrink-0 sticky top-0 z-50">
            <Navbar />
        </div>
        
        <section ref="scrollContainer" class="flex-1 overflow-y-auto p-4 sm:p-6 md:p-8 text-gsblanco relative">
            <div class="max-w-[1600px] mx-auto">
                
                <div class="mb-6 md:mb-8 flex flex-col sm:flex-row sm:items-center justify-between border-b border-gsgris/10 pb-4 md:pb-6 text-gsmenta gap-4">
                    <div class="flex items-center gap-3">
                        <i class="pi pi-sparkles text-xl md:text-2xl"></i>
                        <h2 class="text-xl md:text-2xl font-semibold border-l-4 border-gsmenta/50 pl-3 md:pl-4">
                            Wishlist
                        </h2>
                        <span class="text-gsgris text-xs md:text-sm bg-[#161a21] px-2.5 py-1 rounded-full border border-gsgris/10 hidden xs:inline-block">
                            Filtered: {{ filteredItems.length }} / Total: {{ wishlist?.items.length || 0 }}
                        </span>
                    </div>

                    <div class="relative min-w-[180px] self-start sm:self-auto">
                        <label class="block text-[10px] font-bold text-gsgris uppercase tracking-wider mb-1 ml-1">
                            Format
                        </label>
                        <slot name="select">
                            <select v-model="currentFormat"
                                class="w-full bg-[#161a21] border border-gsgris/20 rounded-xl px-4 py-2.5 text-sm text-gsblanco focus:outline-none focus:border-gsmenta transition-colors cursor-pointer appearance-none pr-10 font-medium">
                                <option value="ALL">All Formats</option>
                                <option v-for="format in FORMAT_TYPES" :key="format.id" :value="format.id">
                                    {{ format.name }}
                                </option>
                            </select>
                        </slot>
                        <div class="pointer-events-none absolute inset-y-0 right-0 flex items-center pr-4 pt-4 text-gsgris">
                            <i class="pi pi-chevron-down text-xs"></i>
                        </div>
                    </div>
                </div>

                <main v-if="filteredItems.length > 0" class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-5 gap-y-10 gap-x-6">
                    <div v-for="item in filteredItems" :key="item.id"
                        class="group flex flex-col bg-[#161a21] rounded-xl border border-gsgris/20 hover:border-gsmenta/50 transition-all duration-300 shadow-lg"
                    >
                        <GameCard :game="item.game" :platform="item.platform"/>
                    </div>
                </main>

                <div v-else-if="wishlist?.items.length === 0" class="flex flex-col items-center justify-center py-20 md:py-28 text-gsgris border border-dashed border-gsgris/10 rounded-2xl bg-[#161a21]/30 backdrop-blur-sm">
                    <i class="pi pi-gift text-4xl md:text-5xl mb-3 md:mb-4 text-gsmenta/30"></i>
                    <p class="text-sm md:text-base font-semibold text-gsblanco mb-1">This wishlist is empty</p>
                    <p class="text-xs md:text-sm text-gsgris text-center max-w-xs px-4">There are no games added to this wishlist yet.</p>
                </div>

                <div v-else class="flex flex-col items-center justify-center py-20 md:py-28 text-gsgris border border-dashed border-gsgris/10 rounded-2xl bg-[#161a21]/30 backdrop-blur-sm">
                    <i class="pi pi-inbox text-4xl md:text-5xl mb-3 md:mb-4 text-gsgris/30"></i>
                    <p class="text-sm md:text-base font-semibold text-gsblanco mb-1">No games found</p>
                    <p class="text-xs md:text-sm text-gsgris text-center max-w-xs px-4">There are no games matching this format in the wishlist.</p>
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
import type { Wishlist } from '@/types/profileTypes';
import GameCard from '@/components/GameCard.vue';
import Navbar from '@/components/Navbar.vue';
import ScrollTopButton from '@/components/ScrollTopButton.vue'; 
import api from "@/api/client";
import router from '@/router';

const FORMAT_TYPES = [
    { id: 'P', name: 'Physical' },
    { id: 'D', name: 'Digital' }
];

const wishlist = ref<Wishlist>();
const authStore = useAuthStore();
const route = useRoute();
const userId = Number(route.params.user_id);
const wishlistId = route.params.wishlist_id;

const currentFormat = ref<string>('ALL');

// Propiedad computada para filtrar dinámicamente por formato
const filteredItems = computed(() => {
    if (!wishlist.value || !wishlist.value.items) return [];

    if (currentFormat.value === 'ALL') {
        return wishlist.value.items;
    }

    const targetFormat = FORMAT_TYPES.find(f => f.id === currentFormat.value);
    if (!targetFormat) return [];

    return wishlist.value.items.filter(item => {
        if (!item.type) return false;

        const apiFormat = item.type.toString().toUpperCase().trim();
        return apiFormat === targetFormat.id || apiFormat === targetFormat.name.toUpperCase();
    });
});

onMounted(async () => {
    try {
        const data = await getWishlist();
        if(data.is_private && !authStore.isOwnProfile(userId)) router.go(-1);
        wishlist.value = data;
    } catch (error: any) {
        console.error('Error cargando la wishlist:', error);
    }
});

async function getWishlist() {
    const response = await api.get(`/api/wishlist/${wishlistId}/`);
    return response.data;
}

const scrollContainer = ref<HTMLElement | null>(null);
</script>