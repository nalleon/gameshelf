<template>
    <span :class="['px-3 py-1 text-xs rounded-md border border-gsgris/50 text-gsoscuro', bgColor]">{{ label }}</span>
</template>

<script setup lang="ts">
import { computed, onMounted } from 'vue';

type Props =
  | { nombre: 'collectionist'; collectionsQuantity: number }
  | { nombre: 'wisher'; wishlistQuantity: number }
  | { nombre: 'player'; libraryQuantity: number }
  | { nombre: 'completionist'; completedQuantity: number }
  | { nombre: 'role'; role: string }

const props = defineProps<Props>()

const label = computed(() => {
  switch(props.nombre){
        case "collectionist":
            if(props.collectionsQuantity < 1){
                return "Newbie Collectionist"
            } 

            if(props.collectionsQuantity >= 1 && props.collectionsQuantity < 50){
                return "Standard Collectionist"
            }

            if(props.collectionsQuantity >= 50 && props.collectionsQuantity < 100){
                return "Valuable Collectionist"
            }

            if(props.collectionsQuantity >= 100 && props.collectionsQuantity < 200){
                return "Pro Collectionist"
            }

            if(props.collectionsQuantity >= 200 && props.collectionsQuantity < 300){
                return "Divine Collectionist"
            }

            if(props.collectionsQuantity > 500 ){
                return "??? Collectionist"
            }
            return
        case "wisher":
            return "New Wisher"
        case "player":  
            return "New Player"
        case "completionist":
            if(props.completedQuantity < 1){
                return "Paper Completionist"
            } 

            if(props.completedQuantity >= 1 && props.completedQuantity < 10){
                return "Bronce Completionist"
            }

            if(props.completedQuantity >= 10 && props.completedQuantity < 30){
                return "Iron Completionist"
            }

            if(props.completedQuantity >= 30 && props.completedQuantity < 50){
                return "Gold Completionist"
            }

            if(props.completedQuantity >= 50 && props.completedQuantity < 100){
                return "Diamond Completionist"
            }

            if(props.completedQuantity >= 100 ){
                return "Divine Completionist"
            }
            return
        case "role":
            return props.role;
    }
})

const bgColor = computed(() => {
  switch (props.nombre) {
    case "collectionist":
        return 'bg-gsgris'

    case "wisher":
        return 'bg-gsgris'

    case "player":  
        return 'bg-gsgris'

    case "completionist":
        return 'bg-gsgris'

    case 'role':
        return props.role?.toLowerCase() === 'admin'
            ? 'bg-amber-400'
            : 'bg-cyan-300'
  }
})

</script>

<style scoped>

</style>