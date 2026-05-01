<template>
    <span :class="['px-3 py-1 text-xs rounded-md border border-gsgris/50 text-gsoscuro', badge.bgColor]">{{ badge.label }}</span>
</template>

<script setup lang="ts">
import { computed, onMounted } from 'vue';

type Props =
  | { nombre: 'collectionist'; collectionsQuantity?: number }
  | { nombre: 'wisher'; wishlistQuantity?: number }
  | { nombre: 'player'; libraryQuantity?: number }
  | { nombre: 'completionist'; completedQuantity?: number }
  | { nombre: 'role'; role?: string }

const props = defineProps<Props>()

const badge = computed(() => {
  let label = "";
  let bgColor = "bg-gsgris";
  let icon = "";

  switch (props.nombre) {
    case "collectionist": {
      const quantity = props.collectionsQuantity;

      if (quantity < 1) {
        label = "hide";
        bgColor = "invisible";
      } else if (quantity < 3) {
        label = "Rookie";
        bgColor = 'bg-gradient-to-b from-[#FEB26F] to-[#CD7638]';
      } else if (quantity < 6) {
        label = "Apprentice";
        bgColor = "bg-gradient-to-b from-[#FFEE9F] to-[#EFA633]";
      } else if (quantity < 11) {
        label = "Archivist";
        bgColor = 'bg-gradient-to-b from-[#9FF7C4] to-[#71D891]';
      } else if (quantity < 21) {
        label = "Expert";
        bgColor = 'bg-gradient-to-b from-[#C597F1] to-[#8354C6]';
      } else if (quantity >= 21) {
        label = "Master";
        bgColor = "bg-gradient-to-b from-[#adf1fd] to-[#125379]";
      }
      break;
    } 

    case "completionist": {
      const quantity = props.completedQuantity;

      if (quantity < 1) {
        label = "Paper Completionist";
        // bgColor = "bg-gradient-to-b from-[#FDF6EC] to-[#FAE2C2]";
        bgColor = "invisible"
      } else if (quantity < 11) {
        label = "Bronce Completionist";
        bgColor = 'bg-gradient-to-b from-[#FEB26F] to-[#CD7638]';
      } else if (quantity < 31) {
        label = "Iron Completionist";
        bgColor = "bg-gradient-to-b from-[#C9D6DE] to-[#9EBFC6]";
      } else if (quantity < 51) {
        label = "Gold Completionist";
        bgColor = "bg-gradient-to-b from-[#FFEE9F] to-[#EFA633]";
      } else if (quantity < 101) {
        label = "Diamond Completionist";
        bgColor = "bg-gradient-to-b from-[#adf1fd] to-[#125379]";
      } else if(quantity >= 101){
        label = "Divine Completionist";
        bgColor = "divine-gradient animate-divine-flow";
      }
      break;
    }

    case "wisher": {
      const quantity = props.wishlistQuantity;

      if (quantity < 1) {
        label = "hide";
        bgColor = "invisible";
      } else if (quantity < 11) {
        label = "Explorer";
        bgColor = 'bg-gradient-to-b from-[#A8E063] to-[#56AB2F]';
      } else if (quantity < 31) {
        label = "Interested Wisher";
        bgColor = "bg-gradient-to-b from-[#FF8C00] to-[#F80759]";
      } else if (quantity < 71) {
        label = "Releases Hunter";
        bgColor = "bg-gradient-to-b from-[#00D2FF] to-[#3A7BD5]";
      } else if (quantity < 151) {
        label = "Visionary";
        bgColor = "bg-gradient-to-b from-[#8E2DE2] to-[#4A00E1]";
      } else if(quantity >= 151){
        label = "Oracle";
        bgColor = "legend-gradient animate-legend-flow";
      }
      break;
    }
    
    case "player": {
      const quantity = props.libraryQuantity;

      if (quantity < 1) {
        label = "hide";
        bgColor = "invisible";
      } else if (quantity < 11) {
        label = "Casual";
        bgColor = 'bg-gradient-to-b from-[#A8E063] to-[#56AB2F]';
      } else if (quantity < 51) {
        label = "Usual Player";
        bgColor = "bg-gradient-to-b from-[#FF8C00] to-[#F80759]";
      } else if (quantity < 151) {
        label = "Dedicated Gamer";
        bgColor = "bg-gradient-to-b from-[#00D2FF] to-[#3A7BD5]";
      } else if (quantity < 301) {
        label = "Veteran";
        bgColor = "bg-gradient-to-b from-[#8E2DE2] to-[#4A00E1]";
      } else if(quantity >= 301){
        label = "Legend";
        bgColor = "legend-gradient animate-legend-flow";
      }
      break;
    }
    case "role":
      label = props.role;
      bgColor =
        props.role?.toLowerCase() === "admin"
          ? "bg-gradient-to-t from-[#92400e] via-[#f59e0b] to-[#fef3c7]"
          : "bg-gradient-to-t from-[#2563eb] via-[#38bdf8] to-[#93c5fd]";
      break;
  }

  return { label, bgColor };
});

</script>

<style scoped>

</style>