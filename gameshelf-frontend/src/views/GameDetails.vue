<template>
    <div class="h-screen flex flex-col bg-[#0b0e14]">
        <div class="flex-shrink-0 sticky top-0 z-50">
            <Navbar />
        </div>

        <section ref="scrollContainer" class="flex-1 overflow-y-auto p-6 sm:p-12 text-white relative">
            <div v-if="game" class="max-w-[1200px] mx-auto">

                <div class="flex flex-col md:flex-row gap-12 mb-12">

                    <div class="w-full md:w-[350px] flex-shrink-0">
                        <img :src="game.cover_detail" :alt="game.title"
                            class="w-full rounded shadow-2xl border-3 border-gsmenta" />
                    </div>

                    <div class="flex-1">

                        <div class="flex items-center gap-4 mb-2 relative">
                            <h1 class="text-5xl font-bold">{{ game.title }}</h1>

                            <div class="flex gap-2">
                                <div class="relative">
                                    <button @click="showPlatformSelector = !showPlatformSelector"
                                        class="p-2 rounded-full hover:bg-white/10 transition-all duration-300"
                                        title="Gestionar favoritos">
                                        <Icon :icon="isGameFavorite ? 'mdi:heart' : 'mdi:heart-outline'"
                                            class="text-4xl transition-transform active:scale-125"
                                            :class="isGameFavorite ? 'text-red-500' : 'text-gray-400 hover:text-red-400'" />
                                    </button>

                                    <div v-if="showPlatformSelector"
                                        class="absolute top-full left-0 mt-2 bg-[#151921] border border-white/10 rounded-lg shadow-2xl z-50 w-64 p-3 overflow-hidden">

                                        <div class="flex justify-between items-center mb-3 px-1">
                                            <span
                                                class="text-xs font-bold text-gray-500 uppercase tracking-wider">Añadir
                                                para:</span>
                                            <button @click="showPlatformSelector = false"
                                                class="text-gray-500 hover:text-white text-xs">Cerrar</button>
                                        </div>

                                        <div class="flex flex-col gap-1">
                                            <button v-for="p in game.platforms" :key="p.id"
                                                @click="toggleFavorite(p.id)"
                                                class="flex justify-between items-center px-3 py-2 rounded-md hover:bg-white/5 transition-colors group">
                                                <span
                                                    :class="favoritePlatforms.includes(p.id) ? 'text-gsmenta font-bold' : 'text-gray-300 group-hover:text-white'">
                                                    {{ p.name }}
                                                </span>
                                                <Icon
                                                    :icon="favoritePlatforms.includes(p.id) ? 'mdi:check-circle' : 'mdi:plus-circle-outline'"
                                                    class="text-xl"
                                                    :class="favoritePlatforms.includes(p.id) ? 'text-gsmenta' : 'text-gray-600 group-hover:text-gray-400'" />
                                            </button>
                                        </div>

                                        <p v-if="favoritePlatforms.length >= 10"
                                            class="text-[10px] text-red-400 mt-2 px-1">
                                            Límite de 10 favoritos alcanzado.
                                        </p>
                                    </div>
                                </div>

                                <div class="relative">
                                    <button
                                        @click="showWishlistSelector = !showWishlistSelector; showPlatformSelector = false"
                                        class="p-2 rounded-full hover:bg-white/10 transition-all">
                                        <Icon :icon="isAnyWishlist ? 'mdi:bookmark' : 'mdi:bookmark-outline'"
                                            class="text-4xl"
                                            :class="isAnyWishlist ? 'text-gsmenta' : 'text-gray-400 hover:text-gsmenta'" />
                                    </button>

                                    <div v-if="showWishlistSelector"
                                        class="absolute top-full left-0 mt-2 bg-[#151921] border border-white/10 rounded-lg shadow-2xl z-[60] w-72 p-3">
                                        <p class="text-xs font-bold text-gray-500 uppercase mb-3">Añadir a Wishlist</p>
                                        <div v-for="p in game.platforms" :key="p.id"
                                            class="mb-4 last:mb-0 border-b border-white/5 pb-3 last:border-0">
                                            <span class="text-xs text-gray-500 block mb-2">{{ p.name }}</span>
                                            <div class="flex gap-2">
                                                <button @click="toggleWishlist(p.id, 'D')"
                                                    :class="wishlistItems.find(i => i.platform.id === p.id && i.type === 'D') ? 'bg-gsmenta text-black' : 'bg-white/5 text-white'"
                                                    class="flex-1 text-[10px] py-1.5 rounded uppercase font-bold transition-all">
                                                    Digital
                                                </button>
                                                <button @click="toggleWishlist(p.id, 'P')"
                                                    :class="wishlistItems.find(i => i.platform.id === p.id && i.type === 'P') ? 'bg-gsmenta text-black' : 'bg-white/5 text-white'"
                                                    class="flex-1 text-[10px] py-1.5 rounded uppercase font-bold transition-all">
                                                    Físico
                                                </button>
                                            </div>
                                        </div>
                                    </div>
                                </div>

                                <div class="relative">
                                    <button
                                        @click="showLibrarySelector = !showLibrarySelector; showPlatformSelector = false; showWishlistSelector = false"
                                        class="p-2 rounded-full hover:bg-white/10 transition-all"
                                        title="Añadir a mi colección">
                                        <Icon :icon="isInLibrary ? 'mdi:library-shelves' : 'mdi:library-outline'"
                                            class="text-4xl"
                                            :class="isInLibrary ? 'text-gsmenta' : 'text-gray-400 hover:text-gsmenta'" />
                                    </button>

                                    <div v-if="showLibrarySelector"
                                        class="absolute top-full left-0 mt-2 bg-[#151921] border border-white/10 rounded-lg shadow-2xl z-[70] w-80 p-4">

                                        <p class="text-xs font-bold text-gray-500 uppercase mb-4">Mi Biblioteca</p>

                                        <div v-for="p in game.platforms" :key="p.id"
                                            class="mb-6 last:mb-0 border-b border-white/5 pb-4 last:border-0">
                                            <div class="flex justify-between items-center mb-2">
                                                <span class="text-sm font-bold text-white">{{ p.name }}</span>
                                                <span v-if="libraryItems.find(i => i.platform.id === p.id)"
                                                    class="text-[10px] text-gsmenta uppercase font-bold">En
                                                    Biblioteca</span>
                                            </div>

                                            <div class="grid grid-cols-2 gap-2">
                                                <button v-for="status in LIBRARY_STATUS" :key="status.id"
                                                    @click="toggleLibrary(p.id, status.id)" :class="libraryItems.some(i => Number(i.platform.id) === Number(p.id) && i.status === status.name)
                                                        ? 'bg-gsmenta text-black shadow-[0_0_10px_#00ff99]'
                                                        : 'bg-white/5 text-gray-400 hover:bg-white/10'"
                                                    class="text-[10px] py-1.5 rounded uppercase font-bold transition-all">
                                                    {{ status.name }}
                                                </button>
                                            </div>

                                            <button v-if="libraryItems.find(i => i.platform.id === p.id)"
                                                @click="toggleLibrary(p.id)"
                                                class="w-full mt-2 text-[9px] text-red-400 hover:text-red-300 uppercase font-bold text-center">
                                                Quitar de esta plataforma
                                            </button>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>

                        <p class="text-gray-400 text-xl mb-8">{{ game.released_at }}</p>

                        <div class="grid grid-cols-1 md:grid-cols-2 gap-y-4 gap-x-8 text-lg mb-8">
                            <div class="flex gap-2 items-center">
                                <span class="text-gray-400">Desarrolladora:</span>
                                <span class="text-gsmenta">
                                    {{ formatText(game?.developers, 'developer') }}
                                    <span v-if="game?.developers && isLong(game?.developers)"
                                        @click="toggleField('developer')"
                                        class="cursor-pointer hover:text-white transition-colors ml-1 font-bold">
                                        {{ expanded.developer ? ' (ver menos)' : '...' }}
                                    </span>
                                </span>
                            </div>

                            <div class="flex gap-2 items-center">
                                <span class="text-gray-400">Distribuidora:</span>
                                <span class="text-gsmenta">
                                    {{ formatText(game?.publishers, 'publisher') }}
                                    <span v-if="game?.publishers && isLong(game?.publishers)"
                                        @click="toggleField('publisher')"
                                        class="cursor-pointer hover:text-white transition-colors ml-1 font-bold">
                                        {{ expanded.publisher ? ' (ver menos)' : '...' }}
                                    </span>
                                </span>
                            </div>

                            <div class="flex gap-2 items-center mt-5">
                                <span class="text-gray-400">Plataformas:</span>
                                <div class="flex items-center gap-3">
                                    <div v-for="item in visibleIcons" :key="item.slug"
                                        class="group relative flex items-center">
                                        <Icon :icon="item.icon"
                                            class="text-2xl text-gsmenta transition-transform group-hover:scale-110"
                                            :title="item.slug" />
                                        <span
                                            class="absolute -top-8 left-1/2 -translate-x-1/2 bg-black text-xs p-1 rounded opacity-0 group-hover:opacity-100 transition-opacity whitespace-nowrap">
                                            {{ item.slug }}
                                        </span>
                                    </div>

                                    <button v-if="processedIcons.length > LIMIT_ICONS"
                                        @click="showAllPlatforms = !showAllPlatforms"
                                        class="text-gsmenta hover:text-white transition-colors font-bold text-xl flex items-center pb-1">
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
                                        <Icon :icon="(review.recommend ? 'mdi:thumb-up' : 'mdi:thumb-down')"
                                            class="text-2xl text-gsmenta transition-transform group-hover:scale-110"
                                            :title="review.recommend ? 'Recomiendo' : 'No recomendado'" />
                                    </span>
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
import api from "@/api/client";
import Navbar from '@/components/Navbar.vue';
import type { Developer, Game, Platform, Publisher } from '@/types/gameDetailsType';
import { useAuthStore } from '@/stores/authStore';
import type { FavoriteItem, Library, LibraryItem, Wishlist, WishlistItem } from '@/types/profileTypes';

