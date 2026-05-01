import { defineStore } from 'pinia'
import type { Game } from '@/types/gameListTypes'

interface GamesState {
    games: Array<Game> | null
}

export const useGameStore = defineStore('game', {

    state: (): GamesState => ({
        games: null
    }),

    getters: {
        gamesLoaded: (state): boolean => !!state.games
    },

    actions: {

        setGamesCache(games: Array<Game>) {
            this.games = games;
            localStorage.setItem('gameList', JSON.stringify(games))
        },

        removeGameCache() {
            this.games = null
            localStorage.removeItem('gameList')
        }
    }
})