<template>
    <div class="h-screen flex flex-col bg-[#0b0e14]"> 
        <div class="flex-shrink-0 sticky top-0 z-50">
            <Navbar/>
        </div>
            <section ref="scrollContainer" class="flex-1 overflow-y-auto p-6 sm:p-8 text-gsblanco relative">            
                <div class="max-w-[1600px] mx-auto">
                <div class="mb-8 flex items-center justify-between text-gsmenta">
                    <h2 class="text-2xl font-semibold border-l-4 border-gsmenta/50 pl-4">
                        Catálogo de Juegos
                    </h2>
                </div>
            </div>
        </section>
    </div>
</template>

<script setup lang="ts">
import Navbar from '@/components/Navbar.vue';



</script>

<style scoped>

</style>