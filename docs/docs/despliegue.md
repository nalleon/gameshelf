---
icon: lucide/server-cog
---

# Despliegue de la aplicación

GameShelf se encuentra completamente dockerizado para facilitar su despliegue y ejecución en diferentes entornos.  
La infraestructura de la aplicación se basa en varios servicios independientes que trabajan conjuntamente para ofrecer una arquitectura modular, escalable y sencilla de mantener.

La aplicación utiliza:

- **Django** como servidor principal de la API.
- **Nginx** como proxy inverso y servidor de archivos estáticos.
- **Redis** para la gestión de colas y tareas asíncronas.
- **RQWorker** para el procesamiento de tareas en segundo plano.

Gracias a Docker y Docker Compose, todo el entorno puede iniciarse de manera rápida y reproducible.

!!! info "Arquitectura basada en contenedores"
    Cada servicio se ejecuta dentro de su propio contenedor, permitiendo separar responsabilidades y simplificando el despliegue del proyecto.

---

# Dockerfile del backend

El backend utiliza una imagen ligera basada en Python Slim.  
Además, se emplea `uv` como gestor moderno de dependencias y entornos virtuales, permitiendo instalaciones más rápidas y eficientes.

```dockerfile title="Dockerfile.backend"
FROM python:3.14-slim

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PATH="/app/.venv/bin:$PATH"

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential gcc g++ libpq-dev curl \
    && rm -rf /var/lib/apt/lists/*

RUN apt-get update && apt-get install -y just
RUN apt-get update && apt-get install -y sqlite3

COPY gameshelf-backend/pyproject.toml .
COPY gameshelf-backend/uv.lock .

RUN uv sync --frozen --no-dev

COPY gameshelf-backend/ .

COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh


RUN adduser --disabled-password --gecos "" django_user

RUN mkdir -p /app/staticfiles /app/media /app/data

RUN chown -R django_user:django_user /app

USER django_user

EXPOSE 8000

ENTRYPOINT ["/entrypoint.sh"]
```

!!! tip "Uso de imágenes ligeras"
    Utilizar `python:slim` reduce el tamaño final de la imagen y mejora los tiempos de despliegue.

---

# Script de inicialización

El contenedor ejecuta automáticamente un script de entrada encargado de preparar la aplicación antes de iniciarse.

Este proceso automatiza:

- La aplicación de migraciones.
- La recolección de archivos estáticos.
- La carga de datos iniciales.
- La creación del superusuario.
- El arranque del servidor Gunicorn.

```sh title="entrypoint.sh"
#!/bin/sh
set -e

uv run python manage.py migrate --noinput
uv run python manage.py collectstatic --noinput --clear

just reset-db
just seed
just create-su

exec uv run gunicorn main.wsgi:application \
    --bind 0.0.0.0:8000 \
    --workers 3
```

!!! warning "Inicialización automática"
    Las operaciones `reset-db`, `seed` y `create-su` se encargan de ejecutar las migraciones y poblar la base de datos.

---

# Dockerfile del frontend

El frontend a su vez, utiliza una imagen ligera basada en Node 20 y construida sobre Alpine Linux.  
Por su parte, utiliza npm como gestor de dependencias.

```dockerfile title="Dockerfile.frontend"
FROM node:20-alpine AS build

WORKDIR /app

COPY gameshelf-frontend/package*.json ./
RUN npm install

COPY gameshelf-frontend/ .

RUN npm run build
```

!!! tip "Uso de imágenes ligeras"
    `node:20-alpine` se usa mucho para contenedores pequeños y rápidos porque Alpine ocupa muy poco espacio comparado con Debian o Ubuntu.

---

# Docker-compose

Cada Dockerfile es empleado en sus respectivos volúmenes, organizados en el siguiente docker-compose:

