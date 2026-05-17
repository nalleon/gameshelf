import { defineStore } from 'pinia';
import { ref } from 'vue';

export const useUiStore = defineStore('ui', () => {
    const flashSuccessMessage = ref<string | null>(null);

    function triggerSuccess(message: string) {
        flashSuccessMessage.value = message;
    }

    function clearSuccess() {
        flashSuccessMessage.value = null;
    }

    return { flashSuccessMessage, triggerSuccess, clearSuccess };
});