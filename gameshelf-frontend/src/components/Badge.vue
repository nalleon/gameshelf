<template>
  <span
    :class="['px-3 py-1 text-xs rounded-full border border-gsgris/50 text-gsoscuro font-bold tracking-wide uppercase', badge.bgColor]">
    {{ badge.label }}
  </span>
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
      const quantity = props.collectionsQuantity ?? 0;

      if (quantity < 1) {
        label = "hide";
        bgColor = "hidden";
      } else if (quantity < 3) {
        label = "Rookie";
        bgColor = 'bg-gradient-to-b from-[#FFC08A]/70 to-[#E1843F]/70';
      } else if (quantity < 6) {
        label = "Apprentice";
        bgColor = 'bg-gradient-to-b from-[#FFF1B3]/70 to-[#F2B84A]/70';
      } else if (quantity < 11) {
        label = "Archivist";
        bgColor = 'bg-gradient-to-b from-[#B8FAD8]/70 to-[#7FE4A1]/70';
      } else if (quantity < 21) {
        label = "Expert";
        bgColor = 'bg-gradient-to-b from-[#D7B7F7]/70 to-[#9A6DD9]/70';
      } else if (quantity >= 21) {
        label = "Master";
        bgColor = 'bg-gradient-to-b from-[#C7F6FF]/70 to-[#2A7FA8]/70';
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
        bgColor = 'bg-gradient-to-b from-[#FFC08A]/70 to-[#E1843F]/70';
      } else if (quantity < 31) {
        label = "Iron Completionist";
        bgColor = 'bg-gradient-to-b from-[#D6E2E8]/70 to-[#A8C4CC]/70';
      } else if (quantity < 51) {
        label = "Gold Completionist";
        bgColor = 'bg-gradient-to-b from-[#FFF1B3]/70 to-[#F2B84A]/70';
      } else if (quantity < 101) {
        label = "Diamond Completionist";
        bgColor = 'bg-gradient-to-b from-[#C7F6FF]/70 to-[#2A7FA8]/70';
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
        bgColor = 'bg-gradient-to-b from-[#B7F58C]/70 to-[#67C93C]/70';
      } else if (quantity < 31) {
        label = "Interested Wisher";
        bgColor = 'bg-gradient-to-b from-[#FFB15C]/70 to-[#FF3D7F]/70';
      } else if (quantity < 71) {
        label = "Releases Hunter";
        bgColor = 'bg-gradient-to-b from-[#3FE0FF]/70 to-[#4A8BFF]/70';
      } else if (quantity < 151) {
        label = "Visionary";
        bgColor = 'bg-gradient-to-b from-[#B07CFF]/70 to-[#5A2CFF]/70';
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
        bgColor = 'bg-gradient-to-b from-[#B7F58C]/70 to-[#67C93C]/70';
      } else if (quantity < 51) {
        label = "Usual Player";
        bgColor = 'bg-gradient-to-b from-[#FFB15C]/70 to-[#FF3D7F]/70';
      } else if (quantity < 151) {
        label = "Dedicated Gamer";
        bgColor = 'bg-gradient-to-b from-[#3FE0FF]/70 to-[#4A8BFF]/70';
      } else if (quantity < 301) {
        label = "Veteran";
        bgColor = 'bg-gradient-to-b from-[#B07CFF]/70 to-[#5A2CFF]/70';
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
          ? "bg-gradient-to-t from-[#A66A1A]/80 via-[#F6C453]/70 to-[#FFF1C2]/80"
          : "bg-gradient-to-t from-[#3A7DFF]/80 via-[#60C8FF]/70 to-[#B5DDFF]/80";
      break;
  }

  return { label, bgColor };
});

</script>

<style scoped></style>