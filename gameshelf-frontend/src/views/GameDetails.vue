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

                                <!-- FAVORITOS -->
                                <div class="relative">
                                    <button 
                                        @click="openDropdown = openDropdown === 'favorites' ? null : 'favorites'"
                                        class="p-2 rounded-full hover:bg-white/10 transition-all duration-300"
                                        title="Gestionar favoritos">
                                        <Icon :icon="isGameFavorite ? 'mdi:heart' : 'mdi:heart-outline'"
                                            class="text-4xl transition-transform active:scale-125"
                                            :class="isGameFavorite ? 'text-red-500' : 'text-gray-400 hover:text-red-400'" />
                                    </button>

                                    <div v-if="openDropdown === 'favorites'"
                                        class="absolute top-full left-0 mt-2 bg-[#151921] border border-white/10 rounded-lg shadow-2xl z-50 w-64 p-3 overflow-hidden">

                                        <div class="flex justify-between items-center mb-3 px-1">
                                            <span class="text-xs font-bold text-gray-500 uppercase tracking-wider">
                                                Add as favorite for:
                                            </span>
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
                                    </div>
                                </div>

                                <!-- WISHLIST -->
                                <div class="relative">
                                    <button
                                        @click="openDropdown = openDropdown === 'wishlist' ? null : 'wishlist'"
                                        class="p-2 rounded-full hover:bg-white/10 transition-all">
                                        <Icon :icon="isAnyWishlist ? 'mdi:bookmark' : 'mdi:bookmark-outline'"
                                            class="text-4xl"
                                            :class="isAnyWishlist ? 'text-gsmenta' : 'text-gray-400 hover:text-gsmenta'" />
                                    </button>

                                    <div v-if="openDropdown === 'wishlist'"
                                        class="absolute top-full left-0 mt-2 bg-[#151921] border border-white/10 rounded-lg shadow-2xl z-[60] w-72 p-3">

                                        <p class="text-xs font-bold text-gray-500 uppercase mb-3">
                                            Add into Wishlist
                                        </p>

                                        <div v-for="p in game.platforms" :key="p.id"
                                            class="mb-4 last:mb-0 border-b border-white/5 pb-3 last:border-0">

                                            <span class="text-xs text-gray-500 block mb-2">{{ p.name }}</span>

                                            <div class="flex gap-2">
                                                <button @click="toggleWishlist(p.id, 'D')"
                                                    :class="wishlistItems.find(i => i.platform.id === p.id && i.type === 'D')
                                                        ? 'bg-gsmenta text-black'
                                                        : 'bg-white/5 text-white'"
                                                    class="flex-1 text-[10px] py-1.5 rounded uppercase font-bold transition-all">
                                                    Digital
                                                </button>

                                                <button @click="toggleWishlist(p.id, 'P')"
                                                    :class="wishlistItems.find(i => i.platform.id === p.id && i.type === 'P')
                                                        ? 'bg-gsmenta text-black'
                                                        : 'bg-white/5 text-white'"
                                                    class="flex-1 text-[10px] py-1.5 rounded uppercase font-bold transition-all">
                                                    Físico
                                                </button>
                                            </div>
                                        </div>
                                    </div>
                                </div>

                                <!-- LIBRARY -->
                                <div class="relative">
                                    <button
                                        @click="openDropdown = openDropdown === 'library' ? null : 'library'"
                                        class="p-2 rounded-full hover:bg-white/10 transition-all"
                                        title="Add into mi colección">
                                        <Icon :icon="isInLibrary ? 'mdi:library-shelves' : 'mdi:library-outline'"
                                            class="text-4xl"
                                            :class="isInLibrary ? 'text-gsmenta' : 'text-gray-400 hover:text-gsmenta'" />
                                    </button>

                                    <div v-if="openDropdown === 'library'"
                                        class="absolute top-full left-0 mt-2 bg-[#151921] border border-white/10 rounded-lg shadow-2xl z-[70] w-80 p-4">

                                        <p class="text-xs font-bold text-gray-500 uppercase mb-4">
                                            My library
                                        </p>

                                        <div v-for="p in game.platforms" :key="p.id"
                                            class="mb-6 last:mb-0 border-b border-white/5 pb-4 last:border-0">

                                            <div class="flex justify-between items-center mb-2">
                                                <span class="text-sm font-bold text-white">{{ p.name }}</span>
                                                <span v-if="libraryItems.find(i => i.platform.id === p.id)"
                                                    class="text-[10px] text-gsmenta uppercase font-bold">
                                                    In library
                                                </span>
                                            </div>

                                            <div class="grid grid-cols-2 gap-2">
                                                <button v-for="status in LIBRARY_STATUS" :key="status.id"
                                                    @click="toggleLibrary(p.id, status.id)"
                                                    :class="libraryItems.some(i => Number(i.platform.id) === Number(p.id) && i.status === status.name)
                                                        ? 'bg-gsmenta text-black shadow-[0_0_10px_#00ff99]'
                                                        : 'bg-white/5 text-gray-400 hover:bg-white/10'"
                                                    class="text-[10px] py-1.5 rounded uppercase font-bold transition-all">
                                                    {{ status.name }}
                                                </button>
                                            </div>
                                        </div>
                                    </div>
                                </div>

                                <!-- COLLECTIONS -->
                                <div class="relative">
                                    <button
                                        @click="openDropdown = openDropdown === 'collections' ? null : 'collections'"
                                        class="p-2 rounded-full hover:bg-white/10 transition-all"
                                        title="Mis Colecciones">
                                        <Icon
                                            :icon="userCollections.some(c => c.items.some(i => i.game.id === game?.id))
                                                ? 'mdi:folder-star'
                                                : 'mdi:folder-plus-outline'"
                                            class="text-4xl"
                                            :class="userCollections.some(c => c.items.some(i => i.game.id === game?.id))
                                                ? 'text-gsmenta'
                                                : 'text-gray-400 hover:text-gsmenta'" />
                                    </button>

                                    <div v-if="openDropdown === 'collections'"
                                        class="absolute top-full left-0 mt-2 bg-[#151921] border border-white/10 rounded-lg shadow-2xl z-[80] w-80 max-h-[500px] flex flex-col overflow-hidden">

                                        <div class="p-4 border-b border-white/5 bg-[#1a1f29]">
                                            <p class="text-xs font-bold text-gray-500 uppercase mb-3">
                                                Add into collection
                                            </p>

                                            <div class="flex gap-2">
                                                <input v-model="newCollectionName"
                                                    type="text"
                                                    placeholder="New collection..."
                                                    class="flex-1 bg-white/5 border border-white/10 rounded px-2 py-1.5 text-xs focus:outline-none focus:border-gsmenta text-white"
                                                    @keyup.enter="createNewCollection" />

                                                <button @click="createNewCollection"
                                                    class="bg-gsmenta text-black px-3 py-1 rounded font-bold hover:brightness-110">
                                                    <Icon icon="mdi:plus" class="text-xl" />
                                                </button>
                                            </div>
                                        </div>

                                        <div class="overflow-y-auto p-4 space-y-4 custom-scrollbar">
                                            <div v-for="col in collectionItemsForGame" :key="col.id"
                                                class="border-b border-white/5 pb-4 last:border-0 last:pb-0">

                                                <div class="flex justify-between items-center mb-2">
                                                    <span class="text-sm font-bold text-gray-200 truncate">
                                                        {{ col.name }}
                                                    </span>
                                                    <span v-if="col.is_private"
                                                        class="text-[10px] text-gray-600 uppercase">
                                                        Private
                                                    </span>
                                                </div>

                                                <div v-for="p in game.platforms" :key="p.id" class="mt-2 space-y-1">

                                                    <p class="text-[9px] text-gray-500 font-bold ml-1 uppercase">
                                                        {{ p.name }}
                                                    </p>

                                                    <div class="flex gap-2">
                                                        <button
                                                            @click="toggleCollectionItem(col.id, p.id, 'D')"
                                                            :class="isInCollection(col, p.id, 'D')
                                                                ? 'bg-gsmenta text-black'
                                                                : 'bg-white/5 text-gray-400'"
                                                            class="flex-1 text-[9px] py-1.5 rounded font-bold transition-all uppercase">
                                                            Digital
                                                        </button>

                                                        <button
                                                            @click="toggleCollectionItem(col.id, p.id, 'P')"
                                                            :class="isInCollection(col, p.id, 'P')
                                                                ? 'bg-gsmenta text-black'
                                                                : 'bg-white/5 text-gray-400'"
                                                            class="flex-1 text-[9px] py-1.5 rounded font-bold transition-all uppercase">
                                                            Physical
                                                        </button>
                                                    </div>
                                                </div>
                                            </div>
                                        </div>
                                    </div>
                                </div>

                            </div>
                        </div>

                        <p class="text-gray-400 text-xl mb-8">{{ game.released_at }}</p>

                        <div class="grid grid-cols-1 md:grid-cols-2 gap-y-4 gap-x-8 text-lg mb-8">
                            <div class="flex gap-2 items-center">
                                <span class="text-gray-400">Desarrolladora:</span>
                                <span class="text-gsmenta">{{ formatText(game?.developers, 'developer') }}</span>
                            </div>

                            <div class="flex gap-2 items-center">
                                <span class="text-gray-400">Distribuidora:</span>
                                <span class="text-gsmenta">{{ formatText(game?.publishers, 'publisher') }}</span>
                            </div>
                        </div>

                        <hr class="border-white/10 mb-8" />

                        <p class="text-gray-300 leading-relaxed text-lg max-w-3xl">
                            {{ game.description }}
                        </p>

                        <div class="mt-16 border-t border-white/10 pt-12">
                            <h2 ref="reviewsTitle" class="text-3xl font-bold mb-8">Reviews</h2>

                            <div v-if="!userHasReviewed || isEditingReview" 
                                class="bg-[#151921] p-6 rounded-lg mb-12 border border-white/10 shadow-xl">
                                
                                <h3 class="text-xl font-bold mb-4 text-gsmenta">
                                    {{ isEditingReview ? 'Edit Review' : 'Write a Review' }}
                                </h3>
                                
                                <textarea
                                    v-model="reviewForm.content"
                                    class="w-full bg-white/5 border border-white/10 rounded-lg p-4 text-white mb-4 min-h-[120px] focus:outline-none focus:border-gsmenta transition-colors"
                                    placeholder="What do you think about this game?"
                                ></textarea>

                                <div class="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4">
                                    <div class="flex items-center gap-4">
                                        <label class="flex items-center gap-2 cursor-pointer group">
                                            <input type="radio" v-model="reviewForm.recommend" :value="true" class="hidden peer" />
                                            <div class="p-2 px-4 rounded border border-white/10 peer-checked:bg-gsmenta peer-checked:text-black group-hover:bg-white/5 transition-all font-bold flex items-center gap-2">
                                                <Icon icon="mdi:thumb-up" class="text-xl" /> 
                                                Recommend
                                            </div>
                                        </label>
                                        <label class="flex items-center gap-2 cursor-pointer group">
                                            <input type="radio" v-model="reviewForm.recommend" :value="false" class="hidden peer" />
                                            <div class="p-2 px-4 rounded border border-white/10 peer-checked:bg-red-500 peer-checked:text-white group-hover:bg-white/5 transition-all font-bold flex items-center gap-2">
                                                <Icon icon="mdi:thumb-down" class="text-xl" /> 
                                                Don't Recommend
                                            </div>
                                        </label>
                                    </div>

                                    <div class="flex gap-3">
                                        <button v-if="isEditingReview" @click="cancelEdit" 
                                            class="bg-white/10 text-white font-bold py-2 px-6 rounded hover:bg-white/20 transition-colors">
                                            Cancel
                                        </button>
                                        <button @click="saveReview" 
                                            class="bg-gsmenta text-black font-bold py-2 px-6 rounded hover:brightness-110 transition-all shadow-[0_0_15px_rgba(0,255,153,0.3)]">
                                            {{ isEditingReview ? 'Update' : 'Post Review' }}
                                        </button>
                                    </div>
                                </div>
                            </div>

                            <div class="space-y-6">
                                <div v-if="reviews.length === 0" class="text-gray-500 italic text-center py-8">
                                    No reviews yet. Be the first to share your thoughts!
                                </div>

                                <div v-for="review in reviews" :key="review.id" 
                                    class="bg-[#151921] p-6 rounded-lg border border-white/10">
                                    
                                    <div class="flex justify-between items-start mb-4">
                                        <div class="flex items-center gap-4">
                                            <div class="bg-white/10 w-12 h-12 rounded-full flex items-center justify-center font-bold text-xl text-gray-300">
                                                {{ review.author?.username?.charAt(0).toUpperCase() || 'U' }}
                                            </div>
                                            <div>
                                                <p class="font-bold text-lg text-gray-200">{{ review.author?.username || 'Unknown User' }}</p>
                                                <div class="flex items-center gap-1 text-sm font-bold mt-1" 
                                                    :class="review.recommend ? 'text-gsmenta' : 'text-red-500'">
                                                    <Icon :icon="review.recommend ? 'mdi:thumb-up' : 'mdi:thumb-down'" />
                                                    <span>{{ review.recommend ? 'Recommended' : 'Not Recommended' }}</span>
                                                </div>
                                            </div>
                                        </div>

                                        <div v-if="review.author?.id === currentUserId" class="flex gap-2">
                                            <button @click="startEdit(review)" 
                                                class="p-2 bg-white/5 rounded text-gray-400 hover:text-gsmenta hover:bg-white/10 transition-all" title="Edit">
                                                <Icon icon="mdi:pencil" class="text-xl" />
                                            </button>
                                            <button @click="deleteReview(review.id)" 
                                                class="p-2 bg-white/5 rounded text-gray-400 hover:text-red-500 hover:bg-white/10 transition-all" title="Delete">
                                                <Icon icon="mdi:trash-can" class="text-xl" />
                                            </button>
                                        </div>
                                    </div>
                                    
                                    <p class="text-gray-300 leading-relaxed whitespace-pre-wrap">{{ review.content }}</p>
                                </div>
                                <div class="space-y-6">
                                </div>

                                <div v-if="totalPages > 1" class="flex justify-center items-center gap-4 mt-8">
                                    <button
                                        @click="changePage(currentPage - 1)"
                                        :disabled="!hasPreviousPage"
                                        class="p-2 rounded bg-white/5 hover:bg-white/10 disabled:opacity-30 disabled:hover:bg-white/5 disabled:cursor-not-allowed transition-all">
                                        <Icon icon="mdi:chevron-left" class="text-3xl text-white" />
                                    </button>

                                    <div class="flex items-center gap-2">
                                        <span class="text-gray-400 font-bold text-sm uppercase tracking-wider">Page</span>
                                        <span class="text-gsmenta font-bold text-lg">{{ currentPage }}</span>
                                        <span class="text-gray-500 font-bold">/</span>
                                        <span class="text-gray-400 font-bold">{{ totalPages }}</span>
                                    </div>

                                    <button
                                        @click="changePage(currentPage + 1)"
                                        :disabled="!hasNextPage"
                                        class="p-2 rounded bg-white/5 hover:bg-white/10 disabled:opacity-30 disabled:hover:bg-white/5 disabled:cursor-not-allowed transition-all">
                                        <Icon icon="mdi:chevron-right" class="text-3xl text-white" />
                                    </button>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>

            </div>

            <div v-else-if="loading" class="flex justify-center items-center h-64 text-gsmenta">
                Loading...
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
import type { Developer, Game, Platform, Publisher, Review } from '@/types/gameDetailsType';
import { useAuthStore } from '@/stores/authStore';
import type { Collection, CollectionItem, Library, LibraryItem, Wishlist, WishlistItem } from '@/types/profileTypes';
import { PLATFORM_MAP } from '@/constants/app';

