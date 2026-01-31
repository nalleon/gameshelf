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
    }

    REVIEW {
        int ID
        string Contenido
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

    %% Biblioteca
    USUARIO ||--o{ BIBLIOTECA : gestiona
    JUEGO ||--o{ BIBLIOTECA : aparece_en
    ESTADO_BIBLIOTECA ||--o{ BIBLIOTECA : define
    EDICIÓN ||--o{ BIBLIOTECA : define
    REGIÓN }o--o{ BIBLIOTECA : aplica

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

### Vistas
#### Wireframe
#### MockUp