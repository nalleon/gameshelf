---
icon: lucide/pencil-ruler
---

# Diseño

## Arquitectura del sistema

## Definición de la estructura del proyecto y base de datos

### Diagrama de Casos de Uso

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

## API

### Endpoints

---

## Diseño de interfaz

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
