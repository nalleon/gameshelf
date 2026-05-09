<template>
    <div class="h-screen flex flex-col bg-[#0b0e14]"> 
        <div class="flex-shrink-0 sticky top-0 z-50">
            <Navbar/>
        </div>

        <section ref="scrollContainer" class="flex-1 overflow-y-auto p-6 sm:p-12 text-white relative">            
            <div v-if="game" class="max-w-[1200px] mx-auto">
                
                <div class="flex flex-col md:flex-row gap-12 mb-12">
                    
                    <div class="w-full md:w-[350px] flex-shrink-0">
                        <img 
                            :src="game.cover_detail" 
                            :alt="game.title" 
                            class="w-full rounded shadow-2xl border-3 border-gsmenta"
                        />
                    </div>

                    <div class="flex-1">
                        <h1 class="text-5xl font-bold mb-2">{{ game.title }}</h1>
                        <p class="text-gray-400 text-xl mb-8">{{ game.released_at }}</p>

                        <div class="grid grid-cols-1 md:grid-cols-2 gap-y-4 gap-x-8 text-lg mb-8">
                            <div class="flex gap-2 items-center">
                                <span class="text-gray-400">Desarrolladora:</span>
                                <span class="text-gsmenta">
                                    {{ formatText(game?.developers, 'developer') }}
                                    <span 
                                        v-if="game?.developers && isLong(game?.developers)" 
                                        @click="toggleField('developer')"
                                        class="cursor-pointer hover:text-white transition-colors ml-1 font-bold"
                                    >
                                        {{ expanded.developer ? ' (ver menos)' : '...' }}
                                    </span>
                                </span>
                            </div>

                            <div class="flex gap-2 items-center">
                                <span class="text-gray-400">Distribuidora:</span>
                                <span class="text-gsmenta">
                                    {{ formatText(game?.publishers, 'publisher') }}
                                    <span 
                                        v-if="game?.publishers && isLong(game?.publishers)" 
                                        @click="toggleField('publisher')"
                                        class="cursor-pointer hover:text-white transition-colors ml-1 font-bold"
                                    >
                                        {{ expanded.publisher ? ' (ver menos)' : '...' }}
                                    </span>
                                </span>
                            </div>

                            <div class="flex gap-2 items-center mt-5">
                                <span class="text-gray-400">Plataformas:</span>
                                <div class="flex items-center gap-3">
                                    <div 
                                        v-for="item in visibleIcons" 
                                        :key="item.slug"
                                        class="group relative flex items-center"
                                    >
                                        <Icon 
                                            :icon="item.icon" 
                                            class="text-2xl text-gsmenta transition-transform group-hover:scale-110"
                                            :title="item.slug" 
                                        />
                                        <span class="absolute -top-8 left-1/2 -translate-x-1/2 bg-black text-xs p-1 rounded opacity-0 group-hover:opacity-100 transition-opacity whitespace-nowrap">
                                            {{ item.slug }}
                                        </span>
                                    </div>

                                    <button 
                                        v-if="processedIcons.length > LIMIT_ICONS"
                                        @click="showAllPlatforms = !showAllPlatforms"
                                        class="text-gsmenta hover:text-white transition-colors font-bold text-xl flex items-center pb-1"
                                    >
                                        {{ showAllPlatforms ? '«' : '...' }}
                                    </button>
                                </div>
                            </div>
                        </div>

                        <hr class="border-white/10 mb-8" />

                        <p class="text-gray-300 leading-relaxed text-lg max-w-3xl">
                            {{ game.description }}
                        </p>
                    </div>
                </div>

                <div class="mt-16">
                    <h3 class="text-gray-500 uppercase tracking-widest text-sm font-bold mb-6">Reviews</h3>
                    <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
                        <div v-for="review in game.reviews" :key="review.id" 
                            class="bg-[#151921] border border-white/5 p-6 rounded-md">
                            <div class="flex justify-between items-start mb-4">
                                <div>
                                    <h4 class="text-gsmenta font-medium">{{ review.author.username }}</h4>
                                    <span class="text-gray-400 ml-1">
                                        <Icon 
                                            :icon="(review.recommend ? 'mdi:thumb-up' : 'mdi:thumb-down')" 
                                            class="text-2xl text-gsmenta transition-transform group-hover:scale-110" 
                                            :title="review.recommend ? 'Recomiendo' : 'No recomendado'" 
                                        /> </span>
                                </div>
                                <span class="text-[10px] bg-green-500/10 text-green-500 px-2 py-1 rounded uppercase">
                                </span>
                            </div>
                        </div>
                    </div>
                </div>

            </div>

            <div v-else-if="loading" class="flex justify-center items-center h-64 text-gsmenta">
                Cargando...
            </div>
        </section>
    </div>
