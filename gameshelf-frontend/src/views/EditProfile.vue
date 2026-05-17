<template>
    <Navbar />
    <div class="min-h-screen bg-gsoscuro text-gsblanco font-sans pb-20 transition-all duration-300"
        :style="{ '--user-color': editForm.color_bg }">
        <header class="relative bg-[#1a1e26] border-b border-gsgris/10">
            <div class="h-32 md:h-40 transition-colors duration-500" :style="{ backgroundColor: editForm.color_bg }" />
            <div class="max-w-4xl mx-auto px-6">
                <div
                    class="flex flex-col md:flex-row items-center md:items-end -mt-14 md:-mt-16 gap-4 md:gap-6 pb-6 text-center md:text-left">
                    <div class="relative group cursor-pointer shrink-0">
                        <div class="w-28 h-28 md:w-32 md:h-32 rounded-full bg-gsoscuro border-4 overflow-hidden shadow-xl"
                            :style="{ borderColor: editForm.color_bg }">
                            <img :src="avatarPreview ?? profile?.avatar"
                                class="w-full h-full object-cover transition-all group-hover:opacity-80 bg-gsoscuro" />
                            <div
                                class="absolute inset-0 flex items-center justify-center bg-gsoscuro/40 group-hover:bg-gsoscuro/60 transition-all rounded-full">
                                <svg xmlns="http://www.w3.org/2000/svg" class="h-8 w-8 dynamic-text" fill="none"
                                    viewBox="0 0 24 24" stroke="currentColor">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                        d="M3 9a2 2 0 012-2h.93a2 2 0 001.664-.89l.812-1.22A2 2 0 0110.07 4h3.86a2 2 0 011.664.89l.812 1.22A2 2 0 0018.07 7H19a2 2 0 012 2v9a2 2 0 01-2 2H5a2 2 0 01-2-2V9z" />
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                        d="M15 13a3 3 0 11-6 0 3 3 0 016 0z" />
                                </svg>
                            </div>
                        </div>
                        <input type="file" @change="handleAvatarChange"
                            class="absolute inset-0 opacity-0 cursor-pointer" ref="fileInputRef" accept="image/*" />
                    </div>
                    <div class="mb-2 w-full min-w-0">
                        <h1 class="text-2xl font-bold text-gsblanco">Edit Profile</h1>
                        <p class="text-gsgris text-sm truncate">Personalize your identity on the platform</p>
                    </div>
                </div>
            </div>
        </header>

        <main class="max-w-4xl mx-auto px-6 mt-10">
            <div v-if="errorMessage"
                class="mb-6 p-4 bg-red-500/10 border border-red-500/30 text-red-400 rounded-xl text-sm">
                {{ errorMessage }}
            </div>

            <div v-if="successMessage"
                class="mb-6 p-4 bg-emerald-500/10 border border-emerald-500/30 text-emerald-400 rounded-xl text-sm">
                {{ successMessage }}
            </div>

            <div v-if="profile && !profile.verified"
                class="mb-8 bg-[#1a1e26] p-4 rounded-2xl border border-amber-500/20 flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
                <div>
                    <p class="font-semibold text-amber-400 flex items-center gap-2 text-sm sm:text-base">
                        <i class="pi pi-exclamation-triangle"></i> Account not verified
                    </p>
                    <p class="text-xs text-gsgris mt-0.5">Verify your email to unlock custom visual styles and extra
                        community functions.</p>
                </div>
                <button type="button" @click="requestEmailVerification" :disabled="loadingVerify"
                    class="w-full sm:w-auto px-4 py-2 rounded-full font-bold text-xs bg-amber-500 text-gsoscuro hover:bg-amber-400 active:scale-95 transition-all shrink-0 cursor-pointer disabled:opacity-50">
                    {{ loadingVerify ? 'Sending...' : 'Verify Email' }}
                </button>
            </div>

            <form @submit.prevent="saveProfile" class="space-y-8">

                <section class="grid grid-cols-1 sm:grid-cols-2 gap-6">
                    <div class="col-span-full">
                        <h3 class="text-xs uppercase tracking-[0.2em] font-bold mb-1 dynamic-text">Personal Information
                        </h3>
                    </div>

                    <div class="space-y-2">
                        <label class="text-sm text-gsgris ml-1">First Name</label>
                        <input v-model="editForm.first_name" type="text"
                            class="w-full bg-[#161a21] border border-gsgris/20 rounded-xl px-4 py-3 focus:outline-none transition-colors dynamic-input"
                            placeholder="Your first name">
                    </div>

                    <div class="space-y-2">
                        <label class="text-sm text-gsgris ml-1">Last Name</label>
                        <input v-model="editForm.last_name" type="text"
                            class="w-full bg-[#161a21] border border-gsgris/20 rounded-xl px-4 py-3 focus:outline-none transition-colors dynamic-input"
                            placeholder="Your last name">
                    </div>

                    <div class="col-span-full space-y-2">
                        <label class="text-sm text-gsgris ml-1">Biography</label>
                        <textarea v-model="editForm.bio" rows="4"
                            class="w-full bg-[#161a21] border border-gsgris/20 rounded-xl px-4 py-3 focus:outline-none transition-colors resize-none dynamic-input"
                            placeholder="Tell us about your gaming tastes..."></textarea>
                    </div>
                </section>

                <section>
                    <h3 class="text-xs uppercase tracking-[0.2em] font-bold mb-3 dynamic-text">Visual Style</h3>

                    <p v-if="!profile?.verified" class="text-xs text-red-400 mb-3 font-medium italic">
                        You have to verify your account to use this function
                    </p>

                    <div class="bg-[#1a1e26] p-4 sm:p-6 rounded-2xl border border-gsgris/10 flex flex-col sm:flex-row gap-4 sm:items-center justify-between transition-all"
                        :class="{ 'opacity-50 select-none': !profile?.verified }">
                        <div>
                            <p class="font-medium">Banner Color</p>
                            <p class="text-xs text-gsgris">This color will be displayed on your profile header.</p>
                        </div>

                        <div class="flex items-center gap-3 self-start sm:self-center"
                            :class="{ 'pointer-events-none': !profile?.verified }">
                            <input type="color" v-model="editForm.color_bg" :disabled="!profile?.verified"
                                class="w-12 h-12 rounded-lg bg-transparent border-none cursor-pointer disabled:cursor-not-allowed">
                            <span class="text-sm font-mono text-gsgris uppercase">{{ editForm.color_bg }}</span>
                        </div>
                    </div>
                </section>

                <section>
                    <h3 class="text-xs uppercase tracking-[0.2em] font-bold mb-4 dynamic-text">Privacy</h3>
                    <div class="bg-[#1a1e26] p-4 rounded-2xl border border-gsgris/10 space-y-4">

                        <div class="flex items-center justify-between p-2 gap-4">
                            <div class="min-w-0">
                                <p class="font-medium text-gsblanco">Private Library</p>
                                <p class="text-xs text-gsgris break-words">Hide your game list and play status.</p>
                            </div>
                            <label class="relative inline-flex items-center cursor-pointer shrink-0">
                                <input type="checkbox" v-model="editForm.library_private" class="sr-only peer">
                                <div
                                    class="w-11 h-6 bg-gsgris/20 peer-focus:outline-none rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all dynamic-switch">
                                </div>
                            </label>
                        </div>

                        <hr class="border-gsgris/10">

                        <div class="flex items-center justify-between p-2 gap-4">
                            <div class="min-w-0">
                                <p class="font-medium text-gsblanco">Private Wishlist</p>
                                <p class="text-xs text-gsgris break-words">Nobody will see the games you want to buy.
                                </p>
                            </div>
                            <label class="relative inline-flex items-center cursor-pointer shrink-0">
                                <input type="checkbox" v-model="editForm.wishlist_private" class="sr-only peer">
                                <div
                                    class="w-11 h-6 bg-gsgris/20 peer-focus:outline-none rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all dynamic-switch">
                                </div>
                            </label>
                        </div>

                        <hr class="border-gsgris/10">

                        <div class="flex items-center justify-between p-2 gap-4">
                            <div class="min-w-0">
                                <p class="font-medium text-gsblanco">Private Collections</p>
                                <p class="text-xs text-gsgris break-words mb-1">Affects all your custom collections.</p>
                                <p class="text-[11px] text-red-400 font-medium italic leading-none">All your collections
                                    will be set on private</p>
                            </div>
                            <label class="relative inline-flex items-center cursor-pointer shrink-0">
                                <input type="checkbox" v-model="editForm.collections_private" class="sr-only peer">
                                <div
                                    class="w-11 h-6 bg-gsgris/20 peer-focus:outline-none rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all dynamic-switch">
                                </div>
                            </label>
                        </div>
                    </div>
                </section>

                <section>
                    <h3 class="text-xs uppercase tracking-[0.2em] text-red-400 font-bold mb-4">Account Management</h3>
                    <div
                        class="bg-red-500/5 p-4 rounded-2xl border border-red-500/10 flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
                        <div>
                            <p class="font-medium text-gsblanco text-sm sm:text-base">Deactivate account</p>
                            <p class="text-xs text-gsgris mt-0.5">Temporarily hide your profile. You can recover
                                everything whenever you want.</p>
                        </div>
                        <button type="button" @click="showDeactivateModal = true"
                            class="w-full sm:w-auto px-5 py-2.5 rounded-xl border border-red-500/30 text-red-400 font-semibold text-xs hover:bg-red-500/10 active:scale-95 transition-all text-center shrink-0 cursor-pointer">
                            Deactivate Account
                        </button>
                    </div>
                </section>

                <div class="flex flex-col-reverse sm:flex-row gap-4 pt-6 border-t border-gsgris/10">
                    <button type="button" @click="$router.push('/profile')"
                        class="w-full sm:w-auto px-8 py-4 border border-gsgris/30 text-gsgris font-semibold rounded-full hover:bg-gsgris/10 transition-all text-center cursor-pointer">
                        Cancel
                    </button>
                    <button type="submit"
                        class="flex-1 font-bold py-4 rounded-full transition-all transform hover:scale-[1.005] active:scale-95 shadow-lg dynamic-btn-submit cursor-pointer">
                        Save Changes
                    </button>
                </div>

            </form>
        </main>
    </div>

    <div v-if="showCropper"
        class="fixed inset-0 bg-black/80 flex items-center justify-center z-50 px-4 py-6 overflow-y-auto">
        <div
            class="relative w-full max-w-xl bg-gsoscuro text-gsblanco rounded-2xl shadow-2xl border border-white/10 overflow-hidden my-auto">
            <div class="absolute top-0 left-0 w-full h-1" :style="{ backgroundColor: editForm.color_bg }"></div>
            <div class="p-4 sm:p-6">
                <h2 class="text-center text-lg font-semibold mb-4">Adjust your profile picture</h2>
                <div class="flex justify-center max-w-full">
                    <Cropper ref="cropperRef" :src="rawImage" class="w-full h-64 sm:h-80 rounded-xl overflow-hidden"
                        :stencil-component="CircleStencil" :stencil-props="{ aspectRatio: 1 }" />
                </div>
                <div class="flex justify-between items-center mt-6">
                    <button class="text-gsgris hover:text-gsblanco transition-colors cursor-pointer"
                        @click="showCropper = false">Cancel</button>
                    <button :style="{ backgroundColor: editForm.color_bg }"
                        class="px-6 py-2.5 rounded-full font-bold text-[#0b0e14] hover:brightness-110 active:scale-95 transition-all shadow-lg shadow-black/20 cursor-pointer"
                        @click="getCroppedImage">
                        Apply
                    </button>
                </div>
            </div>
        </div>
    </div>

    <div v-if="showVerifyModal" class="fixed inset-0 bg-black/80 flex items-center justify-center z-50 px-4">
        <div
            class="relative w-full max-w-md bg-gsoscuro text-gsblanco rounded-2xl shadow-2xl border border-white/10 overflow-hidden">
            <div class="absolute top-0 left-0 w-full h-1 bg-amber-500"></div>
            <div class="p-6">
                <h3 class="text-xl font-bold mb-2 flex items-center gap-2">
                    <i class="pi pi-envelope text-amber-500"></i> Enter Verification Code
                </h3>
                <p class="text-xs text-gsgris mb-4">We have sent a digital code to your email address. Please insert it
                    below to complete security checks.</p>

                <div class="space-y-2 mb-6">
                    <input v-model="verificationCode" type="text" maxlength="10"
                        class="w-full bg-[#161a21] border border-gsgris/20 rounded-xl px-4 py-3 text-center text-xl uppercase tracking-[0.5em] font-mono focus:outline-none focus:border-amber-500 transition-colors"
                        placeholder="000000">
                </div>

                <div class="flex justify-end gap-3">
                    <button @click="showVerifyModal = false"
                        class="px-4 py-2 text-sm text-gsgris hover:text-gsblanco cursor-pointer">
                        Cancel
                    </button>
                    <button @click="confirmEmailVerification"
                        :disabled="loadingVerifySubmit || verificationCode.length < 4"
                        class="px-5 py-2 rounded-xl bg-amber-500 hover:bg-amber-400 text-gsoscuro text-sm font-bold transition-all disabled:opacity-50 cursor-pointer">
                        {{ loadingVerifySubmit ? 'Verifying...' : 'Confirm Code' }}
                    </button>
                </div>
            </div>
        </div>
    </div>

    <div v-if="showDeactivateModal" class="fixed inset-0 bg-black/80 flex items-center justify-center z-50 px-4">
        <div
            class="relative w-full max-w-md bg-gsoscuro text-gsblanco rounded-2xl shadow-2xl border border-red-500/20 overflow-hidden">
            <div class="absolute top-0 left-0 w-full h-1 bg-red-500"></div>
            <div class="p-6">
                <h3 class="text-xl font-bold text-red-400 mb-2 flex items-center gap-2">
                    <i class="pi pi-trash"></i> Deactivate your account?
                </h3>
                <p class="text-sm text-gsgris mb-4 leading-relaxed">
                    Your profile, custom lists, and gaming status will be hidden from public view.
                </p>
                <div class="bg-red-500/5 border border-red-500/10 rounded-xl p-3 mb-6 text-xs text-red-300">
                    <i class="pi pi-info-circle mr-1"></i> <b>Don't worry.</b> Your shelf layout and data are preserved
                    securely. You can easily restore everything and reactivate your profile whenever you want to rejoin
                    **Gameshelf**.
                </div>

                <div class="flex flex-col sm:flex-row justify-end gap-3">
                    <button @click="showDeactivateModal = false"
                        class="w-full sm:w-auto px-4 py-2 text-sm text-gsgris hover:text-gsblanco text-center order-2 sm:order-1 cursor-pointer">
                        Nevermind
                    </button>
                    <button @click="deactivateAccount" :disabled="loadingDeactivate"
                        class="w-full sm:w-auto px-5 py-2.5 rounded-full bg-red-500 hover:bg-red-600 text-gsblanco text-sm font-bold transition-all order-1 sm:order-2 disabled:opacity-50 cursor-pointer">
                        {{ loadingDeactivate ? 'Processing...' : 'Yes, deactivate' }}
                    </button>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { useAuthStore } from '@/stores/authStore';
