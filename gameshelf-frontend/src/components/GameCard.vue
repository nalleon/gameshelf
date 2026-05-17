<template>
    <router-link :to="`/games/${props.game.id}`" 
        class="group relative flex flex-col h-full bg-[#11151d] border border-white/5 hover:border-gsmenta/40 rounded-xl overflow-hidden transition-all duration-300 hover:shadow-[0_0_20px_rgba(0,255,163,0.15)]">
        
        <div class="absolute top-0 left-0 w-full h-[2px] bg-gradient-to-r from-transparent via-gsmenta/20 to-transparent group-hover:via-gsmenta group-hover:shadow-[0_0_8px_#00ffa3] transition-all duration-500 z-20"></div>

        <div class="relative aspect-[3/4] overflow-hidden bg-[#1a1f29] flex items-center justify-center">
            
            <div class="absolute inset-0 bg-gradient-to-t from-[#11151d]/50 via-transparent to-transparent opacity-60 z-10"></div>

            <img :src="game.cover_default || tbaCover" :alt="game.title"
                class="w-full h-full object-cover scale-101 group-hover:scale-105 transition-transform duration-700 ease-out">

            <div v-if="platformIcon"
                class="absolute top-3 left-3 bg-gsoscuro/85 backdrop-blur-md text-gsmenta p-2 rounded-lg border border-gsmenta/40 shadow-[0_0_10px_rgba(0,255,163,0.1)] z-20 font-mono tracking-widest">
                <Icon :icon="platformIcon" class="text-lg" />
            </div>

            <div
                class="absolute top-3 right-3 w-9 h-9 bg-gsoscuro/80 backdrop-blur-md rounded-lg border border-white/10 group-hover:border-gsmenta/30 shadow flex items-center justify-center z-20 transition-colors duration-300">
                <span v-if="['eu', 'us', 'nz', 'jp', 'cn', 'kr', 'br'].includes(region)" :class="`fi fi-${region}`"
                    class="text-md brightness-90 group-hover:brightness-110 transition-all" />

                <i v-else-if="region === 'world'" class="pi pi-globe text-sm text-gsgris group-hover:text-gsmenta transition-colors" />

                <i v-else-if="region === 'asia'" class="pi pi-compass text-sm text-gsgris group-hover:text-gsmenta transition-colors" />

                <i v-else class="pi pi-exclamation-triangle text-sm text-amber-400 drop-shadow-[0_0_5px_rgba(245,158,11,0.5)]" />
            </div>
        </div>

        <div class="p-4 flex flex-col flex-grow relative bg-[#121620]/60 backdrop-blur-xs">
            
            <div class="absolute bottom-0 right-0 w-2 h-2 bg-white/5 group-hover:bg-gsmenta/20 transition-colors clip-corner"></div>

            <h3 class="font-bold text-sm sm:text-base tracking-wide line-clamp-1 text-gsblanco group-hover:text-gsmenta transition-colors duration-300">
                {{ game.title }}
            </h3>

            <p class="font-mono text-[10px] uppercase tracking-widest text-gsgris/70 group-hover:text-gsgris mt-1.5 flex items-center gap-1.5 transition-colors">
                <span class="w-1 h-1 rounded-full bg-gsmenta/40 group-hover:bg-gsmenta animate-pulse"></span>
                {{ game.released_at || 'TBA_DATA' }}
            </p>
        </div>
    </router-link>
</template>

<style scoped>
/* Detalle estético para cortar la esquina inferior derecha */
.clip-corner {
    clip-path: polygon(100% 0, 0 100%, 100% 100%);
}
</style>

<script setup lang="ts">
import { computed } from 'vue'
import { Icon } from '@iconify/vue'
import tbaCover from '@/assets/TBA.png';
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


<style scoped>
.clip-corner {
    clip-path: polygon(100% 0, 0 100%, 100% 100%);
}
</style>