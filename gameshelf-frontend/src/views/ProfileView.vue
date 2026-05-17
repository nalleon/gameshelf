<template>
    <Navbar />

    <transition name="toast-modern">
        <div v-if="showSuccessMessage"
            class="fixed top-6 right-6 z-50 flex items-center gap-4 p-4 rounded-2xl border bg-gsoscuro/80 backdrop-blur-md shadow-[0_20px_50px_rgba(0,0,0,0.5)] min-w-[320px] overflow-hidden"
            :style="{ borderColor: `${userColor}30` }">
            <div class="flex-shrink-0 w-10 h-10 rounded-xl flex items-center justify-center shadow-[0_0_15px_rgba(0,0,0,0.2)]"
                :style="{ backgroundColor: `${userColor}20`, color: userColor }">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24"
                    stroke="currentColor" stroke-width="3">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M5 13l4 4L19 7" />
                </svg>
            </div>

            <div class="flex-grow">
                <p class="text-gsblanco font-bold text-sm leading-tight">Success!</p>
                <p class="text-gsgris text-xs mt-0.5">Profile updated successfully</p>
            </div>

            <button @click="showSuccessMessage = false"
                class="text-gsgris hover:text-gsblanco transition-colors p-1 cursor-pointer">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24"
                    stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
                </svg>
            </button>

            <div class="absolute bottom-0 left-0 h-[3px] shadow-[0_0_10px_rgba(0,0,0,0.5)] progress-bar"
                :style="{ backgroundColor: userColor }"></div>
        </div>
    </transition>

    <div class="min-h-screen bg-gsoscuro text-gsblanco font-sans pb-20" :style="{ '--user-color': userColor }">
        <header class="relative bg-[#1a1e26]">
            <div class="h-48 md:h-55" :style="{ backgroundColor: userColor }" />

            <div class="max-w-5xl mx-auto px-6 relative">
                <div class="flex flex-col md:block -mt-12 md:-mt-20 pb-6 text-left">

                    <div class="flex items-start justify-between w-full">
                        <div class="w-28 h-28 sm:w-32 sm:h-32 md:w-40 md:h-40 rounded-full bg-gsoscuro border-4 overflow-hidden shadow-xl shrink-0"
                            :style="{ border: `4px solid ${userColor}` }">
                            <img v-if="profile?.avatar" :src="profile.avatar" alt="User Avatar"
                                class="w-full h-full rounded-full object-cover bg-gsoscuro" />
                        </div>

                        <router-link v-if="isOwnProfile" to="/profile/edit"
                            class="flex md:hidden items-center gap-1.5 mt-14 px-4 py-1.5 rounded-full border font-bold text-xs tracking-wide shadow-[0_4px_10px_rgba(0,0,0,0.2)] active:scale-95 transition-all duration-200 dynamic-btn-mobile">
                            <i class="pi pi-cog text-base shrink-0"></i>
                            <span>Manage profile</span>
                        </router-link>

                        <router-link v-if="isOwnProfile" to="/profile/edit"
                            class="hidden md:flex items-center gap-2 mt-24 px-5 py-2 rounded-full border font-bold text-sm tracking-wider shadow-[0_4px_12px_rgba(0,0,0,0.2)] hover:-translate-y-0.5 active:scale-95 active:translate-y-0 transition-all duration-300 ease-out shrink-0 dynamic-btn">
    
                            <i class="pi pi-cog text-base shrink-0"></i>
                            <span>Manage profile</span>
                        </router-link>
                    </div>

                    <div class="flex-1 min-w-0 w-full mt-4 md:mt-3">
                        <h1 class="text-2xl sm:text-3xl font-bold truncate max-w-full" :title="fullName">
                            {{ fullName }}
                        </h1>
                        <p class="font-medium truncate" :style="{ color: userColor }">@{{ profile?.user.username }}</p>

                        <div class="flex flex-wrap gap-2 mt-3" v-if="profile">
                            <Badge nombre="role" :role="profile.role ?? 'unknown'" />
                            <Badge nombre="completionist" :completedQuantity="completed" />
                            <Badge nombre="collectionist"
                                :collectionsQuantity="profile.user.collections?.length ?? 0" />
                            <Badge nombre="wisher" :wishlistQuantity="profile.user.wishlist.items?.length ?? 0" />
                            <Badge nombre="player" :libraryQuantity="profile.user.library.items?.length ?? 0" />
                        </div>
                    </div>

                </div>
            </div>
        </header>

        <div class="w-full h-[1px]"
            :style="{ backgroundImage: `linear-gradient(to right, transparent, ${userColor}33, transparent)` }"></div>

        <section class="bg-[#161a21] border-b border-gsgris/10 py-10 relative" v-if="profile">
            <div class="max-w-5xl mx-auto px-6 flex flex-col items-center justify-center gap-6 md:gap-12">

                <button @click="showRadarMobile = !showRadarMobile"
                    class="flex md:hidden items-center gap-2 px-4 py-2 rounded-xl border bg-gsoscuro/40 text-xs uppercase tracking-wider font-bold hover:bg-opacity-20 transition-all duration-300"
                    :style="{ borderColor: `${userColor}33`, color: userColor }">
                    <span>{{ showRadarMobile ? 'Hide Stats chart' : 'Show Stats chart' }}</span>
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 transition-transform duration-300"
                        :class="{ 'rotate-180': showRadarMobile }" fill="none" viewBox="0 0 24 24"
                        stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
                    </svg>
                </button>

                <div
                    class="flex flex-col md:flex-row items-center md:items-stretch justify-between gap-8 md:gap-12 w-full">

                    <div class="hidden md:flex flex-col flex-1 text-left justify-center order-1">
                        <h3 class="text-[10px] uppercase tracking-[0.2em] font-bold mb-3" :style="{ color: userColor }">
                            Biography</h3>
                        <div class="bg-gsoscuro/50 p-5 rounded-2xl border shadow-xl relative overflow-hidden flex items-start"
                            :style="{ borderColor: `${userColor}1a` }">
                            <div class="absolute top-0 left-0 w-full h-[2px]"
                                :style="{ backgroundImage: `linear-gradient(to right, ${userColor}, transparent, transparent)` }">
                            </div>
                            <p class="text-gsblanco/80 leading-relaxed text-sm relative z-10 whitespace-pre-line pt-1">
                                {{ profile?.bio || defaultBio }}
                            </p>
                        </div>
                    </div>

                    <div
                        class="grid grid-cols-1 sm:grid-cols-3 md:flex md:flex-col gap-3 md:gap-2 w-full md:w-auto justify-center order-3 md:order-2 shrink-0">

                        <router-link :to="`/collections/${profile.user.id}`" :class="[
                            'flex flex-row items-center justify-start md:text-left group p-3 px-4 rounded-xl border transition-all duration-300 hover:translate-x-1 active:scale-95 gap-4 md:gap-0',
                            activeHoverIndex === getVisibleIndex('collections') ? 'active-stat-card' : 'inactive-stat-card'
                        ]" @mouseenter="activeHoverIndex = getVisibleIndex('collections')"
                            @mouseleave="activeHoverIndex = null"
                            @touchstart="activeHoverIndex = getVisibleIndex('collections')"
                            @touchend="activeHoverIndex = null">
                            <span
                                :class="['text-xl font-bold md:mr-2 transition-colors duration-300 min-w-[2rem] md:min-w-0 md:inline block stat-number', activeHoverIndex === getVisibleIndex('collections') ? 'text-gsblanco' : '']">
                                {{ statsData.collections }}
                            </span>
                            <span
                                :class="['text-xs uppercase tracking-wider font-semibold transition-colors duration-300 text-left stat-label', activeHoverIndex === getVisibleIndex('collections') ? '' : 'text-gsgris group-hover:text-gsblanco']">
                                Collections
                            </span>
                        </router-link>

                        <router-link v-if="!profile.user.library.is_private || isOwnProfile"
                            :to="`/library/${profile.user.id}`" :class="[
                                'flex flex-row items-center justify-start md:text-left group p-3 px-4 rounded-xl border transition-all duration-300 hover:translate-x-1 active:scale-95 gap-4 md:gap-0',
                                activeHoverIndex === getVisibleIndex('library') ? 'active-stat-card' : 'inactive-stat-card'
                            ]" @mouseenter="activeHoverIndex = getVisibleIndex('library')"
                            @mouseleave="activeHoverIndex = null"
                            @touchstart="activeHoverIndex = getVisibleIndex('library')"
                            @touchend="activeHoverIndex = null">
                            <span
                                :class="['text-xl font-bold md:mr-2 transition-colors duration-300 min-w-[2rem] md:min-w-0 md:inline block stat-number', activeHoverIndex === getVisibleIndex('library') ? 'text-gsblanco' : '']">
                                {{ statsData.library }}
                            </span>
                            <span
                                :class="['text-xs uppercase tracking-wider font-semibold transition-colors duration-300 text-left stat-label', activeHoverIndex === getVisibleIndex('library') ? '' : 'text-gsgris group-hover:text-gsblanco']">
                                Library
                            </span>
                        </router-link>

                        <router-link :to="`/favorites/${profile.user.id}`" :class="[
                            'flex flex-row items-center justify-start md:text-left group p-3 px-4 rounded-xl border transition-all duration-300 hover:translate-x-1 active:scale-95 gap-4 md:gap-0',
                            activeHoverIndex === getVisibleIndex('favorites') ? 'active-stat-card' : 'inactive-stat-card'
                        ]" @mouseenter="activeHoverIndex = getVisibleIndex('favorites')"
                            @mouseleave="activeHoverIndex = null"
                            @touchstart="activeHoverIndex = getVisibleIndex('favorites')"
                            @touchend="activeHoverIndex = null">
                            <span
                                :class="['text-xl font-bold md:mr-2 transition-colors duration-300 min-w-[2rem] md:min-w-0 md:inline block stat-number', activeHoverIndex === getVisibleIndex('favorites') ? 'text-gsblanco' : '']">
                                {{ statsData.favorites }}
                            </span>
                            <span
                                :class="['text-xs uppercase tracking-wider font-semibold transition-colors duration-300 text-left stat-label', activeHoverIndex === getVisibleIndex('favorites') ? '' : 'text-gsgris group-hover:text-gsblanco']">
                                Favorites
                            </span>
                        </router-link>

                        <router-link v-if="!profile.user.wishlist.is_private || isOwnProfile"
                            :to="`/wishlist/${profile.user.id}/${profile.user.wishlist.id}`" :class="[
                                'flex flex-row items-center justify-start md:text-left group p-3 px-4 rounded-xl border transition-all duration-300 hover:translate-x-1 active:scale-95 gap-4 md:gap-0',
                                activeHoverIndex === getVisibleIndex('wishlist') ? 'active-stat-card' : 'inactive-stat-card'
                            ]" @mouseenter="activeHoverIndex = getVisibleIndex('wishlist')"
                            @mouseleave="activeHoverIndex = null"
                            @touchstart="activeHoverIndex = getVisibleIndex('wishlist')"
                            @touchend="activeHoverIndex = null">
                            <span
                                :class="['text-xl font-bold md:mr-2 transition-colors duration-300 min-w-[2rem] md:min-w-0 md:inline block stat-number', activeHoverIndex === getVisibleIndex('wishlist') ? 'text-gsblanco' : '']">
                                {{ statsData.wishlist }}
                            </span>
                            <span
                                :class="['text-xs uppercase tracking-wider font-semibold transition-colors duration-300 text-left stat-label', activeHoverIndex === getVisibleIndex('wishlist') ? '' : 'text-gsgris group-hover:text-gsblanco']">
                                Wishlist
                            </span>
                        </router-link>

                        <router-link v-if="!profile.user.library.is_private || isOwnProfile"
                            :to="`/completed/${profile.user.wishlist.id}`" :class="[
                                'flex flex-row items-center justify-start md:text-left group p-3 px-4 rounded-xl border transition-all duration-300 hover:translate-x-1 active:scale-95 gap-4 md:gap-0',
                                activeHoverIndex === getVisibleIndex('completed') ? 'active-stat-card' : 'inactive-stat-card'
                            ]" @mouseenter="activeHoverIndex = getVisibleIndex('completed')"
                            @mouseleave="activeHoverIndex = null"
                            @touchstart="activeHoverIndex = getVisibleIndex('completed')"
                            @touchend="activeHoverIndex = null">
                            <span
                                :class="['text-xl font-bold md:mr-2 transition-colors duration-300 min-w-[2rem] md:min-w-0 md:inline block stat-number', activeHoverIndex === getVisibleIndex('completed') ? 'text-gsblanco' : '']">
                                {{ statsData.completed }}
                            </span>
                            <span
                                :class="['text-xs uppercase tracking-wider font-semibold transition-colors duration-300 text-left stat-label', activeHoverIndex === getVisibleIndex('completed') ? '' : 'text-gsgris group-hover:text-gsblanco']">
                                Completed
                            </span>
                        </router-link>
                    </div>

                    <div class="flex flex-col items-center justify-center order-2 md:order-3 shrink-0">
                        <h3 class="hidden md:block text-[10px] uppercase tracking-[0.2em] font-bold mb-4"
                            :style="{ color: userColor }">
                            Stats chart
                        </h3>

                        <div :class="[
                            'relative w-64 h-64 md:flex items-center justify-center transition-all duration-300 overflow-hidden',
                            showRadarMobile ? 'flex' : 'hidden'
                        ]">
                            <svg v-if="visibleStats.length >= 3" viewBox="0 0 200 200"
                                class="w-full h-full overflow-visible">
                                <polygon v-for="i in 4" :key="i" :points="getRadarPoints(i * 25)"
                                    class="fill-none stroke-gsgris/20 stroke-1" />

                                <line v-for="(point, index) in axisLines" :key="index" x1="100" y1="100" :x2="point.x"
                                    :y2="point.y" :class="[
                                        'transition-colors duration-300',
                                        activeHoverIndex === index ? 'stroke-1.5' : 'stroke-gsgris/20 stroke-1 stroke-dashed'
                                    ]" :style="activeHoverIndex === index ? { stroke: `${userColor}66` } : {}" />

                                <polygon :points="radarDataPoints" class="stroke-2 transition-all duration-500 ease-out"
                                    :style="{ fill: `${userColor}26`, stroke: userColor }" />

                                <circle v-for="(circle, index) in activeCircles" :key="'c-' + index" :cx="circle.x"
                                    :cy="circle.y" :r="activeHoverIndex === index ? 6 : 4"
                                    :class="['transition-all duration-300 ease-out stroke-2', activeHoverIndex === index ? 'fill-gsblanco' : 'fill-gsoscuro']"
                                    :style="{ stroke: userColor }" />

                                <circle v-for="(circle, index) in activeCircles" :key="'h-' + index" :cx="circle.x"
                                    :cy="circle.y" r="16" class="fill-transparent cursor-pointer"
                                    @mousemove="handleTooltipMove($event, index)" @mouseleave="handleTooltipHide" />
                            </svg>
                            <div v-else class="text-xs text-gsgris text-center px-4">
                                Not enough public data to display chart
                            </div>
                        </div>
                    </div>

                </div>
            </div>

            <div v-if="tooltip.visible && activeHoverIndex !== null"
                class="absolute pointer-events-none z-30 px-3 py-1.5 rounded-xl border bg-gsoscuro/90 backdrop-blur-md shadow-2xl flex flex-col items-center min-w-[90px] transition-all duration-75 ease-out -translate-x-1/2 -translate-y-full"
                :style="{ top: `${tooltip.y - 12}px`, left: `${tooltip.x}px`, borderColor: `${userColor}4d` }">
                <span class="text-[10px] uppercase font-bold text-gsgris tracking-wider leading-none mb-0.5">
                    {{ getStatLabelByIndex(activeHoverIndex) }}
                </span>
                <span class="text-sm font-black leading-none" :style="{ color: userColor }">
                    {{ getStatValueByIndex(activeHoverIndex) }}
                </span>
                <div class="absolute bottom-0 left-1/2 -translate-x-1/2 translate-y-full w-0 h-0 border-x-4 border-x-transparent border-t-4"
                    :style="{ 'border-top-color': `${userColor}4d` }">
                </div>
            </div>
        </section>

        <main class="max-w-5xl mx-auto px-6 mt-12">
            <section class="mb-12 md:hidden">
                <h3 class="text-xs uppercase tracking-[0.2em] font-bold mb-3" :style="{ color: userColor }">Biography
                </h3>
                <div class="bg-gsoscuro p-5 rounded-2xl border shadow-2xl relative overflow-hidden group"
                    :style="{ borderColor: `${userColor}1a` }">
                    <div class="absolute top-0 left-0 w-full h-[2px]"
                        :style="{ backgroundImage: `linear-gradient(to right, ${userColor}, transparent, transparent)` }">
                    </div>
                    <p class="text-gsblanco/80 leading-relaxed text-sm whitespace-pre-line">
                        {{ profile?.bio || defaultBio }}
                    </p>
                </div>
            </section>

            <div class="flex justify-between items-center mb-8">
                <h2 class="text-2xl font-bold border-l-4 pl-4" :style="{ borderColor: userColor }">Favorites</h2>
                <router-link :to="`/favorites/${profile?.user.id}`"
                    class="text-sm font-medium transition-colors opacity-90 hover:opacity-100"
                    :style="{ color: userColor }">
                    View all →
                </router-link>
            </div>

            <div class="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-4 gap-6">
                <template v-if="profile && limitedFavorites.length > 0">
                    <div v-for="game in limitedFavorites" :key="game.id"
                        class="group cursor-pointer flex flex-col bg-[#161a21] rounded-xl border border-gsgris/20 transition-all duration-300 shadow-lg dynamic-card">
                        <GameCard :game="game.game" />
                    </div>
                </template>
                <div v-else class="col-span-full flex justify-center items-center">
                    <img alt="no recent games" src="@/assets/Empty-cuate.svg" class="w-sm" />
                </div>
            </div>
        </main>
    </div>
