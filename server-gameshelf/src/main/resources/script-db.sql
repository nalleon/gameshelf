CREATE TABLE `roles` (
    id INTEGER AUTO_INCREMENT NOT NULL,
    name VARCHAR(45) UNIQUE NOT NULL,
    CONSTRAINT `pk_roles` PRIMARY KEY (id)
);

INSERT INTO `roles` (`name`) VALUES 
    ('ROLE_ADMIN'),
    ('ROLE_USER');

CREATE TABLE `users` (
    id INTEGER AUTO_INCREMENT NOT NULL,
    username VARCHAR(45) UNIQUE NOT NULL,
    password CHAR(200) NOT NULL,
    email CHAR(100) UNIQUE NOT NULL,
    role_id INTEGER,
    verified TINYINT(1) DEFAULT 0,
    verification_token CHAR(255),
    creation_date BIGINT NOT NULL,
    profile_picture CHAR(255) NULL,
    CONSTRAINT `pk_users` PRIMARY KEY (id),
    CONSTRAINT `fk_users_roles` FOREIGN KEY (role_id) REFERENCES roles(id)
);

INSERT INTO `users` (
    `username`,
    `password`,
    `email`,
    `role_id`,
    `verified`,
    `verification_token`,
    `creation_date`,
    `profile_picture`
) VALUES 
    (
        'nalleon',
        '$2a$10$P0fZ.FcD.rBwolLS9P5bAOZETI3K9E5JsiE/NQC82HgkXccYnFvry',
        'nlamail1529@gmail.com',
        1,
        1,
        'readumineko',
        UNIX_TIMESTAMP(),
        NULL
    ),
    (
        'jeristance',
        '$2a$10$P0fZ.FcD.rBwolLS9P5bAOZETI3K9E5JsiE/NQC82HgkXccYnFvry',
        'nabil14716@gmail.com',
        2,
        1,
        'ef34fd1b-c8da-4397-9d7e-06b554a2d617',
        UNIX_TIMESTAMP(),
        NULL
    );

CREATE TABLE `games` (
    id INTEGER AUTO_INCREMENT NOT NULL,
    title CHAR(100) NOT NULL,
    release_date CHAR(100) NULL,
    slug CHAR(100) NOT NULL,
    cover CHAR(255) NULL,
    external_rating INTEGER NULL,
    CONSTRAINT `pk_games` PRIMARY KEY (id),
    UNIQUE KEY `uq_games_title_slug` (title, slug)
);

CREATE TABLE `platforms` (
    id INTEGER AUTO_INCREMENT NOT NULL,
    name VARCHAR(50) UNIQUE NOT NULL,
    CONSTRAINT `pk_platforms` PRIMARY KEY (id),
    UNIQUE KEY `uq_platforms_name` (name)
);

CREATE TABLE `games_platforms` (
    id INTEGER AUTO_INCREMENT NOT NULL,
    game_id INTEGER NOT NULL,
    platform_id INTEGER NOT NULL,
    CONSTRAINT `pk_games_platforms` PRIMARY KEY (id),
    CONSTRAINT `fk_games_platforms_game` FOREIGN KEY (game_id) REFERENCES games(id),
    CONSTRAINT `fk_games_platforms_platform` FOREIGN KEY (platform_id) REFERENCES platforms(id),
    UNIQUE KEY `uq_games_platforms` (game_id, platform_id)
);

CREATE TABLE `regions` (
    id INTEGER AUTO_INCREMENT NOT NULL,
    name VARCHAR(50) UNIQUE NOT NULL,
    initials CHAR(4) UNIQUE NOT NULL,
    CONSTRAINT `pk_regions` PRIMARY KEY (id),
    UNIQUE KEY `uq_regions_name` (name)
);


CREATE TABLE `edition` (
    id INTEGER AUTO_INCREMENT NOT NULL,
    name VARCHAR(100) UNIQUE NOT NULL,
    description VARCHAR(255) UNIQUE NOT NULL,
    CONSTRAINT `pk_editions` PRIMARY KEY (id),
    UNIQUE KEY `uq_editions_name` (name)
);


CREATE TABLE `status` (
    id INTEGER AUTO_INCREMENT NOT NULL,
    name VARCHAR(50) UNIQUE NOT NULL,
    description VARCHAR(255) UNIQUE NOT NULL,
    CONSTRAINT `pk_regions` PRIMARY KEY (id),
    UNIQUE KEY `uq_regions_name` (name)
);

CREATE TABLE `publishers` (
    id INTEGER AUTO_INCREMENT NOT NULL,
    name VARCHAR(50) UNIQUE NOT NULL,
    CONSTRAINT `pk_publisher` PRIMARY KEY (id),
    UNIQUE KEY `uq_publisher_name` (name)
);

