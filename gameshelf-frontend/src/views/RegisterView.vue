<template>
    <Navbar />
    <div class="pt-20">
        <div class="bg-gsoscuro p-10 rounded-lg text-gsblanco mx-auto max-w-md">
            <!-- REGISTER -->
            <form class="text-center">
                <h2 class="text-3xl font-bold mb-10">Register</h2>
                <input class="border rounded-md px-3 py-2 mb-8" type="email" placeholder="Email">
                <br>
                <input class="border rounded-md px-3 py-2 mb-8" type="email" placeholder="Email">
                <br>
                <input class="border rounded-md px-3 py-2 mb-8" type="password" placeholder="Contraseña">
                <br>
                <p>
                    <router-link to="/login">Login</router-link>
                </p>
                <br>
                <button class="bg-gsmenta rounded-md text-gsblanco py-2 px-4 ">Entrar</button>
            </form>
        </div>
    </div>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import { useAuthStore } from '@/stores/authStore'

import Navbar from '@/components/Navbar.vue';
import router from '@/router';


const auth = useAuthStore()
const username = ref('')
const password = ref('')

const requiredFieldMessage = "Este campo es obligatorio";
const usernameError = ref('')
const passwordError = ref('')
const isHiddenUsernameError = ref('invisible')
const isHiddenPasswordError = ref('invisible')


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
    
    console.log(data.token)
    username.value = "";
    password.value = "";

    return data;
}

function submitLogin() {

    isHiddenUsernameError.value = "invisible"
    isHiddenPasswordError.value = "invisible"

    if (username.value === "") {
        usernameError.value = requiredFieldMessage
        isHiddenUsernameError.value = "visible"
        return
    }

    if (password.value === "") {
        passwordError.value = requiredFieldMessage
        isHiddenPasswordError.value = "visible"
        return
    }

    apiLogin().then((data) => {
        auth.login(username.value, data.token)
    })

    router.replace('/')
}
</script>

<style scoped>

</style>