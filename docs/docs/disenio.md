---
icon: lucide/pencil-ruler
---

# Diseño

## :lucide-pyramid: Arquitectura del sistema

> Definición de la arquitectura del sistema

## :lucide-chart-network: Definición de la estructura del proyecto y base de datos

### Diagrama de Casos de Uso

> Diagrama Casos de Uso

### Diagrama de Entidad/Relación

```mermaid
erDiagram
    EDICIÓN {}
    GÉNERO {}
    DESARROLLADORA {}
    DISTRIBUIDORA {}
    PLATAFORMA {}

    REGIÓN {
        CharField Siglas
        ImageField Icono
    }

    CLASIFICACIÓN {
        CharField Nombre
        TextField Descripcion
    }

    JUEGO {
        CharField Titulo
        SlugField Slug
        TextField Descripción
        ImageField Caratula
        DateField Fecha_lanzamiento
    }


    REVIEW {
        TextField Contenido
        BooleanField Recomendado
        DateField Fecha_actualizacion
        DateField Fecha_creacion
    }

    MEDIA {
        ImageField Image
    }

    COLECCION {
        ChardField Tipo
        DateField Fecha_adquisicion
    }

    LISTA_DESEOS {
        SmallPositiveIntegerField Prioridad
        CharField Anotacion
        DateField Fecha_creacion
    }

    BIBLIOTECA {
        DecimalField Horas_jugadas
        DateField Fecha_creacion
        DateField Fecha_actualizacion
    }

    ESTADO {
        ChardField Nombre
    }


    FAVORITO {}

    USUARIO {
        user Django
    }

    PERFIL {
        ImageField Avatar
        TextField Biografia
        BooleanField Verificado
    }

    ROL {
        CharField Nombre
    }


    %% Herencia
    GÉNERO ||--|| CLASIFICACIÓN : "hereda de"
    DESARROLLADORA ||--|| CLASIFICACIÓN : "hereda de"
    DISTRIBUIDORA ||--|| CLASIFICACIÓN : "hereda de"
    PLATAFORMA ||--|| CLASIFICACIÓN : "hereda de"
    REGIÓN ||--|| CLASIFICACIÓN : "hereda de"
    EDICIÓN ||--|| CLASIFICACIÓN : "hereda de"

    %% Relaciones base

    USUARIO ||--|| PERFIL : tiene
    PERFIL ||--|| ROL : tiene
    JUEGO  }|--|{ GÉNERO : tiene
    JUEGO  }|--|{ DESARROLLADORA : tiene
    JUEGO  }|--|{ DISTRIBUIDORA : tiene
    JUEGO  }|--|{ PLATAFORMA : tiene


    %% Coleccion
    USUARIO ||--o{ COLECCION : posee
    JUEGO ||--o{ COLECCION : "forma parte"
    EDICIÓN ||--o{ COLECCION : define
    REGIÓN ||--o{ COLECCION : aplica

    %% Lista de deseos
    USUARIO ||--o{ LISTA_DESEOS : crea
    JUEGO ||--o{ LISTA_DESEOS : contiene
    EDICIÓN ||--o{ LISTA_DESEOS : opcional
    REGIÓN ||--o{ LISTA_DESEOS : opcional

    %% Biblioteca
    USUARIO ||--o{ BIBLIOTECA : gestiona
    JUEGO ||--o{ BIBLIOTECA : "aparece en"
    ESTADO ||--o{ BIBLIOTECA : define

    %% Reviews
    USUARIO ||--o{ REVIEW : escribe
    REVIEW }o--|| JUEGO : sobre
    REVIEW ||--o{ MEDIA : contiene

    %% Favorito
    USUARIO ||--o{ FAVORITO : tiene
    JUEGO   ||--o{ FAVORITO : aparece

```

### Diagrama de Clases

> Diagrama de Clases

## :lucide-braces: API

### Endpoints

- `/api/admin/`: url para la vista de administración que viene por defecto en Django

- `/api/schema/`

- `/api/docs/`: url para comprobar todos los endpoints de la API mediante la librería de Swagger

- `/api/auth/`


- `/api/users/`

- `/api/games/`
    - `/api/games/`: listado de todos los videojuegos
    - `/api/games/add/`: añadir uno videojuego nuevo
    - `/api/games/<int:pk_game>/edit/`: edita un videojuego existente
    - `/api/games/<int:pk_game>/delete/`: borra un videojuego existente

- `/api/reviews/`
    - `/api/reviews/`: listado de todas las reviews
    - `/api/reviews/add/`: añadir una review nueva
    - `/api/reviews/<int:pk_review>/edit/`: edita una review existente
    - `/api/reviews/<int:pk_review>/delete/`: borra una review existente

- `/api/medias/`
    - `/api/medias/`: listado de todas las medias
    - `/api/medias/add/`: añadir una media nueva
    - `/api/medias/<int:pk_media>/edit/`: edita una media existente
    - `/api/medias/<int:pk_media>/delete/`: borra una media existente

