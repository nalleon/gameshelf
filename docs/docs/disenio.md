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

    USUARIO {
        user Django
    }

    PERFIL {
        string Avatar
        string Biografia
        boolean Verificado
    }

    ROL {
        int ID
        string Nombre
    }

    JUEGO {
        int ID
        string Titulo
        string Caratula
        string Slug
        date Fecha_lanzamiento
    }

    CLASIFICACIÓN {
        int ID
        string Nombre
        string Descripcion
    }

    REVIEW {
        int ID
        string Contenido
        boolean Recomendado
        date Fecha_actualizacion
        date Fecha_creacion
    }

    MEDIA_REVIEW {
        int ID
        string Tipo
        string Url
        int Orden
    }

    COLECCION {
        int ID
        string Tipo
        date Fecha_adquisicion
    }

    ESTADO_BIBLIOTECA {
        int ID
        string Nombre
    }

    BIBLIOTECA {
        int ID
        float Horas_jugadas
        date Fecha_creacion
        date Fecha_actualizacion
    }

    EDICIÓN {
        int ID
        string Nombre
        string Descipción
    }

    REGIÓN {
        int ID
        string Nombre
        string Descripcion
        string Icono
        string Siglas
    }


    LISTA_DESEOS {
        int ID
        int Prioridad
        string Anotacion
        date Fecha_creacion
    }

    %% Relaciones base
    USUARIO ||--|| PERFIL : tiene
    PERFIL ||--|| ROL : tiene
    JUEGO }o--|| CLASIFICACIÓN : tiene

    %% Reviews
    USUARIO ||--o{ REVIEW : escribe
    REVIEW }o--|| JUEGO : sobre
    REVIEW ||--o{ MEDIA_REVIEW : contiene

    %% Coleccion
    USUARIO ||--o{ COLECCION : posee
    JUEGO ||--o{ COLECCION : forma_parte
    EDICIÓN ||--o{ COLECCION : define
    REGIÓN }o--o{ COLECCION : aplica

    %% Biblioteca
    USUARIO ||--o{ BIBLIOTECA : gestiona
    JUEGO ||--o{ BIBLIOTECA : aparece_en
    ESTADO_BIBLIOTECA ||--o{ BIBLIOTECA : define


    %% Lista de deseos
    USUARIO ||--o{ LISTA_DESEOS : crea
    JUEGO ||--o{ LISTA_DESEOS : desea
    EDICIÓN }o--o{ LISTA_DESEOS : opcional
    REGIÓN }o--o{ LISTA_DESEOS : opcional
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

#### MockUp
