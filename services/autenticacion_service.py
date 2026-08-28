class AutenticacionService:
    """Gestiona la autenticación y los permisos de los usuarios."""

    def __init__(self, usuario_service):
        self.usuario_service = usuario_service

    def autenticar(self, id_usuario, password):
        """
        Comprueba las credenciales.

        Retorna:
            Usuario autenticado o None.
        """

        usuario = self.usuario_service.buscar_usuario(
            id_usuario
        )

        if usuario is None:
            return None

        if usuario.password != password:
            return None

        return usuario

    def es_administrador(self, usuario):
        """Comprueba si un usuario tiene rol administrador."""

        return (
            usuario is not None
            and usuario.rol == "Administrador"
        )

    def es_usuario_normal(self, usuario):
        """Comprueba si un usuario tiene rol normal."""

        return (
            usuario is not None
            and usuario.rol == "Usuario"
        )