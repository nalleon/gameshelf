---
icon: lucide/pencil-ruler
---

# Diseño

## :lucide-pyramid: Arquitectura del sistema


!!! success "Visión general"
    GameShelf está diseñado como una aplicación web basada en **VUE** y **Django**, siguiendo una arquitectura clara, modular y escalable.

<div class="grid cards" markdown>

-    :lucide-globe: **Capa de presentación**  

     ---

     Interfaz web accesible desde el navegador, construida con VUE y TailwindCSS.

-    :lucide-cpu: **Capa de aplicación**  

     ---

     Lógica de negocio implementada mediante vistas, formularios y servicios de Django.

-    :lucide-database: **Capa de datos**  

     ---

     Persistencia de información mediante Django ORM y base de datos relacional.

-    :lucide-server: **Servicios auxiliares**  

     ---

     Procesamiento en segundo plano y envío de correos mediante Redis y Django-RQ.

</div>

### Esquema general de la arquitectura

```mermaid
flowchart LR
    Browser["Usuario<br/>(Navegador)"]
    Vue["Cliente de la aplicación - VUE"]
    Django["Servidor de la aplicación - Django"]
    DB["Base de datos"]
    Redis["Redis + RQ"]
    Email["Servicio de correo"]

    Browser --> Vue
    Vue --> Django
    Django --> DB
    Django --> Redis
    Redis --> Email
```


## :lucide-chart-network: Definición de la estructura del proyecto y base de datos

!!! info "División de los diagramas"
    Para facilitar la lectura y comprensión de la estructura, se optó por dividir tanto el diagrama E/R como el de clases en tres módulos principales para poder ver las relaciones principales sin saturar la visualización. 
    
    Estos módulos son los siguientes:

     * `Usuarios y perfiles` – Gestión de usuarios, perfiles, roles y favoritos.
     * `Juegos y clasificación` – Juegos, géneros, desarrolladoras, distribuidoras, plataformas, regiones y ediciones.
     * `Colección, lista de deseos y reviews` – Colecciones del usuario, listas de deseos, biblioteca y reseñas.
---

!!! warning "Consecuencias de la división"
    Esto solo afecta a la visualización de la documentación, **NO** influye en el diseño final de la aplicación.


### Diagrama de Casos de Uso

```mermaid
flowchart TB
    %% Actor
    Usuario([Usuario **SIN** privilegios])

    %% Casos de uso
    Registrarse(["Registrarse"])
    IniciarSesion(["Iniciar sesión"])
    ActualizarPerfil(["Actualizar perfil"])
    VerPerfil(["Ver perfil"])
    VerJuego(["Ver juego"])
    MarcarFavorito(["Marcar favorito"])
    AniadirBiblioteca(["Añadir a biblioteca"])
    AniadirColeccion(["Añadir a colección"])
    AniadirResenia(["Añadir una reseña"])
    AniadirListaDeseos(["Añadir a lista de deseados"])

    %% Conexiones
    Usuario --> Registrarse
    Usuario --> IniciarSesion

    Usuario --> VerPerfil
    VerPerfil --> ActualizarPerfil
    Usuario --> VerJuego
    VerJuego --> AniadirBiblioteca
    VerJuego --> AniadirColeccion
    VerJuego --> AniadirResenia
    VerJuego --> AniadirListaDeseos
    VerJuego --> MarcarFavorito
```

---

<div class="grid cards" markdown>

- :lucide-user: Registrarse
    - Actor: Usuario SIN privilegios
    - Descripción: Permite crear una cuenta en el sistema
    - Dependencias: Ninguna

- :lucide-user: Iniciar sesión
    - Actor: Usuario SIN privilegios
    - Descripción: Acceder a la cuenta creada
    - Dependencias: Ninguna

- :lucide-user: Ver perfil
    - Actor: Usuario SIN privilegios
    - Descripción: Consultar información de su perfil
    - Dependencias: Ninguna

- :lucide-user: Actualizar perfil
    - Actor: Usuario SIN privilegios
    - Descripción: Modificar sus datos personales
    - Dependencias: Depende de Ver perfil

- :lucide-gamepad: Ver juego
    - Actor: Usuario SIN privilegios
    - Descripción: Consultar la información de un juego
    - Dependencias: Ninguna

