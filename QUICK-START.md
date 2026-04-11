# ⚡ INICIO RÁPIDO CON DOCKER

## 3 pasos para empezar:

### 1️⃣ Construir las imágenes (primera vez)

```powershell
docker-compose build
```

### 2️⃣ Iniciar los contenedores

```powershell
docker-compose up -d
```

### 3️⃣ Abrir en el navegador

```
http://localhost:5000
```

---

## 📋 Otros comandos útiles

| Comando                                                           | Descripción                    |
| ----------------------------------------------------------------- | ------------------------------ |
| `docker-compose up -d`                                            | Inicia en segundo plano        |
| `docker-compose logs -f`                                          | Ver logs en tiempo real        |
| `docker-compose down`                                             | Detener todos los contenedores |
| `docker-compose ps`                                               | Ver estado de contenedores     |
| `docker-compose exec backend python manage.py crear_datos_prueba` | Crear datos de prueba          |

---

## 🌐 Accesos

- **Aplicación:** http://localhost:5000
- **API Backend:** http://localhost:8000/api/
- **Admin Django:** http://localhost:8000/admin/

---

## 📝 Script PowerShell (Windows)

```powershell
# Si prefieres usar el script helper:
.\start-docker.ps1 up       # Iniciar
.\start-docker.ps1 down     # Detener
.\start-docker.ps1 logs     # Ver logs
.\start-docker.ps1 help     # Ayuda
```

---

ℹ️ Para documentación completa, ver [DOCKER.md](DOCKER.md)
