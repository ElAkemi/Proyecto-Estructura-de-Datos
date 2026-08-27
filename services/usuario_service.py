"""Módulo para la gestión de usuarios."""

from copy import deepcopy

from models.usuario import Usuario
from models.accion import Accion
from structures.lista_doble import ListaDoble

from persistence.usuario_repository import UsuarioRepository


class UsuarioService:
    """
    Servicio encargado de gestionar los usuarios del sistema.

    Utiliza una única instancia compartida de HistorialService
    para las operaciones de deshacer y rehacer.
    """

    def __init__(
        self,
        archivo_csv="data/usuarios.csv",
        historial=None
    ):
        """Inicializa el servicio de usuarios."""

        self.lista_usuarios = ListaDoble()

        self.repository = UsuarioRepository(
            archivo_csv
        )

        self.historial = historial

        self.repository.cargar_usuarios(
            self.lista_usuarios
        )

    # =========================================================
    # CONFIGURACIÓN
    # =========================================================

    def establecer_historial(self, historial):
        """Establece la instancia compartida de HistorialService."""

        self.historial = historial

    # =========================================================
    # AGREGAR
    # =========================================================

    def agregar_usuario(
        self,
        id,
        nombre,
        rol,
        id_usuario_ejecutor=None
    ):
        """Agrega un usuario al sistema."""

        if not isinstance(id, int) or isinstance(id, bool):
            raise ValueError(
                "El ID debe ser un número entero."
            )

        if id <= 0:
            raise ValueError(
                "El ID debe ser mayor que cero."
            )

        if self.lista_usuarios.buscar(id) is not None:
            raise ValueError(
                f"Ya existe un usuario con el ID {id}."
            )

        if (
            not isinstance(nombre, str)
            or not nombre.strip()
        ):
            raise ValueError(
                "El nombre no puede estar vacío."
            )

        if rol not in (
            "Administrador",
            "Usuario"
        ):
            raise ValueError(
                "Rol inválido."
            )

        usuario = Usuario(
            id,
            nombre.strip(),
            rol
        )

        if not self.lista_usuarios.insertar(
            usuario
        ):
            raise ValueError(
                f"Ya existe un usuario con el ID {id}."
            )

        self.repository.guardar_usuarios(
            self.lista_usuarios
        )

        if self.historial is not None:

            accion = Accion(
                "AGREGAR_USUARIO",
                f"Se agregó el usuario: {id}",
                deepcopy(usuario),
                id_usuario_ejecutor
            )

            self.historial.registrar_accion(
                accion
            )

        return True

    # =========================================================
    # MODIFICAR
    # =========================================================

    def modificar_usuario(
        self,
        id,
        nuevo_nombre,
        nuevo_rol,
        id_usuario_ejecutor=None
    ):
        """Modifica un usuario existente."""

        if not isinstance(id, int) or isinstance(id, bool):
            raise ValueError(
                "El ID debe ser un número entero."
            )

        usuario = self.lista_usuarios.buscar(id)

        if usuario is None:
            raise ValueError(
                "El usuario no existe."
            )

        if (
            not isinstance(nuevo_nombre, str)
            or not nuevo_nombre.strip()
        ):
            raise ValueError(
                "El nombre no puede estar vacío."
            )

        if nuevo_rol not in (
            "Administrador",
            "Usuario"
        ):
            raise ValueError(
                "Rol inválido."
            )

        # Guardar estado anterior.
        usuario_anterior = deepcopy(
            usuario
        )

        if not self.lista_usuarios.modificar(
            id,
            nuevo_nombre.strip(),
            nuevo_rol
        ):
            raise ValueError(
                "No fue posible modificar el usuario."
            )

        # Guardar estado nuevo.
        usuario_nuevo = deepcopy(
            self.lista_usuarios.buscar(id)
        )

        self.repository.guardar_usuarios(
            self.lista_usuarios
        )

        if self.historial is not None:

            accion = Accion(
                "MODIFICAR_USUARIO",
                f"Se modificó el usuario: {id}",
                {
                    "anterior": usuario_anterior,
                    "nuevo": usuario_nuevo
                },
                id_usuario_ejecutor
            )

            self.historial.registrar_accion(
                accion
            )

        return True

    # =========================================================
    # ELIMINAR
    # =========================================================

    def eliminar_usuario(
        self,
        id,
        id_usuario_ejecutor=None
    ):
        """Elimina un usuario."""

        if not isinstance(id, int) or isinstance(id, bool):
            raise ValueError(
                "El ID debe ser un número entero."
            )

        usuario = self.lista_usuarios.buscar(id)

        if usuario is None:
            raise ValueError(
                "El usuario no existe."
            )

        usuario_eliminado = deepcopy(
            usuario
        )

        if not self.lista_usuarios.eliminar(id):
            return False

        self.repository.guardar_usuarios(
            self.lista_usuarios
        )

        if self.historial is not None:

            accion = Accion(
                "ELIMINAR_USUARIO",
                f"Se eliminó el usuario: {id}",
                usuario_eliminado,
                id_usuario_ejecutor
            )

            self.historial.registrar_accion(
                accion
            )

        return True

    # =========================================================
    # BUSCAR
    # =========================================================

    def buscar_usuario(self, id):
        """Busca un usuario por ID."""

        if not isinstance(id, int) or isinstance(id, bool):
            raise ValueError(
                "El ID debe ser un número entero."
            )

        usuario = self.lista_usuarios.buscar(id)

        if usuario is None:
            raise ValueError(
                "El usuario no existe."
            )

        return usuario

    # =========================================================
    # MOSTRAR
    # =========================================================

    def mostrar_usuarios(self):
        """Muestra todos los usuarios registrados."""

        self.lista_usuarios.mostrar()