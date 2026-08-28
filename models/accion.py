"""Módulo para representar acciones del sistema."""


class Accion:
    """Representa una acción que puede deshacerse o rehacerse."""

    def __init__(
        self,
        tipo,
        descripcion,
        datos,
        id_usuario=None
    ):
        """
        Inicializa una acción.

        :param tipo: Tipo de acción realizada.
        :param descripcion: Descripción de la acción.
        :param datos: Información necesaria para deshacer o rehacer.
        :param id_usuario: Usuario que ejecutó la acción.
        """

        self.tipo = tipo
        self.descripcion = descripcion
        self.datos = datos
        self.id_usuario = id_usuario