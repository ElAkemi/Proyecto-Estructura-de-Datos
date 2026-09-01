from structures.nodo_cola import NodoCola


class ColaFIFO:
    """
    Cola FIFO para tareas regulares, implementada con
    nodos enlazados (sin usar listas de Python como
    estructura de almacenamiento).

    FIFO significa:
        First In, First Out.

    La primera tarea que entra es la primera que sale.
    """

    def __init__(self):
        self.frente_nodo = None
        self.final_nodo = None
        self.tamano = 0

    def encolar(self, tarea):
        """Agrega una tarea al final de la cola."""

        nuevo_nodo = NodoCola(tarea)

        if self.frente_nodo is None:
            self.frente_nodo = nuevo_nodo
            self.final_nodo = nuevo_nodo
        else:
            self.final_nodo.siguiente = nuevo_nodo
            self.final_nodo = nuevo_nodo

        self.tamano += 1

    def desencolar(self):
        """
        Retira y devuelve la primera tarea.

        Retorna:
            La tarea o None si la cola está vacía.
        """

        if self.esta_vacia():
            return None

        nodo = self.frente_nodo
        self.frente_nodo = nodo.siguiente

        if self.frente_nodo is None:
            self.final_nodo = None

        self.tamano -= 1

        return nodo.dato

    def frente(self):
        """Devuelve la primera tarea sin retirarla."""

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
            La tarea eliminada o None si no existe.
        """

        actual = self.frente_nodo
        anterior = None

        while actual is not None:

            if actual.dato.id == tarea_id:

                if anterior is None:
                    self.frente_nodo = actual.siguiente
                else:
                    anterior.siguiente = actual.siguiente

                if actual is self.final_nodo:
                    self.final_nodo = anterior

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
