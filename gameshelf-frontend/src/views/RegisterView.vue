<template>
    <Navbar />

    <div class="pt-20 h-[92.5vh] bg-gsoscuro/55 flex justify-center items-start px-4">

        <div
            class="bg-gsoscuro p-10 rounded-2xl text-gsblanco mx-auto max-w-[45rem] w-full shadow-2xl border border-white/8 relative overflow-hidden">

            <!-- Línea superior (igual que login/home card) -->
            <div class="absolute top-0 left-0 w-full h-1 bg-linear-to-r from-gsmenta via-gsblanco/70 to-gsbosque"></div>

            <Stepper v-model:value="activeStep" class="basis-[40rem]" linear>
                <StepList>
                    <Step v-slot="{ activateCallback, value, a11yAttrs }" asChild :value="1">
                        <div class="flex flex-row flex-auto gap-2" v-bind="a11yAttrs.root">
                            <button class="bg-transparent border-0 inline-flex flex-col gap-2" @click="activateCallback"
                                v-bind="a11yAttrs.header">
                                <span
                                    :class="['rounded-full border-2 w-12 h-12 inline-flex items-center justify-center', { 'bg-gsmenta text-gsoscuro border-gsmenta': Number(value) <= activeStep, 'border-gsgris': Number(value) > activeStep }]">
                                    <i class="pi pi-user" />
                                </span>
                            </button>
                            <Divider />
                        </div>
                    </Step>

                    <Step v-slot="{ activateCallback, value, a11yAttrs }" asChild :value="2">
                        <div class="flex flex-row flex-auto gap-2 pl-2" v-bind="a11yAttrs.root">
                            <button class="bg-transparent border-0 inline-flex flex-col gap-2" @click="activateCallback"
                                v-bind="a11yAttrs.header">
                                <span
                                    :class="['rounded-full border-2 w-12 h-12 inline-flex items-center justify-center', { 'bg-gsmenta text-gsoscuro border-gsmenta': Number(value) <= activeStep, 'border-gsgris': Number(value) > activeStep }]">
                                    <i class="pi pi-star" />
                                </span>
                            </button>
                            <Divider />
                        </div>
                    </Step>

                    <Step v-slot="{ activateCallback, value, a11yAttrs }" asChild :value="3">
                        <div class="flex flex-row pl-2" v-bind="a11yAttrs.root">
                            <button class="bg-transparent border-0 inline-flex flex-col gap-2" @click="activateCallback"
                                v-bind="a11yAttrs.header">
                                <span
                                    :class="['rounded-full border-2 w-12 h-12 inline-flex items-center justify-center', { 'bg-gsmenta text-gsoscuro border-gsmenta': Number(value) <= activeStep, 'border-gsgris': Number(value) > activeStep }]">
                                    <i class="pi pi-id-card" />
                                </span>
                            </button>
                        </div>
                    </Step>
                </StepList>

                <StepPanels>
                    <!-- STEP 1 -->
                    <StepPanel v-slot="{ activateCallback }" :value="1">
                        <div class="flex flex-col gap-4 mx-auto" style="min-height: 16rem; max-width: 20rem">
                            <div class="text-center mt-4 mb-4 text-xl font-semibold">Create your account</div>

                            <input v-model="username" class="bg-[#1a1e26] border border-gsgris/30 rounded-md px-3 py-2"
                                placeholder="Username">
                            <p :class="isHiddenUsernameError" class="text-red-400 text-xs">{{ usernameError }}</p>

                            <input v-model="email" type="email"
                                class="bg-[#1a1e26] border border-gsgris/30 rounded-md px-3 py-2" placeholder="Email">
                            <p :class="isHiddenEmailError" class="text-red-400 text-xs">{{ emailError }}</p>

                            <input v-model="password" type="password"
                                class="bg-[#1a1e26] border border-gsgris/30 rounded-md px-3 py-2"
                                placeholder="Password">
                            <p :class="isHiddenPasswordError" class="text-red-400 text-xs">{{ passwordError }}</p>
                        </div>

                        <div class="flex flex-col gap-2 mt-4 text-center">
                            <router-link to="/login" class="text-gsgris hover:text-gsblanco text-sm">
                                Already have an account? Login
                            </router-link>
                        </div>

                        <div class="flex pt-6 justify-end">
                            <button @click="() => { if (checkFields()) activateCallback(2); }"
                                class="bg-gsmenta text-gsoscuro px-4 py-2  rounded-full font-bold hover:cursor-pointer">
                                Next
                            </button>
                        </div>
                    </StepPanel>

                    <!-- STEP 2 -->
                    <StepPanel v-slot="{ activateCallback }" :value="2">

                        <div class="flex flex-col gap-10 mx-auto w-full max-w-5xl px-6">

                            <!-- TITLE -->
                            <div class="text-center mt-4 text-xl font-semibold">
                                Personal Information
                            </div>

                            <!-- GRID -->
                            <div class="grid grid-cols-1 md:grid-cols-5 gap-12 items-center">

                                <!-- IZQUIERDA (MÁS ANCHA) -->
                                <div class="md:col-span-3 flex flex-col gap-6">

                                    <input v-model="firstName"
                                        class="w-full bg-[#1a1e26] border border-gsgris/30 rounded-xl px-5 py-4 text-base focus:outline-none focus:border-gsmenta transition-all"
                                        placeholder="First Name (Optional)">

                                    <input v-model="lastName"
                                        class="w-full bg-[#1a1e26] border border-gsgris/30 rounded-xl px-5 py-4 text-base focus:outline-none focus:border-gsmenta transition-all"
                                        placeholder="Last Name (Optional)">

                                </div>

                                <!-- DERECHA (MÁS PEQUEÑA) -->
                                <div class="md:col-span-2 flex flex-col items-center justify-center gap-4">

                                    <div class="relative group cursor-pointer">

                                        <div
                                            class="w-36 h-36 rounded-full bg-[#1a1e26] border border-gsgris/20 overflow-hidden shadow-xl flex items-center justify-center">

                                            <img v-if="croppedImage" :src="croppedImage"
                                                class="w-full h-full object-cover" />

                                            <div v-else class="text-gsgris">
                                                <i class="pi pi-user text-4xl"></i>
                                            </div>

                                            <div
                                                class="absolute inset-0 bg-gsoscuro/40 opacity-0 group-hover:opacity-100 flex items-center justify-center transition-all">
                                                <i class="pi pi-camera text-gsmenta text-xl"></i>
                                            </div>

                                        </div>

                                        <input type="file" accept="image/*" @change="handleAvatarChange"
                                            class="absolute inset-0 opacity-0 cursor-pointer" />

                                    </div>

                                </div>


                            </div>

                            <!-- LOGIN LINK -->
                            <div class="text-center">
                                <router-link to="/login" class="text-gsgris hover:text-gsblanco text-sm">
                                    Already have an account? Login
                                </router-link>
                            </div>

                        </div>

                        <!-- BOTONES -->
                        <div class="flex pt-6 justify-between items-center px-6">

                            <button @click="activateCallback(1)"
                                class="flex items-center gap-2 text-gsgris hover:text-gsblanco transition-colors">
                                <i class="pi pi-arrow-left text-lg" />
                            </button>

                            <button @click="{ activateCallback(3); submitRegister(); }"
                                class="bg-gsmenta hover:bg-gsbosque transition-all text-gsoscuro px-6 py-2 rounded-full font-bold">
                                Register
                            </button>

                        </div>

                    </StepPanel>
                    <!-- STEP 3 -->
                    <StepPanel v-slot="{ activateCallback }" :value="3">
                        <div class="flex flex-col gap-2 mx-auto" style="min-height: 16rem; max-width: 24rem">
                            <div class="text-center mt-4 mb-4 text-xl font-semibold">Account created successfully</div>

                            <div class="flex justify-center">
                                <img alt="logo" src="https://primefaces.org/cdn/primevue/images/stepper/content.svg" />
                            </div>
                        </div>
                    </StepPanel>

                </StepPanels>
            </Stepper>
        </div>
    </div>
    <!-- CROPPER MODAL -->
    <div v-if="showCropper" class="fixed inset-0 bg-black/70 flex items-center justify-center z-50 px-4">

        <div
            class="relative w-full max-w-xl bg-gsoscuro text-gsblanco rounded-2xl shadow-2xl border border-white/8 overflow-hidden">

            <!-- TOP BORDER (igual que cards/login/home) -->
            <div class="absolute top-0 left-0 w-full h-1 bg-linear-to-r from-gsmenta via-gsblanco/70 to-gsbosque"></div>

            <!-- CONTENT -->
            <div class="p-6">

                <h2 class="text-center text-lg font-semibold mb-6">
                    Adjust your profile picture
                </h2>

                <!-- CROPPER -->
                <div class="flex justify-center">

                    <Cropper ref="cropperRef" :src="rawImage" class="w-full h-80 rounded-xl overflow-hidden"
                        :stencil-component="CircleStencil" :stencil-props="{
                            aspectRatio: 1
                        }" />

                </div>

                <!-- BUTTONS -->
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
import { ref } from 'vue';
import { useAuthStore } from '@/stores/authStore'
import { uniqueNamesGenerator, adjectives, names, animals, NumberDictionary } from 'unique-names-generator';

