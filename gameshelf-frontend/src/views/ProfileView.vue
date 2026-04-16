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
                        <div class="flex flex-wrap gap-2 mt-3">
                            <Badge nombre="role" :role="profile?.role ?? 'unknown'"/>
                            <Badge nombre="collectionist" :collectionsQuantity="(profile?.user.collections)?.length ?? 0"/>
                            <Badge nombre="wisher" :wishlistQuantity="(profile?.user.wishlist.items)?.length ?? 0"/>
                            <Badge nombre="player" :libraryQuantity="(profile?.user.library)?.length ?? 0"/>
                            <Badge nombre="completionist" :completedQuantity="completed ?? 0"/>
                            <!-- <p>{{ profile?.role }}</p> -->
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
                    <span class="block text-2xl md:text-3xl font-bold text-gsmenta">{{ (profile?.user.collections)?.length }}</span>
                    <span class="text-gsgris text-xs uppercase tracking-wider font-semibold">Collections</span>
                </div>
                <div class="text-center">
                    <span class="block text-2xl md:text-3xl font-bold text-gsmenta">{{ (profile?.user.library)?.length }}</span>
                    <span class="text-gsgris text-xs uppercase tracking-wider font-semibold">Library</span>
                </div>
                <div class="text-center border-x border-gsgris/20 px-10 md:border-none">
                    <span class="block text-2xl md:text-3xl font-bold text-gsmenta">{{ completed }}</span>
                    <span class="text-gsgris text-xs uppercase tracking-wider font-semibold">Completed</span>
                </div>
                <div class="text-center">
                    <span class="block text-2xl md:text-3xl font-bold text-gsmenta">{{ (profile?.user.wishlist.items)?.length }}</span>
                    <span class="text-gsgris text-xs uppercase tracking-wider font-semibold">Wishlist</span>
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
import type { Collection, Game, LibraryItem, Profile } from '@/types/profileTypes';
import Badge from '@/components/Badge.vue';

const authStore = useAuthStore()
const profile = ref<Profile | null>(null);
const loading = ref(true)

onMounted(async () => {
    apiProfileMe().then((data) => {
        console.log(JSON.stringify(data))
        profile.value = data
        loading.value = false
    })
});

const fullName = computed(() => {
    const first = profile.value?.user.first_name?.trim()
    const last = profile.value?.user.last_name?.trim()

    // Si ambos están vacíos
    if (!first && !last) return 'noname'

    // Combina los que existan y limpia espacios extra
    return `${first || ''} ${last || ''}`.trim()
})

const completed = computed(()=>{
    let completedItems = 0;
    profile.value?.user.library.forEach(item => {
        item.status === "Completed" && completedItems++
    });

    return completedItems
})

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