CREATE TABLE `games_publishers` (
    id INTEGER AUTO_INCREMENT NOT NULL,
    game_id INTEGER NOT NULL,
    publisher_id INTEGER NOT NULL,
    CONSTRAINT `pk_games_publishers` PRIMARY KEY (id),
    CONSTRAINT `fk_games_publishers1` FOREIGN KEY (game_id) REFERENCES games(id),
    CONSTRAINT `fk_games_publishers2` FOREIGN KEY (publisher_id) REFERENCES publishers(id),
    UNIQUE KEY `uq_games_publishers` (game_id, publisher_id)
);


CREATE TABLE `developers` (
    id INTEGER AUTO_INCREMENT NOT NULL,
    name VARCHAR(50) UNIQUE NOT NULL,
    CONSTRAINT `pk_developers` PRIMARY KEY (id),
    UNIQUE KEY `uq_developers_name` (name)
);

CREATE TABLE `games_developers` (
    id INTEGER AUTO_INCREMENT NOT NULL,
    game_id INTEGER NOT NULL,
    developers_id INTEGER NOT NULL,
    CONSTRAINT `pk_games_developers` PRIMARY KEY (id),
    CONSTRAINT `fk_games_developers1` FOREIGN KEY (game_id) REFERENCES games(id),
    CONSTRAINT `fk_games_developers2` FOREIGN KEY (developers_id) REFERENCES developers(id),
    UNIQUE KEY `uq_games_developers` (game_id, developers_id)
);

CREATE TABLE `genres` (
    id INTEGER AUTO_INCREMENT NOT NULL,
    name VARCHAR(50) UNIQUE NOT NULL,
    CONSTRAINT `pk_genres` PRIMARY KEY (id)
);

CREATE TABLE `games_genres` (
    id INTEGER AUTO_INCREMENT NOT NULL,
    game_id INTEGER NOT NULL,
    genre_id INTEGER NOT NULL,
    CONSTRAINT `pk_games_genres` PRIMARY KEY (id),
    CONSTRAINT `fk_games_genres_game` FOREIGN KEY (game_id) REFERENCES games(id),
    CONSTRAINT `fk_games_genres_genre` FOREIGN KEY (genre_id) REFERENCES genres(id),
    UNIQUE KEY `uq_games_genres` (game_id, genre_id)
);

CREATE TABLE reviews (
    id INT AUTO_INCREMENT NOT NULL,
    game_id INT NOT NULL,
    user_id INT NOT NULL,
    content TEXT NOT NULL,
    creation_date BIGINT NOT NULL,
    last_update_date BIGINT,
    CONSTRAINT pk_reviews PRIMARY KEY (id),
    CONSTRAINT fk_reviews_game FOREIGN KEY (game_id) REFERENCES games(id),
    CONSTRAINT fk_reviews_user FOREIGN KEY (user_id) REFERENCES users(id)
);

CREATE TABLE photo_reviews (
    id INT AUTO_INCREMENT NOT NULL,
    review_id INT NOT NULL,
    name VARCHAR(255) NOT NULL,
    additional_text TEXT,
    type VARCHAR(50),
    CONSTRAINT pk_photo_reviews PRIMARY KEY (id),
    CONSTRAINT fk_photo_reviews_review FOREIGN KEY (review_id) REFERENCES reviews(id)
);

CREATE TABLE `collections` (
    id INTEGER AUTO_INCREMENT NOT NULL,
    user_id INTEGER NOT NULL,
    CONSTRAINT `pk_collections` PRIMARY KEY (id),
    CONSTRAINT `fk_collections2` FOREIGN KEY (user_id) REFERENCES users(id)
);

CREATE TABLE `games_collections` (
    id INTEGER AUTO_INCREMENT NOT NULL,
    game_id INTEGER NOT NULL,
    collection_id INTEGER NOT NULL,
    region_id INTEGER NOT NULL,
    platform_id INTEGER NOT NULL,
    CONSTRAINT `pk_games_collections` PRIMARY KEY (id),
    CONSTRAINT `fk_games_collections_games` FOREIGN KEY (game_id) REFERENCES games(id),
    CONSTRAINT `fk_games_collections_collections` FOREIGN KEY (collection_id) REFERENCES collections(id),
    CONSTRAINT `fk_games_collections_regions` FOREIGN KEY (region_id) REFERENCES regions(id),
    CONSTRAINT `fk_games_collections_platforms` FOREIGN KEY (platform_id) REFERENCES platforms(id)
);

CREATE TABLE `favorites` (
    id INTEGER AUTO_INCREMENT NOT NULL,
    game_id INTEGER NOT NULL,
    user_id INTEGER NOT NULL,
    CONSTRAINT `pk_favorites` PRIMARY KEY (id),
    CONSTRAINT `fk_favorites` FOREIGN KEY (game_id) REFERENCES games(id),
    CONSTRAINT `fk_favorites2` FOREIGN KEY (user_id) REFERENCES users(id),
    UNIQUE KEY `uq_favorites` (game_id, user_id)
);
