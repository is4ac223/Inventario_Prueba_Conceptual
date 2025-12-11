"""
Script para crear datos de prueba para el sistema de inventario
"""

from api.models import (
    EncargadoInventario, Inventario, MateriaPrima, Producto,
    UnidadVentaAgrupada, TipoDocumento
)
import os
import django
from datetime import date

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()


def crear_datos_prueba():
    print("Creando datos de prueba...")

    # Limpiar datos existentes
    print("Limpiando datos existentes...")
    EncargadoInventario.objects.all().delete()
    Inventario.objects.all().delete()
    MateriaPrima.objects.all().delete()
    Producto.objects.all().delete()
    UnidadVentaAgrupada.objects.all().delete()

    # Crear encargados de inventario
    print("Creando encargados...")
    encargado1 = EncargadoInventario.objects.create(
        nombre_completo="Juan Pérez",
        fecha_contrato=date(2023, 1, 15),
        tipo_documento=TipoDocumento.DNI
    )

    encargado2 = EncargadoInventario.objects.create(
        nombre_completo="María González",
        fecha_contrato=date(2023, 3, 10),
        tipo_documento=TipoDocumento.CEDULA
    )

    print(f"  ✓ Creados {EncargadoInventario.objects.count()} encargados")

    # Crear inventarios
    print("Creando inventarios...")
    inventario1 = Inventario.objects.create(
        ubicacion_almacenamiento="Almacén Principal - Zona A",
        capacidad_maxima=10000,
        fecha_ultima_revision=date.today()
    )

    inventario2 = Inventario.objects.create(
        ubicacion_almacenamiento="Almacén Secundario - Zona B",
        capacidad_maxima=5000,
        fecha_ultima_revision=date.today()
    )

    print(f"  ✓ Creados {Inventario.objects.count()} inventarios")

    # Crear unidades de venta agrupadas
    print("Creando unidades de venta...")
    unidad_caja = UnidadVentaAgrupada.objects.create(
        nombre="Caja",
        cantidad_contenida=12,
        unidad_medida_base="Unidades"
    )

    unidad_paquete = UnidadVentaAgrupada.objects.create(
        nombre="Paquete",
        cantidad_contenida=6,
        unidad_medida_base="Unidades"
    )

    print(
        f"  ✓ Creadas {UnidadVentaAgrupada.objects.count()} unidades de venta")

    # Crear materias primas
    print("Creando materias primas...")
    materias = [
        {"nombre": "Azúcar", "stock_actual": 500, "stock_minimo": 100,
            "costo_unitario": 2.50, "inventario": inventario1},
        {"nombre": "Harina", "stock_actual": 750, "stock_minimo": 150,
            "costo_unitario": 1.80, "inventario": inventario1},
        {"nombre": "Levadura", "stock_actual": 200, "stock_minimo": 50,
            "costo_unitario": 5.00, "inventario": inventario1},
        {"nombre": "Sal", "stock_actual": 300, "stock_minimo": 80,
            "costo_unitario": 0.50, "inventario": inventario2},
        {"nombre": "Aceite", "stock_actual": 150, "stock_minimo": 50,
            "costo_unitario": 4.20, "inventario": inventario2},
        {"nombre": "Leche en Polvo", "stock_actual": 80, "stock_minimo": 100,
            "costo_unitario": 8.50, "inventario": inventario1},
    ]

    for m in materias:
        MateriaPrima.objects.create(**m)

    print(f"  ✓ Creadas {MateriaPrima.objects.count()} materias primas")

    # Crear productos
    print("Creando productos...")
    productos = [
        {"nombre": "Pan Blanco", "stock_actual": 120, "stock_minimo": 50,
            "precio_unitario": 2.50, "inventario": inventario1},
        {"nombre": "Pan Integral", "stock_actual": 80, "stock_minimo": 40,
            "precio_unitario": 3.00, "inventario": inventario1},
        {"nombre": "Galletas de Chocolate", "stock_actual": 200,
            "stock_minimo": 100, "precio_unitario": 4.50, "inventario": inventario2},
        {"nombre": "Torta de Vainilla", "stock_actual": 30, "stock_minimo": 20,
            "precio_unitario": 12.00, "inventario": inventario2},
        {"nombre": "Croissant", "stock_actual": 60, "stock_minimo": 30,
            "precio_unitario": 3.50, "inventario": inventario1},
        {"nombre": "Pastel de Chocolate", "stock_actual": 15, "stock_minimo": 20,
            "precio_unitario": 15.00, "inventario": inventario2},
    ]

    for p in productos:
        producto = Producto.objects.create(**p)
        # Agregar unidades de venta
        producto.unidades_venta.add(unidad_caja, unidad_paquete)

    print(f"  ✓ Creados {Producto.objects.count()} productos")

    print("\n✅ Datos de prueba creados exitosamente!")
    print("\n📝 Resumen:")
    print(f"   - Encargados: {EncargadoInventario.objects.count()}")
    print(f"   - Inventarios: {Inventario.objects.count()}")
    print(f"   - Materias Primas: {MateriaPrima.objects.count()}")
    print(f"   - Productos: {Producto.objects.count()}")
    print("\n👤 Encargados creados:")
    for enc in EncargadoInventario.objects.all():
        print(f"   - {enc.nombre_completo}")


if __name__ == '__main__':
    crear_datos_prueba()
