"""Módulo que implementa una cola de prioridad basada en listas enlazadas."""


class NodoPrioridad:
    """Representa un nodo individual dentro de la cola de prioridad."""

    def __init__(self, tarea):
        """
        Inicializa un nodo almacenando una tarea.

        :param tarea: Tarea que almacenará el nodo.
        :return: None.
        """

        self.tarea = tarea
        self.siguiente = None


class ColaPrioridad:
    """Implementa una cola de prioridad donde los elementos
    con mayor valor se procesan primero.
    """

    def __init__(self):
        """
        Inicializa una cola de prioridad vacía.

        :return: None.
        """

        self.cabeza = None
        self._tamano = 0

    def encolar(self, tarea):
        """
        Inserta una tarea ordenadamente según su prioridad.

        :param tarea: Tarea que se desea insertar.
        :return: None.
        """

        nuevo_nodo = NodoPrioridad(tarea)

        if (
            self.cabeza is None
            or tarea.prioridad.value > self.cabeza.tarea.prioridad.value
        ):
            nuevo_nodo.siguiente = self.cabeza
            self.cabeza = nuevo_nodo

        else:
            actual = self.cabeza

            while (
                actual.siguiente
                and actual.siguiente.tarea.prioridad.value
                >= tarea.prioridad.value
            ):
                actual = actual.siguiente

            nuevo_nodo.siguiente = actual.siguiente
            actual.siguiente = nuevo_nodo

        self._tamano += 1

    def desencolar(self):
        """
        Extrae la tarea con mayor prioridad.

        :return: Tarea que se encontraba al frente.
        :raises IndexError: Si la cola está vacía.
        """

        if self.esta_vacia():
            raise IndexError(
                "La cola de prioridad está vacía."
            )

        tarea = self.cabeza.tarea
        self.cabeza = self.cabeza.siguiente
        self._tamano -= 1

        return tarea

    def esta_vacia(self) -> bool:
        """
        Verifica si la cola de prioridad está vacía.

        :return: True si está vacía, False en caso contrario.
        """

        return self.cabeza is None

    def obtener_lista(self) -> list:
        """
        Obtiene todas las tareas en orden de prioridad.

        :return: Lista con las tareas almacenadas.
        """

        elementos = []
        actual = self.cabeza

        while actual:
            elementos.append(actual.tarea)
            actual = actual.siguiente

        return elementos

    def buscar_por_id(self, id_tarea: int):
        """
        Busca una tarea utilizando su ID.

        :param id_tarea: Identificador de la tarea que se desea buscar.
        :return: Tarea encontrada o None si no existe.
        """

        id_tarea = int(id_tarea)
        actual = self.cabeza

        while actual:
            if (
                hasattr(actual.tarea, "id_tarea")
                and actual.tarea.id_tarea == id_tarea
            ):
                return actual.tarea

            actual = actual.siguiente

        return None

    def eliminar_por_id(self, id_tarea: int) -> bool:
        """
        Elimina una tarea utilizando su ID.

        :param id_tarea: Identificador de la tarea que se desea eliminar.
        :return: True si se eliminó, False si no se encontró.
        """

        if self.esta_vacia():
            return False

        id_tarea = int(id_tarea)

        if (
            hasattr(self.cabeza.tarea, "id_tarea")
            and self.cabeza.tarea.id_tarea == id_tarea
        ):
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
        """
        Retorna la cantidad de elementos almacenados.

        :return: Cantidad de tareas en la cola.
        """

        return self._tamano