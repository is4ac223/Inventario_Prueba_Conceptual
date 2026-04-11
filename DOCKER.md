# 🐳 Guía de Dockerización - Sistema de Gestión de Inventario

## Requisitos Previos

Antes de ejecutar el proyecto con Docker, asegúrate de tener instalado:

- **Docker**: [Descargar Docker Desktop](https://www.docker.com/products/docker-desktop)
- **Docker Compose**: Incluido en Docker Desktop

Verifica que estén instalados correctamente:

```powershell
docker --version
docker-compose --version
```

---

## 📁 Estructura de Archivos Creados

```
proyecto/
├── docker-compose.yml          # Orquesta frontend y backend
├── .env.example                # Configuración de ejemplo (cópialo a .env)
├── .env.docker                 # Configuración para Docker
├── DOCKER.md                   # Este archivo
├── backend/
│   ├── Dockerfile              # Build del backend Django
│   ├── requirements.txt        # Dependencias Python
│   ├── .dockerignore           # Archivos a ignorar en la imagen
│   └── [resto del código Django]
└── frontend/
    ├── Dockerfile              # Build multi-stage de Svelte
    ├── docker-entrypoint.sh    # Script de inicio
    ├── .dockerignore           # Archivos a ignorar en la imagen
    └── [resto del código Svelte]
```

---

## 🚀 Instrucciones de Ejecución

### **1. Preparación Inicial (Primera Vez)**

```powershell
# Navega a la carpeta del proyecto
cd "C:\Users\is4ac\Documents\Pro\Inventario_Prueba_Conceptual"

# Construye las imágenes Docker (por primera vez)
docker-compose build

# Verifica que las imágenes se hayan construido correctamente
docker images | findstr inventario
```

### **2. Iniciar los Contenedores**

```powershell
# Inicia todos los servicios en segundo plano
docker-compose up -d

# O inicia con logs en tiempo real (más verboso para debugging)
docker-compose up
```

**¿Qué sucede automáticamente?**

- ✅ Se crea la red `inventario_network`
- ✅ Se construye la imagen del backend Django
- ✅ Se construye la imagen del frontend Svelte
- ✅ Se ejecutan las migraciones de Django automáticamente
- ✅ Se inicia el servidor Django en http://localhost:8000
- ✅ Se inicia el servidor Svelte en http://localhost:5000
- ✅ La base de datos SQLite persiste en un volumen

---

## 🌐 Acceso a la Aplicación

Una vez que los contenedores estén en ejecución:

**Frontend (Aplicación Principal):**

```
http://localhost:5000
```

**Backend API (Desarrollo/Debugging):**

```
http://localhost:8000/api/
```

**Admin de Django:**

```
http://localhost:8000/admin/
```

---

## 📊 Verificar Estado de los Contenedores

```powershell
# Ver contenedores en ejecución
docker-compose ps

# Ver logs en tiempo real del backend
docker-compose logs -f backend

# Ver logs en tiempo real del frontend
docker-compose logs -f frontend

# Ver logs de ambos
docker-compose logs -f

# Ver últimas N líneas de logs
docker-compose logs --tail=50
```

**Esperado en los logs:**

```
backend    | Starting development server at http://0.0.0.0:8000/
backend    | Quit the server with CONTROL-C.

frontend   | sirv v2.0.2
frontend   | listening on http://localhost:5000
```

---

## 🛑 Detener los Contenedores

```powershell
# Detiene los contenedores sin eliminarlos
docker-compose stop

# Detiene y elimina los contenedores (los datos persisten en el volumen)
docker-compose down

# Detiene y elimina TODO (contenedores, volúmenes, redes)
# ⚠️ CUIDADO: Esto borra la base de datos SQlite
docker-compose down -v
```

---

## 🔄 Actualizar el Código y Reconstruir

### **Si modificas Python (Backend)**

```powershell
# Opción 1: Reconstruye solo el backend (recomendado)
docker-compose up --build --no-deps backend

# Opción 2: Reconstruye todo
docker-compose down
docker-compose build --no-cache
docker-compose up -d
```

### **Si modificas JavaScript/Svelte (Frontend)**

```powershell
# Opción 1: Reconstruye solo el frontend
docker-compose up --build --no-deps frontend

# Opción 2: Reconstruye todo
docker-compose down
docker-compose build --no-cache
docker-compose up -d
```

---

## 🧪 Comandos Útiles de Django Dentro del Contenedor

### **Ejecutar migraciones manualmente**

```powershell
docker-compose exec backend python manage.py migrate
```

### **Crear datos de prueba**

```powershell
docker-compose exec backend python manage.py crear_datos_prueba
```

### **Crear superusuario (admin)**

```powershell
docker-compose exec backend python manage.py createsuperuser
```

### **Reiniciar base de datos (elimina todos los datos)**

```powershell
docker-compose exec backend rm db.sqlite3
docker-compose exec backend python manage.py migrate
```

### **Ejecutar bash dentro del contenedor backend**

```powershell
docker-compose exec backend bash
```

---

## 🔧 Configuración y Variables de Entorno

### **Archivo `.env.docker`**

Este archivo contiene la configuración para Docker. Puedes modificar:

```env
# Debug mode (cambiar a False en producción)
DEBUG=False

# URLs permitidas para CORS
CORS_ALLOWED_ORIGINS=http://localhost:5000,http://127.0.0.1:5000,http://frontend:5000

# URL de la API (frontend)
API_URL=http://backend:8000/api
```

**Para cambiar la configuración:**

```powershell
# 1. Modifica .env.docker
# 2. Reconstruye los contenedores:
docker-compose down
docker-compose up -d --build
```

---

## 🐛 Solución de Problemas

### **❌ Error: "Port 8000 is already in use"**

**Solución:** Otra aplicación está usando ese puerto

```powershell
# Encuentra qué usa el puerto 8000
netstat -ano | findstr :8000

# O cambia el puerto en docker-compose.yml:
# ports:
#   - "8001:8000"  # Externa:Interna
```

### **❌ Error: "CORS error when calling API"**

**Solución:** Verifica que las URLs de CORS sean correctas:

```powershell
# Revisa los logs
docker-compose logs backend | findstr CORS

# La URL del frontend debe coincidir con CORS_ALLOWED_ORIGINS

# Actualiza .env.docker si es necesario
docker-compose up -d --build
```

### **❌ Error: "Cannot connect to backend from frontend"**

**Solución:** Docker Compose usa DNS, asegúrate de usar el nombre del servicio:

✅ **Correcto (en Docker):** `http://backend:8000/api`  
❌ **Incorrecto:** `http://localhost:8000/api` (localhost no funciona entre contenedores)

El script `docker-entrypoint.sh` debería inyectar la URL correcta automáticamente.

### **❌ Contenedor se reinicia constantemente**

```powershell
# Revisa los logs para ver el error
docker-compose logs -f backend

# Podría ser un error en las migraciones
docker-compose exec backend python manage.py showmigrations
docker-compose exec backend python manage.py migrate
```

### **❌ "Permission denied" en Linux/Mac**

```bash
# En Linux/Mac, asegúrate que el usuario puede usar Docker
sudo usermod -aG docker $USER
```

---

## 📈 Escalado y Desarrollo Avanzado

### **Ejecutar múltiples instancias del frontend**

```powershell
# En docker-compose.yml, crear otro servicio:
# frontend-2:
#   build: ./frontend
#   ports:
#     - "5001:5000"

docker-compose up -d
```

### **Usar PostgreSQL en lugar de SQLite**

Modifica en `backend/settings.py`:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('DB_NAME', 'inventario'),
        'USER': os.getenv('DB_USER', 'postgres'),
        'PASSWORD': os.getenv('DB_PASSWORD', 'password'),
        'HOST': 'postgres',  # nombre del servicio en docker-compose
        'PORT': '5432',
    }
}
```

Agrega a `docker-compose.yml`:

```yaml
postgres:
  image: postgres:15-alpine
  environment:
    POSTGRES_DB: inventario
    POSTGRES_USER: postgres
    POSTGRES_PASSWORD: password
  volumes:
    - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:
