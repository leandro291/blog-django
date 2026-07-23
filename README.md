# Blog API — Django REST Framework

API REST para una plataforma de blogs construida con Django y Django REST Framework. Permite gestionar publicaciones, categorías, comentarios y usuarios con autenticación JWT y documentación automática OpenAPI.

---

## Stack tecnológico

| Tecnología | Versión | Uso |
|---|---|---|
| Python | 3.13 | Runtime |
| Django | 6.0.7 | Framework |
| Django REST Framework | 3.17.1 | API REST |
| drf-spectacular | 0.30.0 | Documentación OpenAPI (Swagger/ReDoc) |
| django-filter | 26.1 | Filtrado de querysets |
| SimpleJWT | 5.5.1 | Autenticación JWT |
| jazzmin | 3.0.5 | Tema del admin |
| PostgreSQL | — | Base de datos |
| Gunicorn | 26.0.0 | Servidor WSGI |

---

## Requisitos previos

- Python 3.13
- PostgreSQL
- pip

---

## Instalación

```bash
# Clonar el repositorio
git clone <url-del-repositorio>
cd blog

# Crear y activar entorno virtual
python -m venv .venv
# Windows:
.venv\Scripts\activate
# Linux/Mac:
source .venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt
```

---

## Variables de entorno

Crea un archivo `.env` en la raíz del proyecto con las siguientes variables:

```env
DB_NAME=blog-django
DB_USER=postgres
DB_PASSWORD=tu_password
DB_HOST=localhost
DB_PORT=5432
SECRET_KEY=tu_secret_key_aqui
DEBUG=True
```

---

## Configuración de la base de datos

```bash
# Crear las tablas
python manage.py migrate

# Crear usuario administrador
python manage.py createsuperuser
```

---

## Ejecutar el proyecto

```bash
python manage.py runserver
```

El servidor estará disponible en `http://localhost:8000`.

---

## Estructura del proyecto

```
blog/
├── blog/                     # Configuración del proyecto
│   ├── settings.py
│   └── urls.py
├── users/                    # App de usuarios
│   ├── models.py             # User (AbstractUser)
│   ├── admin.py
│   └── api/
│       ├── views.py          # RegisterView, UserView
│       ├── serializers.py    # UserRegisterSerializer, UserSerializer, UserUpdateSerializer
│       └── router.py         # /api/auth/register/, /api/auth/login/, /api/auth/me/
├── posts/                    # App de publicaciones
│   ├── models.py             # Post
│   ├── admin.py
│   └── api/
│       ├── views.py          # PostViewSet (ModelViewSet)
│       ├── serializers.py    # PostWriteSerializer, PostReadSerializer
│       ├── permissions.py    # IsAdminOrReadOnly
│       └── router.py         # /api/posts/
├── categories/               # App de categorías
│   ├── models.py             # Category
│   ├── admin.py
│   └── api/
│       ├── views.py          # CategoryViewSet (ModelViewSet)
│       ├── serializers.py    # CategoryWriteSerializer, CategoryReadSerializer
│       ├── permissions.py    # IsAdminOrReadOnly
│       └── router.py         # /api/categories/
├── comments/                 # App de comentarios
│   ├── models.py             # Comment
│   ├── admin.py
│   └── api/
│       ├── views.py          # CommentViewSet (ModelViewSet)
│       ├── serializers.py    # CommentWriteSerializer, CommentReadSerializer
│       ├── permissions.py    # IsOwnerOrReadAndCreateOnly
│       └── router.py         # /api/comments/
├── requirements.txt
├── runtime.txt               # python-3.13.3
├── Procfile
└── manage.py
```

---

## Modelos

### User
Extiende `AbstractUser` de Django.

| Campo | Tipo | Descripción |
|---|---|---|
| id | BigAutoField | PK |
| username | CharField | Nombre de usuario único |
| email | EmailField | Email único (campo de login) |
| password | CharField | Contraseña hasheada |
| first_name | CharField | Nombre |
| last_name | CharField | Apellido |
| is_staff | BooleanField | ¿Es administrador? |

### Post

| Campo | Tipo | Descripción |
|---|---|---|
| id | BigAutoField | PK |
| title | CharField(255) | Título del post |
| content | TextField | Contenido |
| slug | SlugField(255) | URL amigable (unique) |
| miniature | ImageField | Imagen miniatura |
| created_at | DateTimeField | Fecha de creación |
| published | BooleanField | ¿Está publicado? |
| user | FK → User | Autor (CASCADE) |
| category | FK → Category | Categoría (PROTECT) |