const route = useRoute()
const authStore = useAuthStore()

const headers = {
    'Authorization': `Bearer ${authStore.token}`,
    'Content-Type': 'application/json'
}

const gameId = route.params.id
const game = ref<Game | null>(null);

const loading = ref(true)
const openDropdown = ref<null | 'favorites' | 'wishlist' | 'library' | 'collections'>(null)

onMounted(async () => {
    try {
        const data = await getGame()
        game.value = data
        await loadCollections();
        await loadFavoriteStatus();
        await loadWishlistStatus();
        await loadLibraryStatus();
        await loadReviews();
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

// --- Lógica de Add into Favoritos ---
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

            // console.log({
            //     game_id: game.value?.id,
            //     platform_id: platformId,
            //     type
            // });

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

// --- LÓGICA DE COLECCIONES ---
const userCollections = ref<Collection[]>([]);
const showCollectionSelector = ref(false);
const newCollectionName = ref("");
const isNewCollectionPrivate = ref(false);

const loadCollections = async () => {
    try {
        const response = await api.get('/api/collections/')
        // console.log("STATUS:", response.status)
        // console.log("DATA:", response.data)
          
        userCollections.value = response.data.map((col: any) => ({
            ...col,
            items: col.items ?? []
        }));

// userCollections.value = response.data;
        newCollectionName.value = "";
    } catch (err: any) {
        console.error("ERROR:", err.response?.status)
        console.error("DETAIL:", err.response?.data)
    }
}

const collectionItemsForGame = computed(() => {
    if (!game.value) return [];

    return userCollections.value.map(col => ({
        ...col,
        items: col.items.filter(
            (i: any) => i.game?.id === game.value?.id
        )
    }));
});

const createNewCollection = async () => {

    if (!newCollectionName.value.trim()) return;

    try {

        const response = await api.post(
            `/api/collections/`,
            {
                name: newCollectionName.value,
                is_private: isNewCollectionPrivate.value
            }
        );

        userCollections.value.push({
            ...response.data,
            items: []
        });

        newCollectionName.value = "";

    } catch (error: any) {

        alert("Error al crear la colección");

    }
};

const toggleCollectionItem = async (
    collectionId: number,
    platformId: number,
    type: 'P' | 'D'
) => {

    const collection = userCollections.value.find(
        c => c.id === collectionId
    );

    if (!collection) return;

    const existingItem: CollectionItem | undefined =
        collection.items.find(
            item =>
                item.game.id === game.value?.id &&
                item.type === type &&
                item.platform.id === platformId
        );

    try {

        if (existingItem) {

            await api.delete(
                `/api/collections/${collectionId}/items/${existingItem.id}/`
            );

        } else {

            await api.post(
                `/api/collections/${collectionId}/`,
                {
                    game_id: game.value?.id,
                    platform_id: platformId,
                    is_private: false,
                    type: type
                }
            );
        }

        await loadCollections();

    } catch (error: any) {

        console.error(error.response?.data);

        alert(
            error.response?.data?.error ||
            "Error al gestionar colección"
        );
    }
};

// Helper para saber si un juego está en una colección específica
const isInCollection = (
    collection: Collection,
    platformId: number,
    type: 'P' | 'D'
) => {

    return collection.items.some(
        item =>
            item.game.id === game.value?.id &&
            item.type === type &&
            item.platform.id === platformId
    );
};

// --- Details del Game

// --- LÓGICA DE PLATAFORMAS ---
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
// const isLong = (list: Array<any> | undefined) => {
//     if (!list || list.length === 0) return false;
//     return list.map(item => item.name).join(', ').length > LIMIT;
// };

// Función para alternar el estado
// const toggleField = (field: 'developer' | 'publisher' | 'platform') => {
//     expanded.value[field] = !expanded.value[field];
// };

// Función para mostrar el texto procesado
const formatText = (list: Array<Developer> | Array<Publisher> | Array<Platform> | undefined, field: 'developer' | 'publisher' | 'platform') => {
    if (!list || list.length === 0) return '';

    const text = list.map(item => item.name).join(', ');

    if (text.length <= LIMIT || expanded.value[field]) return text;

    return text.substring(0, LIMIT);
};


// --- LÓGICA DE REVIEWS ---

const reviews = ref<Review[]>([]);
const currentUserId = computed(() => authStore.getSelfId());

// Formulario
const reviewForm = ref({
    content: '',
    recommend: true as boolean | null
});
const isEditingReview = ref<number | null>(null);

// Comprobamos si el usuario actual ya ha escrito una review
const userHasReviewed = computed(() => {
    return reviews.value.some(r => r.author?.id === currentUserId.value);
});

const loadReviews = async (page = 1) => {
    try {
        // Ahora pasamos explícitamente el game_id y la página al backend
        const response = await api.get(`/api/reviews/?game_id=${gameId}&page=${page}`, { headers });
        
        // Ya no hace falta filtrar en el frontend porque el backend nos da exactamente lo que queremos
        reviews.value = response.data.results;
        
        // Actualizamos los controles de paginación
        currentPage.value = response.data.current_page;
        totalPages.value = response.data.total_pages;
        hasNextPage.value = response.data.has_next;
        hasPreviousPage.value = response.data.has_previous;
        
    } catch (error) {
        console.error('Error cargando reviews:', error);
    }
};

const saveReview = async () => {
    if (!reviewForm.value.content.trim() || reviewForm.value.recommend === null) {
        alert("Please write a review and select a recommendation.");
        return;
    }

    try {
        if (isEditingReview.value) {
            // EDITAR (PATCH) - Tu backend espera pk_game según el views.py
            await api.patch(`/api/reviews/${isEditingReview.value}/`, {
                content: reviewForm.value.content,
                recommend: reviewForm.value.recommend,
                pk_game: Number(gameId)
            }, { headers });
        } else {
            // CREAR NUEVA (POST) - Tu backend espera game_id según el views.py
            await api.post(`/api/reviews/`, {
                content: reviewForm.value.content,
                recommend: reviewForm.value.recommend,
                game_id: Number(gameId)
            }, { headers });
        }

        // Limpiar estado y recargar
        cancelEdit();
        await loadReviews();
        
    } catch (error: any) {
        console.error('Error guardando review:', error.response?.data);
        alert(error.response?.data?.error || "Error saving the review.");
    }
};

const startEdit = (review: Review) => {
    isEditingReview.value = review.id;
    reviewForm.value = {
        content: review.content,
        recommend: review.recommend
    };
};

const cancelEdit = () => {
    isEditingReview.value = null;
    reviewForm.value = { content: '', recommend: true };
};

const deleteReview = async (reviewId: number) => {
    if (!confirm('Are you sure you want to delete this review?')) return;
    
    try {
        await api.delete(`/api/reviews/${reviewId}/`, { headers });
        
        // Si estaba editando la review que acaba de borrar, reseteamos el formulario
        if (isEditingReview.value === reviewId) {
            cancelEdit();
        }
        
        await loadReviews();
    } catch (error: any) {
        console.error('Error borrando review:', error.response?.data);
    }
};

// Nuevos estados para la paginación
const currentPage = ref(1);
const totalPages = ref(1);
const hasNextPage = ref(false);
const hasPreviousPage = ref(false);
const reviewsTitle = ref<HTMLElement | null>(null);

const changePage = async (newPage: number) => {
    if (newPage >= 1 && newPage <= totalPages.value) {
        await loadReviews(newPage);

        reviewsTitle.value?.scrollIntoView({
            behavior: 'smooth'
        });
    }
};

</script>

<style scoped></style>