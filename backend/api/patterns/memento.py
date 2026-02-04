# -*- coding: utf-8 -*-
"""
Patrón Memento para guardar y restaurar estados del inventario.
Permite hacer respaldos del estado del inventario y restaurarlo.
"""
from datetime import datetime
from typing import Dict, Any


class EstadoInventario:
    """
    Memento - Almacena el estado del inventario.
    No se persiste directamente, pero puede serializarse.
    """

    def __init__(self, ubicacion_almacenamiento, capacidad_maxima,
                 fecha_ultima_revision, total_materia_prima, total_producto,
                 stocks_materias_primas=None, stocks_productos=None):
        self.ubicacion_almacenamiento = ubicacion_almacenamiento
        self.capacidad_maxima = capacidad_maxima
        self.fecha_ultima_revision = fecha_ultima_revision
        self.total_materia_prima = total_materia_prima
        self.total_producto = total_producto
        # Guardar stocks individuales de cada item
        self.stocks_materias_primas = stocks_materias_primas or {}  # {id: stock_actual}
        self.stocks_productos = stocks_productos or {}  # {id: stock_actual}
        self.fecha_respaldo = datetime.now()

    def to_dict(self) -> Dict[str, Any]:
        """Convierte el estado a diccionario para persistencia"""
        return {
            'ubicacion_almacenamiento': self.ubicacion_almacenamiento,
            'capacidad_maxima': self.capacidad_maxima,
            'fecha_ultima_revision': str(self.fecha_ultima_revision),
            'total_materia_prima': self.total_materia_prima,
            'total_producto': self.total_producto,
            'fecha_respaldo': str(self.fecha_respaldo),
            'items_materias_primas': len(self.stocks_materias_primas),
            'items_productos': len(self.stocks_productos)
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]):
        """Crea un estado desde un diccionario"""
        from datetime import datetime
        return cls(
            ubicacion_almacenamiento=data['ubicacion_almacenamiento'],
            capacidad_maxima=data['capacidad_maxima'],
            fecha_ultima_revision=data['fecha_ultima_revision'],
            total_materia_prima=data['total_materia_prima'],
            total_producto=data['total_producto']
        )


class HistorialInventario:
    """
    Caretaker - Gestiona el historial de estados del inventario.
    Patrón Memento - no se persiste como modelo.
    """

    def __init__(self):
        self._historial = []

    def respaldar(self, inventario):
        """
        Guarda el estado actual del inventario incluyendo stocks individuales.

        Args:
            inventario: Instancia del modelo Inventario

        Returns:
            EstadoInventario creado
        """
        from api.models import MateriaPrima, Producto

        # Obtener todas las materias primas y productos
        materias_primas = MateriaPrima.objects.filter(inventario=inventario)
        productos = Producto.objects.filter(inventario=inventario)

        # Guardar stocks actuales de cada item
        stocks_materias_primas = {
            mp.id: mp.stock_actual for mp in materias_primas
        }
        stocks_productos = {
            p.id: p.stock_actual for p in productos
        }

        # Calcular totales
        total_materia_prima = materias_primas.count()
        total_producto = productos.count()

        # Crear memento
        estado = EstadoInventario(
            ubicacion_almacenamiento=inventario.ubicacion_almacenamiento,
            capacidad_maxima=inventario.capacidad_maxima,
            fecha_ultima_revision=inventario.fecha_ultima_revision,
            total_materia_prima=total_materia_prima,
            total_producto=total_producto,
            stocks_materias_primas=stocks_materias_primas,
            stocks_productos=stocks_productos
        )

        self._historial.append(estado)
        return estado

    def deshacer(self, inventario):
        """
        Restaura el inventario al último estado guardado.

        Args:
            inventario: Instancia del modelo Inventario

        Returns:
            EstadoInventario restaurado o None si no hay historial
        """
        if not self._historial:
            return None

        estado = self._historial.pop()
        self._restaurar_estado(inventario, estado)
        return estado

    def _restaurar_estado(self, inventario, estado):
        """
        Restaura el estado del inventario incluyendo stocks individuales.

        Args:
            inventario: Instancia del modelo Inventario
            estado: EstadoInventario a restaurar
        """
        from api.models import MateriaPrima, Producto

        # Restaurar información básica del inventario
        inventario.ubicacion_almacenamiento = estado.ubicacion_almacenamiento
        inventario.capacidad_maxima = estado.capacidad_maxima
        inventario.fecha_ultima_revision = estado.fecha_ultima_revision
        inventario.save()

        # Restaurar stocks de materias primas
        for item_id, stock in estado.stocks_materias_primas.items():
            try:
                materia_prima = MateriaPrima.objects.get(id=item_id)
                materia_prima.stock_actual = stock
                materia_prima.save()
            except MateriaPrima.DoesNotExist:
                # Item ya no existe, simplemente continuar
                pass

        # Restaurar stocks de productos
        for item_id, stock in estado.stocks_productos.items():
            try:
                producto = Producto.objects.get(id=item_id)
                producto.stock_actual = stock
                producto.save()
            except Producto.DoesNotExist:
                # Item ya no existe, simplemente continuar
                pass

    def obtener_historial(self):
        """Retorna la lista de estados guardados"""
        return self._historial.copy()

    def limpiar_historial(self):
        """Limpia todo el historial"""
        self._historial.clear()
