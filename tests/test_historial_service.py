import unittest
import tempfile
import os

from services.tarea_service import TareaService
from services.usuario_service import UsuarioService
from services.historial_service import HistorialService

from persistence.tarea_repository import TareaRepository


class TestHistorialService(unittest.TestCase):
    """Pruebas unitarias para Deshacer y Rehacer."""

    def setUp(self):
        """
        Crea un entorno independiente para cada prueba.
        """

        self.archivo_tareas = tempfile.NamedTemporaryFile(
            delete=False
        ).name

        self.archivo_usuarios = tempfile.NamedTemporaryFile(
            delete=False
        ).name

        self.tarea_repository = TareaRepository(
            self.archivo_tareas
        )

        self.historial = HistorialService()

        self.tarea_service = TareaService(
            self.tarea_repository,
            self.historial
        )

        self.usuario_service = UsuarioService(
            self.archivo_usuarios,
            self.historial
        )

        self.historial.establecer_tarea_service(
            self.tarea_service
        )

        self.historial.establecer_usuario_service(
            self.usuario_service
        )

    def tearDown(self):
        """
        Elimina los archivos temporales después de cada prueba.
        """

        if os.path.exists(self.archivo_tareas):
            os.remove(self.archivo_tareas)

        if os.path.exists(self.archivo_usuarios):
            os.remove(self.archivo_usuarios)

    # =========================================================
    # TAREAS
    # =========================================================

    def test_agregar_tarea_deshacer_rehacer(self):
        """Prueba agregar, deshacer y rehacer una tarea."""

        resultado = self.tarea_service.agregar_tarea(
            1,
            "Tarea de prueba",
            "Alta",
            10
        )

        self.assertTrue(resultado)

        tarea = self.tarea_service.buscar_tarea(1)

        self.assertIsNotNone(tarea)
        self.assertEqual(
            tarea.descripcion,
            "Tarea de prueba"
        )

        # DESHACER

        accion = self.historial.deshacer_accion()

        self.assertIsNotNone(accion)

        tarea = self.tarea_service.buscar_tarea(1)

        self.assertIsNone(tarea)

        # REHACER

        accion = self.historial.rehacer_accion()

        self.assertIsNotNone(accion)

        tarea = self.tarea_service.buscar_tarea(1)

        self.assertIsNotNone(tarea)
        self.assertEqual(
            tarea.descripcion,
            "Tarea de prueba"
        )

    def test_modificar_tarea_deshacer_rehacer(self):
        """Prueba modificar, deshacer y rehacer una tarea."""

        self.tarea_service.agregar_tarea(
            1,
            "Descripción original",
            "Alta",
            10
        )

        # Limpiar la acción de agregar.
        self.historial.deshacer_accion()

        # Volver a agregar sin historial.
        self.historial.pila_deshacer = type(
            self.historial.pila_deshacer
        )()

        self.tarea_service.historial_service = None

        self.tarea_service.agregar_tarea(
            1,
            "Descripción original",
            "Alta",
            10
        )

        self.tarea_service.historial_service = self.historial

        resultado = self.tarea_service.modificar_tarea(
            1,
            nueva_descripcion="Descripción modificada",
            nueva_prioridad="Media",
            nuevo_id_usuario=20
        )

        self.assertTrue(resultado)

        tarea = self.tarea_service.buscar_tarea(1)

        self.assertEqual(
            tarea.descripcion,
            "Descripción modificada"
        )

        # DESHACER

        accion = self.historial.deshacer_accion()

        self.assertIsNotNone(accion)

        tarea = self.tarea_service.buscar_tarea(1)

        self.assertEqual(
            tarea.descripcion,
            "Descripción original"
        )

        # REHACER

        accion = self.historial.rehacer_accion()

        self.assertIsNotNone(accion)

        tarea = self.tarea_service.buscar_tarea(1)

        self.assertEqual(
            tarea.descripcion,
            "Descripción modificada"
        )

    def test_eliminar_tarea_deshacer_rehacer(self):
        """Prueba eliminar, deshacer y rehacer una tarea."""

        self.tarea_service.historial_service = None

        self.tarea_service.agregar_tarea(
            1,
            "Tarea para eliminar",
            "Alta",
            10
        )

        self.tarea_service.historial_service = self.historial

        resultado = self.tarea_service.eliminar_tarea(1)

        self.assertTrue(resultado)

        tarea = self.tarea_service.buscar_tarea(1)

        self.assertIsNone(tarea)

        # DESHACER

        accion = self.historial.deshacer_accion()

        self.assertIsNotNone(accion)

        tarea = self.tarea_service.buscar_tarea(1)

        self.assertIsNotNone(tarea)

        # REHACER

        accion = self.historial.rehacer_accion()

        self.assertIsNotNone(accion)

        tarea = self.tarea_service.buscar_tarea(1)

        self.assertIsNone(tarea)

    # =========================================================
    # SUBTAREAS
    # =========================================================

    def test_agregar_subtarea_deshacer_rehacer(self):
        """Prueba agregar, deshacer y rehacer una subtarea."""

        self.tarea_service.historial_service = None

        self.tarea_service.agregar_tarea(
            1,
            "Tarea principal",
            "Alta",
            10
        )

        self.tarea_service.historial_service = self.historial

        resultado = self.tarea_service.agregar_subtarea(
            1,
            2,
            "Subtarea de prueba"
        )

        self.assertTrue(resultado)

        subtarea = self.tarea_service.buscar_subtarea(2)

        self.assertIsNotNone(subtarea)

        # DESHACER

        accion = self.historial.deshacer_accion()

        self.assertIsNotNone(accion)

        subtarea = self.tarea_service.buscar_subtarea(2)

        self.assertIsNone(subtarea)

        # REHACER

        accion = self.historial.rehacer_accion()

        self.assertIsNotNone(accion)

        subtarea = self.tarea_service.buscar_subtarea(2)

        self.assertIsNotNone(subtarea)

    def test_eliminar_subtarea_deshacer_rehacer(self):
        """
        Prueba eliminar una subtarea y verificar
        que Deshacer y Rehacer funcionen.
        """

        self.tarea_service.historial_service = None

        self.tarea_service.agregar_tarea(
            1,
            "Tarea principal",
            "Alta",
            10
        )

        self.tarea_service.agregar_subtarea(
            1,
            2,
            "Subtarea para eliminar"
        )

        self.tarea_service.historial_service = self.historial

        resultado = self.tarea_service.eliminar_subtarea(2)

        self.assertTrue(resultado)

        subtarea = self.tarea_service.buscar_subtarea(2)

        self.assertIsNone(subtarea)

        # DESHACER

        accion = self.historial.deshacer_accion()

        self.assertIsNotNone(accion)

        subtarea = self.tarea_service.buscar_subtarea(2)

        self.assertIsNotNone(subtarea)

        self.assertEqual(
            subtarea.descripcion,
            "Subtarea para eliminar"
        )

        # REHACER

        accion = self.historial.rehacer_accion()

        self.assertIsNotNone(accion)

        subtarea = self.tarea_service.buscar_subtarea(2)

        self.assertIsNone(subtarea)

    # =========================================================
    # USUARIOS
    # =========================================================

    def test_agregar_usuario_deshacer_rehacer(self):
        """Prueba agregar, deshacer y rehacer un usuario."""

        resultado = self.usuario_service.agregar_usuario(
            1,
            "Juan",
            "Usuario"
        )

        self.assertTrue(resultado)

        usuario = self.usuario_service.lista_usuarios.buscar(1)

        self.assertIsNotNone(usuario)
        self.assertEqual(
            usuario.nombre,
            "Juan"
        )

        # DESHACER

        accion = self.historial.deshacer_accion()

        self.assertIsNotNone(accion)

        usuario = self.usuario_service.lista_usuarios.buscar(1)

        self.assertIsNone(usuario)

        # REHACER

        accion = self.historial.rehacer_accion()

        self.assertIsNotNone(accion)

        usuario = self.usuario_service.lista_usuarios.buscar(1)

        self.assertIsNotNone(usuario)
        self.assertEqual(
            usuario.nombre,
            "Juan"
        )

    def test_modificar_usuario_deshacer_rehacer(self):
        """Prueba modificar, deshacer y rehacer un usuario."""

        self.usuario_service.historial = None

        self.usuario_service.agregar_usuario(
            1,
            "Juan",
            "Usuario"
        )

        self.usuario_service.historial = self.historial

        resultado = self.usuario_service.modificar_usuario(
            1,
            "Juan Modificado",
            "Administrador"
        )

        self.assertTrue(resultado)

        usuario = self.usuario_service.lista_usuarios.buscar(1)

        self.assertEqual(
            usuario.nombre,
            "Juan Modificado"
        )

        self.assertEqual(
            usuario.rol,
            "Administrador"
        )

        # DESHACER

        accion = self.historial.deshacer_accion()

        self.assertIsNotNone(accion)

        usuario = self.usuario_service.lista_usuarios.buscar(1)

        self.assertEqual(
            usuario.nombre,
            "Juan"
        )

        self.assertEqual(
            usuario.rol,
            "Usuario"
        )

        # REHACER

        accion = self.historial.rehacer_accion()

        self.assertIsNotNone(accion)

        usuario = self.usuario_service.lista_usuarios.buscar(1)

        self.assertEqual(
            usuario.nombre,
            "Juan Modificado"
        )

        self.assertEqual(
            usuario.rol,
            "Administrador"
        )

    def test_eliminar_usuario_deshacer_rehacer(self):
        """Prueba eliminar, deshacer y rehacer un usuario."""

        self.usuario_service.historial = None

        self.usuario_service.agregar_usuario(
            1,
            "Juan",
            "Usuario"
        )

        self.usuario_service.historial = self.historial

        resultado = self.usuario_service.eliminar_usuario(1)

        self.assertTrue(resultado)

        usuario = self.usuario_service.lista_usuarios.buscar(1)

        self.assertIsNone(usuario)

        # DESHACER

        accion = self.historial.deshacer_accion()

        self.assertIsNotNone(accion)

        usuario = self.usuario_service.lista_usuarios.buscar(1)

        self.assertIsNotNone(usuario)

        self.assertEqual(
            usuario.nombre,
            "Juan"
        )

        # REHACER

        accion = self.historial.rehacer_accion()

        self.assertIsNotNone(accion)

        usuario = self.usuario_service.lista_usuarios.buscar(1)

        self.assertIsNone(usuario)


if __name__ == "__main__":
    unittest.main(verbosity=2)