<template>
    <header class="sticky top-0 z-50 backdrop-blur border-b bg-gsoscuro">
        <div class="px-6 py-4 flex items-center text-gsblanco justify-between">
            <!-- IZQUIERDA -->
            <div class="border rounded-md">
                <router-link to="/">
                    <img class="w-15 rounded-md" src="../assets/cover-logo-cut.png" alt="Logo">
                </router-link>
            </div>
            <!-- DERECHA (ESCRITORIO) -->
            <nav class="hidden sm:flex gap-6 items-center text-sm">
                <span class="">
                    <input class="border rounded-md px-2 py-1" type="text" placeholder="Search...">
                </span>

                <span v-if="auth.isLogged" class="hover:text-white">
                    <router-link to="/profile">Profile</router-link>
                </span>
                <span v-if="auth.isLogged" class="hover:text-white hover:cursor-pointer">
                    <li @click="handleLogout">Logout</li>
                </span>
                <span v-else class="mx-5 py-1 px-5 bg-gsmenta border border-gsmenta rounded-lg">
                    <router-link to="/login">Login</router-link>
                </span>
            </nav>
        </div>
    </header>
</template>

<script setup lang="ts">
    import {ref} from 'vue'
    import { useAuthStore } from '@/stores/authStore'

    // const isOpen = ref(false)

    // function closeMenu() {
    //     isOpen.value = false
    // }

    const auth = useAuthStore()

    function handleLogout() {
        auth.logout()
    }

</script>

<style scoped>

</style>