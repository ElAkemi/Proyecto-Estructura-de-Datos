"""Módulo de pruebas unitarias para las estructuras de datos del proyecto."""

import os
import sys

RAIZ_MODULO = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if RAIZ_MODULO not in sys.path:
    sys.path.insert(0, RAIZ_MODULO)

import unittest

from estructuras.arbol_tareas import ArbolTareas
from estructuras.cola_fifo import ColaFIFO
from estructuras.cola_prioridad import ColaPrioridad
from modelos.prioridad import Prioridad
from modelos.tarea import Tarea


class TestColaFIFO(unittest.TestCase):
    """Pruebas unitarias para la cola FIFO."""

    def test_fifo_operaciones(self):
        """Verifica las operaciones básicas de encolar y desencolar."""
        cola = ColaFIFO()
        self.assertTrue(cola.esta_vacia())
        cola.encolar("Tarea 1")
        cola.encolar("Tarea 2")

        self.assertEqual(len(cola), 2)
        self.assertEqual(cola.desencolar(), "Tarea 1")
        self.assertEqual(cola.desencolar(), "Tarea 2")
        self.assertTrue(cola.esta_vacia())


class TestColaPrioridad(unittest.TestCase):
    """Pruebas unitarias para la cola con prioridad."""

    def test_orden_prioridad(self):
        """Verifica que los elementos salgan ordenados por su prioridad."""
        cp = ColaPrioridad()
        t1 = Tarea(1, "Baja", Prioridad.BAJA, 101)
        t2 = Tarea(2, "Alta", Prioridad.ALTA, 102)
        t3 = Tarea(3, "Media", Prioridad.MEDIA, 103)

        cp.encolar(t1)
        cp.encolar(t2)
        cp.encolar(t3)

        self.assertEqual(cp.desencolar().id_tarea, 2)  # ALTA
        self.assertEqual(cp.desencolar().id_tarea, 3)  # MEDIA
        self.assertEqual(cp.desencolar().id_tarea, 1)  # BAJA


class TestArbolTareas(unittest.TestCase):
    """Pruebas unitarias para la estructura de árbol de tareas."""

    def test_jerarquia_subtareas(self):
        """Verifica la inserción y búsqueda de jerarquías en el árbol."""
        arbol = ArbolTareas(1, "Tarea Principal")
        self.assertTrue(arbol.agregar_subtarea(10, 1, "Subtarea 1"))
        self.assertTrue(
            arbol.agregar_subtarea(100, 10, "Subtarea Nivel 2")
        )

        nodo_hallado = arbol.buscar_nodo(100)
        self.assertIsNotNone(nodo_hallado)
        self.assertEqual(nodo_hallado.descripcion, "Subtarea Nivel 2")

        todas = arbol.obtener_todas()
        self.assertEqual(len(todas), 3)


if __name__ == "__main__":
    unittest.main()
