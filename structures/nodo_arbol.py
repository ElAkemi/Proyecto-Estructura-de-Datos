class NodoArbol:
    """Nodo de un árbol general de tareas."""

    def __init__(self, tarea):
        self.tarea = tarea

        # Un nodo puede tener múltiples hijos.
        self.hijos = []