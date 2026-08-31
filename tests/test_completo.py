"""
Prueba de integración del Workflow Manager.

Comprueba un flujo completo:
1. Crear usuarios.
2. Crear tareas.
3. Asignar responsables.
4. Crear subtareas.
5. Cambiar estados.
6. Consultar información.
7. Ordenar tareas.
"""

from services.usuario_service import UsuarioService
from services.tarea_service import TareaService


class HistorialMock:

    def __init__(self):
        self.acciones = []

    def registrar_accion(self, accion):
        self.acciones.append(accion)


class UsuarioRepositoryMock:

    def __init__(self):
        self.usuarios = []

    def cargar(self):
        return list(self.usuarios)

    def guardar(self, usuarios):
        self.usuarios = list(usuarios)


class TareaRepositoryMock:

    def __init__(self):
        self.tareas = []

    def cargar(self):
        return list(self.tareas)

    def guardar(self, tareas):
        self.tareas = list(tareas)


def test_flujo_completo():

    historial = HistorialMock()

    # --------------------------------------------------------
    # USUARIOS
    # --------------------------------------------------------

    usuario_repository = UsuarioRepositoryMock()

    usuario_service = UsuarioService(
        usuario_repository,
        historial
    )

    administrador = usuario_service.agregar_usuario(
        1,
        "Administrador",
        "Administrador",
        "admin123"
    )

    usuario = usuario_service.agregar_usuario(
        2,
        "Ana Rojas",
        "Usuario",
        "1234"
    )

    assert administrador.id == 1
    assert usuario.id == 2

    # --------------------------------------------------------
    # TAREAS
    # --------------------------------------------------------

    tarea_repository = TareaRepositoryMock()

    tarea_service = TareaService(
        tarea_repository,
        historial,
        None,
        usuario_service
    )

    # --------------------------------------------------------
    # TAREA PRINCIPAL
    # --------------------------------------------------------

    tarea = tarea_service.agregar_tarea(
        100,
        "URGENTE",
        2,
        "Respaldar Base de Datos",
        None
    )

    assert tarea.id == 100

    # --------------------------------------------------------
    # SUBTAREA
    # --------------------------------------------------------

    subtarea = tarea_service.agregar_tarea(
        101,
        "ALTA",
        2,
        "Comprimir archivos",
        100
    )

    assert subtarea.padre_id == 100

    # --------------------------------------------------------
    # CAMBIO DE ESTADO
    # --------------------------------------------------------

    assert tarea_service.puede_modificar_estado(
        tarea,
        2
    )

    tarea_service.cambiar_estado(
        100,
        "Completada",
        2
    )

    tarea_actualizada = tarea_service.buscar_tarea(
        100
    )

    assert tarea_actualizada.estado == "Completada"

    # --------------------------------------------------------
    # ORDENAMIENTO
    # --------------------------------------------------------

    tareas = tarea_service.ordenar_por_id(
        "burbuja"
    )

    ids = [
        tarea.id
        for tarea in tareas
    ]

    assert ids == sorted(ids)

    # --------------------------------------------------------
    # HISTORIAL
    # --------------------------------------------------------

    assert len(historial.acciones) > 0