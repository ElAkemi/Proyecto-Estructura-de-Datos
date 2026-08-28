class Accion:
    """Representa una acción que puede deshacerse o rehacerse."""

    AGREGAR = "AGREGAR"
    MODIFICAR = "MODIFICAR"
    ELIMINAR = "ELIMINAR"
    CAMBIAR_ESTADO = "CAMBIAR_ESTADO"

    def __init__(
        self,
        tipo,
        descripcion,
        datos=None,
        usuario_id=None
    ):
        self.tipo = tipo
        self.descripcion = descripcion
        self.datos = datos
        self.usuario_id = usuario_id

    def __repr__(self):
        return (
            f"Accion("
            f"tipo='{self.tipo}', "
            f"descripcion='{self.descripcion}'"
            f")"
        )