const route = useRoute()
const authStore = useAuthStore()

const headers = {
    'Authorization': `Bearer ${authStore.token}`,
    'Content-Type': 'application/json'
}

const gameId = route.params.id
const game = ref<Game | null>(null);

const loading = ref(true)

onMounted(async () => {
    try {
        const data = await getGame()
        game.value = data
        await loadFavoriteStatus();
        await loadWishlistStatus();
        await loadLibraryStatus();
    } catch (error: any) {
        console.error('Error:', error)
    } finally {
        loading.value = false
    }
});

async function getGame() {
    const response = await api.get(`/api/games/${gameId}/`)
    return response.data
}

// --- Lógica de añadir a Favoritos ---
const showPlatformSelector = ref(false);
const favoritePlatforms = ref<number[]>([]);

const loadFavoriteStatus = async () => {
    const userId = authStore.getSelfId();

    const response = await api.get(
        `/api/favorites/user/${userId}/`,
        { headers }
    );
    // Filtramos los favoritos que pertenecen a este juego y guardamos sus IDs de plataforma
    favoritePlatforms.value = response.data
        .filter((fav: any) => fav.game.id === game.value?.id)
        .map((fav: any) => fav.platform.id);
};

const toggleFavorite = async (platformId: number) => {
    try {

        const response = await api.post(
            `/api/favorites/toggle/`,
            {
                pk_game: gameId,
                pk_platform: platformId
            },
            { headers }
        );

        // Actualizamos la lista local
        if (response.data.is_favorite) {
            favoritePlatforms.value.push(platformId);
        } else {
            favoritePlatforms.value = favoritePlatforms.value.filter(id => id !== platformId);
        }
    } catch (error: any) {
        alert(error.response?.data?.error || "Error al marcar favorito");
    }
};

