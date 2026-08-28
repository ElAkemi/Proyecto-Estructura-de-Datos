from models.usuario import Usuario
from models.accion import Accion
from structures.lista_doble import ListaDoble


class UsuarioService:
    """Gestiona los usuarios del sistema."""

    def __init__(
        self,
        usuario_repository,
        historial_service=None
    ):
        self.usuario_repository = usuario_repository
        self.lista_usuarios = ListaDoble()
        self.historial = historial_service

        self._cargar_usuarios()

    def _cargar_usuarios(self):
        """Carga los usuarios persistidos en la lista doble."""

        usuarios = self.usuario_repository.cargar()

        for usuario in usuarios:
            self.lista_usuarios.insertar(usuario)

    def agregar_usuario(
        self,
        id_usuario,
        nombre,
        rol,
        password,
        registrar_historial=True
    ):
        """Agrega un nuevo usuario."""

        if not isinstance(id_usuario, int):
            raise ValueError("El ID debe ser un número entero.")

        if id_usuario <= 0:
            raise ValueError(
                "El ID debe ser un número positivo."
            )

        if self.buscar_usuario(id_usuario) is not None:
            raise ValueError(
                "Ya existe un usuario con ese ID."
            )

        if not isinstance(nombre, str) or not nombre.strip():
            raise ValueError(
                "El nombre no puede estar vacío."
            )

        if rol not in Usuario.ROLES_VALIDOS:
            raise ValueError(
                "El rol debe ser Administrador o Usuario."
            )

        if not isinstance(password, str) or not password:
            raise ValueError(
                "La contraseña no puede estar vacía."
            )

        usuario = Usuario(
            id_usuario,
            nombre,
            rol,
            password
        )

        if not self.lista_usuarios.insertar(usuario):
            raise ValueError(
                "No fue posible agregar el usuario."
            )

        self._guardar()

        if registrar_historial and self.historial is not None:
            accion = Accion(
                Accion.AGREGAR,
                f"Se agregó el usuario {id_usuario}",
                usuario.copiar()
            )

            self.historial.registrar_accion(accion)

        return usuario

    def buscar_usuario(self, id_usuario):
        """Busca un usuario por ID."""

        return self.lista_usuarios.buscar(id_usuario)

    def listar_usuarios(self):
        """Devuelve todos los usuarios."""

        return self.lista_usuarios.listar()

    def modificar_usuario(
        self,
        id_usuario,
        nombre,
        rol,
        password=None,
        registrar_historial=True
    ):
        """Modifica un usuario existente."""

        usuario = self.buscar_usuario(id_usuario)

        if usuario is None:
            raise ValueError(
                "No existe un usuario con ese ID."
            )

        if not isinstance(nombre, str) or not nombre.strip():
            raise ValueError(
                "El nombre no puede estar vacío."
            )

        if rol not in Usuario.ROLES_VALIDOS:
            raise ValueError(
                "El rol debe ser Administrador o Usuario."
            )

        usuario_anterior = usuario.copiar()

        if password is None:
            password = usuario.password

        if not isinstance(password, str) or not password:
            raise ValueError(
                "La contraseña no puede estar vacía."
            )

        usuario_nuevo = Usuario(
            id_usuario,
            nombre,
            rol,
            password
        )

        self.lista_usuarios.modificar(usuario_nuevo)

        self._guardar()

        if registrar_historial and self.historial is not None:
            accion = Accion(
                Accion.MODIFICAR,
                f"Se modificó el usuario {id_usuario}",
                {
                    "anterior": usuario_anterior,
                    "nuevo": usuario_nuevo.copiar(),
                }
            )

            self.historial.registrar_accion(accion)

        return usuario
    
    def restaurar_usuario(self, usuario):
        """Restaura un usuario eliminado."""

        if self.buscar_usuario(usuario.id) is not None:
            return False

        if not self.lista_usuarios.insertar(usuario):
            return False

        self._guardar()

        return True

    def existe_usuario(self, id_usuario):
        """Indica si existe un usuario."""

        return self.buscar_usuario(id_usuario) is not None

    def eliminar_usuario(
        self,
        id_usuario,
        registrar_historial=True
    ):
        """Elimina un usuario."""

        usuario = self.buscar_usuario(id_usuario)

        if usuario is None:
            raise ValueError(
                "No existe un usuario con ese ID."
            )

        usuario_eliminado = usuario.copiar()

        if not self.lista_usuarios.eliminar(id_usuario):
            raise ValueError(
                "No fue posible eliminar el usuario."
            )

        self._guardar()

        if registrar_historial and self.historial is not None:
            accion = Accion(
                Accion.ELIMINAR,
                f"Se eliminó el usuario {id_usuario}",
                usuario_eliminado
            )

            self.historial.registrar_accion(accion)

        return True

    def _guardar(self):
        """Persiste todos los usuarios."""

        self.usuario_repository.guardar(
            self.lista_usuarios.listar()
        )