import Navbar from '@/components/Navbar.vue';
import type { Profile } from '@/types/profileTypes';
import { Cropper, CircleStencil } from 'vue-advanced-cropper';
import 'vue-advanced-cropper/dist/style.css';
import api from "@/api/client";
import { useUiStore } from '@/stores/uiStore';

const router = useRouter();
const auth = useAuthStore();
const uiStore = useUiStore();

const profile = ref<Profile | null>(null);
const avatarPreview = ref<string | null>(null);
const showCropper = ref(false);
const rawImage = ref<string | null>(null);
const avatarFile = ref<File | null>(null);
const cropperRef = ref();
const fileInputRef = ref<HTMLInputElement | null>(null);

// Variables de Mensajes Globales
const errorMessage = ref<string | null>(null);
const successMessage = ref<string | null>(null);

// Controladores de Verificación de Email
const showVerifyModal = ref(false);
const verificationCode = ref('');
const loadingVerify = ref(false);
const loadingVerifySubmit = ref(false);

// Controladores de Desactivación de Cuenta
const showDeactivateModal = ref(false);
const loadingDeactivate = ref(false);

const editForm = ref({
    first_name: '',
    last_name: '',
    bio: '',
    color_bg: '#79a998',
    library_private: false,
    wishlist_private: false,
    collections_private: false
});

