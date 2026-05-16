<template>
    <Navbar />

    <div class="min-h-screen pt-20 pb-12 bg-gsoscuro/55 flex flex-col justify-center items-center px-4">
        <div
            class="bg-gsoscuro p-10 rounded-2xl text-gsblanco mx-auto max-w-md w-full shadow-2xl border border-gsmenta/10 relative overflow-hidden">

            <div class="absolute top-0 left-0 w-full h-1 bg-linear-to-r from-gsmenta to-gsbosque"></div>

            <form class="flex flex-col text-center" @submit.prevent="submitLogin">
                <h2 class="text-4xl font-extrabold mb-2 tracking-tight">Welcome</h2>
                <p class="text-gsgris text-sm mb-10 font-medium uppercase tracking-widest">Log in to your account</p>

                <div class="mb-6 text-left">
                    <label class="text-xs font-bold text-gsmenta uppercase ml-1">Username or Email</label>
                    <input v-model="loginField"
                        class="w-full bg-[#1a1e26] border border-gsgris/30 rounded-xl px-4 py-3 mt-1 focus:outline-none focus:border-gsmenta focus:ring-1 focus:ring-gsmenta/50 transition-all placeholder-gsgris/40"
                        placeholder="collector01">
                    <p :class="isHiddenLoginFieldError" class="text-red-400 text-xs mt-2 ml-1 italic">
                        {{ loginFieldError }}
                    </p>
                </div>

                <div class="mb-4 text-left">
                    <label class="text-xs font-bold text-gsmenta uppercase ml-1">Password</label>
                    <input v-model="password" type="password"
                        class="w-full bg-[#1a1e26] border border-gsgris/30 rounded-xl px-4 py-3 mt-1 focus:outline-none focus:border-gsmenta focus:ring-1 focus:ring-gsmenta/50 transition-all placeholder-gsgris/40"
                        placeholder="••••••••">
                    <p :class="isHiddenPasswordError" class="text-red-400 text-xs mt-2 ml-1 italic">
                        {{ passwordError }}
                    </p>
                </div>

                <div class="flex flex-col items-center gap-3 mt-2 mb-8 px-1">
                    <router-link to="/register"
                        class="text-sm text-gsgris hover:text-gsblanco transition-colors underline-offset-4 hover:underline">
                        Don't have an account? Register
                    </router-link>

                    <button type="button" @click="openResetModal"
                        class="text-sm text-gsgris hover:text-gsmenta transition-colors underline-offset-4 hover:underline cursor-pointer">
                        Forgot password?
                    </button>
                </div>

                <p :class="isHiddenGlobalError" class="text-red-400 text-sm mb-4 text-center font-semibold italic">
                    {{ globalError }}
                </p>

                <button type="submit"
                    class="bg-gsmenta hover:bg-gsbosque text-gsoscuro font-bold py-3.5 px-6 rounded-full transition-all transform hover:scale-[1.02] active:scale-95 shadow-lg cursor-pointer uppercase tracking-wider text-sm">
                    Login
                </button>
            </form>
        </div>
    </div>

    <Transition name="fade">
        <div v-if="showResetModal" 
            class="fixed inset-0 z-50 flex items-center justify-center bg-black/75 backdrop-blur-xs p-4"
            @click.self="closeResetModal">
            
            <div class="bg-gsoscuro p-8 rounded-2xl border border-white/10 w-full max-w-md text-gsblanco relative shadow-2xl">
                <div class="absolute top-0 left-0 w-full h-1 bg-linear-to-r from-gsmenta to-gsbosque"></div>

                <div class="flex items-center justify-between mb-6">
                    <div>
                        <h3 class="text-lg font-bold text-gsmenta uppercase tracking-wider">Reset Password</h3>
                        <p class="text-xs text-gsgris mt-1">We will send a recovery link to your email</p>
                    </div>
                    <button @click="closeResetModal" class="w-8 h-8 rounded-full bg-white/5 hover:bg-red-500/20 text-gsgris hover:text-red-400 transition-all flex items-center justify-center border border-white/5 cursor-pointer">
                        <i class="pi pi-times text-xs"></i>
                    </button>
                </div>

                <div v-if="resetSuccess" class="bg-gsmenta/10 border border-gsmenta/30 rounded-xl p-4 mb-6 text-center text-sm text-gsmenta">
                    <i class="pi pi-check-circle mr-2"></i> {{ resetStatusMessage }}
                </div>

                <form v-else @submit.prevent="submitPasswordReset" class="space-y-5">
                    <div>
                        <label class="block text-xs font-bold text-gsgris uppercase mb-2 ml-1">Email Address</label>
                        <input v-model="resetEmail" type="email" required
                            placeholder="your-email@example.com"
                            class="w-full bg-[#1a1e26] border border-white/10 rounded-xl px-4 py-3 text-sm text-gsblanco placeholder-gsgris/40 focus:outline-none focus:border-gsmenta focus:ring-4 focus:ring-gsmenta/10 transition-all duration-200"
                            :disabled="resetLoading" />
                        
                        <p v-if="resetError" class="text-red-400 text-xs mt-2 ml-1 italic">
                            {{ resetError }}
                        </p>
                    </div>

                    <div class="flex items-center justify-end gap-3 pt-2">
                        <button type="button" @click="closeResetModal" :disabled="resetLoading"
                            class="border-2 border-white/10 hover:border-white/20 bg-white/5 text-gsgris hover:text-gsblanco px-5 py-2.5 rounded-full text-xs font-bold uppercase tracking-wider transition-all duration-300 active:scale-95 cursor-pointer disabled:opacity-50">
                            Cancel
                        </button>
                        
                        <button type="submit" :disabled="resetLoading"
                            class="border-2 border-gsmenta/30 hover:border-gsmenta bg-gsmenta/5 hover:bg-gsmenta text-gsblanco hover:text-gsoscuro px-6 py-2.5 rounded-full text-xs font-black uppercase tracking-wider transition-all duration-300 shadow-md shadow-gsmenta/5 hover:shadow-lg hover:shadow-gsmenta/20 active:scale-95 flex items-center justify-center min-w-[120px] cursor-pointer disabled:opacity-50">
                            <i v-if="resetLoading" class="pi pi-spin pi-spinner mr-2 text-xs"></i>
                            <span>{{ resetLoading ? 'Sending...' : 'Send Link' }}</span>
                        </button>
                    </div>
                </form>

                <div v-if="resetSuccess" class="flex justify-end mt-4">
                    <button @click="closeResetModal"
                        class="bg-white/5 border border-white/10 hover:bg-white/10 text-gsblanco px-6 py-2.5 rounded-full text-xs font-bold uppercase tracking-wider transition-all cursor-pointer">
                        Close
                    </button>
                </div>
            </div>
        </div>
    </Transition>
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
const globalError = ref('') 

