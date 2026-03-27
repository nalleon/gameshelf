<template>
  <div class="contenedor">
      <router-view />
  </div>
</template>

<script setup lang="ts">

</script>

<style scoped>
  .contenedor {
      height: 100vh; /* ocupa toda la pantalla */
      background-image: url("./assets/background.jpg");
      background-size: cover;
      background-position: center;
      background-repeat: no-repeat;
  }
</style>