onMounted(async () => {
    await fetchProfileData();
});

async function fetchProfileData() {
    try {
        const data = await apiProfileMe();
        profile.value = data;

        editForm.value = {
            first_name: data.user.first_name || '',
            last_name: data.user.last_name || '',
            bio: data.bio || '',
            color_bg: data.color_bg || '#79a998',
            library_private: data.user.library?.is_private ?? false,
            wishlist_private: data.user.wishlist?.is_private ?? false,
            collections_private: false
        };
    } catch (err) {
        console.error("Error loading profile:", err);
    }
}

async function apiProfileMe() {
    const response = await api.get('/api/users/me/');
    return response.data;
}

function handleLogout() {
    auth.removeUserSesion()
    router.replace('/login')
}

// 1. SOLICITAR CÓDIGO DE VERIFICACIÓN (POST inicial)
async function requestEmailVerification() {
    errorMessage.value = null;
    successMessage.value = null;
    loadingVerify.value = true;
    try {
        // Ejecuta el envío de código
        await api.post('/api/auth/verify-email/');
        verificationCode.value = '';
        showVerifyModal.value = true;
    } catch (error: any) {
        errorMessage.value = error.response?.data?.error || "Could not trigger verification mail process.";
    } finally {
        loadingVerify.value = false;
    }
}

