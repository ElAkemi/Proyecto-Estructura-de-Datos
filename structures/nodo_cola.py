class NodoCola:
    """Nodo utilizado por las colas (FIFO y de prioridad)."""

    def __init__(self, dato):
        self.dato = dato
        self.siguiente = None