- :lucide-star: Marcar favorito
    - Actor: Usuario SIN privilegios
    - Descripción: Añadir un juego a favoritos
    - Dependencias: Depende de Ver juego

- :lucide-archive: Añadir a biblioteca
    - Actor: Usuario SIN privilegios
    - Descripción: Registrar que ha jugado/jugará el juego y sus horas jugadas
    - Dependencias: Depende de Ver juego

- :lucide-archive: Añadir a colección
    - Actor: Usuario SIN privilegios
    - Descripción: Incluir un juego dentro de su colección
    - Dependencias: Depende de Ver juego

- :lucide-edit: Añadir una reseña
    - Actor: Usuario SIN privilegios
    - Descripción: Escribir una reseña sobre un juego
    - Dependencias: Depende de Ver juego

- :lucide-edit: Editar una reseña
    - Actor: Usuario SIN privilegios
    - Descripción: Escribir una reseña sobre un juego
    - Dependencias: Depende de Añadir reseñar (_que sea del **propio usuario**_)


- :lucide-heart: Añadir a lista de deseos
    - Actor: Usuario SIN privilegios
    - Descripción: Añadir el juego a su lista de deseados
    - Dependencias: Depende de Ver juego

- :lucide-heart: Editar lista de deseos
    - Actor: Usuario SIN privilegios
    - Descripción: Añadir el juego a su lista de deseados
    - Dependencias: Depende de Añadir a lista de deseos (_que sea del **propio usuario**_)
    
</div>

---


<div class="grid cards" markdown>

- :lucide-gamepad: Crear juego
    - Actor: Usuario CON privilegios
    - Descripción: Crear un juego
    - Dependencias: Ninguna


- :lucide-gamepad: Editar juego
    - Actor: Usuario CON privilegios
    - Descripción: Editar un juego
    - Dependencias: Ninguna


- :lucide-gamepad: Editar juego
    - Actor: Usuario CON privilegios
    - Descripción: Editar un juego
    - Dependencias: Ninguna




</div>


### Diagrama de Entidad/Relación

#### :lucide-users: Usuarios y Perfiles
---

<div align="center">

```mermaid
erDiagram
    USUARIO {
    }

    PERFIL {
    }

    ROL {
    }

    FAVORITO {}

    %% Relaciones
    USUARIO ||--|| PERFIL : tiene
    PERFIL ||--|| ROL : tiene
    USUARIO ||--o{ FAVORITO : tiene
```

</div>

<br>

#### :lucide-gamepad: Juegos y Clasificación

---

```mermaid
erDiagram
    JUEGO {
    }

    GÉNERO {}
    DESARROLLADORA {}
    DISTRIBUIDORA {}
    PLATAFORMA {}
    REGIÓN {
    }
    EDICIÓN {}
    CLASIFICACIÓN {
    }

    %% Herencia
    GÉNERO ||--|| CLASIFICACIÓN : "hereda de"
    DESARROLLADORA ||--|| CLASIFICACIÓN : "hereda de"
    DISTRIBUIDORA ||--|| CLASIFICACIÓN : "hereda de"
    PLATAFORMA ||--|| CLASIFICACIÓN : "hereda de"
    REGIÓN ||--|| CLASIFICACIÓN : "hereda de"
    EDICIÓN ||--|| CLASIFICACIÓN : "hereda de"

    %% Relaciones
    JUEGO }|--|{ GÉNERO : tiene
    JUEGO }|--|{ DESARROLLADORA : tiene
    JUEGO }|--|{ DISTRIBUIDORA : tiene
    JUEGO }|--|{ PLATAFORMA : tiene
    JUEGO ||--o{ EDICIÓN : tiene
    JUEGO ||--o{ REGIÓN : tiene
```

<br>

#### :lucide-archive: Colección, Lista de Deseos y Reviews
---