- `/api/favorites/`
    - `/api/favorites/`: listado de todos los favoritos
    - `/api/favorites/add/`: añadir un favorito nuevo
    - `/api/favorites/self-add/`: añadir un favorito a la lista del propio usuario
    - `/api/favorites/<int:pk_favorite>/edit/`: edita un favorito existente
    - `/api/favorites/<int:pk_favorite>/delete/`: borra un favorito existente

- `/api/platforms/`
    - `/api/platforms/`: listado de todas las plataformas
    - `/api/platforms/add/`: añadir una plataforma nueva
    - `/api/platforms/<int:pk_platform>/edit/`: edita una plataforma existente
    - `/api/platforms/<int:pk_platform>/delete/`: borra una plataforma existente

- `/api/genres/`
    - `/api/genres/`: listado de todos los géneros de videojuegos
    - `/api/genres/add/`: añadir un género de videojuego
    - `/api/genres/<int:pk_genre>/edit/`: edita un género existente
    - `/api/genres/<int:pk_genre>/delete/`: borra un género existente

- `/api/developers/`
    - `/api/developers/`
    - `/api/developers/`: listado de todos los desarrolladores de videojuegos
    - `/api/developers/add/`: añadir un desarrolladores de videojuegos
    - `/api/developers/<int:pk_developer>/edit/`: edita un desarrollador existente
    - `/api/developers/<int:pk_developer>/delete/`: borra un desarrollador existente

- `/api/publishers/`
    - `/api/publishers/`
    - `/api/publishers/`: listado de todos los publishers de videojuegos
    - `/api/publishers/add/`: añadir un publishers de videojuegos
    - `/api/publishers/<int:pk_publisher>/edit/`: edita un publishers existente
    - `/api/publishers/<int:pk_publisher>/delete/`: borra un publishers existente

- `/api/editions/`
    - `/api/editions/`
    - `/api/editions/`: listado de todas las ediciones de videojuegos
    - `/api/editions/add/`: añadir una edición de videojuego
    - `/api/editions/<int:pk_edition>/edit/`: edita una edición existente
    - `/api/editions/<int:pk_edition>/delete/`: borra una edición existente

- `/api/regions/`
    - `/api/regions/`
    - `/api/regions/`: listado de todas las regiones de videojuegos
    - `/api/regions/add/`: añadir una region de videojuego
    - `/api/regions/<int:pk_region>/edit/`: edita una region existente
    - `/api/regions/<int:pk_region>/delete/`: borra una region existente

- `/api/libraries/`
    - `/api/libraries/`
    - `/api/libraries/`: listado de todos los item de bibliotecas
    - `/api/libraries/add/`: añadir un item de bibliotecas
    - `/api/libraries/<int:pk_library_item>/edit/`: edita un item de bibliotecas
    - `/api/libraries/<int:pk_library_item>/delete/`: borra un item de bibliotecas

- `/api/collections/`
    - `/api/collections/`
    - `/api/collections/`: listado de todos los items de colección
    - `/api/collections/add/`: añadir un item de colección
    - `/api/collections/self-add/`: añadir un item a la colección del propio usuario
    - `/api/collections/<int:pk_collection_item>/edit/`: editar un item de colección
    - `/api/collections/<int:pk_collection_item>/delete/`: borra un item de colección

- `/api/wishlists/`
    - `/api/wishlists/`
    - `/api/wishlists/`: listado de todos los items de wishlists
    - `/api/wishlists/add/`: añadir un item de wishlist
    - `/api/wishlists/self-add/`: añadir un item a la wishlist del propio usuario
    - `/api/wishlists/<int:pk_wishlist_item>/edit/`: editar un item de wishlist
    - `/api/wishlists/<int:pk_wishlist_item>/delete/`: borra un item de wishlist
---

## :lucide-paintbrush: Diseño de interfaz

### Principios del diseño

### Paleta de colores

<figure markdown="span">

![Logo](assets/color-pallete.png)

  <figcaption>
        Paleta de colores escogida en [ColorMind](http://colormind.io/)
  </figcaption>

</figure>

### Vistas

#### Mapa de Navegación

El mapa de navegación fue un diseño inicial sencillo para plantear las funciones de la aplicacion web.

![Mapa-Navegacion](assets/mapa-nav.jpg)

#### Sketch

En cuanto al skecth, hemos hecho un boceto a mano alzada, y ha quedado de la siguiente manera:

![Sketch](assets/sketch.png)

#### Wireframe

El Wireframe de la aplicación lo hemos realizado con [Moqups](moqups.com/es).

En esta etapa del diseño decidimos añadir una pantalla más que en el sketch para detallar la aplicación un poco más, así que obtenemos un total de 4 pantallas (register, login (autenticación), home y pantalla de detalles de un juego).

![Wireframe-Login](assets/wf-1.png)

![Wireframe-Register](assets/wf-2.png)

![Wireframe-Principal](assets/wf-3.png)

![Wireframe-Especifico](assets/wf-4.png)

#### MockUp y Prototipo

Para llevar a cabo tanto el mockup como el prototipo hemos utilizado [Penpot](https://penpot.app/).

##### Mockup

![Mockup-Login](assets/register.png)

![Mockup-Register](assets/login.png)

![Mockup-Principal](assets/home-web.png)

![Mockup-Especifico](assets/game.png)

##### Prototipo

![Prototipo](assets/prototipo.png)
