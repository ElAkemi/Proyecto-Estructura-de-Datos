from structures.nodo_cola import NodoCola


class ColaPrioridad:
    """
    Cola de prioridad para tareas urgentes, implementada con
    nodos enlazados (sin usar listas de Python como
    estructura de almacenamiento).

    Las tareas con mayor prioridad numérica se ubican
    más cerca del frente y se procesan primero. Entre
    tareas de igual prioridad se respeta el orden de
    llegada (la nueva se inserta después de las existentes
    con la misma prioridad).
    """

    def __init__(self):
        self.frente_nodo = None
        self.tamano = 0

    def encolar(self, tarea):
        """Inserta una tarea manteniendo el orden por prioridad."""

        nuevo_nodo = NodoCola(tarea)
        prioridad_nueva = int(tarea.prioridad)

        if (
            self.frente_nodo is None
            or int(self.frente_nodo.dato.prioridad) < prioridad_nueva
        ):
            nuevo_nodo.siguiente = self.frente_nodo
            self.frente_nodo = nuevo_nodo
            self.tamano += 1
            return

        actual = self.frente_nodo

        while (
            actual.siguiente is not None
            and int(actual.siguiente.dato.prioridad) >= prioridad_nueva
        ):
            actual = actual.siguiente

        nuevo_nodo.siguiente = actual.siguiente
        actual.siguiente = nuevo_nodo

        self.tamano += 1

    def desencolar(self):
        """
        Retira la tarea con mayor prioridad (el frente).

        Retorna:
            La tarea o None si está vacía.
        """

        if self.esta_vacia():
            return None

        nodo = self.frente_nodo
        self.frente_nodo = nodo.siguiente

        self.tamano -= 1

        return nodo.dato

    def frente(self):
        """Devuelve la tarea con mayor prioridad sin retirarla."""

        if self.esta_vacia():
            return None

        return self.frente_nodo.dato

    def esta_vacia(self):
        """Indica si la cola está vacía."""

        return self.frente_nodo is None

    def remover_por_id(self, tarea_id):
        """
        Busca y elimina una tarea por ID recorriendo
        los nodos enlazados.

        Retorna:
            La tarea eliminada o None.
        """

        actual = self.frente_nodo
        anterior = None

        while actual is not None:

            if actual.dato.id == tarea_id:

                if anterior is None:
                    self.frente_nodo = actual.siguiente
                else:
                    anterior.siguiente = actual.siguiente

                self.tamano -= 1

                return actual.dato

            anterior = actual
            actual = actual.siguiente

        return None

    def listar(self):
        """Devuelve las tareas actuales de la cola."""

        elementos = []
        actual = self.frente_nodo

        while actual is not None:
            elementos.append(actual.dato)
            actual = actual.siguiente

        return elementos

    def __len__(self):
        """Devuelve la cantidad de tareas."""

        return self.tamano
