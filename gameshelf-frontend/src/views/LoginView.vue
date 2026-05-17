<template>
    <Navbar />
    <div class="min-h-[calc(100vh-80px)] pt-20 pb-12 bg-gsoscuro/55 flex flex-col justify-center items-center px-4">
        <div class="bg-gsoscuro p-10 rounded-2xl text-gsblanco mx-auto max-w-md w-full shadow-2xl border border-gsmenta/10 relative overflow-hidden">
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

            <div
                class="bg-gsoscuro p-8 rounded-2xl border border-white/10 w-full max-w-md text-gsblanco relative shadow-2xl">
                <div class="absolute top-0 left-0 w-full h-1 bg-linear-to-r from-gsmenta to-gsbosque"></div>

                <div class="flex items-center justify-between mb-6">
                    <div>
                        <h3 class="text-lg font-bold text-gsmenta uppercase tracking-wider">Reset Password</h3>
                        <p class="text-xs text-gsgris mt-1">
                            <span v-if="resetStep === 'email'">We will send a recovery code to your email</span>
                            <span v-else-if="resetStep === 'code'">Verify your identity with the code sent</span>
                            <span v-else-if="resetStep === 'new-password'">Secure your shelf with a new password</span>
                            <span v-else-if="resetStep === 'success'">Everything is ready to roll</span>
                        </p>
                    </div>
                    <button @click="closeResetModal"
                        class="w-8 h-8 rounded-full bg-white/5 hover:bg-red-500/20 text-gsgris hover:text-red-400 transition-all flex items-center justify-center border border-white/5 cursor-pointer">
                        <i class="pi pi-times text-xs"></i>
                    </button>
                </div>

                <div v-if="resetError"
                    class="bg-red-500/10 border border-red-500/30 text-red-400 rounded-xl p-3 text-xs mb-4 italic">
                    <i class="pi pi-exclamation-circle mr-1"></i> {{ resetError }}
                </div>

                <form v-if="resetStep === 'email'" @submit.prevent="submitPasswordReset" class="space-y-5">
                    <div>
                        <label class="block text-xs font-bold text-gsgris uppercase mb-2 ml-1">Email Address</label>
                        <input v-model="resetEmail" type="email" required placeholder="your-email@example.com"
                            class="w-full bg-[#1a1e26] border border-white/10 rounded-xl px-4 py-3 text-sm text-gsblanco placeholder-gsgris/40 focus:outline-none focus:border-gsmenta transition-all"
                            :disabled="resetLoading" />
                    </div>
                    <div class="flex items-center justify-end gap-3 pt-2">
                        <button type="button" @click="closeResetModal"
                            class="border border-white/10 hover:bg-white/5 text-gsgris px-5 py-2.5 rounded-full text-xs font-bold uppercase cursor-pointer">Cancel</button>
                        <button type="submit" :disabled="resetLoading"
                            class="bg-gsmenta text-gsoscuro px-6 py-2.5 rounded-full text-xs font-black uppercase transition-all shadow-md active:scale-95 flex items-center cursor-pointer disabled:opacity-50">
                            <i v-if="resetLoading" class="pi pi-spin pi-spinner mr-2 text-xs"></i>
                            <span>Send Code</span>
                        </button>
                    </div>
                </form>

                <form v-else-if="resetStep === 'code'" @submit.prevent="submitValidateCode" class="space-y-5">
                    <div>
                        <label class="block text-xs font-bold text-gsgris uppercase mb-2 ml-1 text-center">Verification
                            Code</label>
                        <input v-model="verificationCode" type="text" maxlength="10" required placeholder="000000"
                            @keydown.space.prevent
                            @input="handleCodeInput"
                            class="w-full bg-[#1a1e26] border border-white/10 rounded-xl px-4 py-3 text-center uppercase text-xl tracking-[0.5em] font-mono text-gsblanco focus:outline-none focus:border-gsmenta transition-all"
                            :disabled="resetLoading" />
                    </div>
                    <div class="flex items-center justify-end gap-3 pt-2">
                        <button type="button" @click="resetStep = 'email'"
                            class="border border-white/10 hover:bg-white/5 text-gsgris px-5 py-2.5 rounded-full text-xs font-bold uppercase cursor-pointer">Back</button>
                        <button type="submit" :disabled="resetLoading || verificationCode.length < 4"
                            class="bg-gsmenta text-gsoscuro px-6 py-2.5 rounded-full text-xs font-black uppercase transition-all shadow-md active:scale-95 flex items-center cursor-pointer disabled:opacity-50">
                            <i v-if="resetLoading" class="pi pi-spin pi-spinner mr-2 text-xs"></i>
                            <span>Validate</span>
                        </button>
                    </div>
                </form>

                <form v-else-if="resetStep === 'new-password'" @submit.prevent="submitChangePassword" class="space-y-5">
                    <div class="space-y-4">
                        <div>
                            <label class="block text-xs font-bold text-gsgris uppercase mb-1 ml-1">New Password</label>
                            <input v-model="newPassword" type="password" required placeholder="••••••••"
                                class="w-full bg-[#1a1e26] border border-white/10 rounded-xl px-4 py-3 text-sm text-gsblanco focus:outline-none focus:border-gsmenta transition-all"
                                :disabled="resetLoading" />
                        </div>
                        <div>
                            <label class="block text-xs font-bold text-gsgris uppercase mb-1 ml-1">Confirm New
                                Password</label>
                            <input v-model="confirmNewPassword" type="password" required placeholder="••••••••"
                                class="w-full bg-[#1a1e26] border border-white/10 rounded-xl px-4 py-3 text-sm text-gsblanco focus:outline-none focus:border-gsmenta transition-all"
                                :disabled="resetLoading" />
                        </div>
                    </div>
                    <div class="flex items-center justify-end gap-3 pt-2">
                        <button type="submit" :disabled="resetLoading"
                            class="w-full bg-gsmenta text-gsoscuro py-3 rounded-full text-xs font-black uppercase transition-all shadow-md active:scale-95 flex items-center justify-center cursor-pointer disabled:opacity-50">
                            <i v-if="resetLoading" class="pi pi-spin pi-spinner mr-2 text-xs"></i>
                            <span>Update Password</span>
                        </button>
                    </div>
                </form>

                <div v-else-if="resetStep === 'success'" class="space-y-6 text-center py-4">
                    <div
                        class="w-16 h-16 bg-gsmenta/10 text-gsmenta border border-gsmenta/20 rounded-full flex items-center justify-center mx-auto text-2xl">
                        <i class="pi pi-check"></i>
                    </div>
                    <p class="text-sm text-gsgris leading-relaxed px-2">
                        Your account password has been successfully updated. You can now use your new credentials to
                        enter your dashboard.
                    </p>
                    <button @click="closeResetModal"
                        class="w-full bg-white/5 border border-white/10 hover:bg-white/10 text-gsblanco py-3 rounded-full text-xs font-bold uppercase cursor-pointer transition-colors">
                        Got it, back to Login
                    </button>
                </div>

            </div>
        </div>
    </Transition>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import { useAuthStore } from '@/stores/authStore'