### Category

| Campo | Tipo | Descripción |
|---|---|---|
| id | BigAutoField | PK |
| title | CharField(255) | Nombre de la categoría |
| slug | SlugField(255) | URL amigable (unique) |
| published | BooleanField | ¿Está publicada? |

### Comment

| Campo | Tipo | Descripción |
|---|---|---|
| id | BigAutoField | PK |
| content | TextField | Contenido del comentario |
| created_at | DateTimeField | Fecha de creación |
| user | FK → User | Autor del comentario (CASCADE) |
| post | FK → Post | Post al que pertenece (CASCADE) |

### Diagrama ER

```
┌──────────────────┐          ┌──────────────────┐
│       User       │          │     Category     │
├──────────────────┤          ├──────────────────┤
│ id          (PK) │          │ id          (PK) │
│ username         │          │ title            │
│ email            │          │ slug        (UQ) │
│ password         │          │ published        │
│ first_name       │          └────────┬─────────┘
│ last_name        │                   │
│ is_staff         │                   │
└───────┬──────────┘                   │
        │                              │
        │    ┌──────────────────┐      │
        │    │       Post       │      │
        │    ├──────────────────┤      │
        ├────│ user_id     (FK)│      │
        │    │ id          (PK) │      │
        │    │ title            │      │
        │    │ content          │      │
        │    │ slug        (UQ) │      │
        │    │ miniature        │      │
        │    │ created_at       │      │
        │    │ published        │      │
        │    │ category_id (FK) │◄─────┘
        │    └────────┬─────────┘
        │             │
        │             │
        │    ┌────────┴─────────┐
        │    │     Comment      │
        │    ├──────────────────┤
        └────│ user_id     (FK) │
             │ id          (PK) │
             │ post_id     (FK) │
             │ content          │
             │ created_at       │
             └──────────────────┘
```

---

## Endpoints de la API

### Autenticación

| Método | Endpoint | Descripción | Autenticación |
|---|---|---|---|
| POST | `/api/auth/register/` | Registrar nuevo usuario | No |
| POST | `/api/auth/login/` | Login (obtener token JWT) | No |
| POST | `/api/auth/token/refresh/` | Refrescar token JWT | No |
| GET | `/api/auth/me/` | Ver perfil del usuario actual | JWT |
| PUT | `/api/auth/me/` | Actualizar perfil del usuario actual | JWT |

### Posts

| Método | Endpoint | Descripción | Autenticación |
|---|---|---|---|
| GET | `/api/posts/` | Listar posts publicados | No |
| POST | `/api/posts/` | Crear nuevo post | Admin |
| GET | `/api/posts/{slug}/` | Ver post por slug | No |
| PUT | `/api/posts/{slug}/` | Actualizar post | Admin |
| DELETE | `/api/posts/{slug}/` | Eliminar post | Admin |

**Filtros disponibles:** `?category__slug=django`, `?category=1`

### Categories

| Método | Endpoint | Descripción | Autenticación |
|---|---|---|---|
| GET | `/api/categories/` | Listar categorías | No |
| POST | `/api/categories/` | Crear categoría | Admin |
| GET | `/api/categories/{id}/` | Ver categoría | No |
| PUT | `/api/categories/{id}/` | Actualizar categoría | Admin |
| DELETE | `/api/categories/{id}/` | Eliminar categoría | Admin |

### Comments

| Método | Endpoint | Descripción | Autenticación |
|---|---|---|---|
| GET | `/api/comments/` | Listar comentarios | No |
| POST | `/api/comments/` | Crear comentario | JWT |
| GET | `/api/comments/{id}/` | Ver comentario | No |
| PUT | `/api/comments/{id}/` | Actualizar comentario | Propietario |
| DELETE | `/api/comments/{id}/` | Eliminar comentario | Propietario |

---

## Ejemplos de requests

### Registrar usuario

```bash
curl -X POST http://localhost:8000/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{"username": "testuser", "email": "test@example.com", "password": "testpass123"}'
```

### Login

```bash
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"email": "test@example.com", "password": "testpass123"}'
```

