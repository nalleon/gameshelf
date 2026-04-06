import { defineStore } from 'pinia'
import type { User } from '@/types/authTypes'

interface AuthState {
  user: string | null
  token: string | null
}

export const useAuthStore = defineStore('auth', {

  state: (): AuthState => ({
    user: null,
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
    
    login(user: string, token: string) {
      this.user = user
      this.token = token
      localStorage.setItem('token', token) // persistencia simple
    },
    
    logout() {
      this.user = null
      this.token = null
      localStorage.removeItem('token')
    }
  }
})