import unittest
import tempfile
import os

from models.usuario import Usuario
from models.tarea import Tarea
from models.prioridad import Prioridad

from structures.lista_doble import ListaDoble
from structures.pila import Pila
from structures.cola_fifo import ColaFIFO
from structures.cola_prioridad import ColaPrioridad
from structures.nodo_arbol import NodoArbolTarea

from services.ordenador_tareas import OrdenadorTareas
from services.tarea_service import TareaService

from persistence.tarea_repository import TareaRepository


class TestGlobal(unittest.TestCase):

    # =========================================================
    # USUARIO
    # =========================================================

    def test_usuario_valido(self):
        usuario = Usuario(1, "Ana", "Usuario")

        self.assertEqual(usuario.id, 1)
        self.assertEqual(usuario.nombre, "Ana")
        self.assertEqual(usuario.rol, "Usuario")

    def test_usuario_administrador(self):
        usuario = Usuario(2, "Carlos", "Administrador")

        self.assertEqual(usuario.id, 2)
        self.assertEqual(usuario.nombre, "Carlos")
        self.assertEqual(usuario.rol, "Administrador")

    def test_usuario_rol_invalido(self):
        with self.assertRaises(ValueError):
            Usuario(1, "Ana", "Invitado")

    # =========================================================
    # LISTA DOBLEMENTE ENLAZADA
    # =========================================================

    def test_lista_doble_insertar(self):
        lista = ListaDoble()

        usuario = Usuario(
            1,
            "Ana",
            "Usuario"
        )

        resultado = lista.insertar(usuario)

        self.assertTrue(resultado)

    def test_lista_doble_buscar(self):
        lista = ListaDoble()

        usuario = Usuario(
            1,
            "Ana",
            "Usuario"
        )

        lista.insertar(usuario)

        encontrado = lista.buscar(1)

        self.assertIsNotNone(encontrado)
        self.assertEqual(encontrado.nombre, "Ana")

    def test_lista_doble_id_repetido(self):
        lista = ListaDoble()

        lista.insertar(
            Usuario(1, "Ana", "Usuario")
        )

        resultado = lista.insertar(
            Usuario(1, "Carlos", "Usuario")
        )

        self.assertFalse(resultado)

    def test_lista_doble_eliminar(self):
        lista = ListaDoble()

        lista.insertar(
            Usuario(1, "Ana", "Usuario")
        )

        resultado = lista.eliminar(1)

        self.assertTrue(resultado)
        self.assertIsNone(lista.buscar(1))

    def test_lista_doble_eliminar_inexistente(self):
        lista = ListaDoble()

        self.assertFalse(
            lista.eliminar(999)
        )

    # =========================================================
    # PILA
    # =========================================================

    def test_pila_apilar(self):
        pila = Pila()

        pila.apilar("A")
        pila.apilar("B")

        self.assertFalse(
            pila.esta_vacia()
        )

    def test_pila_lifo(self):
        pila = Pila()

        pila.apilar("A")
        pila.apilar("B")
        pila.apilar("C")

        self.assertEqual(
            pila.desapilar(),
            "C"
        )

        self.assertEqual(
            pila.desapilar(),
            "B"
        )

        self.assertEqual(
            pila.desapilar(),
            "A"
        )

    def test_pila_peek(self):
        pila = Pila()

        pila.apilar("A")

        self.assertEqual(
            pila.peek(),
            "A"
        )

        self.assertFalse(
            pila.esta_vacia()
        )

    def test_pila_vacia(self):
        pila = Pila()

        self.assertTrue(
            pila.esta_vacia()
        )

        self.assertIsNone(
            pila.peek()
        )

    # =========================================================
    # COLA FIFO
    # =========================================================

    def crear_tarea(self, id_tarea, prioridad):
        return Tarea(
            id_tarea,
            f"Tarea {id_tarea}",
            prioridad,
            1
        )

    def test_cola_fifo_encolar(self):
        cola = ColaFIFO()

        tarea = self.crear_tarea(
            1,
            Prioridad.ALTA
        )

        cola.encolar(tarea)

        self.assertFalse(
            cola.esta_vacia()
        )

        self.assertEqual(
            len(cola),
            1
        )

    def test_cola_fifo(self):
        cola = ColaFIFO()

        tarea1 = self.crear_tarea(
            1,
            Prioridad.BAJA
        )

        tarea2 = self.crear_tarea(
            2,
            Prioridad.ALTA
        )

        cola.encolar(tarea1)
        cola.encolar(tarea2)

        self.assertEqual(
            cola.ver_frente(),
            tarea1
        )

        self.assertEqual(
            cola.desencolar(),
            tarea1
        )

        self.assertEqual(
            cola.desencolar(),
            tarea2
        )

    def test_cola_fifo_vacia(self):
        cola = ColaFIFO()

        with self.assertRaises(IndexError):
            cola.desencolar()

    def test_cola_fifo_buscar(self):
        cola = ColaFIFO()

        tarea = self.crear_tarea(
            10,
            Prioridad.MEDIA
        )

        cola.encolar(tarea)

        self.assertEqual(
            cola.buscar_por_id(10),
            tarea
        )

    def test_cola_fifo_buscar_inexistente(self):
        cola = ColaFIFO()

        self.assertIsNone(
            cola.buscar_por_id(999)
        )

    def test_cola_fifo_eliminar(self):
        cola = ColaFIFO()

        cola.encolar(
            self.crear_tarea(
                1,
                Prioridad.ALTA
            )
        )

        cola.encolar(
            self.crear_tarea(
                2,
                Prioridad.MEDIA
            )
        )

        self.assertTrue(
            cola.eliminar_por_id(1)
        )

        self.assertIsNone(
            cola.buscar_por_id(1)
        )

    def test_cola_fifo_eliminar_inexistente(self):
        cola = ColaFIFO()

        self.assertFalse(
            cola.eliminar_por_id(999)
        )

    # =========================================================
    # COLA DE PRIORIDAD
    # =========================================================

    def test_cola_prioridad(self):
        cola = ColaPrioridad()

        baja = self.crear_tarea(
            1,
            Prioridad.BAJA
        )

        alta = self.crear_tarea(
            2,
            Prioridad.ALTA
        )

        media = self.crear_tarea(
            3,
            Prioridad.MEDIA
        )

        cola.encolar(baja)
        cola.encolar(alta)
        cola.encolar(media)

        self.assertEqual(
            cola.desencolar(),
            alta
        )

        self.assertEqual(
            cola.desencolar(),
            media
        )

        self.assertEqual(
            cola.desencolar(),
            baja
        )

    def test_cola_prioridad_vacia(self):
        cola = ColaPrioridad()

        with self.assertRaises(IndexError):
            cola.desencolar()

    def test_cola_prioridad_buscar(self):
        cola = ColaPrioridad()

        tarea = self.crear_tarea(
            5,
            Prioridad.ALTA
        )

        cola.encolar(tarea)

        self.assertEqual(
            cola.buscar_por_id(5),
            tarea
        )

    def test_cola_prioridad_eliminar(self):
        cola = ColaPrioridad()

        cola.encolar(
            self.crear_tarea(
                1,
                Prioridad.ALTA
            )
        )

        cola.encolar(
            self.crear_tarea(
                2,
                Prioridad.BAJA
            )
        )

        self.assertTrue(
            cola.eliminar_por_id(1)
        )

        self.assertIsNone(
            cola.buscar_por_id(1)
        )

    # =========================================================
    # ARBOL
    # =========================================================

    def crear_arbol(self):
        return NodoArbolTarea(
            id_subtarea=1,
            descripcion="Principal",
            id_padre=None
        )

    def test_arbol_raiz(self):
        arbol = self.crear_arbol()

        nodo = arbol.buscar_nodo(1)

        self.assertIsNotNone(nodo)
        self.assertEqual(
            nodo.descripcion,
            "Principal"
        )

    def test_arbol_agregar_subtarea(self):
        arbol = self.crear_arbol()

        resultado = arbol.agregar_subtarea(
            1,
            2,
            "Subtarea"
        )

        self.assertTrue(resultado)

        nodo = arbol.buscar_nodo(2)

        self.assertIsNotNone(nodo)

    def test_arbol_subtarea_anidada(self):
        arbol = self.crear_arbol()

        arbol.agregar_subtarea(
            1,
            2,
            "Subtarea 1"
        )

        resultado = arbol.agregar_subtarea(
            2,
            3,
            "Subtarea 2"
        )

        self.assertTrue(resultado)

        nodo = arbol.buscar_nodo(3)

        self.assertIsNotNone(nodo)
        self.assertEqual(
            nodo.id_padre,
            2
        )

    def test_arbol_buscar_inexistente(self):
        arbol = self.crear_arbol()

        self.assertIsNone(
            arbol.buscar_nodo(999)
        )

    def test_arbol_obtener_todas(self):
        arbol = self.crear_arbol()

        arbol.agregar_subtarea(
            1,
            2,
            "Subtarea 1"
        )

        arbol.agregar_subtarea(
            1,
            3,
            "Subtarea 2"
        )

        resultado = arbol.obtener_todas()

        self.assertEqual(
            len(resultado),
            3
        )

    # =========================================================
    # ORDENAMIENTO
    # =========================================================

    def crear_tareas(self):
        return [
            self.crear_tarea(
                5,
                Prioridad.MEDIA
            ),
            self.crear_tarea(
                2,
                Prioridad.ALTA
            ),
            self.crear_tarea(
                8,
                Prioridad.BAJA
            ),
            self.crear_tarea(
                1,
                Prioridad.ALTA
            ),
            self.crear_tarea(
                4,
                Prioridad.MEDIA
            )
        ]

    def ids(self, tareas):
        return [
            tarea.id_tarea
            for tarea in tareas
        ]

    def test_mergesort(self):
        resultado = OrdenadorTareas.mergesort(
            self.crear_tareas()
        )

        self.assertEqual(
            self.ids(resultado),
            [1, 2, 4, 5, 8]
        )

    def test_mergesort_reverso(self):
        resultado = OrdenadorTareas.mergesort(
            self.crear_tareas(),
            reverso=True
        )

        self.assertEqual(
            self.ids(resultado),
            [8, 5, 4, 2, 1]
        )

    def test_bubblesort(self):
        resultado = OrdenadorTareas.bubblesort(
            self.crear_tareas()
        )

        self.assertEqual(
            self.ids(resultado),
            [1, 2, 4, 5, 8]
        )

    def test_bubblesort_reverso(self):
        resultado = OrdenadorTareas.bubblesort(
            self.crear_tareas(),
            reverso=True
        )

        self.assertEqual(
            self.ids(resultado),
            [8, 5, 4, 2, 1]
        )

    def test_quicksort(self):
        resultado = OrdenadorTareas.quicksort(
            self.crear_tareas()
        )

        self.assertEqual(
            self.ids(resultado),
            [1, 2, 4, 5, 8]
        )

    def test_quicksort_reverso(self):
        resultado = OrdenadorTareas.quicksort(
            self.crear_tareas(),
            reverso=True
        )

        self.assertEqual(
            self.ids(resultado),
            [8, 5, 4, 2, 1]
        )

    def test_ordenamientos_lista_vacia(self):
        self.assertEqual(
            OrdenadorTareas.mergesort([]),
            []
        )

        self.assertEqual(
            OrdenadorTareas.bubblesort([]),
            []
        )

        self.assertEqual(
            OrdenadorTareas.quicksort([]),
            []
        )

    def test_ordenamientos_un_elemento(self):
        tarea = self.crear_tarea(
            1,
            Prioridad.ALTA
        )

        for metodo in [
            OrdenadorTareas.mergesort,
            OrdenadorTareas.bubblesort,
            OrdenadorTareas.quicksort
        ]:
            resultado = metodo([tarea])

            self.assertEqual(
                resultado,
                [tarea]
            )

    # =========================================================
    # TAREA SERVICE
    # =========================================================

    def setUp(self):
        archivo = tempfile.NamedTemporaryFile(
            delete=False,
            suffix=".csv"
        )

        archivo.close()

        self.archivo_tareas = archivo.name

        self.repository = TareaRepository(
            self.archivo_tareas
        )

        self.tarea_service = TareaService(
            self.repository
        )

    def tearDown(self):
        if os.path.exists(
            self.archivo_tareas
        ):
            os.remove(
                self.archivo_tareas
            )

    def test_tarea_service_agregar(self):
        resultado = self.tarea_service.agregar_tarea(
            1,
            "Crear sistema",
            Prioridad.ALTA,
            1
        )

        self.assertTrue(resultado)

        tarea = self.tarea_service.buscar_tarea(1)

        self.assertIsNotNone(tarea)
        self.assertEqual(
            tarea.descripcion,
            "Crear sistema"
        )

    def test_tarea_service_id_repetido(self):
        self.tarea_service.agregar_tarea(
            1,
            "Tarea",
            Prioridad.ALTA,
            1
        )

        resultado = self.tarea_service.agregar_tarea(
            1,
            "Otra",
            Prioridad.BAJA,
            1
        )

        self.assertFalse(resultado)

    def test_tarea_service_descripcion_vacia(self):
        resultado = self.tarea_service.agregar_tarea(
            1,
            "",
            Prioridad.ALTA,
            1
        )

        self.assertFalse(resultado)

    def test_tarea_service_id_invalido(self):
        resultado = self.tarea_service.agregar_tarea(
            0,
            "Tarea",
            Prioridad.ALTA,
            1
        )

        self.assertFalse(resultado)

    def test_tarea_service_usuario_invalido(self):
        resultado = self.tarea_service.agregar_tarea(
            1,
            "Tarea",
            Prioridad.ALTA,
            0
        )

        self.assertFalse(resultado)

    def test_tarea_service_buscar(self):
        self.tarea_service.agregar_tarea(
            1,
            "Tarea",
            Prioridad.MEDIA,
            1
        )

        tarea = self.tarea_service.buscar_tarea(1)

        self.assertIsNotNone(tarea)

    def test_tarea_service_buscar_inexistente(self):
        self.assertIsNone(
            self.tarea_service.buscar_tarea(999)
        )

    def test_tarea_service_modificar(self):
        self.tarea_service.agregar_tarea(
            1,
            "Original",
            Prioridad.BAJA,
            1
        )

        resultado = self.tarea_service.modificar_tarea(
            1,
            nueva_descripcion="Modificada",
            nueva_prioridad=Prioridad.ALTA,
            nuevo_id_usuario=2
        )

        self.assertTrue(resultado)

        tarea = self.tarea_service.buscar_tarea(1)

        self.assertEqual(
            tarea.descripcion,
            "Modificada"
        )

        self.assertEqual(
            tarea.prioridad,
            Prioridad.ALTA
        )

        self.assertEqual(
            tarea.id_usuario,
            2
        )

    def test_tarea_service_modificar_inexistente(self):
        resultado = self.tarea_service.modificar_tarea(
            999,
            nueva_descripcion="Nueva"
        )

        self.assertFalse(resultado)

    def test_tarea_service_eliminar(self):
        self.tarea_service.agregar_tarea(
            1,
            "Tarea",
            Prioridad.ALTA,
            1
        )

        resultado = self.tarea_service.eliminar_tarea(1)

        self.assertTrue(resultado)

        self.assertIsNone(
            self.tarea_service.buscar_tarea(1)
        )

    def test_tarea_service_eliminar_inexistente(self):
        self.assertFalse(
            self.tarea_service.eliminar_tarea(999)
        )

    # =========================================================
    # SUBTAREAS
    # =========================================================

    def crear_tarea_service(self):
        self.tarea_service.agregar_tarea(
            1,
            "Tarea principal",
            Prioridad.ALTA,
            1
        )

    def test_tarea_agregar_subtarea(self):
        self.crear_tarea_service()

        resultado = self.tarea_service.agregar_subtarea(
            1,
            2,
            "Subtarea"
        )

        self.assertTrue(resultado)

        subtarea = self.tarea_service.buscar_subtarea(2)

        self.assertIsNotNone(subtarea)

    def test_tarea_agregar_subtarea_anidada(self):
        self.crear_tarea_service()

        self.tarea_service.agregar_subtarea(
            1,
            2,
            "Subtarea 1"
        )

        resultado = self.tarea_service.agregar_subtarea(
            2,
            3,
            "Subtarea 2"
        )

        self.assertTrue(resultado)

        self.assertIsNotNone(
            self.tarea_service.buscar_subtarea(3)
        )

    def test_tarea_subtarea_id_repetido(self):
        self.crear_tarea_service()

        self.tarea_service.agregar_subtarea(
            1,
            2,
            "Subtarea"
        )

        resultado = self.tarea_service.agregar_subtarea(
            1,
            2,
            "Otra"
        )

        self.assertFalse(resultado)

    def test_tarea_subtarea_padre_inexistente(self):
        self.crear_tarea_service()

        resultado = self.tarea_service.agregar_subtarea(
            999,
            2,
            "Subtarea"
        )

        self.assertFalse(resultado)

    def test_tarea_buscar_subtarea_inexistente(self):
        self.assertIsNone(
            self.tarea_service.buscar_subtarea(999)
        )

    def test_tarea_eliminar_subtarea(self):
        self.crear_tarea_service()

        self.tarea_service.agregar_subtarea(
            1,
            2,
            "Subtarea"
        )

        resultado = self.tarea_service.eliminar_subtarea(2)

        self.assertTrue(resultado)

        self.assertIsNone(
            self.tarea_service.buscar_subtarea(2)
        )

    def test_tarea_eliminar_subtarea_inexistente(self):
        self.assertFalse(
            self.tarea_service.eliminar_subtarea(999)
        )

    def test_tarea_completar_subtarea(self):
        self.crear_tarea_service()

        self.tarea_service.agregar_subtarea(
            1,
            2,
            "Subtarea"
        )

        resultado = self.tarea_service.completar_subtarea(2)

        self.assertTrue(resultado)

        subtarea = self.tarea_service.buscar_subtarea(2)

        self.assertTrue(
            subtarea.completada
        )

    def test_tarea_completar_inexistente(self):
        resultado = self.tarea_service.completar_subtarea(
            999
        )

        self.assertFalse(resultado)

    def test_tarea_listar_subtareas(self):
        self.crear_tarea_service()

        self.tarea_service.agregar_subtarea(
            1,
            2,
            "Subtarea 1"
        )

        self.tarea_service.agregar_subtarea(
            1,
            3,
            "Subtarea 2"
        )

        resultado = self.tarea_service.listar_subtareas(1)

        self.assertEqual(
            len(resultado),
            3
        )

    def test_tarea_listar_inexistente(self):
        resultado = self.tarea_service.listar_subtareas(
            999
        )

        self.assertEqual(
            resultado,
            []
        )


if __name__ == "__main__":
    unittest.main()