Respuesta:
```json
{
  "access": "eyJhbGciOi...",
  "refresh": "eyJhbGciOi..."
}
```

### Ver perfil (requiere token)

```bash
curl http://localhost:8000/api/auth/me/ \
  -H "Authorization: Bearer eyJhbGciOi..."
```

### Actualizar perfil

```bash
curl -X PUT http://localhost:8000/api/auth/me/ \
  -H "Authorization: Bearer eyJhbGciOi..." \
  -H "Content-Type: application/json" \
  -d '{"first_name": "Juan", "last_name": "Pérez"}'
```

### Crear post (requiere admin)

```bash
curl -X POST http://localhost:8000/api/posts/ \
  -H "Authorization: Bearer eyJhbGciOi..." \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Mi primer post",
    "content": "Contenido del post...",
    "slug": "mi-primer-post",
    "category": 1
  }'
```

### Filtrar posts por categoría

```bash
curl "http://localhost:8000/api/posts/?category__slug=django"
```

### Crear comentario

```bash
curl -X POST http://localhost:8000/api/comments/ \
  -H "Authorization: Bearer eyJhbGciOi..." \
  -H "Content-Type: application/json" \
  -d '{"content": "Excelente post!", "post": 1}'
```

---

## Permisos

| Permiso | Aplicado a | Lectura | Escritura |
|---|---|---|---|
| Sin auth | Posts, Categories, Comments | Todos | Nadie |
| `IsAdminOrReadOnly` | Posts, Categories | Todos | Solo staff |
| `IsOwnerOrReadAndCreateOnly` | Comments | Todos | Propietario del comentario |
| `IsAuthenticated` | UserView (me) | — | Usuario autenticado |

---

## Documentación de la API

La documentación se genera automáticamente con drf-spectacular:

| Herramienta | URL |
|---|---|
| Swagger UI | `http://localhost:8000/api/schema/swagger-ui/` |
| ReDoc | `http://localhost:8000/api/schema/redoc/` |
| Schema OpenAPI (JSON) | `http://localhost:8000/api/schema/` |

---

## Despliegue en Render

### 1. Crear un Web Service en Render

1. Conecta tu repositorio de GitHub/GitLab en [render.com](https://render.com)
2. Selecciona **Web Service**
3. Configura:

| Campo | Valor |
|---|---|
| Runtime | Python 3 |
| Build Command | `pip install -r requirements.txt` |
| Start Command | `gunicorn blog.wsgi` |
| Python Version | 3.13 |

### 2. Variables de entorno en Render

Agrega estas variables en la sección **Environment** del servicio:

```env
DB_NAME=blog-django
DB_USER=tu_usuario_db
DB_PASSWORD=tu_password_db
DB_HOST=tu_host_render
DB_PORT=5432
SECRET_KEY=tu_secret_key_largo_y_aleatorio
DEBUG=False
```

### 3. Base de datos

Render puede proveer una base de datos PostgreSQL. En la sección **New** > **PostgreSQL**, crea una instancia y usa los datos de conexión en las variables de entorno.

### 4. Migraciones

Render ejecuta automáticamente `python manage.py migrate` al hacer deploy gracias al Procfile:

```
release: python manage.py migrate
web: gunicorn blog.wsgi
```

### 5. Deploy

```bash
git add .
git commit -m "deploy"
git push origin main
```

---

## Troubleshooting

| Error | Causa | Solución |
|---|---|---|
| `relation "users_user" does not exist` | Migraciones no ejecutadas | `python manage.py migrate` |
| `password must not be empty` | Password no hasheado al guardar | Verificar `set_password()` en el serializer |
| `ModuleNotFoundError: No module named 'psycopg2'` | Falta dependencia PostgreSQL | `pip install psycopg2-binary` |
| `401 Unauthorized` | Token expirado o ausente | Refrescar token con `/api/auth/token/refresh/` |
| `403 Forbidden` | Sin permisos de escritura | Verificar que el usuario sea admin o propietario |
| `column "email" already exists` | Constraint duplicado en DB | Verificar datos en la tabla `users_user` |
| `ALLOWED_HOSTS` error en producción | Dominio no permitido | Agregar el dominio de Render en `ALLOWED_HOSTS` en `settings.py` |
| `DEBUG=False` pero la app no carga | Faltan variables de entorno | Verificar que todas las variables del `.env` estén configuradas en Render |
