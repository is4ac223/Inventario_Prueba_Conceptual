<<<<<<< HEAD

# Sistema de Gestión de Inventario

Sistema de demostración para registro de movimientos de inventario con Django (backend) y Svelte (frontend).

## 🚀 Características

- **Autenticación simple** para Encargados de Inventario
- **Registro de movimientos** de inventario (Entrada, Salida, Ajuste, Pérdida)
- **Visualización en tiempo real** del estado del inventario
- **Validaciones** de stock negativo con confirmación
- **Interfaz intuitiva** dividida en dos paneles

## 📋 Requisitos Previos

- Python 3.8+
- Node.js 14+
- pip
- npm

## 🔧 Instalación

### Backend (Django)

1. Navegar a la carpeta backend:

```bash
cd backend
```

2. Instalar dependencias:

```bash
pip install djangorestframework django-cors-headers
```

3. Ejecutar migraciones:

```bash
python manage.py migrate
```

4. Crear datos de prueba:

```bash
python manage.py crear_datos_prueba
```

5. Iniciar el servidor:

```bash
python manage.py runserver
```

El backend estará disponible en `http://localhost:8000`

### Frontend (Svelte)

1. Navegar a la carpeta frontend:

```bash
cd frontend
```

2. Instalar dependencias:

```bash
npm install
```

3. Iniciar el servidor de desarrollo:

```bash
npm run dev
```

El frontend estará disponible en `http://localhost:5000`

## 👤 Usuarios de Prueba

El comando `crear_datos_prueba` crea los siguientes usuarios:

- **Juan Pérez**
- **María González**

Para hacer login, ingrese el nombre completo exacto.

## 📦 Datos de Ejemplo

Se crean automáticamente:

- 2 Encargados de Inventario
- 2 Inventarios
- 6 Materias Primas (Azúcar, Harina, Levadura, Sal, Aceite, Leche en Polvo)
- 6 Productos (Pan Blanco, Pan Integral, Galletas, Torta, Croissant, Pastel)

## 🎯 Caso de Uso Implementado

### Registrar Movimiento de Inventario

**Actor Principal:** Encargado de Inventario

**Flujo Básico:**

1. El encargado inicia sesión con su nombre
2. Selecciona el tipo de ítem (Producto o Materia Prima)
3. Elige el ítem específico del catálogo
4. Selecciona el tipo de movimiento (Entrada, Salida, Ajuste, Pérdida)
5. Ingresa la cantidad y el motivo
6. El sistema valida los datos
7. Si hay advertencia de stock negativo, solicita confirmación
8. El sistema registra el movimiento y actualiza el stock
9. El inventario se actualiza en tiempo real

**Validaciones:**

- Ítem debe existir en el catálogo
- Cantidad debe ser numérica y mayor a 0
- Motivo es obligatorio
- Advertencia si el stock resultante es negativo

## 🏗️ Estructura del Proyecto

```
Prueba_Concepto/
├── backend/                    # Django REST API
│   ├── api/
│   │   ├── models.py          # Modelos de datos
│   │   ├── serializers.py     # Serializers REST
│   │   ├── views.py           # Vistas y lógica de negocio
│   │   └── urls.py            # Endpoints API
│   └── backend/
│       └── settings.py        # Configuración Django
└── frontend/                  # Svelte SPA
    └── src/
        ├── App.svelte         # Componente principal
        └── components/
            ├── Login.svelte           # Login de encargado
            ├── Dashboard.svelte       # Dashboard principal
            ├── RegistroMovimiento.svelte  # Formulario de registro
            └── VistaInventario.svelte     # Visualización de stock
```

## 🔌 API Endpoints

### Autenticación

- `POST /api/login/` - Login de encargado

### Consulta

- `GET /api/productos/` - Listar productos
- `GET /api/materias-primas/` - Listar materias primas
- `GET /api/movimientos/` - Listar movimientos

### Operaciones

- `POST /api/registrar-movimiento/` - Registrar movimiento de inventario

### Ejemplo de Registro de Movimiento

```json
{
  "item_id": 1,
  "item_tipo": "producto",
  "tipo_movimiento": "SALIDA",
  "cantidad": 10,
  "motivo": "Venta del día",
  "encargado_id": 1,
  "confirmar": false
}
```

## 🎨 Capturas de Pantalla

### Login

Interfaz simple de autenticación donde el encargado ingresa su nombre completo.

### Dashboard

- **Panel Izquierdo:** Formulario de registro de movimientos
- **Panel Derecho:** Vista en tiempo real del inventario con indicadores de stock

### Características Visuales

- Código de colores para estados de stock (Normal, Bajo, Sin stock)
- Actualización automática del inventario
- Mensajes de confirmación y advertencia
- Interfaz responsive

## 🛠️ Tecnologías Utilizadas

### Backend

- Django 6.0
- Django REST Framework 3.16
- django-cors-headers 4.9
- SQLite (desarrollo)

### Frontend

- Svelte
- Rollup (bundler)
- Fetch API

## 📝 Notas de Desarrollo

- El proyecto usa SQLite para demostración. Para producción, use PostgreSQL o MySQL.
- CORS está habilitado solo para localhost:5000
- Los datos de prueba incluyen items con stock bajo para demostrar las validaciones
- El inventario se actualiza automáticamente cada 10 segundos

## 🔒 Consideraciones de Seguridad

Este es un proyecto de demostración. Para producción:

- Implementar autenticación real (JWT, OAuth)
- Agregar permisos y roles
- Validar entradas en el backend
- Usar HTTPS
- Implementar rate limiting
- Agregar logging de auditoría

## 📄 Licencia

# Proyecto de demostración educativa.

# Inventario_Prueba_Conceptual

Prueba conceptual para un modulo de gestion de inventario

> > > > > > > 6ae905fd1f6d5f3c51138079ff77127465e6fd07
