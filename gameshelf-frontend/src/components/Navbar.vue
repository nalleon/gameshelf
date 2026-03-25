<template>
    <header class="sticky top-0 z-50 backdrop-blur border-b bg-gsoscuro">
        <div class="px-6 py-4 flex items-center text-gsblanco justify-between">
            <!-- IZQUIERDA -->
            <div class="border">
                <router-link to="/">
                    <img class="w-15" src="../assets/cover-logo-cut.png" alt="Logo">
                </router-link>
            </div>
            <!-- DERECHA (ESCRITORIO) -->
            <nav class="hidden sm:flex gap-6 items-center text-sm">
                <span>
                    <input class="border rounded-md px-2 py-1" type="text" placeholder="Search...">
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