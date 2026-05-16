<template>
    <Navbar />
    <div class="min-h-screen bg-gsoscuro text-gsblanco font-sans pb-20">
        <header class="relative bg-[#1a1e26] border-b border-gsgris/10">
            <div class="h-32 md:h-40 transition-colors duration-500" :style="{ backgroundColor: editForm.color_bg }" />
            <div class="max-w-4xl mx-auto px-6">
                <div class="flex items-end -mt-12 gap-6 pb-6">
                    <div class="relative group cursor-pointer">
                        <div
                            class="w-28 h-28 md:w-32 md:h-32 rounded-2xl bg-gsoscuro border-4 border-gsoscuro overflow-hidden shadow-xl">
                            <img :src="avatarPreview ?? profile?.avatar"
                                class="w-full h-full object-cover transition-all group-hover:opacity-80" />
                            <div
                                class="absolute inset-0 flex items-center justify-center bg-gsoscuro/40 group-hover:bg-gsoscuro/60 transition-all rounded-2xl">
                                <svg xmlns="http://www.w3.org/2000/svg" class="h-8 w-8 text-gsmenta" fill="none"
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
                    <div class="mb-2">
                        <h1 class="text-2xl font-bold text-gsblanco">Edit Profile</h1>
                        <p class="text-gsgris text-sm">Personalize your identity on the platform</p>
                    </div>
                </div>
            </div>
        </header>

        <main class="max-w-4xl mx-auto px-6 mt-10">
            <form @submit.prevent="saveProfile" class="space-y-8">

                <section class="grid grid-cols-1 md:grid-cols-2 gap-6">
                    <div class="col-span-full">
                        <h3 class="text-xs uppercase tracking-[0.2em] text-gsmenta font-bold mb-4">Personal Information
                        </h3>
                    </div>

                    <div class="space-y-2">
                        <label class="text-sm text-gsgris ml-1">First Name</label>
                        <input v-model="editForm.first_name" type="text"
                            class="w-full bg-[#161a21] border border-gsgris/20 rounded-xl px-4 py-3 focus:outline-none focus:border-gsmenta transition-colors"
                            placeholder="Your first name">
                    </div>

                    <div class="space-y-2">
                        <label class="text-sm text-gsgris ml-1">Last Name</label>
                        <input v-model="editForm.last_name" type="text"
                            class="w-full bg-[#161a21] border border-gsgris/20 rounded-xl px-4 py-3 focus:outline-none focus:border-gsmenta transition-colors"
                            placeholder="Your last name">
                    </div>

                    <div class="col-span-full space-y-2">
                        <label class="text-sm text-gsgris ml-1">Biography</label>
                        <textarea v-model="editForm.bio" rows="4"
                            class="w-full bg-[#161a21] border border-gsgris/20 rounded-xl px-4 py-3 focus:outline-none focus:border-gsmenta transition-colors resize-none"
                            placeholder="Tell us about your gaming tastes..."></textarea>
                    </div>
                </section>

                <section>
                    <h3 class="text-xs uppercase tracking-[0.2em] text-gsmenta font-bold mb-2">Visual Style</h3>
                    
                    <p v-if="!profile?.verified" class="text-xs text-red-400 mb-3 font-medium italic">
                        You have to verify your account to use this function
                    </p>

                    <div class="bg-[#1a1e26] p-6 rounded-2xl border border-gsgris/10 flex items-center justify-between transition-all"
                        :class="{ 'opacity-50 select-none': !profile?.verified }">
                        <div>
                            <p class="font-medium">Banner Color</p>
                            <p class="text-xs text-gsgris">This color will be displayed on your profile header.</p>
                        </div>
                        
                        <div class="flex items-center gap-3" :class="{ 'pointer-events-none': !profile?.verified }">
                            <input type="color" v-model="editForm.color_bg"
                                :disabled="!profile?.verified"
                                class="w-12 h-12 rounded-lg bg-transparent border-none cursor-pointer disabled:cursor-not-allowed">
                            <span class="text-sm font-mono text-gsgris uppercase">{{ editForm.color_bg }}</span>
                        </div>
                    </div>
                </section>

                <section>
                    <h3 class="text-xs uppercase tracking-[0.2em] text-gsmenta font-bold mb-4">Privacy</h3>
                    <div class="bg-[#1a1e26] p-4 rounded-2xl border border-gsgris/10 space-y-4">
                        
                        <div class="flex items-center justify-between p-2">
                            <div>
                                <p class="font-medium text-gsblanco">Private Library</p>
                                <p class="text-xs text-gsgris">Hide your game list and play status.</p>
                            </div>
                            <label class="relative inline-flex items-center cursor-pointer">
                                <input type="checkbox" v-model="editForm.library_private" class="sr-only peer">
                                <div class="w-11 h-6 bg-gsgris/20 peer-focus:outline-none rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-gsmenta"></div>
                            </label>
                        </div>

                        <hr class="border-gsgris/10">

                        <div class="flex items-center justify-between p-2">
                            <div>
                                <p class="font-medium text-gsblanco">Private Wishlist</p>
                                <p class="text-xs text-gsgris">Nobody will see the games you want to buy.</p>
                            </div>
                            <label class="relative inline-flex items-center cursor-pointer">
                                <input type="checkbox" v-model="editForm.wishlist_private" class="sr-only peer">
                                <div class="w-11 h-6 bg-gsgris/20 peer-focus:outline-none rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-gsmenta"></div>
                            </label>
                        </div>

                        <hr class="border-gsgris/10">

                        <div class="flex items-center justify-between p-2">
                            <div>
                                <p class="font-medium text-gsblanco">Private Collections</p>
                                <p class="text-xs text-gsgris">Affects all your custom collections.</p>
                                <p class="text-xs text-red-500">All your collections will be set on private</p>
                            </div>
                            <label class="relative inline-flex items-center cursor-pointer">
                                <input type="checkbox" v-model="editForm.collections_private" class="sr-only peer">
                                <div class="w-11 h-6 bg-gsgris/20 peer-focus:outline-none rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-gsmenta"></div>
                            </label>
                        </div>
                    </div>
                </section>

                <div class="flex flex-col md:flex-row gap-4 pt-6 border-t border-gsgris/10">
                    <button type="submit"
                        class="flex-1 bg-gsmenta text-gsoscuro font-bold py-4 rounded-xl hover:bg-[#68d391] transition-all transform hover:scale-[1.01] active:scale-95 shadow-lg shadow-gsmenta/10">
                        Save Changes
                    </button>
                    <button type="button" @click="$router.push('/profile')"
                        class="px-8 py-4 border border-gsgris/30 text-gsgris font-semibold rounded-xl hover:bg-gsgris/10 transition-all">
                        Cancel
                    </button>
                </div>

            </form>
        </main>
    </div>
    <div v-if="showCropper" class="fixed inset-0 bg-black/70 flex items-center justify-center z-50 px-4">
        <div class="relative w-full max-w-xl bg-gsoscuro text-gsblanco rounded-2xl shadow-2xl border border-white/8 overflow-hidden">
            <div class="absolute top-0 left-0 w-full h-1 bg-linear-to-r from-gsmenta via-gsblanco/70 to-gsbosque"></div>
            <div class="p-6">
                <h2 class="text-center text-lg font-semibold mb-6">
                    Adjust your profile picture
                </h2>
                <div class="flex justify-center">
                    <Cropper ref="cropperRef" :src="rawImage" class="w-full h-80 rounded-xl overflow-hidden"
                        :stencil-component="CircleStencil" :stencil-props="{
                            aspectRatio: 1
                        }" />
                </div>
                <div class="flex justify-between mt-6">
                    <button class="text-gsgris hover:text-gsblanco transition-colors" @click="showCropper = false">
                        Cancel
                    </button>
                    <button
                        class="bg-gsmenta hover:bg-gsbosque text-gsoscuro px-5 py-2 rounded-full font-bold transition-all"
                        @click="getCroppedImage">
                        Apply
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
import { Cropper, CircleStencil } from 'vue-advanced-cropper'
import 'vue-advanced-cropper/dist/style.css'
import api from "@/api/client";