</template>

<script setup lang="ts">
import { computed, onMounted, ref, watch } from 'vue';
import { useRoute } from 'vue-router'
import type { Profile } from '@/types/profileTypes';
import { useAuthStore } from '@/stores/authStore';
import Navbar from '@/components/Navbar.vue';
import Badge from '@/components/Badge.vue';
import GameCard from '@/components/GameCard.vue';
import api from "@/api/client";

const authStore = useAuthStore()
const profile = ref<Profile | null>(null);
const loading = ref(true)
const showSuccessMessage = ref(false)

const activeHoverIndex = ref<number | null>(null)
const showRadarMobile = ref(false)
const tooltip = ref({
    visible: false,
    x: 0,
    y: 0
})

const route = useRoute()
const defaultBio = 'This collector has not yet written their story... But their shelf speaks for itself!'

// Propiedad computada centralizada para extraer el color del usuario de forma segura
const userColor = computed(() => {
    return profile.value?.color_bg || '#79a998';
});

const isOwnProfile = computed(() => {
    if (!route.params.id) {
        return true
    }
    return authStore.isOwnProfile(
        Number(route.params.id)
    )
})

watch(
    () => route.params.id,
    fetchProfile,
    { immediate: true }
)

onMounted(() => {
    if (route.query.updated === 'true') {
        showSuccessMessage.value = true

        window.history.replaceState(
            {},
            '',
            route.path
        )

        setTimeout(() => {
            showSuccessMessage.value = false
        }, 3000)
    }
})