const isGameFavorite = computed(() => favoritePlatforms.value.length > 0);

// --- LÓGICA DE WISHLIST ---
const isInWishlist = ref(false);
const wishlistData = ref<Wishlist | null>(null);
const wishlistItems = ref<WishlistItem[]>([]);
const wishlistId = computed(() => wishlistData.value?.id);

const showWishlistSelector = ref(false);

const loadWishlistStatus = async () => {
    try {
        // Obtenemos la wishlist del propio usuario autenticado
        const response = await api.get(`/api/wishlist/`, { headers });

        wishlistData.value = response.data;

        // Filtramos los items del game actual
        wishlistItems.value = response.data.items.filter(
            (item: WishlistItem) => item.game.id === game.value?.id
        );
    } catch (error: any) {
        console.error('Error cargando wishlist:', error);
    }
};

const toggleWishlist = async (platformId: number, type: 'P' | 'D') => {
    // TS sabe que existingItem será un WishlistItem o undefined
    const existingItem = wishlistItems.value.find(
        (item: WishlistItem) => item.platform.id === platformId && item.type === (type as any)
        // Nota: Si 'type' en tu interfaz es string, quizás necesites un cast pequeño o actualizar la interfaz
    );

    try {
        if (existingItem) {
            await api.delete(
                `/api/wishlist/items/${existingItem.id}/`
            );
            wishlistItems.value = wishlistItems.value.filter(item => item.id !== existingItem.id);
        } else {
            if (!wishlistId.value) return;

            const payload = {
                game_id: game.value?.id,
                platform_id: platformId,
                priority: 5,
                annotation: "",
                is_private: false,
                type: type
            };

            const response = await api.post(
                `/api/wishlist/${wishlistId.value}/`,
                payload
            );

            // Añadimos el nuevo item (que viene con el formato WishlistItem)
            wishlistItems.value.push(response.data);
        }
    } catch (error: any) {
        console.error(error);
    }
};

