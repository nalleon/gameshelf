import { defineStore } from 'pinia';
import { ref } from 'vue';

export const useUiStore = defineStore('ui', () => {
    // uiStore.ts
    const flashSuccessMessage = ref<string | null>(null);
    const flashSuccessColor = ref<string>('#79a998');

    function triggerSuccess(message: string, color = '#79a998') {
        flashSuccessMessage.value = message;
        flashSuccessColor.value = color;
    }

    function clearSuccess() {
        flashSuccessMessage.value = null;
        flashSuccessColor.value = '#79a998';
    }

    return { flashSuccessMessage, flashSuccessColor, triggerSuccess, clearSuccess };
});