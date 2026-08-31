import pytest

from models.tarea import Tarea
from services.tarea_service import TareaService
from services.usuario_service import UsuarioService
from structures.lista_doble import ListaDoble
from structures.arbol_tareas import ArbolTareas


class HistorialMock:
    """Historial simulado para las pruebas."""

    def __init__(self):
        self.acciones = []

    def registrar_accion(self, accion):
        self.acciones.append(accion)


class UsuarioRepositoryMock:
    """Repositorio de usuarios en memoria."""

    def __init__(self):
        self.usuarios = []

    def cargar(self):
        return list(self.usuarios)

    def guardar(self, usuarios):
        self.usuarios = list(usuarios)


class TareaRepositoryMock:
    """Repositorio de tareas en memoria."""

    def __init__(self):
        self.tareas = []

    def cargar(self):
        return list(self.tareas)

    def guardar(self, tareas):
        self.tareas = list(tareas)


@pytest.fixture
def servicio():
    historial = HistorialMock()

    usuario_repository = UsuarioRepositoryMock()
    usuario_service = UsuarioService(
        usuario_repository,
        historial
    )

    usuario_service.agregar_usuario(
        10,
        "Ana Rojas",
        "Usuario",
        "1234"
    )

    tarea_repository = TareaRepositoryMock()
    arbol = ArbolTareas()

    return TareaService(
        tarea_repository,
        historial,
        None,
        usuario_service
    )


def test_agregar_tarea(servicio):
    tarea = servicio.agregar_tarea(
        1,
        "ALTA",
        10,
        "Respaldar Base de Datos",
        None
    )

    assert tarea.id == 1
    assert tarea.descripcion == "Respaldar Base de Datos"
    assert tarea.responsable_id == 10


def test_no_permite_tarea_duplicada(servicio):
    servicio.agregar_tarea(
        1,
        "ALTA",
        10,
        "Respaldar Base de Datos",
        None
    )

    with pytest.raises(ValueError):
        servicio.agregar_tarea(
            1,
            "BAJA",
            10,
            "Otra tarea",
            None
        )


def test_buscar_tarea(servicio):
    servicio.agregar_tarea(
        1,
        "ALTA",
        10,
        "Respaldar Base de Datos",
        None
    )

    tarea = servicio.buscar_tarea(1)

    assert tarea is not None
    assert tarea.descripcion == "Respaldar Base de Datos"


def test_modificar_tarea(servicio):
    servicio.agregar_tarea(
        1,
        "ALTA",
        10,
        "Respaldar Base de Datos",
        None
    )

    servicio.modificar_tarea(
        1,
        "Respaldar servidores",
        "URGENTE",
        10
    )

    tarea = servicio.buscar_tarea(1)

    assert tarea.descripcion == "Respaldar servidores"
    assert tarea.responsable_id == 10


def test_eliminar_tarea(servicio):
    servicio.agregar_tarea(
        1,
        "ALTA",
        10,
        "Respaldar Base de Datos",
        None
    )

    servicio.eliminar_tarea(1)

    assert servicio.buscar_tarea(1) is None


def test_cambiar_estado(servicio):
    servicio.agregar_tarea(
        1,
        "ALTA",
        10,
        "Respaldar Base de Datos",
        None
    )

    servicio.cambiar_estado(
        1,
        "Completada",
        10
    )

    tarea = servicio.buscar_tarea(1)

    assert tarea.estado == "Completada"


def test_usuario_no_puede_modificar_tarea_ajena(servicio):
    servicio.agregar_tarea(
        1,
        "ALTA",
        10,
        "Respaldar Base de Datos",
        None
    )

    tarea = servicio.buscar_tarea(1)

    assert (
        servicio.puede_modificar_estado(
            tarea,
            99
        )
        is False
    )


def test_usuario_puede_modificar_su_tarea(servicio):
    servicio.agregar_tarea(
        1,
        "ALTA",
        10,
        "Respaldar Base de Datos",
        None
    )

    tarea = servicio.buscar_tarea(1)

    assert (
        servicio.puede_modificar_estado(
            tarea,
            10
        )
        is True
    )


def test_agregar_subtarea(servicio):
    servicio.agregar_tarea(
        1,
        "ALTA",
        10,
        "Respaldar Base de Datos",
        None
    )

    subtarea = servicio.agregar_tarea(
        2,
        "MEDIA",
        10,
        "Comprimir archivos",
        1
    )

    assert subtarea.padre_id == 1


def test_listar_tareas(servicio):
    servicio.agregar_tarea(
        1,
        "ALTA",
        10,
        "Tarea 1",
        None
    )

    servicio.agregar_tarea(
        2,
        "BAJA",
        10,
        "Tarea 2",
        None
    )

    tareas = servicio.listar_tareas()

    assert len(tareas) == 2


def test_ordenamiento_por_id(servicio):
    servicio.agregar_tarea(
        3,
        "BAJA",
        10,
        "Tarea 3",
        None
    )

    servicio.agregar_tarea(
        1,
        "ALTA",
        10,
        "Tarea 1",
        None
    )

    servicio.agregar_tarea(
        2,
        "MEDIA",
        10,
        "Tarea 2",
        None
    )

    tareas = servicio.ordenar_por_id("burbuja")

    ids = [tarea.id for tarea in tareas]

    assert ids == [1, 2, 3]