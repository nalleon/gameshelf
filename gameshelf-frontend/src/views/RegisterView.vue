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
                        <div class="flex flex-col gap-4 mx-auto" style="min-height: 16rem; max-width: 24rem">
                            <div class="text-center mt-4 mb-4 text-xl font-semibold">Personal Information</div>

                            <input v-model="firstName" class="bg-[#1a1e26] border border-gsgris/30 rounded-md px-3 py-2"
                                placeholder="First Name (Optional)">
                            <input v-model="lastName" class="bg-[#1a1e26] border border-gsgris/30 rounded-md px-3 py-2"
                                placeholder="Last Name (Optional)">

                            <div class="flex flex-col gap-2 mt-4 text-center">
                                <router-link to="/login" class="text-gsgris hover:text-gsblanco text-sm">
                                    Already have an account? Login
                                </router-link>
                            </div>
                        </div>

                        <div class="flex pt-6 justify-between">
                            <button @click="activateCallback(1)"
                                class="flex items-center gap-2 text-gsgris hover:text-gsblanco transition-colors hover:cursor-pointer">
                                <i class="pi pi-arrow-left" />
                            </button>

                            <button @click="{ activateCallback(3); submitRegister(); }"
                                class="bg-gsmenta text-gsoscuro px-6 py-2 rounded-full font-bold hover:cursor-pointer">
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

const generateRandomFirstName = () => {
    return uniqueNamesGenerator({
        dictionaries: [adjectives, animals], // Adjetivo + Nombre
        separator: '',
        style: 'capital', // Para que sea AdjetivoNombre123
    });
};


async function apiRegister() {
    const webhookUrl = 'http://127.0.0.1:8000/api/auth/register/'

    if (!firstName.value.trim()) {
        firstName.value = generateRandomFirstName();
    }

    if (!lastName.value.trim()) {
        lastName.value = String(numberDictionary);
    }

    const payload = {
        username: username.value,
        first_name: firstName.value,
        last_name: lastName.value,
        email: email.value,
        password: password.value
    }

    const headers = {
        'Content-Type': 'application/json'
    }

    try {
        const response = await axios.post(webhookUrl, payload, { headers })
        const data = response.data;

        // console.log(data.token)
        username.value = "";
        email.value = "";
        password.value = "";

        return data;
    } catch (error) {
        if (error.response) {
            console.error("Error en registro:", error.response.data);
        } else {
            console.error("Error de red o configuración:", error.message);
        }
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