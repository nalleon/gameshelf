<template>
  <div :class="['min-h-dvh', 'bg-gsoscuro', fondoClase]">
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
  /* Cambiado height por min-height */
  min-height: 100dvh;
  background-image: url("/src/assets/background.jpg");
  background-size: cover;
  background-position: center;
  background-repeat: no-repeat;
  /* IMPORTANTE: Esto hace que la imagen se quede congelada en la pantalla 
     mientras el contenido pasa por encima flotando */
  background-attachment: fixed;
}
</style>