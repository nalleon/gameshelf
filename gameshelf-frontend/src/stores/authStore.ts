import { defineStore } from 'pinia'
import { jwtDecode } from 'jwt-decode'
import { useSearchStore } from './searchStore' // 1. Importa tu store de búsqueda (ajusta la ruta)

interface AuthState {
  token: string | null
}

export const useAuthStore = defineStore('auth', {

  state: (): AuthState => ({
    token: null
  }),

  getters: {
    isLogged: (state): boolean => !!state.token
  },

  actions: {
    init() {
      const token = localStorage.getItem('token')
      if (token) this.token = token
    },
    
    setUserSesion(token: string) {
      this.token = token
      localStorage.setItem('token', token)
    },
    
    removeUserSesion() {
      this.token = null
      localStorage.removeItem('token')
      
      // Search Store 
      const searchStore = useSearchStore()
      searchStore.searchType = 'games' // Valor por defecto
    },

    getSelfId(){
      if (!this.token) return 0

      try {
        const decoded = jwtDecode<{ user_id: string | number }>(this.token)

        const tokenUserId = Number(decoded.user_id)

        return tokenUserId;

      } catch (e) {
        console.error("Token no válido", e)
        return false
      }
    },

    isOwnProfile(id: number): boolean {
      if (!this.token) return false
      
      try {
        const decoded = jwtDecode<{ user_id: string | number }>(this.token)

        const tokenUserId = Number(decoded.user_id)
        return tokenUserId === id

      } catch (e) {
        console.error("Token no válido", e)
        return false
      }
    }
  }
})