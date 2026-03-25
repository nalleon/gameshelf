<template>
    <Navbar />
    <div class="contenedor pt-20">
        <div class="bg-gsoscuro p-10 rounded-lg text-gsblanco mx-auto max-w-md">
            <!-- REGISTER -->
            <form class="text-center">
                <h2 class="text-3xl font-bold mb-10">Register</h2>
                <input class="border rounded-md px-3 py-2 mb-8" type="email" placeholder="Email">
                <br>
                <input class="border rounded-md px-3 py-2 mb-8" type="password" placeholder="Contraseña">
                <br>
                <p><router-link to="/login">Login</router-link></p>
                <br>
                <button class="bg-gsmenta rounded-md text-gsblanco py-2 px-4 ">Entrar</button>
            </form>
        </div>
    </div>
</template>

<script setup lang="ts">
import Navbar from '@/components/Navbar.vue';


</script>

<style scoped>
    .contenedor {
        height: 90vh; /* ocupa toda la pantalla */
        background-image: url("../assets/background.jpg");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
    }
</style>