<template>
    <div class="h-screen flex flex-col bg-[#0b0e14]">
        <div class="flex-shrink-0 sticky top-0 z-50">
            <Navbar />
        </div>
        
        <section ref="scrollContainer" class="flex-1 overflow-y-auto p-6 sm:p-8 text-gsblanco relative">
            <div class="max-w-[1600px] mx-auto">

                <div class="mb-8 flex flex-col sm:flex-row sm:items-center justify-between gap-4 border-b border-gsgris/10 pb-6">
                    <div class="flex flex-col md:flex-row md:items-center gap-4 text-gsmenta">
                        <div class="flex items-center gap-4">
                            <h2 class="text-2xl font-semibold border-l-4 border-gsmenta/50 pl-4 capitalize">
                                {{ 'Library' }}
                            </h2>
                            <span class="text-gsgris text-sm bg-[#161a21] px-3 py-1 rounded-xl border border-gsgris/10">
                                Filtered: {{ filteredItems.length }} / Total: {{ library?.items.length || 0 }}
                            </span>
                        </div>
                        <span v-if="totalHours > 0" class="self-start text-gsgris text-sm bg-[#161a21] px-3 py-1 rounded-xl border border-gsgris/10 flex items-center gap-2">
                            <i class="pi pi-clock text-gsmenta/70 text-xs"></i>
                            Total Playtime: <span class="text-gsblanco font-semibold">{{ totalHours }}h</span>
                        </span>
                    </div>

                    <div class="relative min-w-[180px]">
                        <label class="block text-[10px] font-bold text-gsgris uppercase tracking-wider mb-1 ml-1">
                            List Status
                        </label>
                        <select v-model="currentStatus"
                            class="w-full bg-[#161a21] border border-gsgris/20 rounded-xl px-4 py-2.5 text-sm text-gsblanco focus:outline-none focus:border-gsmenta transition-colors cursor-pointer appearance-none pr-10 font-medium">
                            <option value="ALL">All Games</option>
                            <option v-for="status in LIBRARY_STATUS" :key="status.id" :value="status.id">
                                {{ status.name }}
                            </option>
                        </select>
                        <div class="pointer-events-none absolute inset-y-0 right-0 flex items-center pr-4 pt-4 text-gsgris">
                            <i class="pi pi-chevron-down text-xs"></i>
                        </div>
                    </div>
                </div>

                <main v-if="filteredItems.length > 0"
                    class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-5 gap-y-10 gap-x-6">
                    <div v-for="item in filteredItems" :key="item.id"
                        class="group flex flex-col bg-[#161a21] rounded-xl border border-gsgris/20 hover:border-gsmenta/50 transition-all duration-300 shadow-lg overflow-hidden">
                        <GameCard :game="item.game" :platform="item.platform" />
                        
                        <div class="p-3 border-t border-gsgris/10 bg-[#0f1217]/40 flex items-center justify-between mt-auto">
                            <span class="text-gsgris text-xs flex items-center gap-1.5">
                                <i class="pi pi-clock text-[11px] group-hover:text-gsmenta transition-colors"></i>
                                <span>Playtime</span>
                            </span>
                            <span class="text-xs font-bold text-gsblanco">
                                {{ item.hours_played && item.hours_played > 0 ? `${item.hours_played}h` : '--' }}
                            </span>
                        </div>
                    </div>
                </main>

                <div v-else-if="library?.items.length === 0"
                    class="flex flex-col items-center justify-center py-24 text-gsgris border border-dashed border-gsgris/10 rounded-2xl bg-[#161a21]/30">
                    <i class="pi pi-folder-open text-5xl mb-4 text-gsmenta/40"></i>
                    <p class="text-base font-semibold text-gsblanco mb-1">This library is empty</p>
                    <p class="text-sm text-gsgris">There are no games added to this library yet.</p>
                </div>

                <div v-else
                    class="flex flex-col items-center justify-center py-20 text-gsgris border border-dashed border-gsgris/10 rounded-2xl bg-[#161a21]/30">
                    <i class="pi pi-inbox text-4xl mb-3 text-gsgris/40"></i>
                    <p class="text-sm font-medium">No games found in this category.</p>
                </div>
            </div>

            <ScrollTopButton :target="scrollContainer" :threshold="300" />
        </section>
    </div>
</template>

<script setup lang="ts">
import { computed, onMounted, ref } from 'vue';
import { useRoute } from 'vue-router'
import type { Library } from '@/types/profileTypes';
import GameCard from '@/components/GameCard.vue';
import Navbar from '@/components/Navbar.vue';
import ScrollTopButton from '@/components/ScrollTopButton.vue';
import api from "@/api/client";
import { useAuthStore } from '@/stores/authStore';
import router from '@/router';

const LIBRARY_STATUS = [
    { id: 'PLN', name: 'Planning' },
    { id: 'PLY', name: 'Playing' },
    { id: 'CMP', name: 'Completed' },
    { id: 'PSD', name: 'Paused' },
    { id: 'DRP', name: 'Dropped' },
];

const authStore = useAuthStore();
const library = ref<Library>();
const route = useRoute()
const userId = Number(route.params.user_id);

const currentStatus = ref<string>('ALL');

const filteredItems = computed(() => {
    if (!library.value || !library.value.items) return [];

    if (currentStatus.value === 'ALL') {
        return library.value.items;
    }

    const targetStatus = LIBRARY_STATUS.find(s => s.id === currentStatus.value);
    if (!targetStatus) return [];

    return library.value.items.filter(item => {
        if (!item.status) return false;

        const apiStatus = item.status.toString().toUpperCase().trim();
        return apiStatus === targetStatus.id || apiStatus === targetStatus.name.toUpperCase();
    });
});

// Calcula las horas acumuladas únicamente de los juegos que están pasando el filtro actual
const totalHours = computed(() => {
    return filteredItems.value.reduce((acc, item) => acc + (Number(item.hours_played) || 0), 0);
});

onMounted(async () => {
    try {
        const data = await getLibrary()
        if (data.is_private && !authStore.isOwnProfile(userId)) router.go(-1)

        library.value = data
        console.log(data)
    } catch (error: any) {
        console.error('Error cargando la librería:', error)
    }
});

async function getLibrary() {
    const response = await api.get(`/api/library/users/${userId}/`);
    return response.data;
}

const scrollContainer = ref<HTMLElement | null>(null);
</script>

<style scoped>
.fade-enter-active,
.fade-leave-active {
    transition: opacity 0.25s ease;
}

.fade-enter-from,
.fade-leave-to {
    opacity: 0;
}
</style>