import Navbar from '@/components/Navbar.vue';
import router from '@/router';

import Stepper from 'primevue/stepper';
import StepList from 'primevue/steplist';
import StepPanels from 'primevue/steppanels';
import StepItem from 'primevue/stepitem';
import Step from 'primevue/step';
import StepPanel from 'primevue/steppanel';
import axios from 'axios';
import { Cropper, CircleStencil } from 'vue-advanced-cropper'
import 'vue-advanced-cropper/dist/style.css'
import api from "@/api/client";
const showCropper = ref(false)
const rawImage = ref<string | null>(null)
const croppedImage = ref<string | null>(null)

const auth = useAuthStore()
const activeStep = ref(1);

const username = ref('')
const email = ref('')
const password = ref('')

const firstName = ref('')
const lastName = ref('')

const requiredFieldMessage = "Este campo es obligatorio";

const usernameError = ref('')
const emailError = ref('')
const passwordError = ref('')

const isHiddenUsernameError = ref('invisible')
const isHiddenEmailError = ref('invisible')
const isHiddenPasswordError = ref('invisible')

const numberDictionary = NumberDictionary.generate({ min: 100, max: 9999 });

const avatarFile = ref<File | null>(null)
const avatarPreview = ref<string | null>(null)
const cropperRef = ref()