// Computed para saber si el icono de wishlist debe resaltar
const isAnyWishlist = computed(() => wishlistItems.value.length > 0);

// --- LÓGICA DE LIBRERÍA ---
const libraryData = ref<Library | null>(null);
const libraryItems = ref<LibraryItem[]>([]);
const showLibrarySelector = ref(false);

// Mapeo de estados para el select/botones
const LIBRARY_STATUS = [
    { id: 'PLN', name: 'Planning' },
    { id: 'PLY', name: 'Playing' },
    { id: 'CMP', name: 'Completed' },
    { id: 'PSD', name: 'Paused' },
    { id: 'DRP', name: 'Dropped' },
];

const loadLibraryStatus = async () => {
    try {
        const response = await api.get(`/api/library/`, { headers });
        libraryData.value = response.data;
        // Filtramos items para este juego
        libraryItems.value = response.data.items.filter(
            (item: LibraryItem) => item.game.id === game.value?.id
        );
    } catch (error: any) {
        console.error('Error cargando librería:', error);
    }
};

const toggleLibrary = async (platformId: number, status?: string) => {
    // 1. Buscamos si el juego ya existe en esta plataforma dentro de la librería
    const existingItem = libraryItems.value.find(
        (item: LibraryItem) => item.platform.id === platformId
    );

    try {
        if (existingItem) {
            // Si el usuario pulsa el MISMO estado que ya tiene, lo borramos (Toggle)
            // Si pulsa un estado diferente, lo actualizamos (PATCH)
            if (!status || existingItem.status === status) {
                await api.delete(
                    `/api/library/${existingItem.id}/`
                );
                libraryItems.value = libraryItems.value.filter(item => item.id !== existingItem.id);
            } else {
                // ACTUALIZAR ESTADO (PATCH)
                const response = await api.patch(
                    `/api/library/${existingItem.id}/`,
                    {
                        status,
                        platform_id: platformId
                    }
                );
                // Actualizamos el item en nuestro array local
                const index = libraryItems.value.findIndex(item => item.id === existingItem.id);
                if (index !== -1) libraryItems.value[index] = response.data;
            }
        } else if (status) {
            // CREAR NUEVO (POST)
            const payload = {
                game_id: game.value?.id,
                platform_id: platformId,
                status: status,
                is_private: false,
                hours_played: 0
            };

            await api.post(
                `/api/library/`,
                payload
            );

            // Recargamos para traer el objeto con el formato correcto del serializador
            await loadLibraryStatus();
        }
    } catch (error: any) {
        console.error("Error en Library:", error.response?.data);
    }
};

const isInLibrary = computed(() => libraryItems.value.length > 0);


// --- Details del Game

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

<style scoped></style>