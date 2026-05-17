<template>
    <div class="h-screen flex flex-col bg-[#0b0e14]">
        <div class="flex-shrink-0 sticky top-0 z-50">
            <Navbar />
        </div>
        
        <section ref="scrollContainer" class="flex-1 overflow-y-auto p-4 sm:p-6 md:p-8 text-gsblanco relative">
            <div class="max-w-[1600px] mx-auto">
                
                <div class="mb-6 md:mb-8 flex flex-col sm:flex-row sm:items-center justify-between border-b border-gsgris/10 pb-4 md:pb-6 text-gsmenta gap-4">
                    <div class="flex items-center gap-3">
                        <i class="pi pi-check-circle text-xl md:text-2xl text-gsmenta"></i>
                        <h2 class="text-xl md:text-2xl font-semibold border-l-4 border-gsmenta/50 pl-3 md:pl-4">
                            Completed
                        </h2>
                    </div>
                    <div class="flex flex-wrap gap-2 self-start sm:self-auto">
                        <span class="text-gsgris text-xs md:text-sm bg-[#161a21] px-3 py-1.5 rounded-xl border border-gsgris/10 flex items-center gap-2">
                            Total Completed: <span class="text-gsblanco font-semibold">{{ completed.length }}</span>
                        </span>
                        <span v-if="totalHours > 0" class="text-gsgris text-xs md:text-sm bg-[#161a21] px-3 py-1.5 rounded-xl border border-gsgris/10 flex items-center gap-2">
                            <i class="pi pi-clock text-gsmenta/70"></i>
                            Total Time: <span class="text-gsblanco font-semibold">{{ totalHours }}h</span>
                        </span>
                    </div>
                </div>

                <main v-if="completed.length > 0" class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-5 gap-y-10 gap-x-6">
                    <div v-for="item in completed" :key="item.id"
                        class="group flex flex-col bg-[#161a21] rounded-xl border border-gsgris/20 hover:border-gsmenta/50 transition-all duration-300 shadow-lg overflow-hidden"
                    >
                        <GameCard :game="item.game" :platform="item.platform"/>
                        
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

                <div v-else class="flex flex-col items-center justify-center py-20 md:py-28 text-gsgris border border-dashed border-gsgris/10 rounded-2xl bg-[#161a21]/30 backdrop-blur-sm">
                    <i class="pi pi-verified text-4xl md:text-5xl mb-3 md:mb-4 text-gsmenta/30"></i>
                    <p class="text-sm md:text-base font-semibold text-gsblanco mb-1">No completed games</p>
                    <p class="text-xs md:text-sm text-gsgris text-center max-w-xs px-4">There are no games marked as completed yet.</p>
                </div>
            </div>

            <ScrollTopButton :target="scrollContainer" :threshold="300" />
        </section>
    </div>
</template>

<script setup lang="ts">
import { onMounted, ref, computed } from 'vue';
import { useRoute } from 'vue-router';
import type { Library, LibraryItem } from '@/types/profileTypes';
import GameCard from '@/components/GameCard.vue';
import Navbar from '@/components/Navbar.vue';
import ScrollTopButton from '@/components/ScrollTopButton.vue'; 
import api from "@/api/client";
import { useAuthStore } from '@/stores/authStore';
import router from '@/router';

const library = ref<Library>();
const completed = ref<Array<LibraryItem>>([]);

const route = useRoute();
const authStore = useAuthStore();
const userId = Number(route.params.user_id);

const totalHours = computed(() => {
    return completed.value.reduce((acc, item) => acc + (Number(item.hours_played) || 0), 0);
});

onMounted(async () => {
    try {
        const data = await getLibrary();
        if(data.is_private && !authStore.isOwnProfile(userId)) router.go(-1);
        
        library.value = data;
        completed.value = await loadCompleted(data);
    } catch (error: any) {
        console.error('Error cargando los completados:', error);
    }
});

async function getLibrary() {
    const response = await api.get(`/api/library/users/${userId}/`);
    return response.data;
}

async function loadCompleted(libraryLoaded: Library) {
    if (!libraryLoaded || !libraryLoaded.items) return [];
    return libraryLoaded.items.filter(item => item.status === "Completed");
}

const scrollContainer = ref<HTMLElement | null>(null);
</script>