import Navbar from '@/components/Navbar.vue';
import router from '@/router';
import api from "@/api/client"

const auth = useAuthStore()
const loginField = ref('')
const password = ref('')

const requiredFieldMessage = "This field is required";
const loginFieldError = ref('')
const passwordError = ref('')
const globalError = ref('')

const isHiddenLoginFieldError = ref('hidden')
const isHiddenPasswordError = ref('hidden')
const isHiddenGlobalError = ref('hidden')

// --- FLUJO MULTIPASO DEL RECOVERY MODAL ---
type ResetStep = 'email' | 'code' | 'new-password' | 'success';
const showResetModal = ref(false)
const resetStep = ref<ResetStep>('email')
const resetLoading = ref(false)
const resetError = ref('')

// Campos del formulario secuencial
const resetEmail = ref('')
const verificationCode = ref('')
const newPassword = ref('')
const confirmNewPassword = ref('')

function openResetModal() {
    resetStep.value = 'email'
    resetEmail.value = ''
    verificationCode.value = ''
    newPassword.value = ''
    confirmNewPassword.value = ''
    resetError.value = ''
    resetLoading.value = false
    showResetModal.value = true
}

function closeResetModal() {
    showResetModal.value = false
}

// FILTRADO DINÁMICO DE ESPACIOS
function handleCodeInput(event: Event) {
    const target = event.target as HTMLInputElement;
    verificationCode.value = target.value.replace(/\s+/g, '');
}

// 1. Enviar Email para solicitar Código
async function submitPasswordReset() {
    resetError.value = ''
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
    if (!resetEmail.value.trim() || !emailRegex.test(resetEmail.value)) {
        resetError.value = "Please enter a valid email address."
        return
    }

    resetLoading.value = true
    try {
        await api.post('/api/auth/password-reset/', {
            email: resetEmail.value.trim()
        })
        resetStep.value = 'code'
    } catch (error: any) {
        resetError.value =
            error.response?.data?.message ||
            "This email address is not registered or could not be processed."
    } finally {
        resetLoading.value = false
    }
}

// 2. Validar Código Temporal recibido por Correo
async function submitValidateCode() {
    resetError.value = ''
    resetLoading.value = true
    try {
        await api.post('/api/auth/password-reset/validate/', {
            token: verificationCode.value.trim().toUpperCase()
        })
        resetStep.value = 'new-password'
    } catch (error: any) {
        resetError.value =
            error.response?.data?.error ||
            "The verification code is invalid or has expired."
    } finally {
        resetLoading.value = false
    }
}

async function submitChangePassword() {
    resetError.value = ''

    if (newPassword.value === "") {
        resetError.value = "Password is required."
        return
    }

    const passwordRegex =
        /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*()_+\-=\[\]{};':"\\|,.<>\/?~`]).{8,}$/

    if (!passwordRegex.test(newPassword.value)) {
        resetError.value =
            "Password must be at least 8 characters long and include uppercase, lowercase, numbers, and a special character."
        return
    }

    if (newPassword.value !== confirmNewPassword.value) {
        resetError.value = "Passwords do not match."
        return
    }

    resetLoading.value = true

    try {
        await api.post('/api/auth/change-password/', {
            token: verificationCode.value.trim().toUpperCase(),
            new_password: newPassword.value
        })

        resetStep.value = 'success'

    } catch (error: any) {
        resetError.value =
            error.response?.data?.error ||
            "Unable to change password. Please try again."

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
    return response.data;
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
            globalError.value = "Invalid username or password."
        } else {
            globalError.value =
                "Connection error. Please try again later."
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