async function fetchProfile() {
    loading.value = true;
    try {
        profile.value = route.params.id
            ? (await api.get(`/api/users/${route.params.id}/`)).data
            : (await api.get('/api/users/me/')).data;
    } catch (error: unknown) {
        console.error(error);
    } finally {
        loading.value = false;
    }
}

const fullName = computed(() => {
    const first = profile.value?.user.first_name?.trim()
    const last = profile.value?.user.last_name?.trim()

    if (!first && !last) return 'noname'
    return `${first || ''} ${last || ''}`.trim()
})

const completed = computed(() => {
    if (!profile.value?.user.library.items) return 0
    return profile.value.user.library.items.filter(item => item.status === "Completed").length
})

const limitedFavorites = computed(() => {
    return profile.value?.user.favorites?.slice(0, 4) || []
})

const statsData = computed(() => {
    return {
        collections: profile.value?.user.collections?.length ?? 0,
        library: profile.value?.user.library.items?.length ?? 0,
        favorites: profile.value?.user.favorites?.length ?? 0,
        wishlist: profile.value?.user.wishlist.items?.length ?? 0,
        completed: completed.value
    };
});

const visibleStats = computed(() => {
    if (!profile.value) return [];

    const list = [
        { key: 'collections', label: 'Collections', value: statsData.value.collections },
        { key: 'library', label: 'Library', value: statsData.value.library, isPrivate: profile.value.user.library.is_private },
        { key: 'favorites', label: 'Favorites', value: statsData.value.favorites },
        { key: 'wishlist', label: 'Wishlist', value: statsData.value.wishlist, isPrivate: profile.value.user.wishlist.is_private },
        { key: 'completed', label: 'Completed', value: statsData.value.completed, isPrivate: profile.value.user.library.is_private }
    ];

    return list.filter(stat => !stat.isPrivate || isOwnProfile.value);
});

