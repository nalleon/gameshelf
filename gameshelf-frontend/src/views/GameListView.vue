<template>
    <Navbar/>
    <div class="mt-10 grid grid-cols-5 grid-rows-3 gap-4 gap-y-20 justify-items-center">
        <div class="bg-gray-50 w-50 h-80" v-for="game in games">
            {{ game }}
        </div>
    </div>
</template>

<script setup lang="ts">
import Navbar from '@/components/Navbar.vue';

const games = ['Juan', 'Pedro', 'Ana', 'game 4', 'game 5', 'game 6']

</script>

<style scoped>
    
</style>