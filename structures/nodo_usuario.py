class NodoUsuario:
    """Nodo utilizado por la lista doblemente enlazada de usuarios."""

    def __init__(self, usuario):
        self.usuario = usuario
        self.anterior = None
        self.siguiente = None