```docker-compose title="docker-compose"

services:
  django:
    build:
      context: .
      dockerfile: Dockerfile.backend
    container_name: gameshelf_backend
    restart: always

    env_file:
      - ./gameshelf-backend/.env

    user: "1000:1000"

    volumes:
      - static_volume:/app/staticfiles
      - media_volume:/app/media
      - db_volume:/app/data

    expose:
      - 8000

    depends_on:
      - redis

    command: uv run gunicorn main.wsgi:application --bind 0.0.0.0:8000 --workers 3

  rqworker:
    build:
      context: .
      dockerfile: Dockerfile.backend
    container_name: gameshelf_rqworker
    restart: always

    env_file:
      - ./gameshelf-backend/.env

    user: "1000:1000"

    depends_on:
      - redis

    command: uv run python manage.py rqworker default


  redis:
    image: redis:7-alpine
    container_name: gameshelf_redis

    restart: always

    volumes:
      - redis_data:/data


  nginx:
    image: nginx:stable-alpine
    container_name: gameshelf_nginx
    restart: always

    ports:
      - "80:80"

    volumes:
      - ./docker/nginx/default.conf:/etc/nginx/conf.d/default.conf
      - static_volume:/app/staticfiles
      - media_volume:/app/media
      - frontend_dist:/usr/share/nginx/html
    depends_on:
      - django

  frontend:
    build:
      context: .
      dockerfile: Dockerfile.frontend
    volumes:
      - frontend_dist:/app/dist

volumes:
  static_volume:
  media_volume:
  redis_data:
  db_volume:
  frontend_dist:
```

# Configuración de Nginx

Nginx actúa como proxy inverso entre el cliente y Django.  
Además, sirve directamente los archivos estáticos y multimedia para mejorar el rendimiento de la aplicación.

```nginx title="default.conf"
server {
    listen 80;

    server_name gameshelf.arkania.es;

    client_max_body_size 20M;

    location / {
        root /usr/share/nginx/html;
        try_files $uri $uri/ /index.html;
    }

    location /api/ {
        proxy_pass http://django:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /admin/ {
        proxy_pass http://django:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /static/ {
        alias /app/staticfiles/;
    }

    location /media/ {
        alias /app/media/;
    }
}
```

!!! info "Proxy inverso"
    Nginx recibe las peticiones externas y las redirige internamente al servidor Django.

---

# Orquestación con Docker Compose

La gestión completa de contenedores se realiza mediante Docker Compose.  
Cada servicio cumple una función concreta dentro de la infraestructura de la aplicación.

```yaml title="docker-compose.yml"
services:
  django:
    build:
      context: .
    container_name: gameshelf_backend
    restart: always
    env_file:
      - ./gameshelf-backend/.env

    user: "1000:1000"

    volumes:
      - static_volume:/app/staticfiles
      - media_volume:/app/media

    expose:
      - 8000

    depends_on:
      - redis

  rqworker:
    build:
      context: .
    container_name: gameshelf_rqworker
    restart: always
    command: python manage.py rqworker default
    env_file:
      - ./gameshelf-backend/.env
    user: "1000:1000"
    depends_on:
      - redis
      - django

  redis:
    image: redis:7-alpine
    container_name: gameshelf_redis
    restart: always
    volumes:
      - redis_data:/data

  nginx:
    image: nginx:stable-alpine
    container_name: gameshelf_nginx
    restart: always
    ports:
      - "8080:80"
    volumes:
      - ./docker/nginx/default.conf:/etc/nginx/conf.d/default.conf
      - static_volume:/app/staticfiles
      - media_volume:/app/media
    depends_on:
      - django

volumes:
  static_volume:
  media_volume:
  redis_data:
```

!!! success "Infraestructura modular"
    Docker Compose permite iniciar todos los servicios de la aplicación mediante un único comando.

---

# Arquitectura del despliegue

El flujo general de la infraestructura desplegada es el siguiente:

1. El cliente realiza peticiones al servidor Nginx.
2. Nginx redirige las solicitudes al contenedor de Django.
3. Django procesa la lógica de negocio y responde al cliente.
4. Las tareas asíncronas son enviadas a Redis.
5. RQWorker consume las tareas pendientes y las ejecuta en segundo plano.
6. Los archivos estáticos y multimedia son servidos directamente por Nginx.

!!! abstract "Ventajas de la arquitectura"
    - Separación de responsabilidades.
    - Facilidad de escalado.
    - Despliegue reproducible.
    - Mantenimiento simplificado.
    - Mejor gestión de servicios.