<template>
    <Navbar />
    <div class="pt-20 h-[92.5vh] bg-gsoscuro/95 flex justify-center items-start px-4">
        <div class="bg-gsoscuro p-10 rounded-2xl text-gsblanco mx-auto max-w-[45rem] w-full shadow-2xl border border-gsgris/20">
            
            <Stepper v-model:value="activeStep" class="basis-[40rem]" linear>
                <StepList>
                    <Step v-slot="{ activateCallback, value, a11yAttrs }" asChild :value="1">
                        <div class="flex flex-row flex-auto gap-2" v-bind="a11yAttrs.root">
                            <button class="bg-transparent border-0 inline-flex flex-col gap-2" @click="activateCallback" v-bind="a11yAttrs.header">
                                <span :class="['rounded-full border-2 w-12 h-12 inline-flex items-center justify-center', { 'bg-gsmenta text-gsoscuro border-gsmenta': Number(value) <= activeStep, 'border-gsgris': Number(value) > activeStep }]">
                                    <i class="pi pi-user" />
                                </span>
                            </button>
                            <Divider />
                        </div>
                    </Step>
                    <Step v-slot="{ activateCallback, value, a11yAttrs }" asChild :value="2">
                        <div class="flex flex-row flex-auto gap-2 pl-2" v-bind="a11yAttrs.root">
                            <button class="bg-transparent border-0 inline-flex flex-col gap-2" @click="activateCallback" v-bind="a11yAttrs.header">
                                <span :class="['rounded-full border-2 w-12 h-12 inline-flex items-center justify-center', { 'bg-gsmenta text-gsoscuro border-gsmenta': Number(value) <= activeStep, 'border-gsgris': Number(value) > activeStep }]">
                                    <i class="pi pi-star" />
                                </span>
                            </button>
                            <Divider />
                        </div>
                    </Step>
                    <Step v-slot="{ activateCallback, value, a11yAttrs }" asChild :value="3">
                        <div class="flex flex-row pl-2" v-bind="a11yAttrs.root">
                            <button class="bg-transparent border-0 inline-flex flex-col gap-2" @click="activateCallback" v-bind="a11yAttrs.header">
                                <span :class="['rounded-full border-2 w-12 h-12 inline-flex items-center justify-center', { 'bg-gsmenta text-gsoscuro border-gsmenta': Number(value) <= activeStep, 'border-gsgris': Number(value) > activeStep }]">
                                    <i class="pi pi-id-card" />
                                </span>
                            </button>
                        </div>
                    </Step>
                </StepList>

                <StepPanels>
                    <!-- STEP 1: Credenciales de cuenta -->
                    <StepPanel v-slot="{ activateCallback }" :value="1">
                        <div class="flex flex-col gap-4 mx-auto" style="min-height: 16rem; max-width: 20rem">
                            <div class="text-center mt-4 mb-4 text-xl font-semibold">Create your account</div>
                            
                            <input v-model="username" class="bg-[#1a1e26] border border-gsgris/30 rounded-md px-3 py-2" placeholder="Username">
                            <p :class="isHiddenUsernameError" class="text-red-400 text-xs">{{ usernameError }}</p>

                            <input v-model="email" type="email" class="bg-[#1a1e26] border border-gsgris/30 rounded-md px-3 py-2" placeholder="Email">
                            <p :class="isHiddenEmailError" class="text-red-400 text-xs">{{ emailError }}</p>

                            <input v-model="password" type="password" class="bg-[#1a1e26] border border-gsgris/30 rounded-md px-3 py-2" placeholder="Password">
                            <p :class="isHiddenPasswordError" class="text-red-400 text-xs">{{ passwordError }}</p>
                        </div>
                        <div class="flex flex-col gap-2 mt-4 text-center">
                            <router-link to="/login" class="text-gsgris hover:text-gsblanco text-sm">Already have an account? Login</router-link>
                        </div>
                        <div class="flex pt-6 justify-end">
                            <button @click="() => { 
                                    if (checkFields()) activateCallback(2); 
                                }"  
                                class="bg-gsmenta text-gsoscuro px-4 py-2 rounded-md font-bold hover:cursor-pointer">
                                    Next
                            </button>
                        </div>
                    </StepPanel>

                    <!-- STEP 2: Información Personal -->
                    <StepPanel v-slot="{ activateCallback }" :value="2">
                        <div class="flex flex-col gap-4 mx-auto" style="min-height: 16rem; max-width: 24rem">
                            <div class="text-center mt-4 mb-4 text-xl font-semibold">Personal Information</div>
                            <input v-model="firstName" class="bg-[#1a1e26] border border-gsgris/30 rounded-md px-3 py-2" placeholder="First Name">
                            <input v-model="lastName" class="bg-[#1a1e26] border border-gsgris/30 rounded-md px-3 py-2" placeholder="Last Name">
                            
                            <div class="flex flex-col gap-2 mt-4 text-center">
                                <router-link to="/login" class="text-gsgris hover:text-gsblanco text-sm">Already have an account? Login</router-link>
                            </div>
                        </div>
                        <div class="flex pt-6 justify-between">
                            <button @click="activateCallback(1)" class="text-gsgris px-4 py-2 underline hover:cursor-pointer">Back</button>
                            <!-- Botón que ejecuta tu función final -->
                            <button @click="{activateCallback(3); submitRegister();}" class="bg-gsmenta text-gsoscuro px-6 py-2 rounded-md font-bold hover:cursor-pointer">Register</button>
                        </div>
                    </StepPanel>

                    <!-- STEP 3: Éxito -->
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

import Navbar from '@/components/Navbar.vue';
import router from '@/router';

import Stepper from 'primevue/stepper';
import StepList from 'primevue/steplist';
import StepPanels from 'primevue/steppanels';
import StepItem from 'primevue/stepitem';
import Step from 'primevue/step';
import StepPanel from 'primevue/steppanel';


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

function checkFields(){
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

<style scoped>

</style>