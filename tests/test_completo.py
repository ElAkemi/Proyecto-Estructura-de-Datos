import unittest
import tempfile
import os

from models.usuario import Usuario
from models.tarea import Tarea
from models.prioridad import Prioridad
from models.accion import Accion

from persistence.usuario_repository import UsuarioRepository
from persistence.tarea_repository import TareaRepository

from services.usuario_service import UsuarioService
from services.tarea_service import TareaService
from services.historial_service import HistorialService
from services.sistema_service import SistemaService
from services.ordenador_tareas import OrdenadorTareas

from structures.arbol_tareas import ArbolTareas
from structures.nodo_arbol import NodoArbolTarea
from structures.lista_doble import ListaDoble
from structures.pila import Pila
from structures.cola_fifo import ColaFIFO
from structures.cola_prioridad import ColaPrioridad


class TestCompleto(unittest.TestCase):

    # =========================================================
    # UTILIDADES
    # =========================================================

    def crear_archivo(self):
        archivo = tempfile.NamedTemporaryFile(
            delete=False,
            suffix=".csv"
        )
        archivo.close()
        return archivo.name

    def eliminar_archivo(self, archivo):
        if os.path.exists(archivo):
            os.remove(archivo)

    def crear_tarea(
        self,
        id_tarea,
        prioridad=Prioridad.MEDIA
    ):
        return Tarea(
            id_tarea,
            f"Tarea {id_tarea}",
            prioridad,
            1
        )

    # =========================================================
    # MODELO PRIORIDAD
    # =========================================================

    def test_prioridades(self):
        self.assertIsNotNone(
            Prioridad.ALTA
        )

        self.assertIsNotNone(
            Prioridad.MEDIA
        )

        self.assertIsNotNone(
            Prioridad.BAJA
        )

    def test_prioridad_desde_texto(self):
        self.assertEqual(
            Prioridad.desde_texto("Alta"),
            Prioridad.ALTA
        )

        self.assertEqual(
            Prioridad.desde_texto("Media"),
            Prioridad.MEDIA
        )

        self.assertEqual(
            Prioridad.desde_texto("Baja"),
            Prioridad.BAJA
        )

    def test_prioridad_texto_invalido(self):
        with self.assertRaises(ValueError):
            Prioridad.desde_texto("Invalida")

    # =========================================================
    # MODELO USUARIO
    # =========================================================

    def test_usuario_modelo(self):
        usuario = Usuario(
            1,
            "Ana",
            "Usuario"
        )

        self.assertEqual(
            usuario.id,
            1
        )

        self.assertEqual(
            usuario.nombre,
            "Ana"
        )

        self.assertEqual(
            usuario.rol,
            "Usuario"
        )

    def test_usuario_administrador(self):
        usuario = Usuario(
            2,
            "Carlos",
            "Administrador"
        )

        self.assertEqual(
            usuario.rol,
            "Administrador"
        )

    def test_usuario_rol_invalido(self):
        with self.assertRaises(ValueError):
            Usuario(
                1,
                "Ana",
                "Invitado"
            )

    # =========================================================
    # MODELO TAREA
    # =========================================================

    def test_tarea_modelo(self):
        tarea = Tarea(
            1,
            "Programar",
            Prioridad.ALTA,
            5
        )

        self.assertEqual(
            tarea.id_tarea,
            1
        )

        self.assertEqual(
            tarea.descripcion,
            "Programar"
        )

        self.assertEqual(
            tarea.prioridad,
            Prioridad.ALTA
        )

        self.assertEqual(
            tarea.id_usuario,
            5
        )

    def test_tarea_incrementar_ciclo(self):
        tarea = self.crear_tarea(1)

        ciclo_inicial = tarea.ciclos_espera

        tarea.incrementar_ciclo_espera()

        self.assertEqual(
            tarea.ciclos_espera,
            ciclo_inicial + 1
        )

    # =========================================================
    # MODELO ACCION
    # =========================================================

    def test_accion(self):
        usuario = Usuario(
            1,
            "Ana",
            "Usuario"
        )

        accion = Accion(
            "AGREGAR",
            "Se agregó un usuario",
            usuario
        )

        self.assertEqual(
            accion.tipo,
            "AGREGAR"
        )

        self.assertEqual(
            accion.descripcion,
            "Se agregó un usuario"
        )

        self.assertEqual(
            accion.datos,
            usuario
        )

    # =========================================================
    # LISTA DOBLE
    # =========================================================

    def test_lista_doble_completa(self):
        lista = ListaDoble()

        usuario1 = Usuario(
            1,
            "Ana",
            "Usuario"
        )

        usuario2 = Usuario(
            2,
            "Carlos",
            "Administrador"
        )

        self.assertTrue(
            lista.insertar(usuario1)
        )

        self.assertTrue(
            lista.insertar(usuario2)
        )

        self.assertIsNotNone(
            lista.buscar(1)
        )

        self.assertIsNotNone(
            lista.buscar(2)
        )

        self.assertFalse(
            lista.insertar(usuario1)
        )

        self.assertTrue(
            lista.eliminar(1)
        )

        self.assertIsNone(
            lista.buscar(1)
        )

        self.assertFalse(
            lista.eliminar(999)
        )

    # =========================================================
    # PILA
    # =========================================================

    def test_pila_completa(self):
        pila = Pila()

        self.assertTrue(
            pila.esta_vacia()
        )

        self.assertIsNone(
            pila.peek()
        )

        pila.apilar("A")
        pila.apilar("B")
        pila.apilar("C")

        self.assertEqual(
            pila.peek(),
            "C"
        )

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

        self.assertTrue(
            pila.esta_vacia()
        )

    def test_pila_desapilar_vacia(self):
        pila = Pila()

        self.assertIsNone(
            pila.desapilar()
        )

        self.assertTrue(
            pila.esta_vacia()
        )

    # =========================================================
    # COLA FIFO
    # =========================================================

    def test_cola_fifo_completa(self):
        cola = ColaFIFO()

        tarea1 = self.crear_tarea(1)
        tarea2 = self.crear_tarea(2)

        cola.encolar(tarea1)
        cola.encolar(tarea2)

        self.assertEqual(
            len(cola),
            2
        )

        self.assertEqual(
            cola.ver_frente(),
            tarea1
        )

        self.assertEqual(
            cola.obtener_lista(),
            [tarea1, tarea2]
        )

        self.assertEqual(
            cola.desencolar(),
            tarea1
        )

        self.assertEqual(
            len(cola),
            1
        )

        self.assertEqual(
            cola.desencolar(),
            tarea2
        )

        self.assertTrue(
            cola.esta_vacia()
        )

    def test_cola_fifo_desencolar_vacia(self):
        cola = ColaFIFO()

        with self.assertRaises(IndexError):
            cola.desencolar()

    def test_cola_fifo_eliminar_frente(self):
        cola = ColaFIFO()

        cola.encolar(
            self.crear_tarea(1)
        )

        cola.encolar(
            self.crear_tarea(2)
        )

        self.assertTrue(
            cola.eliminar_por_id(1)
        )

        self.assertEqual(
            len(cola),
            1
        )

    def test_cola_fifo_eliminar_final(self):
        cola = ColaFIFO()

        cola.encolar(
            self.crear_tarea(1)
        )

        cola.encolar(
            self.crear_tarea(2)
        )

        self.assertTrue(
            cola.eliminar_por_id(2)
        )

        self.assertEqual(
            len(cola),
            1
        )

    def test_cola_fifo_incrementar_ciclos(self):
        cola = ColaFIFO()

        tarea = self.crear_tarea(1)

        cola.encolar(tarea)

        resultado = (
            cola.incrementar_ciclos_y_extraer_escaladas(
                1
            )
        )

        self.assertEqual(
            resultado,
            [tarea]
        )

        self.assertTrue(
            cola.esta_vacia()
        )

    # =========================================================
    # COLA PRIORIDAD
    # =========================================================

    def test_cola_prioridad_completa(self):
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

        lista = cola.obtener_lista()

        self.assertEqual(
            lista[0],
            alta
        )

        self.assertEqual(
            lista[1],
            media
        )

        self.assertEqual(
            lista[2],
            baja
        )

        self.assertEqual(
            cola.desencolar(),
            alta
        )

        self.assertEqual(
            len(cola),
            2
        )

    def test_cola_prioridad_eliminar_cabeza(self):
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

    def test_cola_prioridad_eliminar_intermedio(self):
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
                Prioridad.MEDIA
            )
        )

        cola.encolar(
            self.crear_tarea(
                3,
                Prioridad.BAJA
            )
        )

        self.assertTrue(
            cola.eliminar_por_id(2)
        )

        self.assertEqual(
            len(cola),
            2
        )

    # =========================================================
    # NODO ARBOL
    # =========================================================

    def test_nodo_arbol(self):
        raiz = NodoArbolTarea(
            1,
            "Principal",
            None
        )

        self.assertEqual(
            raiz.id_subtarea,
            1
        )

        self.assertEqual(
            raiz.descripcion,
            "Principal"
        )

        self.assertIsNone(
            raiz.id_padre
        )

    def test_nodo_arbol_completo(self):
        raiz = NodoArbolTarea(
            1,
            "Principal",
            None
        )

        self.assertTrue(
            raiz.agregar_subtarea(
                1,
                2,
                "Subtarea"
            )
        )

        self.assertIsNotNone(
            raiz.buscar_nodo(2)
        )

        self.assertIsNone(
            raiz.buscar_nodo(999)
        )

        elementos = raiz.obtener_todas()

        self.assertEqual(
            len(elementos),
            2
        )

    # =========================================================
    # ARBOL TAREAS
    # =========================================================

    def test_arbol_tareas(self):
        arbol = ArbolTareas(
            1,
            "Tarea principal"
        )

        self.assertTrue(
            arbol.agregar_subtarea(
                2,
                1,
                "Subtarea"
            )
        )

        self.assertIsNotNone(
            arbol.buscar_nodo(2)
        )

        self.assertEqual(
            len(arbol.obtener_todas()),
            2
        )

    # =========================================================
    # ORDENAMIENTO
    # =========================================================

    def crear_lista_tareas(self):
        return [
            self.crear_tarea(5),
            self.crear_tarea(2),
            self.crear_tarea(8),
            self.crear_tarea(1),
            self.crear_tarea(4)
        ]

    def obtener_ids(self, lista):
        return [
            tarea.id_tarea
            for tarea in lista
        ]

    def test_mergesort_completo(self):
        tareas = self.crear_lista_tareas()

        resultado = OrdenadorTareas.mergesort(
            tareas
        )

        self.assertEqual(
            self.obtener_ids(resultado),
            [1, 2, 4, 5, 8]
        )

        resultado = OrdenadorTareas.mergesort(
            tareas,
            reverso=True
        )

        self.assertEqual(
            self.obtener_ids(resultado),
            [8, 5, 4, 2, 1]
        )

    def test_bubblesort_completo(self):
        tareas = self.crear_lista_tareas()

        resultado = OrdenadorTareas.bubblesort(
            tareas
        )

        self.assertEqual(
            self.obtener_ids(resultado),
            [1, 2, 4, 5, 8]
        )

        resultado = OrdenadorTareas.bubblesort(
            tareas,
            reverso=True
        )

        self.assertEqual(
            self.obtener_ids(resultado),
            [8, 5, 4, 2, 1]
        )

    def test_quicksort_completo(self):
        tareas = self.crear_lista_tareas()

        resultado = OrdenadorTareas.quicksort(
            tareas
        )

        self.assertEqual(
            self.obtener_ids(resultado),
            [1, 2, 4, 5, 8]
        )

        resultado = OrdenadorTareas.quicksort(
            tareas,
            reverso=True
        )

        self.assertEqual(
            self.obtener_ids(resultado),
            [8, 5, 4, 2, 1]
        )

    def test_ordenamiento_con_clave(self):
        tareas = [
            self.crear_tarea(
                1,
                Prioridad.BAJA
            ),
            self.crear_tarea(
                2,
                Prioridad.ALTA
            ),
            self.crear_tarea(
                3,
                Prioridad.MEDIA
            )
        ]

        resultado = OrdenadorTareas.mergesort(
            tareas,
            clave=lambda x: x.prioridad.value
        )

        self.assertEqual(
            resultado[0].prioridad,
            Prioridad.BAJA
        )

    # =========================================================
    # USUARIO REPOSITORY
    # =========================================================

    def test_usuario_repository(self):
        archivo = self.crear_archivo()

        try:
            repository = UsuarioRepository(
                archivo
            )

            usuarios = ListaDoble()

            usuario1 = Usuario(
                1,
                "Ana",
                "Usuario"
            )

            usuario2 = Usuario(
                2,
                "Carlos",
                "Administrador"
            )

            self.assertTrue(
                usuarios.insertar(usuario1)
            )

            self.assertTrue(
                usuarios.insertar(usuario2)
            )

            repository.guardar_usuarios(
                usuarios
            )

            usuarios_cargados = ListaDoble()

            resultado = repository.cargar_usuarios(
                usuarios_cargados
            )

            self.assertIsNone(
                resultado
            )

            usuario_cargado1 = (
                usuarios_cargados.buscar(1)
            )

            usuario_cargado2 = (
                usuarios_cargados.buscar(2)
            )

            self.assertIsNotNone(
                usuario_cargado1
            )

            self.assertIsNotNone(
                usuario_cargado2
            )

            self.assertEqual(
                usuario_cargado1.nombre,
                "Ana"
            )

            self.assertEqual(
                usuario_cargado1.rol,
                "Usuario"
            )

            self.assertEqual(
                usuario_cargado2.nombre,
                "Carlos"
            )

            self.assertEqual(
                usuario_cargado2.rol,
                "Administrador"
            )

        finally:
            self.eliminar_archivo(archivo)

    # =========================================================
    # TAREA REPOSITORY
    # =========================================================

    def test_tarea_repository(self):
        archivo = self.crear_archivo()

        try:
            repository = TareaRepository(
                archivo
            )

            tarea = self.crear_tarea(
                1,
                Prioridad.ALTA
            )

            raiz = NodoArbolTarea(
                1,
                "Tarea 1",
                None
            )

            resultado = repository.guardar_tareas(
                [tarea],
                {1: raiz}
            )

            self.assertIsNone(
                resultado
            )

            tareas, arboles = (
                repository.cargar_tareas()
            )

            self.assertEqual(
                len(tareas),
                1
            )

            self.assertEqual(
                tareas[0].id_tarea,
                1
            )

            self.assertIn(
                1,
                arboles
            )

        finally:
            self.eliminar_archivo(archivo)

    # =========================================================
    # TAREA SERVICE
    # =========================================================

    def crear_tarea_service(self):
        archivo = self.crear_archivo()

        repository = TareaRepository(
            archivo
        )

        service = TareaService(
            repository
        )

        return service, archivo

    def test_tarea_service_completo(self):
        service, archivo = (
            self.crear_tarea_service()
        )

        try:
            self.assertTrue(
                service.agregar_tarea(
                    1,
                    "Tarea principal",
                    Prioridad.ALTA,
                    1
                )
            )

            self.assertIsNotNone(
                service.buscar_tarea(1)
            )

            self.assertTrue(
                service.modificar_tarea(
                    1,
                    nueva_descripcion="Modificada",
                    nueva_prioridad=Prioridad.MEDIA,
                    nuevo_id_usuario=2
                )
            )

            tarea = service.buscar_tarea(1)

            self.assertEqual(
                tarea.descripcion,
                "Modificada"
            )

            self.assertTrue(
                service.agregar_subtarea(
                    1,
                    2,
                    "Subtarea"
                )
            )

            self.assertTrue(
                service.completar_subtarea(2)
            )

            subtarea = service.buscar_subtarea(2)

            self.assertTrue(
                subtarea.completada
            )

            self.assertTrue(
                service.eliminar_subtarea(2)
            )

            self.assertIsNone(
                service.buscar_subtarea(2)
            )

            self.assertTrue(
                service.eliminar_tarea(1)
            )

            self.assertIsNone(
                service.buscar_tarea(1)
            )

        finally:
            self.eliminar_archivo(archivo)

    # =========================================================
    # HISTORIAL SERVICE
    # =========================================================

    def test_historial_usuario_agregar(self):
        archivo = self.crear_archivo()

        try:
            historial = HistorialService()

            usuarios = ListaDoble()

            repository = UsuarioRepository(
                archivo
            )

            usuario = Usuario(
                1,
                "Ana",
                "Usuario"
            )

            usuarios.insertar(
                usuario
            )

            accion = Accion(
                "AGREGAR_USUARIO",
                "Agregar usuario",
                usuario
            )

            historial.registrar_accion(
                accion
            )

            self.assertFalse(
                historial.pila_deshacer.esta_vacia()
            )

            self.assertEqual(
                historial.pila_deshacer.peek(),
                accion
            )

            self.assertTrue(
                historial.pila_rehacer.esta_vacia()
            )

        finally:
            self.eliminar_archivo(archivo)

    # =========================================================
    # SISTEMA SERVICE
    # =========================================================

    def test_sistema_service(self):
        usuarios = self.crear_archivo()
        tareas = self.crear_archivo()
        auditoria = self.crear_archivo()

        try:
            sistema = SistemaService(
                archivo_usuarios=usuarios,
                archivo_tareas=tareas,
                archivo_auditoria=auditoria
            )

            self.assertIsNotNone(
                sistema.historial
            )

            self.assertIsNotNone(
                sistema.usuarios
            )

            self.assertIsNotNone(
                sistema.tarea_service
            )

            self.assertIs(
                sistema.historial.usuario_service,
                sistema.usuarios
            )

            self.assertIs(
                sistema.historial.tarea_service,
                sistema.tarea_service
            )

        finally:
            self.eliminar_archivo(usuarios)
            self.eliminar_archivo(tareas)
            self.eliminar_archivo(auditoria)


if __name__ == "__main__":
    unittest.main()