const isHiddenLoginFieldError = ref('hidden')
const isHiddenPasswordError = ref('hidden')
const isHiddenGlobalError = ref('hidden') 

// --- ESTADOS PARA EL MODAL DE RECUPERACIÓN ---
const showResetModal = ref(false)
const resetEmail = ref('')
const resetLoading = ref(false)
const resetError = ref('')
const resetSuccess = ref(false)
const resetStatusMessage = ref('')

function openResetModal() {
    resetEmail.value = ''
    resetError.value = ''
    resetSuccess.value = false
    resetLoading.value = false
    showResetModal.value = true
}

function closeResetModal() {
    showResetModal.value = false
}

async function submitPasswordReset() {
    resetError.value = ''
    
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
    if (!resetEmail.value.trim() || !emailRegex.test(resetEmail.value)) {
        resetError.value = "Por favor, introduce un correo electrónico válido."
        return
    }

    resetLoading.value = true
    try {
        const response = await api.post('/api/auth/password-reset/', {
            email: resetEmail.value.trim()
        })

        resetSuccess.value = true
        resetStatusMessage.value = response.data?.message || "Si el correo está registrado, recibirás un enlace de recuperación pronto."
    } catch (error: any) {
        console.error(error)
        if (error.response && error.response.data && error.response.data.message) {
            resetError.value = error.response.data.message
        } else if (error.response && error.response.status === 404) {
            resetError.value = "Este correo electrónico no está registrado en el sistema."
        } else {
            resetError.value = "Hubo un problema al procesar tu solicitud. Inténtalo de nuevo."
        }
    } finally {
        resetLoading.value = false
    }
}

// --- LOGICA DE LOGIN EXISTENTE ---
async function apiLogin() {
    const payload = {
        login: loginField.value,
        password: password.value
    }

    const response = await api.post('/api/auth/login/', payload);
    const data = response.data;

    loginField.value = "";
    password.value = "";

    return data;
}

async function submitLogin() {
    isHiddenLoginFieldError.value = "hidden"
    isHiddenPasswordError.value = "hidden"
    isHiddenGlobalError.value = "hidden"

    if (loginField.value === "") {
        loginFieldError.value = requiredFieldMessage
        isHiddenLoginFieldError.value = "inline"
        return
    }

    if (password.value === "") {
        passwordError.value = requiredFieldMessage
        isHiddenPasswordError.value = "inline"
        return
    }

    try {
        const data = await apiLogin();
        
        if (data && data.token) {
            auth.setUserSesion(data.token)
            router.replace('/profile')
        }
    } catch (error: any) {
        if (error.response && (error.response.status === 401 || error.response.status === 400)) {
            globalError.value = "El usuario o la contraseña no son correctos.";
        } else {
            globalError.value = "Error de conexión. Por favor, inténtalo más tarde.";
        }
        isHiddenGlobalError.value = "inline"
        password.value = "" 
    }
}
</script>

<style scoped>
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.25s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>