import unittest
import tempfile
import os

from services.tarea_service import TareaService
from persistence.tarea_repository import TareaRepository
from models.prioridad import Prioridad


class TestTareaService(unittest.TestCase):

    def setUp(self):
        archivo_temporal = tempfile.NamedTemporaryFile(
            delete=False,
            suffix=".csv"
        )

        archivo_temporal.close()

        self.archivo_csv = archivo_temporal.name

        self.repository = TareaRepository(
            self.archivo_csv
        )

        self.service = TareaService(
            self.repository
        )

    def tearDown(self):
        if os.path.exists(self.archivo_csv):
            os.remove(self.archivo_csv)

    def test_agregar_tarea(self):
        resultado = self.service.agregar_tarea(
            1,
            "Desarrollar sistema",
            Prioridad.ALTA,
            1
        )

        self.assertTrue(resultado)

        tarea = self.service.buscar_tarea(1)

        self.assertIsNotNone(tarea)
        self.assertEqual(tarea.id_tarea, 1)
        self.assertEqual(tarea.descripcion, "Desarrollar sistema")
        self.assertEqual(tarea.id_usuario, 1)

    def test_no_permitir_id_repetido(self):
        self.service.agregar_tarea(
            1,
            "Tarea original",
            Prioridad.MEDIA,
            1
        )

        resultado = self.service.agregar_tarea(
            1,
            "Tarea repetida",
            Prioridad.ALTA,
            1
        )

        self.assertFalse(resultado)

    def test_no_permitir_descripcion_vacia(self):
        resultado = self.service.agregar_tarea(
            1,
            "",
            Prioridad.ALTA,
            1
        )

        self.assertFalse(resultado)

    def test_no_permitir_id_usuario_invalido(self):
        resultado = self.service.agregar_tarea(
            1,
            "Tarea",
            Prioridad.ALTA,
            0
        )

        self.assertFalse(resultado)

    def test_no_permitir_id_tarea_invalido(self):
        resultado = self.service.agregar_tarea(
            0,
            "Tarea",
            Prioridad.ALTA,
            1
        )

        self.assertFalse(resultado)

    def test_buscar_tarea(self):
        self.service.agregar_tarea(
            1,
            "Tarea",
            Prioridad.MEDIA,
            1
        )

        tarea = self.service.buscar_tarea(1)

        self.assertIsNotNone(tarea)
        self.assertEqual(tarea.descripcion, "Tarea")

    def test_buscar_tarea_inexistente(self):
        tarea = self.service.buscar_tarea(999)

        self.assertIsNone(tarea)

    def test_modificar_tarea(self):
        self.service.agregar_tarea(
            1,
            "Tarea original",
            Prioridad.BAJA,
            1
        )

        resultado = self.service.modificar_tarea(
            1,
            nueva_descripcion="Tarea modificada",
            nueva_prioridad=Prioridad.ALTA,
            nuevo_id_usuario=2
        )

        self.assertTrue(resultado)

        tarea = self.service.buscar_tarea(1)

        self.assertEqual(
            tarea.descripcion,
            "Tarea modificada"
        )

        self.assertEqual(
            tarea.prioridad,
            Prioridad.ALTA
        )

        self.assertEqual(
            tarea.id_usuario,
            2
        )

    def test_modificar_tarea_inexistente(self):
        resultado = self.service.modificar_tarea(
            999,
            nueva_descripcion="Nueva"
        )

        self.assertFalse(resultado)

    def test_no_permitir_descripcion_vacia_al_modificar(self):
        self.service.agregar_tarea(
            1,
            "Tarea original",
            Prioridad.MEDIA,
            1
        )

        resultado = self.service.modificar_tarea(
            1,
            nueva_descripcion=""
        )

        self.assertFalse(resultado)

        tarea = self.service.buscar_tarea(1)

        self.assertEqual(
            tarea.descripcion,
            "Tarea original"
        )

    def test_eliminar_tarea(self):
        self.service.agregar_tarea(
            1,
            "Tarea",
            Prioridad.ALTA,
            1
        )

        resultado = self.service.eliminar_tarea(1)

        self.assertTrue(resultado)

        self.assertIsNone(
            self.service.buscar_tarea(1)
        )

    def test_eliminar_tarea_inexistente(self):
        resultado = self.service.eliminar_tarea(999)

        self.assertFalse(resultado)

    def test_agregar_subtarea(self):
        self.service.agregar_tarea(
            1,
            "Tarea principal",
            Prioridad.ALTA,
            1
        )

        resultado = self.service.agregar_subtarea(
            1,
            2,
            "Subtarea"
        )

        self.assertTrue(resultado)

        subtarea = self.service.buscar_subtarea(2)

        self.assertIsNotNone(subtarea)

        self.assertEqual(
            subtarea.id_subtarea,
            2
        )

        self.assertEqual(
            subtarea.descripcion,
            "Subtarea"
        )

    def test_agregar_subtarea_anidada(self):
        self.service.agregar_tarea(
            1,
            "Tarea principal",
            Prioridad.ALTA,
            1
        )

        self.service.agregar_subtarea(
            1,
            2,
            "Subtarea 1"
        )

        resultado = self.service.agregar_subtarea(
            2,
            3,
            "Subtarea 2"
        )

        self.assertTrue(resultado)

        subtarea = self.service.buscar_subtarea(3)

        self.assertIsNotNone(subtarea)

        self.assertEqual(
            subtarea.id_padre,
            2
        )

    def test_no_permitir_id_subtarea_repetido(self):
        self.service.agregar_tarea(
            1,
            "Tarea",
            Prioridad.ALTA,
            1
        )

        self.service.agregar_subtarea(
            1,
            2,
            "Subtarea"
        )

        resultado = self.service.agregar_subtarea(
            1,
            2,
            "Otra subtarea"
        )

        self.assertFalse(resultado)

    def test_no_permitir_subtarea_sin_padre(self):
        self.service.agregar_tarea(
            1,
            "Tarea",
            Prioridad.ALTA,
            1
        )

        resultado = self.service.agregar_subtarea(
            999,
            2,
            "Subtarea"
        )

        self.assertFalse(resultado)

    def test_buscar_subtarea(self):
        self.service.agregar_tarea(
            1,
            "Tarea",
            Prioridad.ALTA,
            1
        )

        self.service.agregar_subtarea(
            1,
            2,
            "Subtarea"
        )

        resultado = self.service.buscar_subtarea(2)

        self.assertIsNotNone(resultado)

    def test_buscar_subtarea_inexistente(self):
        resultado = self.service.buscar_subtarea(999)

        self.assertIsNone(resultado)

    def test_eliminar_subtarea(self):
        self.service.agregar_tarea(
            1,
            "Tarea",
            Prioridad.ALTA,
            1
        )

        self.service.agregar_subtarea(
            1,
            2,
            "Subtarea"
        )

        resultado = self.service.eliminar_subtarea(2)

        self.assertTrue(resultado)

        self.assertIsNone(
            self.service.buscar_subtarea(2)
        )

    def test_eliminar_subtarea_inexistente(self):
        resultado = self.service.eliminar_subtarea(999)

        self.assertFalse(resultado)

    def test_listar_subtareas(self):
        self.service.agregar_tarea(
            1,
            "Tarea principal",
            Prioridad.ALTA,
            1
        )

        self.service.agregar_subtarea(
            1,
            2,
            "Subtarea 1"
        )

        self.service.agregar_subtarea(
            1,
            3,
            "Subtarea 2"
        )

        resultado = self.service.listar_subtareas(1)

        self.assertEqual(
            len(resultado),
            3
        )

    def test_completar_subtarea(self):
        self.service.agregar_tarea(
            1,
            "Tarea",
            Prioridad.ALTA,
            1
        )

        self.service.agregar_subtarea(
            1,
            2,
            "Subtarea"
        )

        resultado = self.service.completar_subtarea(2)

        self.assertTrue(resultado)

        subtarea = self.service.buscar_subtarea(2)

        self.assertTrue(
            subtarea.completada
        )


if __name__ == "__main__":
    unittest.main()