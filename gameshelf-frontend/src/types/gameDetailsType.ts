import type { User } from "./profileTypes"

export interface Game {
    id: number,
    title: string,
    slug: string,
    description: string,
    cover_default: string,
    cover_detail: string,
    released_at: Date,
    age_rating: string,
    mature_content: boolean,
    platforms: Array<Platform>,
    genres: Array<Genre>,
    developers: Array<Developer>,
    publishers: Array<Publisher>,
    // edition: Edition,
    region: Region,
    reviews: Array<Review>,
}

// Game Details
export interface Genre {
    id: number,
    name: string,
    slug: string,
    description: string,
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

export interface Platform {
    id: number,
    name: string,
    slug: string,
    slug_aliases: string,
}

// Extra info
export interface Developer {
    id: number,
    name: string,
    slug: string,
}

export interface Publisher {
    id: number,
    name: string,
    slug: string,
}

// Reviews
export interface Review {
    id: number,
    content: string,
    recommend: boolean,
    author: User,
    media: Array<Media>,
    created_at: string,
    updated_at: string,
}

export interface Media {
    id: number,
    image: string
}