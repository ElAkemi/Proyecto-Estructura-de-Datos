import unittest
import tempfile
import os

from services.usuario_service import UsuarioService
from services.historial_service import HistorialService


class TestUsuarioService(unittest.TestCase):

    def setUp(self):
        # Crear un archivo temporal para cada prueba
        archivo_temporal = tempfile.NamedTemporaryFile(
            delete=False,
            suffix=".csv"
        )

        archivo_temporal.close()

        self.archivo_csv = archivo_temporal.name

        # Crear el historial compartido
        self.historial = HistorialService()

        # Crear el servicio de usuarios
        self.service = UsuarioService(
            self.archivo_csv,
            historial=self.historial
        )

        # Conectar el historial con el servicio de usuarios
        self.historial.establecer_usuario_service(
            self.service
        )

    def tearDown(self):
        # Eliminar el archivo temporal después de cada prueba
        if os.path.exists(self.archivo_csv):
            os.remove(self.archivo_csv)

    # =========================================================
    # AGREGAR
    # =========================================================

    def test_agregar_usuario(self):
        resultado = self.service.agregar_usuario(
            1,
            "Ana",
            "Usuario"
        )

        self.assertTrue(resultado)

        usuario = self.service.buscar_usuario(1)

        self.assertEqual(usuario.id, 1)
        self.assertEqual(usuario.nombre, "Ana")
        self.assertEqual(usuario.rol, "Usuario")

    # =========================================================
    # VALIDACIONES
    # =========================================================

    def test_no_permitir_id_repetido(self):
        self.service.agregar_usuario(
            1,
            "Ana",
            "Usuario"
        )

        with self.assertRaises(ValueError):
            self.service.agregar_usuario(
                1,
                "Carlos",
                "Usuario"
            )

    def test_no_permitir_nombre_vacio(self):
        with self.assertRaises(ValueError):
            self.service.agregar_usuario(
                1,
                "",
                "Usuario"
            )

    def test_no_permitir_rol_invalido(self):
        with self.assertRaises(ValueError):
            self.service.agregar_usuario(
                1,
                "Ana",
                "Invitado"
            )

    # =========================================================
    # MODIFICAR
    # =========================================================

    def test_modificar_usuario(self):
        self.service.agregar_usuario(
            1,
            "Ana",
            "Usuario"
        )

        resultado = self.service.modificar_usuario(
            1,
            "Ana Maria",
            "Administrador"
        )

        self.assertTrue(resultado)

        usuario = self.service.buscar_usuario(1)

        self.assertEqual(
            usuario.nombre,
            "Ana Maria"
        )

        self.assertEqual(
            usuario.rol,
            "Administrador"
        )

    # =========================================================
    # ELIMINAR
    # =========================================================

    def test_eliminar_usuario(self):
        self.service.agregar_usuario(
            1,
            "Ana",
            "Usuario"
        )

        resultado = self.service.eliminar_usuario(1)

        self.assertTrue(resultado)

        with self.assertRaises(ValueError):
            self.service.buscar_usuario(1)

    # =========================================================
    # DESHACER AGREGAR
    # =========================================================

    def test_deshacer_agregar(self):
        self.service.agregar_usuario(
            1,
            "Ana",
            "Usuario"
        )

        resultado = self.service.historial.deshacer_accion()

        self.assertIsNotNone(resultado)

        with self.assertRaises(ValueError):
            self.service.buscar_usuario(1)

    # =========================================================
    # REHACER AGREGAR
    # =========================================================

    def test_rehacer_agregar(self):
        self.service.agregar_usuario(
            1,
            "Ana",
            "Usuario"
        )

        resultado_deshacer = (
            self.service.historial.deshacer_accion()
        )

        self.assertIsNotNone(
            resultado_deshacer
        )

        resultado_rehacer = (
            self.service.historial.rehacer_accion()
        )

        self.assertIsNotNone(
            resultado_rehacer
        )

        usuario = self.service.buscar_usuario(1)

        self.assertEqual(
            usuario.nombre,
            "Ana"
        )

        self.assertEqual(
            usuario.rol,
            "Usuario"
        )

    # =========================================================
    # DESHACER MODIFICAR
    # =========================================================

    def test_deshacer_modificar(self):
        self.service.agregar_usuario(
            1,
            "Ana",
            "Usuario"
        )

        self.service.modificar_usuario(
            1,
            "Ana Maria",
            "Administrador"
        )

        resultado = (
            self.service.historial.deshacer_accion()
        )

        self.assertIsNotNone(
            resultado
        )

        usuario = self.service.buscar_usuario(1)

        self.assertEqual(
            usuario.nombre,
            "Ana"
        )

        self.assertEqual(
            usuario.rol,
            "Usuario"
        )

    # =========================================================
    # DESHACER ELIMINAR
    # =========================================================

    def test_deshacer_eliminar(self):
        self.service.agregar_usuario(
            1,
            "Ana",
            "Usuario"
        )

        self.service.eliminar_usuario(1)

        resultado = (
            self.service.historial.deshacer_accion()
        )

        self.assertIsNotNone(
            resultado
        )

        usuario = self.service.buscar_usuario(1)

        self.assertEqual(
            usuario.nombre,
            "Ana"
        )

        self.assertEqual(
            usuario.rol,
            "Usuario"
        )

    # =========================================================
    # GUARDAR Y CARGAR
    # =========================================================

    def test_guardar_y_cargar_usuarios(self):
        self.service.agregar_usuario(
            1,
            "Ana",
            "Usuario"
        )

        self.service.agregar_usuario(
            2,
            "Carlos",
            "Administrador"
        )

        # Crear otro servicio usando el mismo CSV
        nuevo_service = UsuarioService(
            self.archivo_csv
        )

        usuario1 = nuevo_service.buscar_usuario(1)
        usuario2 = nuevo_service.buscar_usuario(2)

        self.assertEqual(
            usuario1.nombre,
            "Ana"
        )

        self.assertEqual(
            usuario1.rol,
            "Usuario"
        )

        self.assertEqual(
            usuario2.nombre,
            "Carlos"
        )

        self.assertEqual(
            usuario2.rol,
            "Administrador"
        )


if __name__ == "__main__":
    unittest.main()