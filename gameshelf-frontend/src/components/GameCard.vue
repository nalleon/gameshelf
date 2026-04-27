<template>
    <router-link :to="`/game-list/detail/${props.game.slug}`">
        <!-- Contenedor de Imagen -->
        <div class="relative aspect-[3/4] rounded-t-xl overflow-hidden">
            <img :src="game.cover_default" :alt="game.title" class="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500">
            <!-- Badge de Plataforma -->
            <div class="absolute top-2 left-2 bg-gsoscuro/80 backdrop-blur-sm text-gsmenta text-[10px] font-bold px-2 py-0.5 rounded border border-gsmenta/30 uppercase">
                {{ platform}}
            </div>
            <div class="absolute top-2 left-2 bg-gsoscuro/80 backdrop-blur-sm text-gsmenta text-[15px] font-bold px-2 py-0.5 rounded border border-gsmenta/30 uppercase text-xl">
                {{ region }}
            </div>
        </div>

        <!-- Información del Juego -->
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
import type { Game } from '@/types/gameListTypes';
import type { Platform } from '@/types/profileTypes';
import { computed } from 'vue';

interface Props {
    game: Game,
    platform?: Platform
}

const props = defineProps<Props>()

const platform = computed(()=> {
    switch (props.platform?.name) {
        case "pc-microsoft-windows":
            return `<img :src="" class="h-[15px]">` 
    }
});

const region = computed(()=> {
    switch (props.game.region.name) {
        case "to_be_add":
            return '⚠️'
        case "europe":
            return '🇪🇺'
        case "north_america":
            return '🇺🇸'
        case "new_zeland":
            return '🇳🇿'
        case "japan":
            return '🇯🇵'
        case "china":
            return '🇨🇳'
        case "asia":
            return '🌏'
        case "worldwide":
            return '🌐'
        case "korea":
            return '🇰🇷'
        case "brazil":
            return '🇧🇷'
        default:             
            return '⚠️'

    }
});

</script>