const router = useRouter();
const authStore = useAuthStore();
const profile = ref<Profile | null>(null);
const avatarPreview = ref<string | null>(null);
const showCropper = ref(false)
const rawImage = ref<string | null>(null)
const avatarFile = ref<File | null>(null)
const cropperRef = ref()
const fileInputRef = ref<HTMLInputElement | null>(null);
const errorMessage = ref<string | null>(null); // Para mostrar errores del backend

// Formulario reactivo
// 1. Actualizar el objeto inicial
const editForm = ref({
    first_name: '',
    last_name: '',
    bio: '',
    color_bg: '#79a998',
    library_private: false,    // Nuevo
    wishlist_private: false,   // Nuevo
    collections_private: false // Nuevo
});

// 2. Actualizar onMounted para leer estos valores del backend
onMounted(async () => {
    const data = await apiProfileMe();
    profile.value = data;

    editForm.value = {
        first_name: data.user.first_name || '',
        last_name: data.user.last_name || '',
        bio: data.bio || '',
        color_bg: data.color_bg || '#79a998',
        // Asegúrate que tu API devuelva estos campos o sus equivalentes
        library_private: data.user.library?.is_private ?? false,
        wishlist_private: data.user.wishlist?.is_private ?? false,
        collections_private: false
    };
});

