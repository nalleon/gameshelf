<template>
    <Navbar />

    <div class="min-h-screen bg-gsoscuro text-gsblanco px-6 py-10">
        <div class="max-w-6xl mx-auto">

            <!-- HEADER -->
            <div class="mb-10">
                <!-- <h1 class="text-3xl font-bold">
                    Search Users
                </h1> -->

                <p class="text-gsgris mt-2">
                    Results for:
                    <span class="text-gsmenta font-semibold">
                        "{{ route.query.q }}"
                    </span>
                </p>
            </div>

            <!-- LOADING -->
            <div v-if="loading" class="text-center py-20">
                Loading...
            </div>

            <!-- RESULTS -->
            <div v-else-if="profiles.length > 0" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                <router-link v-for="profile in profiles" :key="profile.id" :to="`/profile/${profile.id}`"
                    class="bg-[#161a21] border border-white/10 rounded-2xl p-5 hover:border-gsmenta/40 transition-all duration-300 group">
                    <div class="flex items-center gap-4">

                        <!-- AVATAR -->
                        <img v-if="profile.avatar" :src="profile.avatar" alt=""
                            class="w-18 h-18 rounded-full object-cover border-2"
                            :style="{ borderColor: profile.color_bg || '#79a998' }" />

                        <!-- INFO -->
                        <div class="flex-1">
                            <h2 class="font-bold text-lg group-hover:text-gsmenta transition-colors">
                                {{ fullName(profile) }}
                            </h2>

                            <p class="text-sm text-gsgris">
                                @{{ profile.user.username }}
                            </p>

                            <p class="text-xs text-gsgris mt-2 line-clamp-2">
                                {{
                                    profile.bio ||
                                    'Este usuario aún no tiene biografía.'
                                }}
                            </p>
                        </div>

                    </div>
                </router-link>
            </div>

            <!-- EMPTY -->
            <div v-else class="flex flex-col items-center justify-center py-20">
                <img src="@/assets/Empty-cuate.svg" class="w-80 opacity-80" />

                <p class="text-gsgris mt-6">
                    No users found
                </p>
            </div>

        </div>
    </div>
</template>

<script setup lang="ts">
import { onMounted, ref, watch } from 'vue'
import { useRoute } from 'vue-router'
import axios from 'axios'
import api from "@/api/client";
import Navbar from '@/components/Navbar.vue'
import type { Profile } from '@/types/profileTypes'

const route = useRoute()

const profiles = ref<Profile[]>([])
const loading = ref(false)

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