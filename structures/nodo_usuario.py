"""Módulo que define el nodo utilizado en la lista doblemente enlazada."""


class NodoUsuario:
    """Representa un nodo de la lista doblemente enlazada de usuarios."""

    def __init__(self, usuario):
        """
        Inicializa un nodo con un usuario.

        :param usuario: Objeto Usuario que almacenará el nodo.
        :return: None.
        """

        self.usuario = usuario
        self.siguiente = None
        self.anterior = None