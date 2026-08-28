from persistence.usuario_repository import UsuarioRepository
from persistence.tarea_repository import TareaRepository

from services.auditoria_service import AuditoriaService
from services.autenticacion_service import AutenticacionService
from services.historial_service import HistorialService
from services.usuario_service import UsuarioService
from services.tarea_service import TareaService


class SistemaService:
    """Servicio principal que coordina todos los módulos."""

    def __init__(
        self,
        ruta_usuarios="data/usuarios.csv",
        ruta_tareas="data/tareas.csv",
        ruta_auditoria="data/auditoria_log.csv"
    ):
        # Repositorios.
        self.usuario_repository = UsuarioRepository(
            ruta_usuarios
        )

        self.tarea_repository = TareaRepository(
            ruta_tareas
        )

        # Auditoría.
        self.auditoria = AuditoriaService(
            ruta_auditoria
        )

        # Historial.
        self.historial = HistorialService(
            self.auditoria
        )

        # Usuarios.
        self.usuario_service = UsuarioService(
            self.usuario_repository,
            self.historial
        )

        # Tareas.
        self.tarea_service = TareaService(
            self.tarea_repository,
            self.historial,
            self.auditoria,
            self.usuario_service
        )

        # Conectar historial con ambos servicios.
        self.historial.configurar(
            self.usuario_service,
            self.tarea_service
        )

        # Autenticación.
        self.autenticacion = AutenticacionService(
            self.usuario_service
        )

        self._crear_administrador_inicial()

    def _crear_administrador_inicial(self):
        """
        Crea un administrador inicial si el sistema
        todavía no tiene usuarios.

        Credenciales iniciales:
            ID: 1
            Contraseña: admin123
        """

        if self.usuario_service.lista_usuarios.esta_vacia():

            self.usuario_service.agregar_usuario(
                id_usuario=1,
                nombre="Administrador",
                rol="Administrador",
                password="admin123",
                registrar_historial=False
            )

    def iniciar_sesion(
        self,
        id_usuario,
        password
    ):
        """Autentica un usuario."""

        if not isinstance(id_usuario, int):
            raise ValueError(
                "El ID debe ser un número entero."
            )

        return self.autenticacion.autenticar(
            id_usuario,
            password
        )

    def puede_administrar(self, usuario):
        """Comprueba permisos administrativos."""

        return self.autenticacion.es_administrador(
            usuario
        )

    def puede_cambiar_estado(
        self,
        usuario,
        id_tarea
    ):
        """Comprueba si un usuario puede cambiar una tarea."""

        tarea = self.tarea_service.buscar_tarea(
            id_tarea
        )

        if tarea is None:
            return False

        return self.tarea_service.puede_modificar_estado(
            tarea,
            usuario.id
        )

    def cambiar_estado(
        self,
        usuario,
        id_tarea,
        nuevo_estado
    ):
        """
        Cambia el estado verificando previamente
        los permisos.
        """

        if not self.puede_cambiar_estado(
            usuario,
            id_tarea
        ):
            raise PermissionError(
                "No tiene permisos para modificar "
                "esta tarea."
            )

        return self.tarea_service.cambiar_estado(
            id_tarea,
            nuevo_estado,
            usuario.id
        )

    def deshacer(self, usuario):
        """Ejecuta Undo."""

        return self.historial.deshacer_accion(
            usuario.id
        )

    def rehacer(self, usuario):
        """Ejecuta Redo."""

        return self.historial.rehacer_accion(
            usuario.id
        )