const generateRandomFirstName = () => {
    return uniqueNamesGenerator({
        dictionaries: [adjectives, animals], // Adjetivo + Nombre
        separator: '',
        style: 'capital', // Para que sea AdjetivoNombre123
    });
};

async function apiRegister() {
    if (!firstName.value.trim()) {
        firstName.value = generateRandomFirstName();
    }

    if (!lastName.value.trim()) {
        lastName.value = String(numberDictionary);
    }

    const formData = new FormData();

    formData.append('username', username.value);
    formData.append('first_name', firstName.value);
    formData.append('last_name', lastName.value);
    formData.append('email', email.value);
    formData.append('password', password.value);

    if (avatarFile.value) {
        formData.append('avatar', avatarFile.value);
    }

    try {
        const response = await api.post('/api/auth/register/', formData);

        const data = response.data;

        username.value = "";
        email.value = "";
        password.value = "";

        return data;

    } catch (error: unknown) {
        console.error("Error en registro:", error);
        return null;
    }
}
function checkFields() {
    isHiddenUsernameError.value = "invisible"
    isHiddenEmailError.value = "invisible"
    isHiddenPasswordError.value = "invisible"

    if (username.value === "") {
        usernameError.value = requiredFieldMessage
        isHiddenUsernameError.value = "visible"
        return false;
    }

    if (email.value === "") {
        emailError.value = requiredFieldMessage
        isHiddenEmailError.value = "visible"
        return false;
    }

    if (password.value === "") {
        passwordError.value = requiredFieldMessage
        isHiddenPasswordError.value = "visible"
        return false;
    }

    return true;
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
        croppedImage.value = URL.createObjectURL(file)

        showCropper.value = false
    }, 'image/jpeg')
}

function submitRegister() {

    if (!checkFields()) {
        return;
    }


    apiRegister().then((data) => {
        auth.setUserSesion(data.token)
        router.replace('/profile')
    })
}
</script>

<style scoped></style>