```mermaid
erDiagram
    USUARIO {
    }

    COLECCION {
    }

    LISTA_DESEOS {
    }

    BIBLIOTECA {
    }

    ESTADO {
    }

    REVIEW {
    }

    MEDIA {
    }

    JUEGO {
    }

    %% Relaciones
    USUARIO ||--o{ COLECCION : posee
    JUEGO ||--o{ COLECCION : "forma parte"
    USUARIO ||--o{ LISTA_DESEOS : crea
    JUEGO ||--o{ LISTA_DESEOS : contiene
    USUARIO ||--o{ BIBLIOTECA : gestiona
    JUEGO ||--o{ BIBLIOTECA : "aparece en"
    ESTADO ||--o{ BIBLIOTECA : define
    USUARIO ||--o{ REVIEW : escribe
    REVIEW }o--|| JUEGO : sobre
    REVIEW ||--o{ MEDIA : contiene

```


<br>

### Diagrama de Clases

#### :lucide-users: Usuarios y Perfiles

```mermaid
classDiagram
    %% Módulo Usuarios y Perfiles
    class USUARIO {
        user: Django
    }

    class PERFIL {
        Avatar: ImageField
        Biografia: TextField
        Verificado: BooleanField
    }

    class ROL {
        Nombre: CharField
    }

    class FAVORITO

    %% Relaciones
    USUARIO "1" -- "1" PERFIL : tiene
    PERFIL "1" -- "1" ROL : tiene
    USUARIO "1" -- "*" FAVORITO : tiene
```

<br>

#### :lucide-gamepad: Juegos y Clasificación

---
```mermaid
classDiagram
    %% Módulo Juegos y Clasificación
    class JUEGO {
        Titulo: CharField
        Slug: SlugField
        Descripcion: TextField
        Caratula: ImageField
        Fecha_lanzamiento: DateField
    }

    class GÉNERO
    class DESARROLLADORA
    class DISTRIBUIDORA
    class PLATAFORMA
    class REGIÓN {
        Siglas: CharField
        Icono: ImageField
    }
    class EDICIÓN
    class CLASIFICACIÓN {
        Nombre: CharField
        Descripcion: TextField
    }

    %% Herencia
    GÉNERO --|> CLASIFICACIÓN
    DESARROLLADORA --|> CLASIFICACIÓN
    DISTRIBUIDORA --|> CLASIFICACIÓN
    PLATAFORMA --|> CLASIFICACIÓN
    REGIÓN --|> CLASIFICACIÓN
    EDICIÓN --|> CLASIFICACIÓN

    %% Relaciones
    JUEGO "*" -- "*" GÉNERO : tiene
    JUEGO "*" -- "*" DESARROLLADORA : tiene
    JUEGO "*" -- "*" DISTRIBUIDORA : tiene
    JUEGO "*" -- "*" PLATAFORMA : tiene
    JUEGO "1" -- "*" EDICIÓN : tiene
    JUEGO "*" -- "*" REGIÓN : tiene
```

<br>

#### :lucide-archive: Colección, Lista de Deseos y Reviews
---

```mermaid
classDiagram
    %% Módulo Colecciones y Reviews
    class COLECCION {
        Tipo: CharField
        Fecha_adquisicion: DateField
    }

    class LISTA_DESEOS {
        Prioridad: SmallPositiveIntegerField
        Anotacion: CharField
        Fecha_creacion: DateField
    }

    class BIBLIOTECA {
        Horas_jugadas: DecimalField
        Fecha_creacion: DateField
        Fecha_actualizacion: DateField
    }

    class ESTADO {
        Nombre: CharField
    }

    class REVIEW {
        Contenido: TextField
        Recomendado: BooleanField
        Fecha_actualizacion: DateField
        Fecha_creacion: DateField
    }

    class MEDIA {
        Image: ImageField
    }

    class JUEGO {
        Titulo: CharField
    }

    class USUARIO {
        user: Django
    }

    %% Relaciones
    USUARIO "1" -- "*" COLECCION : posee
    JUEGO "1" -- "*" COLECCION : forma_parte
    USUARIO "1" -- "*" LISTA_DESEOS : crea
    JUEGO "1" -- "*" LISTA_DESEOS : contiene
    USUARIO "1" -- "*" BIBLIOTECA : gestiona
    JUEGO "1" -- "*" BIBLIOTECA : aparece_en
    ESTADO "1" -- "*" BIBLIOTECA : define
    USUARIO "1" -- "*" REVIEW : escribe
    REVIEW "1" -- "1" JUEGO : sobre
    REVIEW "1" -- "*" MEDIA : contiene
```

## :lucide-braces: API

### Endpoints

