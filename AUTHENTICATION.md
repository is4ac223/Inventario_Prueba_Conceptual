# Sistema de Autenticación Mejorado

## Descripción General

El sistema de autenticación ha sido mejorado para requerir tanto nombre de usuario como contraseña, reemplazando el sistema anterior que solo requería nombre.

## Cambios Implementados

### Backend (Django)

#### 1. Modelo `EncargadoInventario` Actualizado

Se agregó un campo `password` al modelo:

```python
class EncargadoInventario(models.Model):
    nombre_completo = models.TextField()
    password = models.CharField(max_length=255, blank=True, default='')
    fecha_contrato = models.DateField()
    tipo_documento = models.CharField(...)

    def set_password(self, raw_password):
        """Hash y guarda la contraseña"""
        self.password = make_password(raw_password)
        self.save()

    def check_password(self, raw_password):
        """Verifica si la contraseña proporcionada es correcta"""
        return check_password(raw_password, self.password)
```

**Características de Seguridad:**

- Las contraseñas se hashean usando el algoritmo de Django (PBKDF2 por defecto)
- Las contraseñas NUNCA se almacenan en texto plano
- Métodos para verificar contraseñas de forma segura

#### 2. Serializer de Login `EncargadoInventarioLoginSerializer`

Nuevo serializer que maneja la validación de credenciales:

```python
class EncargadoInventarioLoginSerializer(serializers.Serializer):
    nombre_completo = serializers.CharField(required=True, max_length=255)
    password = serializers.CharField(required=True, max_length=255)

    def validate(self, data):
        # Valida nombre y contraseña
        # Levanta excepción si credenciales son inválidas
        return data
```

#### 3. Vista `LoginEncargadoView` Mejorada

La vista ahora utiliza el serializer para validar credenciales:

```python
class LoginEncargadoView(APIView):
    def post(self, request):
        serializer = EncargadoInventarioLoginSerializer(data=request.data)

        if serializer.is_valid():
            encargado = serializer.validated_data['encargado']
            # Retorna datos del usuario sin contraseña
            return Response({...}, status=status.HTTP_200_OK)

        return Response({
            'error': serializer.errors
        }, status=status.HTTP_401_UNAUTHORIZED)
```

#### 4. Migración

Se creó la migración `0006_encargadoinventario_password` que agrega el campo a la base de datos existente.

### Frontend (Svelte)

#### Componente `Login.svelte` Actualizado

El formulario ahora solicita dos campos:

```svelte
<form on:submit|preventDefault={handleSubmit}>
    <div class="form-group">
        <label for="nombre">Nombre Completo:</label>
        <input type="text" bind:value={nombreCompleto} ... />
    </div>

    <div class="form-group">
        <label for="password">Contraseña:</label>
        <input type="password" bind:value={password} ... />
    </div>
</form>
```

**Cambios:**

- Agregado campo de contraseña (tipo password)
- Validación básica del cliente
- Manejo mejorado de errores del servidor
- Mensajes de error más descriptivos

## Endpoints de API

### POST `/api/login/`

**Request:**

```json
{
  "nombre_completo": "Juan Pérez",
  "password": "juan123"
}
```

**Response (Éxito - 200):**

```json
{
  "mensaje": "Login exitoso",
  "encargado": {
    "id": 1,
    "nombre_completo": "Juan Pérez",
    "fecha_contrato": "2023-01-15",
    "tipo_documento": "DNI"
  }
}
```

**Response (Error - 401):**

```json
{
  "error": {
    "non_field_errors": ["Contraseña incorrecta"]
  }
}
```

## Credenciales de Prueba

Las credenciales de prueba se crean automáticamente al ejecutar:

```bash
python manage.py crear_datos_prueba
```

| Usuario        | Contraseña |
| -------------- | ---------- |
| Juan Pérez     | juan123    |
| María González | maria123   |

## Migración de Datos Existentes

### Para Usuarios Existentes

Si tenías usuarios creados antes de esta actualización, deben establecer sus contraseñas:

**Opción 1: Usar Django Admin**

```bash
python manage.py createsuperuser  # Si no existe
python manage.py runserver
# Ve a http://localhost:8000/admin
# Edita cada usuario y establece contraseña
```

**Opción 2: Script de Migración**

```python
from api.models import EncargadoInventario

# Establece contraseña para todos los usuarios sin contraseña
for encargado in EncargadoInventario.objects.filter(password=''):
    encargado.set_password(f"{encargado.nombre_completo.lower().replace(' ', '')}123")
    print(f"Contraseña establecida para {encargado.nombre_completo}")
```

**Opción 3: Recrear Datos de Prueba**

```bash
# Esto borra todos los datos y crea nuevos con contraseñas
python manage.py crear_datos_prueba
```

## Mejoras de Seguridad

1. **Hashing de Contraseñas**: Usa PBKDF2 por defecto (configurable)
2. **Validación del Servidor**: Validación completa en el backend
3. **Códigos HTTP Apropiados**: 401 para credenciales inválidas
4. **Campos Seguros**: No retorna contraseña en respuestas
5. **Validación del Cliente**: Previene envíos vacíos

## Próximos Pasos Recomendados

Para mejorar aún más la seguridad:

1. **Implementar JWT**: Para mantener sesiones sin estado
2. **Rate Limiting**: Limitar intentos de login fallidos
3. **2FA (Two-Factor Authentication)**: Autenticación de dos factores
4. **Audit Log**: Registrar intentos de login
5. **Session Management**: Implementar logout y destrucción de sesiones
6. **Password Reset**: Sistema de recuperación de contraseña

## Troubleshooting

### Error: "Contraseña incorrecta"

- Verifica que escribiste bien la contraseña
- Las contraseñas son sensibles a mayúsculas/minúsculas
- Para usuarios creados manualmente, asegúrate de usar `set_password()`

### Error: "Encargado no encontrado"

- Verifica el nombre completo exacto
- El nombre es insensible a mayúsculas (case-insensitive)
- Ejecuta `python manage.py crear_datos_prueba` para tener datos de prueba

### Campo password vacío para usuarios antiguos

- Usa uno de los métodos de migración descritos arriba
- O ejecuta `python manage.py crear_datos_prueba` para empezar de nuevo
