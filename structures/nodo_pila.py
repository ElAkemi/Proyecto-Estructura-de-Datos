"""Módulo que representa un nodo de la pila."""


class NodoPila:
    """Representa un nodo dentro de la pila."""

    def __init__(self, accion):
        """
        Inicializa un nodo con una acción.

        :param accion: Acción que almacenará el nodo.
        :return: None.
        """

        self.accion = accion
        self.siguiente = None