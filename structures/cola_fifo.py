class ColaFIFO:
    """
    Cola FIFO para tareas regulares.

    FIFO significa:
        First In, First Out.

    La primera tarea que entra es la primera que sale.
    """

    def __init__(self):
        self.elementos = []

    def encolar(self, tarea):
        """Agrega una tarea al final de la cola."""

        self.elementos.append(tarea)

    def desencolar(self):
        """
        Retira y devuelve la primera tarea.

        Retorna:
            La tarea o None si la cola está vacía.
        """

        if self.esta_vacia():
            return None

        return self.elementos.pop(0)

    def frente(self):
        """Devuelve la primera tarea sin retirarla."""

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
            La tarea eliminada o None si no existe.
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