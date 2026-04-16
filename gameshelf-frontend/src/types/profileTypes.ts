// User Interfaces
export interface Profile {
    id: number,
    user: User,
    avatar: string,
    bio: string,
    verified: boolean,
    role: string
}

export interface User {
    id: number,
    username: string,
    first_name: string,
    last_name: string,
    email: string,
    collections: Array<Collection>
    library: Array<LibraryItem>
    wishlist: Wishlist
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
    annotation: string,
    is_private: boolean,
    game: Game
}

export interface LibraryItem {
    id: number
    game: Game,
    status: string,
    hours_played: string,
    created_at: string,
    updated_at: string,
}

export interface Game {
    id: number,
    title: string,
    slug: string,
    description: string,
    cover_default: string,
    edition: Edition,
    region: Region,
}

export interface Edition {
    id: number,
    name: string,
    slug: string,
    description: string,
}

export interface Region {
    id: number,
    name: string,
    slug: string,
    description: string,
    acronym: string,
}
