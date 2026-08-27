"""Módulo principal de configuración de los servicios del sistema."""

from services.historial_service import HistorialService
from services.usuario_service import UsuarioService
from services.tarea_service import TareaService

from persistence.usuario_repository import UsuarioRepository
from persistence.tarea_repository import TareaRepository


class SistemaService:
    """Coordina los servicios principales del sistema."""

    def __init__(
        self,
        archivo_usuarios="data/usuarios.csv",
        archivo_tareas="data/tareas.csv",
        archivo_auditoria="data/auditoria_log.csv"
    ):
        """Inicializa los servicios principales del sistema."""

        usuario_repository = UsuarioRepository(
            archivo_usuarios
        )

        tarea_repository = TareaRepository(
            archivo_tareas
        )

        self.historial = HistorialService(
            archivo_auditoria=archivo_auditoria
        )

        self.usuarios = UsuarioService(
            archivo_csv=archivo_usuarios,
            historial=self.historial
        )

        self.tarea_service = TareaService(
            tarea_repository=tarea_repository,
            historial_service=self.historial
        )

        self.historial.establecer_usuario_service(
            self.usuarios
        )

        self.historial.establecer_tarea_service(
            self.tarea_service
        )