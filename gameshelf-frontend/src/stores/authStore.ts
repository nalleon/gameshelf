import { defineStore } from 'pinia'
import { jwtDecode } from 'jwt-decode'

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