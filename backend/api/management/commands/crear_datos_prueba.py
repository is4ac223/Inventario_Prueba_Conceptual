from django.core.management.base import BaseCommand
from datetime import date

from api.models import EncargadoInventario, TipoDocumento


class Command(BaseCommand):
    help = 'Asigna contraseñas a encargados de inventario (solo contraseñas, sin modificar otros datos)'

    def handle(self, *args, **kwargs):
        self.stdout.write("Asignando contraseñas a encargados...")

        # Obtener o crear encargado 1
        self.stdout.write("\nProcesando: Juan Pérez")
        encargado1, created = EncargadoInventario.objects.get_or_create(
            nombre_completo="Juan Pérez",
            defaults={
                'fecha_contrato': date(2023, 1, 15),
                'tipo_documento': TipoDocumento.DNI
            }
        )
        encargado1.set_password("juan123")
        encargado1.save()

        if created:
            self.stdout.write(f"  ✓ Creado nuevo encargado")
        else:
            self.stdout.write(f"  ✓ Encargado ya existía")
        self.stdout.write(f"  ✓ Contraseña asignada: juan123")

        # Obtener o crear encargado 2
        self.stdout.write("\nProcesando: María González")
        encargado2, created = EncargadoInventario.objects.get_or_create(
            nombre_completo="María González",
            defaults={
                'fecha_contrato': date(2023, 3, 10),
                'tipo_documento': TipoDocumento.CEDULA
            }
        )
        encargado2.set_password("maria123")
        encargado2.save()

        if created:
            self.stdout.write(f"  ✓ Creado nuevo encargado")
        else:
            self.stdout.write(f"  ✓ Encargado ya existía")
        self.stdout.write(f"  ✓ Contraseña asignada: maria123")
        self.stdout.write(self.style.SUCCESS(
            '\n✅ Contraseñas asignadas correctamente!'))
        self.stdout.write("\n👤 Credenciales disponibles:")
        self.stdout.write("   - Usuario: Juan Pérez")
        self.stdout.write("     Contraseña: juan123")
        self.stdout.write("   - Usuario: María González")
        self.stdout.write("     Contraseña: maria123")
        self.stdout.write("\n📝 Nota: Solo se modificaron las contraseñas.")
        self.stdout.write(
            "   El resto de datos del inventario no fue alterado.")