- `/api/admin/`: url para la vista de administración que viene por defecto en Django

- `/api/schema/`

- `/api/docs/`: url para comprobar todos los endpoints de la API mediante la librería de Swagger

- `/api/auth/`
    - POST - `/api/auth/activate/`: Envia el email de activacion si la cuenta existe.
    - POST - `/api/auth/activate/validate/`: Activa correctamente la cuenta si existe.
    - POST - `/api/auth/change-password/`: Cambia la contraseña del usuario.
    - DELETE - `/api/auth/deactivate/`: Desactiva la cuenta del usuario (soft delete).  
    - POST - `/api/auth/login/`: Hace el login.
    - POST - `/api/auth/password-reset/`: Envia el email de restablecer la contraseña.
    - POST - `/api/auth/password-reset/validate/`: Valida el restablecimiento de la contraseña.
    - POST - `/api/auth/register/`: Registra un nuevo usuario.
    - POST - `/api/auth/verify-email/`: Envia el email de verificacion del usuario.
    - POST - `/api/auth/verify-email/validate/`: Verifica correctamente la cuenta si existe.


- `/api/users/`
    - GET - `/api/users/`: Lista todos los usuarios.
    - GET - `/api/users/{id}/`: Devuelve la informacion de un usuario con la id especificada.  
    - PATCH - `/api/users/{id}/`: Actualiza la informacion de un usuario.
    - GET - `/api/users/me/`: Devuelve la informacion del propio usuario.
    - GET - `/api/users/search/`: Busca un usuario.

- `/api/games/`
    - GET - `/api/games/`: Devuelve todos los videojuegos.
    - GET - `/api/games/{id}/`: Devuelve la información de un videojuego con la id especificada.
    - PUT - `/api/games/{id}/`: Actualiza un videojuego existente.
    - DELETE - `/api/games/{id}/`: Elimina un videojuego existente.
    - GET - `/api/games/igdb/`: Devuelve los juegos de IGDB por titulo. 
    - POST - `/api/games/igdb/`: Añade los juegos de IGDB en la base de datos.
    - GET `/api/games/search/`: Busqueda de juegos con filtros.

- `/api/reviews/`
    - GET - `/api/reviews/`: Devuelve todas las reviews.
    - POST -  `/api/reviews`: Crea una nueva review.
    - GET - `/api/reviews/{id}/`: Devuelve la información de una review con la id especificada.
    - PATCH - `/api/reviews/{id}/`: Actualiza una review con la id especificada.
    - DELETE - `/api/reviews/{id}/`: Elimina una review con la id especificada.
    - POST - `/api/reviews/{id}/media/`: Añade media a una review con la id especificada.
    - DELETE - `/api/reviews/media/{id}/`: Elimina la media de una review con la id especificada.

- `/api/favorites/`
    - PATCH - `/api/favorites/{id}/`: Actualiza un favorito existente con la id especificada.
    - DELETE - `/api/favorites/{id}/`: Elimina un favorito existente con la id especificada.
    - POST - `/api/favorites/toggle/`: Alterna el estado de un favorito.
    - GET `/api/favorites/user/{id}/`: Lista todos los favoritos del usuario con la id especificada.
    - POST `/api/favorites/user/{id}/`: Añade un favorito al usuario con la id especificada.

- `/api/platforms/`
    - GET - `/api/platforms/`: Lista todas las plataformas.
    - GET - `/api/platforms/{id}/`: Devuelve la informacion de una plataforma con la id especificada.
    - PUT - `/api/platforms/{id}/`: Actualiza la plataforma con la id especificada.
    - DELETE - `/api/platforms/{id}/`: Elimina la plataforma con la id especificada.

- `/api/genres/`
    - GET - `/api/genres/`: Lista todos los géneros.
    - GET - `/api/genres/{id}/`: Devuelve la información del genero con la id especificada.
    - PUT - `/api/genres/{id}/`: Actualiza el genero con la id especificada.
    - DELETE - `/api/genres/{id}/`: Elimina el genero con la id especificada

- `/api/developers/`
    - GET - `/api/developers/`: Lista todos los desarrolladores.
    - GET - `/api/developers/{id}/`: Devuelve la información del desarrollador con la id especificada.
    - PUT - `/api/developers/{id}/`: Actualiza el desarrollador con la id especificada.
    - DELETE - `/api/developers/{id}/`: Elimina el desarrollador con la id especificada.