const getVisibleIndex = (key: string): number | null => {
    const idx = visibleStats.value.findIndex(s => s.key === key);
    return idx !== -1 ? idx : null;
};

const handleTooltipMove = (event: MouseEvent, index: number) => {
    activeHoverIndex.value = index

    const target = event.currentTarget as SVGElement;
    const section = target.closest('section');

    if (section) {
        const bounds = section.getBoundingClientRect();
        tooltip.value.x = event.clientX - bounds.left;
        tooltip.value.y = event.clientY - bounds.top;
        tooltip.value.visible = true;
    }
}

const handleTooltipHide = () => {
    activeHoverIndex.value = null
    tooltip.value.visible = false
}

const getStatLabelByIndex = (index: number): string => {
    return visibleStats.value[index]?.label || '';
};

const getStatValueByIndex = (index: number): number => {
    return visibleStats.value[index]?.value ?? 0;
};

const CENTER = 100;
const MAX_RADIUS = 80;

const maxStatValue = computed(() => {
    if (visibleStats.value.length === 0) return 1;
    const max = Math.max(...visibleStats.value.map(s => s.value));
    return max === 0 ? 1 : max;
});

const valueToXY = (value: number, max: number, index: number) => {
    const totalSides = visibleStats.value.length;
    const radius = (value / max) * MAX_RADIUS;
    const angle = (Math.PI * 2 / totalSides) * index - Math.PI / 2;
    return {
        x: CENTER + radius * Math.cos(angle),
        y: CENTER + radius * Math.sin(angle)
    };
};

