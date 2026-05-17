<template>
  <span
    :class="['px-3 py-1 text-xs rounded-full border border-gsoscuro/20 text-gsoscuro font-bold tracking-wide uppercase shadow-sm', badge.bgColor]">
    {{ badge.label }}
  </span>
</template>

<script setup lang="ts">
import { computed } from 'vue';

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

  switch (props.nombre) {
    case "collectionist": {
      const quantity = props.collectionsQuantity ?? 0;

      if (quantity < 1) {
        label = "hide";
        bgColor = "hidden";
      } else if (quantity < 3) {
        label = "Rookie";
        bgColor = 'bg-gradient-to-b from-[#FFD5B4] to-[#FFA768]';
      } else if (quantity < 6) {
        label = "Apprentice";
        bgColor = 'bg-gradient-to-b from-[#FFF7CC] to-[#FFDF7A]';
      } else if (quantity < 11) {
        label = "Archivist";
        bgColor = 'bg-gradient-to-b from-[#D4FFE6] to-[#99FFBB]';
      } else if (quantity < 21) {
        label = "Expert";
        bgColor = 'bg-gradient-to-b from-[#EAD6FF] to-[#CDA3FF]';
      } else if (quantity >= 21) {
        label = "Master";
        bgColor = 'bg-gradient-to-b from-[#E0FAFF] to-[#99EFFF]';
      }
      break;
    }

    case "completionist": {
      const quantity = props.completedQuantity ?? 0;

      if (quantity < 1) {
        label = "Paper Completionist";
        bgColor = "hidden";
      } else if (quantity < 11) {
        label = "Bronce Completionist";
        bgColor = 'bg-gradient-to-b from-[#FFD5B4] to-[#FFA768]';
      } else if (quantity < 31) {
        label = "Iron Completionist";
        bgColor = 'bg-gradient-to-b from-[#EDF4F8] to-[#CBDCE6]';
      } else if (quantity < 51) {
        label = "Gold Completionist";
        bgColor = 'bg-gradient-to-b from-[#FFF7CC] to-[#FFDF7A]';
      } else if (quantity < 101) {
        label = "Diamond Completionist";
        bgColor = 'bg-gradient-to-b from-[#E0FAFF] to-[#99EFFF]';
      } else if (quantity >= 101) {
        label = "Divine Completionist";
        bgColor = "divine-gradient animate-divine-flow";
      }
      break;
    }
    case "wisher": {
      const quantity = props.wishlistQuantity ?? 0;

      if (quantity < 1) {
        label = "hide";
        bgColor = "hidden";
      } else if (quantity < 11) {
        label = "Explorer";
        bgColor = 'bg-gradient-to-b from-[#E6FFA8] to-[#C9FF4D]';
      } else if (quantity < 31) {
        label = "Interested Wisher";
        bgColor = 'bg-gradient-to-b from-[#FFDBB5] to-[#FF8FAB]';
      } else if (quantity < 71) {
        label = "Releases Hunter";
        bgColor = 'bg-gradient-to-b from-[#B5F5FF] to-[#7AB8FF]';
      } else if (quantity < 151) {
        label = "Visionary";
        bgColor = 'bg-gradient-to-b from-[#E5D4FF] to-[#B08AFF]';
      } else if (quantity >= 151) {
        label = "Oracle";
        bgColor = "legend-gradient animate-legend-flow";
      }
      break;
    }

    case "player": {
      const quantity = props.libraryQuantity ?? 0;

      if (quantity < 1) {
        label = "hide";
        bgColor = "hidden";
      } else if (quantity < 11) {
        label = "Casual";
        bgColor = 'bg-gradient-to-b from-[#E6FFA8] to-[#C9FF4D]';
      } else if (quantity < 51) {
        label = "Usual Player";
        bgColor = 'bg-gradient-to-b from-[#FFDBB5] to-[#FF8FAB]';
      } else if (quantity < 151) {
        label = "Dedicated Gamer";
        bgColor = 'bg-gradient-to-b from-[#B5F5FF] to-[#7AB8FF]';
      } else if (quantity < 301) {
        label = "Veteran";
        bgColor = 'bg-gradient-to-b from-[#E5D4FF] to-[#B08AFF]';
      } else if (quantity >= 301) {
        label = "Legend";
        bgColor = "legend-gradient animate-legend-flow";
      }
      break;
    }

    case "role":
      if (!props.role) break;

      label = props.role;

      bgColor =
        props.role?.toLowerCase() === "admin"
          ? "bg-gradient-to-b from-[#FFEAA8] to-[#FFCD43]"
          : "bg-gradient-to-b from-[#D1E4FF] to-[#70A5FF]";
      break;
  }

  return { label, bgColor };
});
</script>