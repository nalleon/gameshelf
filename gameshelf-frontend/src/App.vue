<template>
  <div :class="['h-screen', 'bg-gsoscuro', fondoClase]">
    <router-view />
  </div>
</template>

<script setup lang="ts">
import { useRoute } from 'vue-router'
import { computed } from 'vue'

const route = useRoute()

const fondoClase = computed(() => {
  if (
    route.path === '/login' ||
    route.path === '/' ||
    route.path === '/register'
  ) {
    return 'contenedorFoto'
  }

  return ''
})
</script>

<style>
.contenedorFoto {
  height: 100vh;
  background-image: url("/src/assets/background.jpg");
  background-size: cover;
  background-position: center;
  background-repeat: no-repeat;
}
</style>