// 2. ENVIAR EL CÓDIGO INTRODUCIDO POR EL USUARIO
async function confirmEmailVerification() {
    errorMessage.value = null;
    successMessage.value = null;
    loadingVerifySubmit.value = true;

    
    try {
        await api.post('/api/auth/verify-email/validate/', { token: verificationCode.value.toUpperCase() });
        showVerifyModal.value = false;
        successMessage.value = "Your account has been successfully verified! Enjoy visual customization.";

        await fetchProfileData();
    } catch (error: any) {
        errorMessage.value = error.response?.data?.error || "Invalid security code provided.";
    } finally {
        loadingVerifySubmit.value = false;
    }
}

// 3. DESACTIVACIÓN DE CUENTA
async function deactivateAccount() {
    errorMessage.value = null;
    loadingDeactivate.value = true;
    try {
        await api.post('/api/auth/deactivate/');
        showDeactivateModal.value = false;

        // Si tienes una función logout centralizada en tu authStore, ejecútala aquí
        handleLogout

        // Redirigir fuera de la aplicación protegida
        router.push('/login');
    } catch (error: any) {
        showDeactivateModal.value = false;
        errorMessage.value = error.response?.data?.error || "An error occurred during account deactivation.";
    } finally {
        loadingDeactivate.value = false;
    }
}

