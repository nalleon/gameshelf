<template>
    <header class="sticky top-0 z-50 backdrop-blur border-b">
        <div class="max-w-4xl mx-auto px-6 py-4 flex items-center justify-between">
            <!-- IZQUIERDA -->
            <p class="font-semibold">
                <router-link to="/">Pedro Martín Escuela</router-link>
            </p>
            <!-- DERECHA (ESCRITORIO) -->
            <nav class="hidden sm:flex gap-6 text-sm">
                <span class="hover:text-white">
                    <router-link to="/">Home</router-link>
                </span>
                <span class="hover:text-white">
                    <router-link to="/gamelist">Game List</router-link>
                </span>
                <span class="hover:text-white">
                    <router-link to="/profile">Profile</router-link>
                </span>
            </nav>
        </div>
    </header>
</template>

<script setup lang="ts">
    import {ref} from 'vue'

    const isOpen = ref(false)

    function closeMenu() {
        isOpen.value = false
    }
</script>

<style scoped>

</style>