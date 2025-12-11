from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import date

from api.models import (
    EncargadoInventario, Inventario, MateriaPrima, Producto,
    UnidadVentaAgrupada, TipoDocumento
)


class Command(BaseCommand):
    help = 'Crea datos de prueba para el sistema de inventario'

    def handle(self, *args, **kwargs):
        self.stdout.write("Creando datos de prueba...")

        # Limpiar datos existentes
        self.stdout.write("Limpiando datos existentes...")
        EncargadoInventario.objects.all().delete()
        Inventario.objects.all().delete()
        MateriaPrima.objects.all().delete()
        Producto.objects.all().delete()
        UnidadVentaAgrupada.objects.all().delete()

        # Crear encargados de inventario
        self.stdout.write("Creando encargados...")
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

        self.stdout.write(
            f"  ✓ Creados {EncargadoInventario.objects.count()} encargados")

        # Crear inventarios
        self.stdout.write("Creando inventarios...")
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

        self.stdout.write(
            f"  ✓ Creados {Inventario.objects.count()} inventarios")

        # Crear unidades de venta agrupadas
        self.stdout.write("Creando unidades de venta...")
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

        self.stdout.write(
            f"  ✓ Creadas {UnidadVentaAgrupada.objects.count()} unidades de venta")

        # Crear materias primas
        self.stdout.write("Creando materias primas...")
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

        self.stdout.write(
            f"  ✓ Creadas {MateriaPrima.objects.count()} materias primas")

        # Crear productos
        self.stdout.write("Creando productos...")
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
            producto.unidades_venta.add(unidad_caja, unidad_paquete)

        self.stdout.write(f"  ✓ Creados {Producto.objects.count()} productos")

        self.stdout.write(self.style.SUCCESS(
            '\n✅ Datos de prueba creados exitosamente!'))
        self.stdout.write("\n📝 Resumen:")
        self.stdout.write(
            f"   - Encargados: {EncargadoInventario.objects.count()}")
        self.stdout.write(f"   - Inventarios: {Inventario.objects.count()}")
        self.stdout.write(
            f"   - Materias Primas: {MateriaPrima.objects.count()}")
        self.stdout.write(f"   - Productos: {Producto.objects.count()}")
        self.stdout.write("\n👤 Encargados creados (para login):")
        for enc in EncargadoInventario.objects.all():
            self.stdout.write(f"   - {enc.nombre_completo}")
