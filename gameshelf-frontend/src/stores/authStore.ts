import { defineStore } from 'pinia'
import type { User } from '@/types/authTypes'

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
    }
  }
})