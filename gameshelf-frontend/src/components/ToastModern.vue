<template>
    <transition name="toast-modern">
        <div v-if="message"
            class="fixed top-6 right-6 z-50 flex items-center gap-4 p-4 rounded-2xl border bg-gsoscuro/80 backdrop-blur-md shadow-[0_20px_50px_rgba(0,0,0,0.5)] min-w-[320px] overflow-hidden"
            :style="{ borderColor: `${color}30` }">
            
            <div class="shrink-0 w-10 h-10 rounded-xl flex items-center justify-center shadow-[0_0_15px_rgba(0,0,0,0.2)]"
                :style="{ backgroundColor: `${color}20`, color: color }">
                <slot name="icon">
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24"
                        stroke="currentColor" stroke-width="3">
                        <path stroke-linecap="round" stroke-linejoin="round" d="M5 13l4 4L19 7" />
                    </svg>
                </slot>
            </div>

            <div class="grow">
                <p class="text-gsblanco font-bold text-sm leading-tight">{{ title }}</p>
                <p class="text-gsgris text-xs mt-0.5">{{ message }}</p>
            </div>

            <button @click="uiStore.clearSuccess()"
                class="text-gsgris hover:text-gsblanco transition-colors p-1 cursor-pointer">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24"
                    stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
                </svg>
            </button>

            <div class="absolute bottom-0 left-0 h-[3px] shadow-[0_0_10px_rgba(0,0,0,0.5)] progress-bar"
                :style="{ backgroundColor: color, '--anim-duration': `${duration}ms` }"></div>
        </div>
    </transition>
</template>

<script setup lang="ts">
import { watch, computed, onMounted, onUnmounted } from 'vue';
import { useUiStore } from '@/stores/uiStore';

interface Props {
    title: string;
    color?: string;
    duration?: number;
}

const props = withDefaults(defineProps<Props>(), {
    color: '#79a998',
    duration: 3000,
});

defineEmits(['close']);

const uiStore = useUiStore();
const message = computed(() => uiStore.flashSuccessMessage);
const color = computed(() => uiStore.flashSuccessColor);

let timer: ReturnType<typeof setTimeout> | null = null;

const startTimer = () => {
    if (timer) clearTimeout(timer);
    timer = setTimeout(() => uiStore.clearSuccess(), props.duration);
};

onMounted(() => {
    if (message.value) startTimer();  
});

watch(message, (val) => {
    if (val) startTimer();
});

onUnmounted(() => {
    if (timer) clearTimeout(timer);
    uiStore.clearSuccess();
});
</script>

<style scoped>
.toast-modern-enter-active,
.toast-modern-leave-active {
    transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
}

.toast-modern-enter-from {
    opacity: 0;
    transform: translateY(-20px) scale(0.95);
}

.toast-modern-leave-to {
    opacity: 0;
    transform: translateY(10px) scale(0.95);
}

@keyframes progress {
    from { width: 100%; }
    to { width: 0%; }
}

.progress-bar {
    /* Usamos la Variable CSS inyectada desde el template, con 3000ms de respaldo */
    animation: progress var(--anim-duration, 3000ms) linear forwards;
}
</style>