async function saveProfile() {
    if (!profile.value) return;
    errorMessage.value = null;
    successMessage.value = null;

    const formData = new FormData();
    formData.append('first_name', editForm.value.first_name);
    formData.append('last_name', editForm.value.last_name);
    formData.append('bio', editForm.value.bio);
    formData.append('color_bg', editForm.value.color_bg);
    formData.append('library_private', String(editForm.value.library_private));
    formData.append('wishlist_private', String(editForm.value.wishlist_private));
    formData.append('collections_private', String(editForm.value.collections_private));

    if (avatarFile.value) {
        formData.append('avatar', avatarFile.value);
    }

    try {
        await api.patch(`/api/users/${profile.value.id}/`, formData);

        uiStore.triggerSuccess("Profile edited successfully", profile.value.color_bg);

        router.push('/profile');
    } catch (error: any) {
        errorMessage.value = error.response?.data?.error || "Error saving profile data";
    }
}

function handleAvatarChange(event: Event) {
    const file = (event.target as HTMLInputElement).files?.[0];
    if (!file) return;

    rawImage.value = URL.createObjectURL(file);
    showCropper.value = true;
}

function getCroppedImage() {
    const canvas = cropperRef.value.getResult().canvas;
    if (!canvas) return;

    canvas.toBlob((blob: Blob | null) => {
        if (!blob) return;

        const file = new File([blob], 'avatar.jpg', { type: 'image/jpeg' });
        avatarFile.value = file;
        avatarPreview.value = URL.createObjectURL(file);

        showCropper.value = false;
    }, 'image/jpeg');
}
</script>

<style scoped>
.dynamic-text {
    color: var(--user-color);
}

.dynamic-input:focus {
    border-color: var(--user-color);
    box-shadow: 0 0 0 2px color-mix(in srgb, var(--user-color) 20%, transparent);
}

.dynamic-switch {
    transition: all 0.2s ease;
}

.peer:checked~.dynamic-switch {
    background-color: var(--user-color);
}

.dynamic-btn-submit {
    background-color: var(--user-color);
    color: #0b0e14;
}

.dynamic-btn-submit:hover {
    background-color: color-mix(in srgb, var(--user-color) 85%, white   );
    box-shadow: 0 10px 25px color-mix(in srgb, var(--user-color) 20%, transparent);
}

.dynamic-btn-apply {
    background-color: var(--user-color);
    color: #0b0e14;
}

.dynamic-btn-apply:hover {
    background-color: color-mix(in srgb, var(--user-color) 85%, black);
}
</style>