import type { Game } from "./gameListTypes"

// User Interfaces
export interface Profile {
    id: number,
    user: User,
    avatar: string,
    bio: string,
    verified: boolean,
    role: string,
    color_bg: string,
}

export interface User {
    id: number,
    username: string,
    first_name: string,
    last_name: string,
    email: string,
    favorites: Array<FavoriteItem>,
    collections: Array<Collection>
    library: Library
    wishlist: Wishlist
    avatar: string
}

export interface FavoriteItem {
    id: number,
    platform: Platform,
    game: Game
}

export interface Collection {
    id: number,
    name: string,
    is_private: boolean,
    created_at: Date,
    items: Array<CollectionItem>
}

export interface CollectionItem{
    id: number,
    is_private: boolean,
    platform: Platform,
    type: string,
    game: Game
}

export interface Wishlist {
    id: number,
    name: string,
    is_private: boolean,
    created_at: Date,
    items: Array<WishlistItem>
}

export interface WishlistItem{
    id: number,
    priority: number,
    type: string,
    annotation: string,
    is_private: boolean,
    game: Game,
    platform: Platform,
}

export interface Library {
    id: number
    is_private: boolean,
    created_at: string,
    updated_at: string,
    items: Array<LibraryItem>
}

export interface LibraryItem {
    id: number
    game: Game,
    platform: Platform,
    status: string,
    is_private: boolean,
    hours_played: number,
    created_at: string,
    updated_at: string,
}

export interface Platform {
    id: number,
    name: string,
    slug: string,
}
