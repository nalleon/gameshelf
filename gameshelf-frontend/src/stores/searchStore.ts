import { defineStore } from 'pinia'
import { ref, watch } from 'vue'

export const useSearchStore = defineStore('search', () => {
    const searchType = ref<'games' | 'users'>(
        (localStorage.getItem('searchType') as 'games' | 'users') || 'games'
    )

    watch(searchType, (value) => {
        localStorage.setItem('searchType', value)
    })

    return {
        searchType
    }
})