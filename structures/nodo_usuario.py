class NodoUsuario:
    def __init__(self, Usuario):
        self.usuario = Usuario
        self.siguiente = None
        self.anterior = None