const getRadarPoints = (radiusPercent: number) => {
    const totalSides = visibleStats.value.length;
    let points = [];
    for (let i = 0; i < totalSides; i++) {
        const angle = (Math.PI * 2 / totalSides) * i - Math.PI / 2;
        const radius = (radiusPercent / 100) * MAX_RADIUS;
        points.push(`${CENTER + radius * Math.cos(angle)},${CENTER + radius * Math.sin(angle)}`);
    }
    return points.join(' ');
};

const axisLines = computed(() => {
    const totalSides = visibleStats.value.length;
    return Array.from({ length: totalSides }).map((_, i) => {
        const angle = (Math.PI * 2 / totalSides) * i - Math.PI / 2;
        return {
            x: CENTER + MAX_RADIUS * Math.cos(angle),
            y: CENTER + MAX_RADIUS * Math.sin(angle)
        };
    });
});

const activeCircles = computed(() => {
    return visibleStats.value.map((stat, i) => valueToXY(stat.value, maxStatValue.value, i));
});

const radarDataPoints = computed(() => {
    return activeCircles.value.map(p => `${p.x},${p.y}`).join(' ');
});
</script>

<style scoped>

.dynamic-btn {
    border-color: calc(var(--user-color) + '4d');
    /* Fallback / Opacidad controlada abajo */
    border-color: var(--user-color);
    background-color: color-mix(in srgb, var(--user-color) 10%, transparent);
    color: var(--user-color);
}

