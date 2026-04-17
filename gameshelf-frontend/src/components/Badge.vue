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
                return "Epic Collectionist"
            }

            if(props.collectionsQuantity >= 500 ){
                return "Divine Collectionist"
            }

            if(props.collectionsQuantity >= 1000 ){
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
            return ""
        case "role":
            return props.role;
    }
})

const bgColor = computed(() => {
    switch (props.nombre) {
        case "collectionist":
            if(props.collectionsQuantity < 1){
                return "bg-gsgris"
            }

            if(props.collectionsQuantity >= 1 && props.collectionsQuantity < 50){
                return 'bg-gradient-to-b from-[#FEB26F] to-[#CD7638]'
            }

            if(props.collectionsQuantity >= 50 && props.collectionsQuantity < 100){
                return "bg-gradient-to-b from-[#FFEE9F] to-[#EFA633]"
            }
            
            if(props.collectionsQuantity >= 100 && props.collectionsQuantity < 200){
                return 'bg-gradient-to-b from-[#9FF7C4] to-[#71D891]'
            }

            if(props.collectionsQuantity >= 200 && props.collectionsQuantity < 300){
                return 'bg-gradient-to-b from-[#C597F1] to-[#8354C6]'
            }

            if(props.collectionsQuantity >= 500 ){
                return "bg-gradient-to-b from-[#adf1fd] to-[#125379]"   // Diamond 
            }

            if(props.collectionsQuantity >= 1000 ){
                return "??? Collectionist"
            }
            return 'bg-gsgris'

        case "wisher":
            return 'bg-gsgris'

        case "player":  
            return 'bg-gsgris'

        case "completionist":
            if(props.completedQuantity < 1){
                return "bg-gradient-to-b from-[#FDF6EC] to-[#FAE2C2]" // Paper
            } 

            if(props.completedQuantity >= 1 && props.completedQuantity < 10){
                return 'bg-gradient-to-b from-[#FEB26F] to-[#CD7638]' // Bronze
            }

            if(props.completedQuantity >= 10 && props.completedQuantity < 30){
                return "bg-gradient-to-b from-[#C9D6DE] to-[#9EBFC6]"   // Iron
            }

            if(props.completedQuantity >= 30 && props.completedQuantity < 50){
                return "bg-gradient-to-b from-[#FFEE9F] to-[#EFA633]"   // Gold
            }

            if(props.completedQuantity >= 50 && props.completedQuantity < 100){
                return "bg-gradient-to-b from-[#adf1fd] to-[#125379]"   // Diamond 
            }

            if(props.completedQuantity >= 100 ){
                // return "divine-gradient animate-divine-flow animate-shimmer"
                return "divine-gradient animate-divine-flow"
            }
            return "bg-gsgris"

        case 'role':
            return props.role?.toLowerCase() === 'admin'
                ? 'bg-gradient-to-t from-[#92400e] via-[#f59e0b] to-[#fef3c7]'
                : 'bg-gradient-to-t from-[#2563eb] via-[#38bdf8] to-[#93c5fd]'
    }
})

</script>

<style scoped>

</style>