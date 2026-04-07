<template>
    <Navbar/>
    <div class="mt-10 grid grid-cols-5 grid-rows-3 gap-4 gap-y-20 justify-items-center">
        <div class="bg-gray-50 w-50 h-80" v-for="game in games">
            <p class="text-gs-claro">{{ game.title }}</p>
        </div>
    </div>
</template>

<script setup lang="ts">
import Navbar from '@/components/Navbar.vue';
import { onMounted, ref } from 'vue';
import type { Game } from '@/types/generalTypes';


let games = ref<Game[]>([])

onMounted(async () => {
    try {
        const webhookUrl = 'http://127.0.0.1:8000/api/games/'

        const response = await fetch(webhookUrl, 
            {
                method: "GET",
                headers: {
                    'Content-Type': 'application/json'
                }    
            }
        );

        const data = await response.json();
        games.value = data;
        console.log(data)
    } catch (err) {
        console.error(err);
    }
});


</script>

<style scoped>
    
</style>