- `/api/publishers/`
    - GET - `/api/publishers/`: Lista todas las editoriales.
    - GET - `/api/publishers/{id}/`: Devuelve la información de la editorial con la id especificada.
    - PUT - `/api/publishers/{id}/`: Actualiza la editorial con la id especificada.
    - DELETE - `/api/publishers/{id}/`: Elimina la editorial con la id especificada.

- `/api/editions/`
    - GET - `/api/editions/`: Lista todas las ediciones.
    - POST - `/api/editions/`: Crea una nueva edicion
    - GET - `/api/editions/{id}/`: Devuelve la información de la edicion con la id especificada.
    - PUT - `/api/editions/{id}/`: Actualiza la edicion con la id especificada.
    - DELETE - `/api/editions/{id}/`: Elimina la edicion con la id especificada.

- `/api/regions/`
    - GET - `/api/regions/`: Lista todas las regiones.
    - GET - `/api/regions/{id}/`: Devuelve la informacion de la region con la id especificada.
    - PUT - `/api/regions/{id}/`: Actualiza la region con la id especificada.
    - DELETE - `/api/regions/{id}/`: Elimina la region con la id especificada.

- `/api/library/`
    - GET - `/api/library/`: Lista todas las librerias.
    - POST - `/api/library/`: Añade un videojuego a la libreria.
    - PATCH - `/api/library/`: Actualiza la libreria.
    - GET - `/api/library/{id}/`: Devuelve la informacion de un videojuego con la id especificada de la libreria.
    - PATCH - `/api/library/{id}/`: Actualiza el videojuego con la id especificada de la libreria.
    - DELETE - `/api/library/{id}/`: Elimina el videojuego con la id especificada de la libreria.
    - GET - `/api/library/user/{id}/`: Devuelve la informacion de la libreria de un usuario con la id especificada

- `/api/collections/`
    - GET - `/api/collections/`: Lista todas las colecciones.
    - POST - `/api/collections/`: Crea una coleccion.
    - POST - `/api/collections/{id}/`: Añade un videojuego a tu coleccion.
    - PATCH - `/api/collections/{id}/`: Actualiza la coleccion con la id especificada.
    - DELETE - `/api/collections/{id}/`: Elimina un videojuego de la colección
    - GET - `/api/collections/{id}/items/{id}/`: Obtiene el videojuego con una id especificada de una coleccion con tambien una id especificada.
    - PATCH - `/api/collections/{id}/items/{id}/`: Actualiza la informacion de un item con una id especificada de una coleccion con tambien una id especificada.
    - DELETE - `/api/collections/{id}/items/{id}/`: Elimina un videojuego con una id especificada de una coleccion con tambien una id especificada.
    - GET - `/api/collections/{id}/user/{id}/`: Devuelve la información de la coleccion con una id especificada de un usuario con la id tambien especificada.

- `/api/wishlists/`
    - GET - `/api/wishlist/`: Devuelve la wishlist del usuario.
    - GET - `/api/wishlist/{id}/`: Devuelve la wishlist del usuario con la id especificada.
    - POST - `/api/wishlist/{id}/`: Añade un videojuego con la id especificada a la wishlist.
    - PATCH - `/api/wishlist/{id}/`: Actualiza la informacion de la wishlist.
    - GET - `/api/wishlist/items/{id}/`: Devuelve un videojuego con la id especificada de la wishlist.
    - PATCH - `/api/wishlist/items/{id}/`: Actualiza la informacion de un videojuego con la id especificada en la wishlist.
    - DELETE - `/api/wishlist/items/{id}/`: Elimina un videojuego con la id especificada de la wishlist.

!!! info "Interacción con la API"
    Se puede interactuar con la API utilizando el Swagger. Para hacerlo, acceda a este [enlace](https://grupo10.tail647188.ts.net/api/docs/).
---

## :lucide-paintbrush: Diseño de interfaz

### Principios del diseño

### Paleta de colores

<figure markdown="span">

![Logo](assets/color-pallete.png)

<figcaption class="caption-center">
Paleta de colores escogida en <a href="http://colormind.io/">ColorMind</a>
</figcaption>.

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