.dynamic-btn:hover {
    background-color: var(--user-color);
    color: #0b0e14;
    /* Color oscuro gsoscuro */
    box-shadow: 0 0 20px color-mix(in srgb, var(--user-color) 40%, transparent);
}

.dynamic-btn-mobile {
    border-color: var(--user-color);
    background-color: color-mix(in srgb, var(--user-color) 10%, transparent);
    color: var(--user-color);
}

.dynamic-btn-mobile:active {
    background-color: var(--user-color);
    color: #0b0e14;
}

/* Tarjetas de estadísticas inactivas */
.inactive-stat-card {
    border-color: rgba(156, 163, 175, 0.1);
    background-color: rgba(11, 14, 20, 0.3);
}

.inactive-stat-card:hover {
    border-color: color-mix(in srgb, var(--user-color) 20%, transparent);
    background-color: color-mix(in srgb, var(--user-color) 5%, transparent);
}

.inactive-stat-card .stat-number {
    color: var(--user-color);
}

/* Tarjetas de estadísticas activas (Hover/Focus) */
.active-stat-card {
    border-color: color-mix(in srgb, var(--user-color) 30%, transparent);
    background-color: color-mix(in srgb, var(--user-color) 10%, transparent);
    box-shadow: 0 0 15px color-mix(in srgb, var(--user-color) 15%, transparent);
}

.active-stat-card .stat-number {
    text-shadow: 0 0 10px rgba(255, 255, 255, 0.6);
}

.active-stat-card .stat-label {
    color: var(--user-color);
}

/* Hover de las GameCards en favoritos */
.dynamic-card:hover {
    border-color: color-mix(in srgb, var(--user-color) 50%, transparent);
}

/* TOAST ANIMATIONS */
.toast-modern-enter-active,
.toast-modern-leave-active {
    transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
}

.toast-modern-enter-from {
    opacity: 0;
    transform: translateY(-20px) scale(0.95);
}

.toast-modern-leave-to {
    opacity: 0;
    transform: translateY(10px) scale(0.95);
}

@keyframes progress {
    from {
        width: 100%;
    }

    to {
        width: 0%;
    }
}

.progress-bar {
    animation: progress 3s linear forwards;
}
</style>