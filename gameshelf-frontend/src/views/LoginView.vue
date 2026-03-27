<template>
    <Navbar />
    <div class="pt-20">
        <div class="bg-gsoscuro p-10 rounded-lg text-gsblanco mx-auto max-w-md">
            <!-- LOGIN -->
            <form class="text-center" @submit.prevent="submitLogin">
                <h2 class="text-3xl font-bold mb-10">Login</h2>
                <input class="border rounded-md px-3 py-2 mb-8" v-model="username" placeholder="Nombre de Usuario">
                <br>
                <input class="border rounded-md px-3 py-2 mb-8" v-model="password" type="password" placeholder="Contraseña">
                <br>
                <p>
                    <router-link to="/register">Register</router-link>
                </p>
                <br>
                <button class="bg-gsmenta rounded-md text-gsblanco py-2 px-4" type="submit">Entrar</button>
            </form>
        </div>
    </div>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import { useAuthStore } from '@/stores/authStore'

import Navbar from '@/components/Navbar.vue';


const auth = useAuthStore()
const username = ref('')
const password = ref('')

async function apiLogin(){
    const webhookUrl = 'http://127.0.0.1:8000/api/auth/login/'
    const payload = {
        login: username.value,
        password: password.value
    }

    const response = await fetch(webhookUrl, 
        {
            method: "POST",
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(payload)
        }
    );
    const data = await response.json();
    
    console.log(data)
}

function submitLogin() {

    apiLogin();

    // const fakeUser = { id: 1, name: 'Juan', email: email.value }
    // const fakeToken = 'abc123'
    // auth.login(fakeUser, fakeToken)
}
</script>

<style scoped>
    
</style>