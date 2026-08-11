import unittest
import tempfile
import os

from services.usuario_service import UsuarioService


class TestUsuarioService(unittest.TestCase):

    def setUp(self):
        # Crear un archivo temporal para cada prueba
        archivo_temporal = tempfile.NamedTemporaryFile(
            delete=False,
            suffix=".csv"
        )

        archivo_temporal.close()

        self.archivo_csv = archivo_temporal.name

        # Crear el servicio utilizando el CSV temporal
        self.service = UsuarioService(self.archivo_csv)

    def tearDown(self):
        # Eliminar el archivo temporal después de cada prueba
        if os.path.exists(self.archivo_csv):
            os.remove(self.archivo_csv)

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

        self.assertEqual(usuario.nombre, "Ana Maria")
        self.assertEqual(usuario.rol, "Administrador")

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

    def test_deshacer_agregar(self):
        self.service.agregar_usuario(
            1,
            "Ana",
            "Usuario"
        )

        self.service.historial.deshacer_accion()

        with self.assertRaises(ValueError):
            self.service.buscar_usuario(1)

    def test_rehacer_agregar(self):
        self.service.agregar_usuario(
            1,
            "Ana",
            "Usuario"
        )

        self.service.historial.deshacer_accion()
        self.service.historial.rehacer_accion()

        usuario = self.service.buscar_usuario(1)

        self.assertEqual(usuario.nombre, "Ana")
        self.assertEqual(usuario.rol, "Usuario")

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

        self.service.historial.deshacer_accion()

        usuario = self.service.buscar_usuario(1)

        self.assertEqual(usuario.nombre, "Ana")
        self.assertEqual(usuario.rol, "Usuario")

    def test_deshacer_eliminar(self):
        self.service.agregar_usuario(
            1,
            "Ana",
            "Usuario"
        )

        self.service.eliminar_usuario(1)

        self.service.historial.deshacer_accion()

        usuario = self.service.buscar_usuario(1)

        self.assertEqual(usuario.nombre, "Ana")
        self.assertEqual(usuario.rol, "Usuario")

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
        nuevo_service = UsuarioService(self.archivo_csv)

        usuario1 = nuevo_service.buscar_usuario(1)
        usuario2 = nuevo_service.buscar_usuario(2)

        self.assertEqual(usuario1.nombre, "Ana")
        self.assertEqual(usuario1.rol, "Usuario")

        self.assertEqual(usuario2.nombre, "Carlos")
        self.assertEqual(usuario2.rol, "Administrador")


if __name__ == "__main__":
    unittest.main()