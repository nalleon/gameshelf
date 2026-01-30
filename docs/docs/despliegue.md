---
icon: lucide/codepen
---

# Despliegue

## Entorno de producción

El entorno de despliegue sería un contenedor de Docker alojado en un servidor de producción. Necesitaríamos confirgurar un contenedoor propio, subir el proyecto comprimido, o clonar el repositorio con GitHub. Luego sería necesario aplicar una configuración de nginx específica en el contenedor, y exponer la web para el acceso público.

## Proceso de despliegue

El proceso de despliegue sería el siguiente:

- Crear un contenedor de __Docker__ con las __dependencias__ necesarias instaladas:

    - Nginx
    - GitHub
    - SQLite
    - Python
    - Django

- Ejecutar el comando `git clone https://github.com/nalleon/lumino.git` para __obtener__ el código del __repositorio__.

- Realizar la __configuración de Nginx__ para el __virtual host__ que alojará la web a nivel __público__

## Planes de recuperación

En el apartado técnico, al __desplegar la web__ tendremos que implementar una forma de __manejar errores__ y controlar todo __sistemáticamente__. 

Una forma de tener todo __controlado__ sería un sistema de notificaciones al __personal__ que se encargue de __mantener el servidor__. En cuanto algún __error__ ocurriese, mandaría una __notificación__ por correo y así se acudiría rápidamente a manejarlo, __cortar el acceso__ a la zona que da el __error__, __solucionarlo__ y  abrir el acceso normal a __todo el mundo__.

Además, se configuraría una __regla__ en el __virtual host__, para que se vayan haciendo los __logs__ de la web en unas __carpetas específicas__.

## Sostenibilidad

La sostenibilidad del entorno de producción de __Lumino__ se aborda desde el punto de vista del uso eficiente de los recursos, la facilidad de mantenimiento y la reducción del impacto técnico y económico a largo plazo.

El uso de __contenedores Docker__ permite un despliegue ligero y controlado, evitando instalaciones innecesarias en el servidor y optimizando el consumo de recursos. Al ejecutarse únicamente los servicios necesarios (Django, Nginx y la base de datos), se reduce el uso de CPU y memoria frente a configuraciones más complejas.

La utilización de __software libre__ como Django, Nginx, Docker y SQLite contribuye a la sostenibilidad económica del proyecto, eliminando costes de licencias y facilitando su mantenimiento y evolución futura. Además, la __automatización del despliegue__ y la posibilidad de recrear el entorno de producción de forma rápida permiten minimizar tiempos de inactividad y reducir el esfuerzo necesario para tareas de mantenimiento o recuperación ante fallos.


