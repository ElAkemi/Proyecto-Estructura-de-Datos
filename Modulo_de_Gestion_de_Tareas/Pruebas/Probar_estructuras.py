import unittest
try:
    from .Models.Tarea import Tarea

    from .Models.Prioridad import Prioridad
    from .Estructuras.ColaFIFO import ColaFIFO
    from .Estructuras.ColaPrioridad import ColaPrioridad
    from .Estructuras.ArbolTareas import ArbolTareas
    from .Models.NodoArbol import NodoArbolTarea
except (ImportError, ValueError):
    from Models.Tarea import Tarea
    from Models.Prioridad import Prioridad
    from Estructuras.ColaFIFO import ColaFIFO
    from Estructuras.ColaPrioridad import ColaPrioridad
    from Estructuras.ArbolTareas import ArbolTareas
    from Models.NodoArbol import NodoArbolTarea


class TestColaFIFO(unittest.TestCase):
    def test_fifo_operaciones(self):
        cola = ColaFIFO()
        self.assertTrue(cola.esta_vacia())
        cola.encolar("Tarea 1")
        cola.encolar("Tarea 2")
        self.assertEqual(len(cola), 2)
        self.assertEqual(cola.desencolar(), "Tarea 1")
        self.assertEqual(cola.desencolar(), "Tarea 2")
        self.assertTrue(cola.esta_vacia())

class TestColaPrioridad(unittest.TestCase):
    def test_orden_prioridad(self):
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
    def test_jerarquia_subtareas(self):
        arbol = ArbolTareas(1, "Tarea Principal")
        self.assertTrue(arbol.agregar_subtarea(10, 1, "Subtarea 1"))
        self.assertTrue(arbol.agregar_subtarea(100, 10, "Subtarea Nivel 2"))
        
        nodo_hallado = arbol.buscar_nodo(100)
        self.assertIsNotNone(nodo_hallado)
        self.assertEqual(nodo_hallado.descripcion, "Subtarea Nivel 2")
        
        todas = arbol.obtener_todas()
        self.assertEqual(len(todas), 3)

if __name__ == "__main__":
    unittest.main()