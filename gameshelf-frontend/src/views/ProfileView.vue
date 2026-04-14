<template>
    <Navbar/>
    <div class="min-h-screen bg-gsoscuro text-gsblanco font-sans pb-20">
        <!-- Header / Banner -->
        <header class="relative bg-[#1a1e26]">
            <!-- Banner con degradado usando tus colores -->
            <div class="h-48 md:h-55 bg-gradient-to-r from-gsbosque to-gsmenta"></div>
            
            <div class="max-w-5xl mx-auto px-6">
                <div class="flex flex-col md:flex-row items-end -mt-12 md:-mt-10 gap-6 pb-6">
                <!-- Avatar -->
                    <div class="w-32 h-32 md:w-40 md:h-40 rounded-2xl bg-gsoscuro border-4 border-gsoscuro overflow-hidden shadow-xl">
                        <img :src="profile?.avatar"  alt="User Avatar" class="w-full h-full object-cover" />
                    </div>

                    <!-- User Details -->
                    <div class="flex-1">
                        <h1 class="text-3xl md:text-4xl font-bold">{{ fullName }}</h1>
                        <p class="text-gsmenta font-medium">@{{ profile?.user.username }}</p>
                        <div class="flex gap-2 mt-3">
                            <span class="px-3 py-1 bg-gsgris/30 text-xs rounded-md border border-gsgris/50">Coleccionista Pro</span>
                            <span class="px-3 py-1 bg-gsgris/30 text-xs rounded-md border border-gsgris/50">Explorador</span>
                        </div>
                    </div>

                    <!-- Action Button -->
                    <button class="mb-2 px-6 py-2 border border-gsmenta text-gsmenta rounded-xl hover:bg-gsmenta hover:text-gsoscuro transition-all duration-300 font-semibold">
                        Editar Perfil
                    </button>
                </div>
            </div>
        </header>

        <!-- Stats Bar -->
        <section class="bg-[#161a21] border-y border-gsgris/10 py-8">
            <div class="max-w-5xl mx-auto px-6 flex justify-around md:justify-center md:gap-24">
                <div class="text-center">
                    <span class="block text-2xl md:text-3xl font-bold text-gsmenta">124</span>
                    <span class="text-gsgris text-xs uppercase tracking-wider font-semibold">Juegos</span>
                </div>
                <div class="text-center border-x border-gsgris/20 px-10 md:border-none">
                    <span class="block text-2xl md:text-3xl font-bold text-gsmenta">12</span>
                    <span class="text-gsgris text-xs uppercase tracking-wider font-semibold">Completados</span>
                </div>
                <div class="text-center">
                    <span class="block text-2xl md:text-3xl font-bold text-gsmenta">45</span>
                    <span class="text-gsgris text-xs uppercase tracking-wider font-semibold">Deseados</span>
                </div>
            </div>
        </section>

        <!-- Main Content -->
        <main class="max-w-5xl mx-auto px-6 mt-12">
            <div class="flex justify-between items-center mb-8">
                <h2 class="text-2xl font-bold border-l-4 border-gsmenta pl-4">Mi Estantería Reciente</h2>
                <a href="#" class="text-gsmenta hover:text-gsbosque text-sm font-medium transition-colors">Ver toda la colección →</a>
            </div>
            
            <!-- Game Grid -->
            <div class="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-4 gap-6">
                <div v-for="i in 4" :key="i" class="group cursor-pointer">
                <div class="relative aspect-[3/4] bg-gsgris rounded-xl overflow-hidden transition-transform duration-300 group-hover:-translate-y-2 shadow-lg">
                    <!-- Overlay para el estado -->
                    <div class="absolute top-3 left-3 px-2 py-1 bg-gsoscuro/80 backdrop-blur-md rounded text-[10px] uppercase font-bold text-gsmenta border border-gsmenta/30">
                    Jugando
                    </div>
                    <div class="w-full h-full bg-gradient-to-t from-gsoscuro via-transparent to-transparent opacity-60"></div>
                </div>
                <div class="mt-4">
                    <h3 class="font-semibold text-gsblanco group-hover:text-gsmenta transition-colors line-clamp-1">The Legend of Zelda</h3>
                    <p class="text-gsgris text-sm italic">Switch</p>
                </div>
                </div>
            </div>
        </main>
    </div>
</template>

<script setup lang="ts">
import Navbar from '@/components/Navbar.vue';
import { computed, onMounted, ref } from 'vue';
import { useAuthStore } from '@/stores/authStore';
import type { Profile } from '@/types/generalTypes';

const profile = ref<Profile | null>(null);
    
const fullName = computed(() => {
    const first = profile.value?.user.first_name?.trim()
    const last = profile.value?.user.last_name?.trim()

    // Si ambos están vacíos
    if (!first && !last) return 'noname'

    // Combina los que existan y limpia espacios extra
    return `${first || ''} ${last || ''}`.trim()
})

const authStore = useAuthStore()

onMounted(async () => {

    apiProfileMe().then((data) => {
        console.log(JSON.stringify(data))
        profile.value = data
    })
});

async function apiProfileMe(){
    const webhookUrl = `http://127.0.0.1:8000/api/users/me/`

    const response = await fetch(webhookUrl, 
        {
            method: "GET",
            headers: {
                'Authorization': `Bearer ${authStore.token}`, 
                'Content-Type': 'application/json'
            }
        }
    );
    const data = await response.json();

    return data;
}


</script>

<style scoped>

</style>