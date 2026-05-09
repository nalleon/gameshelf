export interface Game {
    id: number,
    title: string,
    slug: string,
    description: string,
    cover_default: string,
    cover_detail: string,
    released_at: Date,
    genres: Array<Genre>,
    // edition: Edition,
    region: Region,
}

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