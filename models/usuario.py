class Usuario:
    """Representa un usuario del sistema."""

    ROLES_VALIDOS = ("Administrador", "Usuario")

    def __init__(self, id, nombre, rol, password):
        if not isinstance(id, int) or id <= 0:
            raise ValueError("El ID debe ser un entero positivo.")

        if not isinstance(nombre, str) or not nombre.strip():
            raise ValueError("El nombre no puede estar vacío.")

        if rol not in self.ROLES_VALIDOS:
            raise ValueError(
                "El rol debe ser 'Administrador' o 'Usuario'."
            )

        if not isinstance(password, str) or not password:
            raise ValueError("La contraseña no puede estar vacía.")

        self.id = id
        self.nombre = nombre.strip()
        self.rol = rol
        self.password = password

    def copiar(self):
        """Devuelve una copia independiente del usuario."""
        return Usuario(
            self.id,
            self.nombre,
            self.rol,
            self.password
        )

    def __repr__(self):
        return (
            f"Usuario("
            f"id={self.id}, "
            f"nombre='{self.nombre}', "
            f"rol='{self.rol}'"
            f")"
        )