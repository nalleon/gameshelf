<template>
    <Navbar />

    <div class="pt-20 h-[92.5vh] bg-gsoscuro/55 flex justify-center items-start px-4">
        <!-- Tarjeta Principal -->
        <div
            class="bg-gsoscuro p-10 rounded-2xl text-gsblanco mx-auto max-w-md w-full shadow-2xl border border-gsmenta/10 relative overflow-hidden">

            <!-- Detalle estético superior -->
            <div class="absolute top-0 left-0 w-full h-1 bg-linear-to-r from-gsmenta to-gsbosque"></div>

            <!-- FORMULARIO LOGIN -->
            <form class="flex flex-col text-center" @submit.prevent="submitLogin">
                <h2 class="text-4xl font-extrabold mb-2 tracking-tight">Welcome</h2>
                <p class="text-gsgris text-sm mb-10 font-medium uppercase tracking-widest">Log in to your account</p>

                <!-- Campo Username/Email -->
                <div class="mb-6 text-left">
                    <label class="text-xs font-bold text-gsmenta uppercase ml-1">Username or Email</label>
                    <input v-model="loginField"
                        class="w-full bg-[#1a1e26] border border-gsgris/30 rounded-xl px-4 py-3 mt-1 focus:outline-none focus:border-gsmenta focus:ring-1 focus:ring-gsmenta/50 transition-all placeholder-gsgris/40"
                        placeholder="collector01">
                    <!-- Error Login Field -->
                    <p :class="isHiddenLoginFieldError" class="text-red-400 text-xs mt-2 ml-1 italic">
                        {{ loginFieldError }}
                    </p>
                </div>

                <!-- Campo Password -->
                <div class="mb-4 text-left">
                    <label class="text-xs font-bold text-gsmenta uppercase ml-1">Password</label>
                    <input v-model="password" type="password"
                        class="w-full bg-[#1a1e26] border border-gsgris/30 rounded-xl px-4 py-3 mt-1 focus:outline-none focus:border-gsmenta focus:ring-1 focus:ring-gsmenta/50 transition-all placeholder-gsgris/40"
                        placeholder="••••••••">
                    <!-- Error Password -->
                    <p :class="isHiddenPasswordError" class="text-red-400 text-xs mt-2 ml-1 italic">
                        {{ passwordError }}
                    </p>
                </div>

                <!-- Links de navegación -->
                <div class="flex justify-between items-center mt-2 mb-8 px-1">
                    <router-link to="/register"
                        class="text-sm text-gsgris hover:text-gsblanco transition-colors underline-offset-4 hover:underline">
                        Don't have an account? Register
                    </router-link>
                </div>

                <!-- Botón Submit -->
                <button type="submit"
                    class="bg-gsmenta hover:bg-gsbosque text-gsoscuro font-bold py-3.5 px-6 rounded-full transition-all transform hover:scale-[1.02] active:scale-95 shadow-lg cursor-pointer uppercase tracking-wider text-sm">
                    Login
                </button>
            </form>
        </div>
    </div>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import { useAuthStore } from '@/stores/authStore'
import axios from 'axios';
import { jwtDecode } from 'jwt-decode'

import Navbar from '@/components/Navbar.vue';
import router from '@/router';

import api from "@/api/client"


const auth = useAuthStore()
const loginField = ref('')
const password = ref('')

const requiredFieldMessage = "Este campo es obligatorio";
const loginFieldError = ref('')
const passwordError = ref('')
const isHiddenLoginFieldError = ref('invisible')
const isHiddenPasswordError = ref('invisible')


async function apiLogin() {
    const payload = {
        login: loginField.value,
        password: password.value
    }

    try {
        const response = await api.post('/api/auth/login/', payload);

        const data = response.data;

        loginField.value = "";
        password.value = "";

        return data;
    } catch (error: any) {
        if (error.response) {
            console.error("Error en login:", error.response.data);
        } else {
            console.error("Error de red o configuración:", error.message);
        }
        return null;
    }
}

function submitLogin() {

    isHiddenLoginFieldError.value = "invisible"
    isHiddenPasswordError.value = "invisible"

    if (loginField.value === "") {
        loginFieldError.value = requiredFieldMessage
        isHiddenLoginFieldError.value = "visible"
        return
    }

    if (password.value === "") {
        passwordError.value = requiredFieldMessage
        isHiddenPasswordError.value = "visible"
        return
    }

    apiLogin().then((data) => {
        auth.setUserSesion(data.token)
        router.replace('/profile')
    })
}

</script>

<style scoped></style>