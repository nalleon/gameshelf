-- 2 usuarios administradores (is_staff=1, is_superuser=1)
INSERT INTO auth_user 
    (password, last_login, is_superuser, username, first_name, last_name, email, is_staff, is_active, date_joined)
VALUES
(
    'pbkdf2_sha256$1200000$eHNQ1hvwvwusEKWkDCzDDP$735p5QbkaNd3NXoMjaVIePwL4/l8U4jEFNaVimonHyc=',
    NULL, 1, 'admin2', 'Carlos', 'García', 'admin2@example.com', 1, 1, datetime('now')
), -- Pk 2
(
    'pbkdf2_sha256$1200000$eHNQ1hvwvwusEKWkDCzDDP$735p5QbkaNd3NXoMjaVIePwL4/l8U4jEFNaVimonHyc=',
    NULL, 1, 'admin3', 'Lucas', 'López', 'admin3@example.com', 1, 1, datetime('now')
), -- Pk 3
(
    'pbkdf2_sha256$1200000$eHNQ1hvwvwusEKWkDCzDDP$735p5QbkaNd3NXoMjaVIePwL4/l8U4jEFNaVimonHyc=',
    NULL, 0, 'juan', 'Juan', 'Martínez', 'juan@example.com', 0, 1, datetime('now')
), -- Pk 4
(
    'pbkdf2_sha256$1200000$eHNQ1hvwvwusEKWkDCzDDP$735p5QbkaNd3NXoMjaVIePwL4/l8U4jEFNaVimonHyc=',
    NULL, 0, 'ana', 'Ana', 'Rodríguez', 'ana@example.com', 0, 1, datetime('now')
), -- Pk 5
(
    'pbkdf2_sha256$1200000$eHNQ1hvwvwusEKWkDCzDDP$735p5QbkaNd3NXoMjaVIePwL4/l8U4jEFNaVimonHyc=',
    NULL, 0, 'pedro', 'Pedro', 'Martín', 'pedro@example.com', 0, 1, datetime('now')
); --Pk 6


-- admin1 (id=1) -> verificado, admin2 (id=2) -> no verificado
-- usuario1 (id=3) -> verificado, usuario2 (id=4) -> verificado, usuario3 (id=5) -> no verificado

INSERT INTO users_profile (avatar, bio, verified, user_id, color_bg, role, deleted_at)
VALUES
    ('avatars/default.png', 'Administrador principal del sistema.', 1, 2, '#79A998', 'A', NULL),
    ('avatars/default.png', 'Administrador secundario del sistema.', 0, 3, '#A97979', 'A', NULL),
    ('avatars/default.png', 'Amante de los videojuegos de rol.', 1, 4, '#7979A9', 'U', NULL),
    ('avatars/default.png', 'Fan de los juegos de estrategia.', 1, 5, '#A9A979', 'U', NULL),
    ('avatars/default.png', 'Jugador casual de fin de semana.', 0, 6, '#79A9A9', 'U', NULL);
