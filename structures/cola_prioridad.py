class ColaPrioridad:
    """
    Cola de prioridad para tareas urgentes.

    Las tareas con mayor prioridad numérica
    se procesan primero.
    """

    def __init__(self):
        self.elementos = []

    def encolar(self, tarea):
        """
        Agrega una tarea y mantiene la cola ordenada
        de mayor a menor prioridad.
        """

        self.elementos.append(tarea)

        self.elementos.sort(
            key=lambda tarea: -int(tarea.prioridad)
        )

    def desencolar(self):
        """
        Retira la tarea con mayor prioridad.

        Retorna:
            La tarea o None si está vacía.
        """

        if self.esta_vacia():
            return None

        return self.elementos.pop(0)

    def frente(self):
        """Devuelve la tarea con mayor prioridad sin retirarla."""

        if self.esta_vacia():
            return None

        return self.elementos[0]

    def esta_vacia(self):
        """Indica si la cola está vacía."""

        return len(self.elementos) == 0

    def remover_por_id(self, tarea_id):
        """
        Busca y elimina una tarea por ID.

        Retorna:
            La tarea eliminada o None.
        """

        for indice, tarea in enumerate(self.elementos):

            if tarea.id == tarea_id:
                return self.elementos.pop(indice)

        return None

    def listar(self):
        """Devuelve las tareas actuales de la cola."""

        return list(self.elementos)

    def __len__(self):
        """Devuelve la cantidad de tareas."""

        return len(self.elementos)