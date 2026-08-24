"""Módulo que implementa una cola de prioridad basada en listas enlazadas."""

class NodoPrioridad:
    """Representa un nodo individual dentro de la cola de prioridad."""

    def __init__(self, tarea):
        """Inicializa un nuevo nodo almacenando una tarea y la referencia al siguiente."""
        self.tarea = tarea
        self.siguiente = None


class ColaPrioridad:
    """Implementa una cola de prioridad donde los elementos con mayor valor se procesan primero."""

    def __init__(self):
        """Inicializa la cola de prioridad vacía."""
        self.cabeza = None
        self._tamano = 0

    def encolar(self, tarea):
        """Inserta una tarea ordenadamente según la prioridad asignada."""
        nuevo_nodo = NodoPrioridad(tarea)

        if self.cabeza is None or tarea.prioridad.value > self.cabeza.tarea.prioridad.value:
            nuevo_nodo.siguiente = self.cabeza
            self.cabeza = nuevo_nodo
        else:
            actual = self.cabeza
            while (
                actual.siguiente
                and actual.siguiente.tarea.prioridad.value >= tarea.prioridad.value
            ):
                actual = actual.siguiente

            nuevo_nodo.siguiente = actual.siguiente
            actual.siguiente = nuevo_nodo

        self._tamano += 1

    def desencolar(self):
        """Extrae y retorna la tarea de mayor prioridad al frente de la cola."""
        if self.esta_vacia():
            raise IndexError("La cola de prioridad está vacía.")

        tarea = self.cabeza.tarea
        self.cabeza = self.cabeza.siguiente
        self._tamano -= 1
        return tarea

    def esta_vacia(self) -> bool:
        """Verifica si la cola de prioridad no contiene elementos."""
        return self.cabeza is None

    def obtener_lista(self) -> list:
        """Retorna todas las tareas contenidas en la cola como una lista."""
        elementos = []
        actual = self.cabeza
        while actual:
            elementos.append(actual.tarea)
            actual = actual.siguiente
        return elementos

    def buscar_por_id(self, id_tarea: int):
        """Busca y retorna una tarea por su id_tarea."""
        actual = self.cabeza
        while actual:
            if hasattr(actual.tarea, "id_tarea") and actual.tarea.id_tarea == id_tarea:
                return actual.tarea
            actual = actual.siguiente
        return None

    def eliminar_por_id(self, id_tarea: int) -> bool:
        """Elimina una tarea de la cola especificando su id_tarea."""
        if self.esta_vacia():
            return False

        if hasattr(self.cabeza.tarea, "id_tarea") and self.cabeza.tarea.id_tarea == id_tarea:
            self.cabeza = self.cabeza.siguiente
            self._tamano -= 1
            return True

        actual = self.cabeza
        while actual.siguiente:
            if (
                hasattr(actual.siguiente.tarea, "id_tarea")
                and actual.siguiente.tarea.id_tarea == id_tarea
            ):
                actual.siguiente = actual.siguiente.siguiente
                self._tamano -= 1
                return True
            actual = actual.siguiente

        return False

    def __len__(self):
        """Retorna la cantidad total de elementos almacenados."""
        return self._tamano
    