// 3. Actualizar saveProfile para enviar los booleanos
async function saveProfile() {
    if (!profile.value) return;
    errorMessage.value = null;

    const formData = new FormData();
    formData.append('first_name', editForm.value.first_name);
    formData.append('last_name', editForm.value.last_name);
    formData.append('bio', editForm.value.bio);
    formData.append('color_bg', editForm.value.color_bg);
    
    // FormData envía strings, el backend debe manejarlos o puedes enviarlo como JSON
    formData.append('library_private', String(editForm.value.library_private));
    formData.append('wishlist_private', String(editForm.value.wishlist_private));
    formData.append('collections_private', String(editForm.value.collections_private));

    if (avatarFile.value) {
        formData.append('avatar', avatarFile.value);
    }

    try {
        await api.patch(`/api/users/${profile.value.id}/`, formData);
        router.push({
            path: '/profile',
            query: { updated: 'true' }
        });
    } catch (error: any) {
        errorMessage.value = error.response?.data?.error || "Error al guardar";
    }
}

async function apiProfileMe() {
    const response = await api.get('/api/users/me/');
    return response.data;
}

function handleAvatarChange(event: Event) {
    const file = (event.target as HTMLInputElement).files?.[0]
    if (!file) return

    rawImage.value = URL.createObjectURL(file)
    showCropper.value = true
}

function getCroppedImage() {
    const canvas = cropperRef.value.getResult().canvas

    canvas.toBlob((blob: Blob | null) => {
        if (!blob) return

        const file = new File([blob], 'avatar.jpg', { type: 'image/jpeg' })
        avatarFile.value = file
        avatarPreview.value = URL.createObjectURL(file)

        showCropper.value = false
    }, 'image/jpeg')
}

// async function saveProfile() {
//     if (!profile.value) return;

//     errorMessage.value = null;

//     const formData = new FormData();

//     formData.append('first_name', editForm.value.first_name);
//     formData.append('last_name', editForm.value.last_name);
//     formData.append('bio', editForm.value.bio);
//     formData.append('color_bg', editForm.value.color_bg);

//     const file = avatarFile.value;

//     if (file) {
//         formData.append('avatar', file);
//     }

//     try {
//         await api.patch(
//             `/api/users/${profile.value.id}/`,
//             formData
//         );

//         router.push('/profile');

//     } catch (error: any) {

//         errorMessage.value =
//             error.response?.data?.error ||
//             "Ocurrió un error al guardar";
//     }
// }
</script>

<style scoped></style>