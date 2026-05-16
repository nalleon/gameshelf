<template>
    <router-link :to="`/games/${props.game.id}`">
        <div class="relative aspect-[3/4] rounded-t-xl overflow-hidden">
            <img :src="game.cover_default" :alt="game.title"
                class="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500">

            <!-- Platform Icon -->
            <div v-if="platformIcon"
                class="absolute top-2 left-2 bg-gsoscuro/80 backdrop-blur-sm text-gsmenta p-1.5 rounded border border-gsmenta/30 shadow-lg z-10">
                <Icon :icon="platformIcon" class="text-xl" />
            </div>

            <!-- Region -->
            <div
                class="absolute top-2 right-2 w-9 h-9 bg-gsoscuro/70 backdrop-blur-sm rounded border border-gsmenta/20 shadow flex items-center justify-center">
                <!-- FLAGS -->
                <span v-if="['eu', 'us', 'nz', 'jp', 'cn', 'kr', 'br'].includes(region)" :class="`fi fi-${region}`"
                    class="text-lg" />

                <!-- PRIME ICONS fallback -->
                <i v-else-if="region === 'world'" class="pi pi-globe text-base" />

                <i v-else-if="region === 'asia'" class="pi pi-compass text-base" />

                <i v-else class="pi pi-exclamation-triangle text-base text-yellow-400" />
            </div>
        </div>

        <div class="p-4 flex flex-col flex-grow">
            <h3 class="font-bold text-base line-clamp-1 group-hover:text-gsmenta transition-colors">
                {{ game.title }}
            </h3>

            <p class="text-gsgris text-xs mt-1 mb-4 italic leading-tight">
                {{ game.released_at }}
            </p>
        </div>
    </router-link>
</template>
<script setup lang="ts">
import { computed } from 'vue'
import { Icon } from '@iconify/vue'

import { PLATFORM_MAP } from '@/constants/app'
import type { Game } from '@/types/gameListTypes'
import type { Platform } from '@/types/profileTypes'

interface Props {
    game: Game
    platform?: Platform
}

const props = defineProps<Props>()

const platformIcon = computed(() => {
    const slug = props.platform?.slug
    if (!slug) return null

    return PLATFORM_MAP[slug] || 'mdi:gamepad-variant'
})

const region = computed(() => {
    const regionMaps: Record<string, string> = {
        europe: 'eu',
        north_america: 'us',
        new_zeland: 'nz',
        japan: 'jp',
        china: 'cn',
        korea: 'kr',
        brazil: 'br',

        asia: 'asia',
        worldwide: 'world',

        to_be_add: 'warning',
    }

    return regionMaps[props.game?.region?.name] || 'warning'
})
</script>