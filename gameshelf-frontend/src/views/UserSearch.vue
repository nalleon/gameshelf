<template>
    <Navbar />

    <div class="min-h-screen bg-[#0b0e14] text-gsblanco p-4 sm:p-6 md:p-8">
        <div class="max-w-[1600px] mx-auto">

            <div class="mb-6 md:mb-8 flex flex-col sm:flex-row sm:items-center justify-between border-b border-gsgris/10 pb-4 md:pb-6 gap-4">
                <div class="flex flex-col md:flex-row md:items-center gap-3 md:gap-6">
                    <div class="flex items-center gap-3 text-gsmenta">
                        <i class="pi pi-search text-xl md:text-2xl"></i>
                        <h2 class="text-xl md:text-2xl font-semibold border-l-4 border-gsmenta/50 pl-3 md:pl-4">
                            Search Results
                        </h2>
                    </div>
                    
                    <div class="flex items-center gap-2 text-xs md:text-sm text-gsgris bg-[#161a21]/60 px-3 py-1.5 rounded-xl border border-gsgris/10 w-fit">
                        <i class="pi pi-tag text-[10px] md:text-xs text-gsmenta/70"></i>
                        <span>Results for:</span>
                        <span class="text-gsmenta font-bold tracking-wide">
                            {{ route.query.q }}
                        </span>
                    </div>
                </div>
            </div>

            <div v-if="loading" class="text-center py-20 text-gsmenta flex flex-col items-center gap-3">
                <i class="pi pi-spin pi-spinner text-3xl"></i>
                <span class="text-sm font-medium text-gsgris">Searching database...</span>
            </div>

            <div v-else-if="profiles.length > 0" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                <router-link v-for="profile in profiles" :key="profile.id" :to="`/profile/${profile.id}`"
                    class="bg-[#161a21] border border-gsgris/20 rounded-2xl p-5 hover:border-gsmenta/40 transition-all duration-300 shadow-lg group">
                    <div class="flex items-center gap-4">

                        <img v-if="profile.avatar" :src="profile.avatar" alt=""
                            class="w-18 h-18 rounded-full object-cover border-2"
                            :style="{ borderColor: profile.color_bg || '#79a998' }" />

                        <div class="flex-1">
                            <h2 class="font-bold text-lg group-hover:text-gsmenta transition-colors">
                                {{ fullName(profile) }}
                            </h2>

                            <p class="text-sm text-gsmenta">
                                @{{ profile.user.username }}
                            </p>

                            <p class="text-xs text-gsgris mt-2 line-clamp-2">
                                {{ profile.bio || defaultBio }}
                            </p>
                        </div>

                    </div>
                </router-link>
            </div>

            <div v-else class="flex flex-col items-center justify-center py-16 md:py-24 text-gsgris border border-dashed border-gsgris/10 rounded-2xl bg-[#161a21]/30 backdrop-blur-sm px-4">
                <div class="bg-[#161a21] border border-gsgris/10 p-5 rounded-full shadow-md mb-4 flex items-center justify-center">
                    <i class="pi pi-search-minus text-3xl text-gsmenta/40"></i>
                </div>

                <h3 class="text-base md:text-lg font-semibold text-gsblanco mb-1 text-center">No users found</h3>
                <p class="text-xs md:text-sm text-gsgris text-center max-w-sm">
                    We couldn't find any collector matching <span class="text-gsmenta">"{{ route.query.q }}"</span>. Check the spelling or try another username.
                </p>
            </div>

        </div>
    </div>
</template>

<script setup lang="ts">
import { onMounted, ref, watch } from 'vue'
import { useRoute } from 'vue-router'
import api from "@/api/client";
import Navbar from '@/components/Navbar.vue'
import type { Profile } from '@/types/profileTypes'

const route = useRoute()

const profiles = ref<Profile[]>([])
const loading = ref(false)
const defaultBio = 'This collector has not yet written their story... But their shelf speaks for itself!'

onMounted(fetchUsers)

async function fetchUsers() {
    const query = route.query.q;

    if (!query) {
        profiles.value = [];
        return;
    }

    loading.value = true;

    try {
        const response = await api.get('/api/users/search/', {
            params: {
                q: query
            }
        });

        profiles.value = response.data;

    } catch (error: unknown) {
        console.error('Error searching users:', error);

    } finally {
        loading.value = false;
    }
}

function fullName(profile: any) {
    const first = profile.user.first_name?.trim()
    const last = profile.user.last_name?.trim()

    if (!first && !last) return 'noname'

    return `${first || ''} ${last || ''}`.trim()
}

watch(
    () => route.query.q,
    fetchUsers
)
</script>