```

---

## 📦 Desplegamiento en Producción

Para deployar en un servidor remoto (AWS, DigitalOcean, etc.):

### **1. Generar una SECRET_KEY segura**

```powershell
# En Python:
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

### **2. Crear archivo `.env.prod` en el servidor**

```env
DEBUG=False
SECRET_KEY=<generated-random-key>
ALLOWED_HOSTS=tudominio.com,www.tudominio.com
CORS_ALLOWED_ORIGINS=https://tudominio.com,https://www.tudominio.com

# Si usas un dominio, cambia a HTTPS
CSRF_TRUSTED_ORIGINS=https://tudominio.com,https://www.tudominio.com

API_URL=https://api.tudominio.com
```

### **3. Ejecutar con el archivo de producción**

```bash
docker-compose --env-file .env.prod up -d
```

### **4. Usar Nginx como proxy reverso (recomendado)**

Crea `nginx.conf`:

```nginx
upstream backend {
    server backend:8000;
}

upstream frontend {
    server frontend:5000;
}

server {
    listen 80;
    server_name tudominio.com;

    location / {
        proxy_pass http://frontend;
    }

    location /api {
        proxy_pass http://backend;
    }
}
```

---

## ✅ Checklist Final

- [ ] Docker y Docker Compose instalados
- [ ] Terminal abierta en la carpeta del proyecto
- [ ] Ejecutado `docker-compose build`
- [ ] Ejecutado `docker-compose up -d`
- [ ] Accedido a http://localhost:5000
- [ ] Verificado los logs sin errores
- [ ] Creados datos de prueba (opcional)

---

## 📞 Contacto y Soporte

Si encuentras problemas:

1. Revisa los logs: `docker-compose logs -f`
2. Ejecuta `docker-compose down -v` y vuelve a empezar limpio
3. Verifica que no hay puertos conflictivos: `netstat -ano | findstr :8000`
4. Asegúrate de tener suficiente espacio en disco (mín. 5GB)

---

**¡Listo! 🎉 Tu aplicación está containerizada y lista para producción.**