</template>

<script setup lang="ts">
import { computed, onMounted, ref } from 'vue';
import { useRoute } from 'vue-router'
import axios from 'axios';
import { Icon } from '@iconify/vue'

import Navbar from '@/components/Navbar.vue';
import type { Developer, Game, Platform, Publisher } from '@/types/gameDetailsType';

const route = useRoute()

const gameId = route.params.id
const game = ref<Game | null>(null);
const loading = ref(true)

onMounted(async () => {
    try {
        const data = await getGame()
        game.value = data
    } catch (error) {
        console.error('Error cargando el juego:', error)
    } finally {
        loading.value = false
    }
});

async function getGame() {
    const webhookUrl = `http://127.0.0.1:8000/api/games/${gameId}/`
    const response = await axios.get(webhookUrl)
    return response.data
}

// --- LÓGICA DE PLATAFORMAS ---
const PLATFORM_MAP: Record<string, string> = {
    'linux': 'simple-icons:linux',
    'playstation-2': 'simple-icons:playstation2',
    'playstation-3': 'simple-icons:playstation3',
    'playstation-4': 'simple-icons:playstation4',
    'playstation-5': 'simple-icons:playstation5',
    'pc-microsoft-windows': 'mdi:computer-classic',
    'xbox': 'simple-icons:xbox',
    'nintendo-switch': 'simple-icons:nintendoswitch',
    'android': 'simple-icons:android',
};

const LIMIT_ICONS = 3; // Número de iconos antes de mostrar los puntos
const showAllPlatforms = ref(false);

// 2. Procesar el string de plataformas a un array de iconos
const processedIcons = computed(() => {
    if (!game.value?.platforms) return [];
    
    const slugs = game.value.platforms.map(p => p.slug.trim()) // Extraemos solo el nombre de cada plataforma
    
    return slugs.map(slug => ({
        slug: slug,
        icon: PLATFORM_MAP[slug] || 'mdi:controller-classic' // Icono por defecto si no existe en el mapa
    }));
});

// 3. Lista visible basada en el límite y el estado de expansión
const visibleIcons = computed(() => {
    if (showAllPlatforms.value) return processedIcons.value;
    return processedIcons.value.slice(0, LIMIT_ICONS);
});


// --- LÓGICA DE INFORMACIÓN AMPLIADA ---
const LIMIT = 20;
const expanded = ref({
    developer: false,
    publisher: false,
    platform: false
});

// Comprobar la longitud del texto para decidir si mostrar el botón de expansión
const isLong = (list: Array<any> | undefined) => {
    if (!list || list.length === 0) return false;
    return list.map(item => item.name).join(', ').length > LIMIT;
};

// Función para alternar el estado
const toggleField = (field: 'developer' | 'publisher' | 'platform') => {
    expanded.value[field] = !expanded.value[field];
};

// Función para mostrar el texto procesado
const formatText = (list: Array<Developer> | Array<Publisher> | Array<Platform> | undefined, field: 'developer' | 'publisher' | 'platform') => {
    if (!list || list.length === 0) return '';

    const text = list.map(item => item.name).join(', ');

    if (text.length <= LIMIT || expanded.value[field]) return text;

    return text.substring(0, LIMIT);
};

</script>

<style scoped>

</style>