---
icon: lucide/info
---

# Introducción

Este documento pretende presentar al equipo educativo nuestra propuesta de proyecto como alumnado de C.F.G.S. Desarrollo de Aplicaciones Web (DAW). 

En la actualidad, no solo el coleccionismo de videojuegos, si no el juego en sí, se ha convertido en una afición cada vez más popular entre jugadores de todas las edades. Sin embargo, los entusiastas de este hobby a menudo enfrentan limitaciones a la hora de organizar, compartir y descubrir nuevas entregas, especialmente aquellas que varían según región, plataforma o formato. Con el objetivo de responder a esta necesidad, surge nuestra aplicación: _**GameShelf**_. 

Este proyecto busca: 

- Permitir a los usuarios registrar, clasificar y consultar tanto su colección personal de videojuegos como llevar un registro de aquellos que ha jugado de forma detallada.

- Integrar funcionalidades sociales como reseñas, y el descubrimiento de nuevos títulos que añadir a tu lista de pendientes de jugar o la de tu colección.

- Ofrecer una base de datos que distinga ediciones según región, consola y formato, con especial atención a títulos retro y físicos.

- Facilitar el descubrimiento de juegos o ciertas ediciones a través de las colecciones de otros usuarios, impulsando la pasión por el coleccionismo.

Esta aplicación esta dirigida a todo jugador que quiera tener un registro de su colección y/o lista de juegos, y que busquen una herramienta sencilla y eficaz para organizarlas y encontrar nuevos elementos para complementarlas.


## Características principales 

- Gestión detallada de versiones regionales de cada juego, permitiendo distinguir entre diferentes títulos según región (USA, EU, JP, CN, etc) y su plataforma (por ejemplo, Inazuma Eleven 3 para Nintendo DS en Japón vs. Nintendo 3DS en Occidente).

- Soporte para diferentes formatos de juegos: físico y digital.

- Gestión detallada del tipo de edición: standard, day one, deluxe, coleccionista, entre otras.

- Interfaz intuitiva y sencilla, pensada para jugadores que buscan una herramienta fácil de usar y eficaz.

- Posibilidad de buscar y encontrar nuevas adquisiciones para complementar y ampliar tu colección.

- Registro completo y actualizado de tu biblioteca personal de videojuegos.


- Visualización clara y organizada de la colección, con filtros para facilitar el acceso rápido a cualquier título.

- Soporte para múltiples plataformas y tipos de juegos, adaptándose a colecciones variadas.


## Arquitectura y tecnologías

Estas son las tecnologías que se utilizaran a lo largo del desarrollo de GameShelf:

- **Documentación:**
    - [MkDocs + Zensical](https://daringfireball.net/projects/markdown/) para la creación de la documentación.
    - [DrawIO](https://app.diagrams.net/) para el diseño de los diagramas.
    - [Miro](https://miro.com/diagramming/) para el diseño de la interfaz.

- **Bases de Datos:**
    - [MySQL](https://www.sqlite.org/index.html) como base de datos relacional.

- **Testing**

- **Frameworks:**
    - [Django](https://spring.io/projects/spring-boot) para el desarrollo de la aplicación del lado del servidor con Python.
    - [Vue](https://es.react.dev/) para el desarollo del cliente web de la aplicación con TypeScript.

- **Securización:**

- **Despliegue:**
    - [Docker](https://www.docker.com/) para la creación de contenedores y despliegue del proyecto en diferentes entornos.

- **APIs externas:**
    - [RAWGApi](https://rawg.io/apidocs) para obtener los videojuegos. 