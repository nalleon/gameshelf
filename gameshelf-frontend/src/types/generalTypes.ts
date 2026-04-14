// User Interfaces
export interface User {
    id: number,
    username: string,
    first_name: string,
    last_name: string,
    email: string
}

export interface Profile {
    id: number,
    user: User,
    avatar: string,
    bio: string,
    verified: boolean,
    role: string
}

// Game interfaces
export interface Game {
    title: string
    slug: string
}
