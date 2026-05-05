# Variables de Entorno

Este documento describe todas las variables de entorno utilizadas en el proyecto Sistema de Inventario.

## Descripción General

Las variables de entorno se cargan desde el archivo `.env` en el directorio `backend/` usando la librería `python-dotenv`.

## Variables de Seguridad Django

### SECRET_KEY

- **Descripción**: Clave secreta de Django utilizada para cifrado y hash
- **Valor por defecto**: `django-insecure-=(n-vfkp*frj!ttrqhfyol08-z_b(ilzgjb@-d_^1yamq76iu9`
- **En Producción**: DEBE ser una clave fuerte y única
- **Tipo**: String

### DEBUG

- **Descripción**: Activa el modo debug de Django
- **Valor por defecto**: `True` (para desarrollo)
- **En Producción**: DEBE ser `False`
- **Tipo**: Boolean (True/False)

## Variables de Acceso

### ALLOWED_HOSTS

- **Descripción**: Lista de hosts permitidos separados por comas
- **Valor por defecto**: `localhost,127.0.0.1`
- **Ejemplo**: `localhost,127.0.0.1,0.0.0.0`
- **Tipo**: String (separado por comas)

## Variables CORS (Cross-Origin Resource Sharing)

### CORS_ALLOW_ALL_ORIGINS

- **Descripción**: Permite todas las fuentes de origen (NO recomendado en producción)
- **Valor por defecto**: `False`
- **En Producción**: Siempre `False`
- **Tipo**: Boolean (True/False)

### CORS_ALLOWED_ORIGINS

- **Descripción**: Lista de orígenes permitidos para CORS, separados por comas
- **Valor por defecto**: `http://localhost:5000,http://127.0.0.1:5000`
- **Ejemplo**: `http://localhost:5000,http://localhost:3000,https://example.com`
- **Tipo**: String (separado por comas)

### CSRF_TRUSTED_ORIGINS

- **Descripción**: Orígenes de confianza para protección CSRF, separados por comas
- **Valor por defecto**: `http://localhost:5000,http://127.0.0.1:5000,http://localhost:3000,http://127.0.0.1:3000`
- **Tipo**: String (separado por comas)

## Variables de Configuración Frontend

### FRONTEND_URL

- **Descripción**: URL del frontend para referencia y redireccionamientos
- **Valor por defecto**: `http://localhost:5000`
- **En Producción**: URL del dominio en producción
- **Tipo**: String

## Variables de Base de Datos

### DATABASE_ENGINE

- **Descripción**: Motor de base de datos a utilizar
- **Valor por defecto**: `django.db.backends.sqlite3`
- **Opciones**:
  - `django.db.backends.sqlite3` (desarrollo)
  - `django.db.backends.postgresql` (producción)
  - `django.db.backends.mysql` (alternativa)
- **Tipo**: String

### DATABASE_NAME

- **Descripción**: Nombre o ruta de la base de datos
- **Valor por defecto**: `db.sqlite3` (para SQLite)
- **Para PostgreSQL**: nombre de la base de datos
- **Tipo**: String

## Configuración para Desarrollo

Archivo `.env` recomendado para desarrollo:

```env
# Django Security Settings
SECRET_KEY=django-insecure-=(n-vfkp*frj!ttrqhfyol08-z_b(ilzgjb@-d_^1yamq76iu9
DEBUG=True

# Allowed Hosts
ALLOWED_HOSTS=localhost,127.0.0.1,0.0.0.0

# CORS Settings
CORS_ALLOW_ALL_ORIGINS=False
CORS_ALLOWED_ORIGINS=http://localhost:5000,http://127.0.0.1:5000,http://localhost:3000,http://127.0.0.1:3000
CSRF_TRUSTED_ORIGINS=http://localhost:5000,http://127.0.0.1:5000,http://localhost:3000,http://127.0.0.1:3000

# Frontend URL
FRONTEND_URL=http://localhost:5000

# Database
DATABASE_ENGINE=django.db.backends.sqlite3
DATABASE_NAME=db.sqlite3
```

## Configuración para Producción

Archivo `.env` recomendado para producción:

```env
# Django Security Settings
SECRET_KEY=your-very-secure-random-key-here
DEBUG=False

# Allowed Hosts
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com

# CORS Settings
CORS_ALLOW_ALL_ORIGINS=False
CORS_ALLOWED_ORIGINS=https://yourdomain.com,https://www.yourdomain.com
CSRF_TRUSTED_ORIGINS=https://yourdomain.com,https://www.yourdomain.com

# Frontend URL
FRONTEND_URL=https://yourdomain.com

# Database (PostgreSQL)
DATABASE_ENGINE=django.db.backends.postgresql
DATABASE_NAME=inventario_db
```

## Cómo Usar .env

1. Copia `.env.example` a `.env`:

   ```bash
   cp backend/.env.example backend/.env
   ```

2. Edita el archivo `.env` con tus valores específicos

3. Las variables se cargan automáticamente en `backend/settings.py`

4. NUNCA hagas commit del archivo `.env` a control de versiones

## Seguridad

- El archivo `.env` está en `.gitignore` para evitar commits accidentales
- Las credenciales NUNCA deben estar en el repositorio
- Usa valores fuertes para `SECRET_KEY` en producción
- Siempre usa `DEBUG=False` en producción
- Especifica solo los orígenes permitidos en CORS en producción

## Generando una SECRET_KEY segura

Para generar una clave segura en Python:

```python
from django.core.management.utils import get_random_secret_key
print(get_random_secret_key())
```

O desde el shell:

```bash
python manage.py shell
>>> from django.core.management.utils import get_random_secret_key
>>> print(get_random_secret_key())
```
