<template>
    <Navbar />
    <div class="pt-20">
        <div class="bg-gsoscuro p-10 rounded-lg text-gsblanco mx-auto max-w-md">
            <!-- REGISTER -->
            <form class="text-center" @submit.prevent="submitRegister">
                <h2 class="text-3xl font-bold mb-10">Register</h2>
                <input class="border rounded-md px-3 py-2 mb-4" v-model="username" placeholder="Username">
                <p :class="isHiddenUsernameError" class="text-red-400 text-sm">{{ usernameError }}</p>
                <br>
                <input class="border rounded-md px-3 py-2 mb-4" v-model="email" type="email" placeholder="Email">
                <p :class="isHiddenEmailError" class="text-red-400 text-sm">{{ emailError }}</p>
                <br>
                <input class="border rounded-md px-3 py-2 mb-4" v-model="password" type="password" placeholder="Password">
                <p :class="isHiddenPasswordError" class="text-red-400 text-sm">{{ passwordError }}</p>
                <br>
                <p>
                    <router-link to="/login">Login</router-link>
                </p>
                <br>
                <button class="bg-gsmenta rounded-md text-gsblanco py-2 px-4 hover:cursor-pointer" type="submit">Register</button>
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
const email = ref('')
const password = ref('')

const requiredFieldMessage = "Este campo es obligatorio";
const usernameError = ref('')
const emailError = ref('')
const passwordError = ref('')

const isHiddenUsernameError = ref('invisible')
const isHiddenEmailError = ref('invisible')
const isHiddenPasswordError = ref('invisible')


async function apiRegister(){
    const webhookUrl = 'http://127.0.0.1:8000/api/auth/register/'
    const payload = {
        username: username.value,
        email: email.value,
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
    email.value = "";
    password.value = "";

    return data;
}

function submitRegister() {

    isHiddenUsernameError.value = "invisible"
    isHiddenEmailError.value = "invisible"
    isHiddenPasswordError.value = "invisible"

    if (username.value === "") {
        usernameError.value = requiredFieldMessage
        isHiddenUsernameError.value = "visible"
        return
    }

    if (email.value === "") {
        emailError.value = requiredFieldMessage
        isHiddenEmailError.value = "visible"
        return
    }

    if (password.value === "") {
        passwordError.value = requiredFieldMessage
        isHiddenPasswordError.value = "visible"
        return
    }

    apiRegister().then((data) => {
        auth.login(username.value, data.token)
        router.replace('/gamelist')
    })
}
</script>

<style scoped>

</style>