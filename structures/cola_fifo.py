"""Módulo que implementa una cola FIFO con nodos."""


class NodoCola:
    """Representa un nodo individual en una lista simplemente enlazada."""

    def __init__(self, dato):
        """
        Inicializa un nuevo nodo con el dato recibido.

        :param dato: Elemento que almacenará el nodo.
        :return: None.
        """

        self.dato = dato
        self.siguiente = None


class ColaFIFO:
    """Implementa una estructura de datos Cola FIFO basada en nodos."""

    def __init__(self):
        """
        Inicializa una cola vacía.

        :return: None.
        """

        self._frente = None
        self._final = None
        self._tamano = 0

    def encolar(self, dato):
        """
        Agrega un nuevo elemento al final de la cola.

        :param dato: Elemento que se desea agregar.
        :return: None.
        """

        nuevo_nodo = NodoCola(dato)

        if self.esta_vacia():
            self._frente = nuevo_nodo
            self._final = nuevo_nodo
        else:
            self._final.siguiente = nuevo_nodo
            self._final = nuevo_nodo

        self._tamano += 1

    def desencolar(self):
        """
        Extrae y retorna el elemento que se encuentra al frente.

        :return: Elemento que estaba al frente de la cola.
        :raises IndexError: Si la cola está vacía.
        """

        if self.esta_vacia():
            raise IndexError("La cola está vacía.")

        dato = self._frente.dato
        self._frente = self._frente.siguiente

        if self._frente is None:
            self._final = None

        self._tamano -= 1

        return dato

    def ver_frente(self):
        """
        Consulta el elemento ubicado al frente sin removerlo.

        :return: Elemento del frente o None si la cola está vacía.
        """

        if self.esta_vacia():
            return None

        return self._frente.dato

    def esta_vacia(self) -> bool:
        """
        Verifica si la cola no contiene elementos.

        :return: True si está vacía, False en caso contrario.
        """

        return self._frente is None

    def obtener_lista(self) -> list:
        """
        Obtiene todos los elementos de la cola en orden FIFO.

        :return: Lista con los elementos almacenados.
        """

        elementos = []
        actual = self._frente

        while actual:
            elementos.append(actual.dato)
            actual = actual.siguiente

        return elementos

    def buscar_por_id(self, id_tarea: int):
        """
        Busca una tarea dentro de la cola utilizando su ID.

        :param id_tarea: Identificador de la tarea que se desea buscar.
        :return: Tarea encontrada o None si no existe.
        """

        id_buscado = int(id_tarea)
        actual = self._frente

        while actual:
            if getattr(actual.dato, "id_tarea", None) == id_buscado:
                return actual.dato

            actual = actual.siguiente

        return None

    def eliminar_por_id(self, id_tarea: int) -> bool:
        """
        Elimina una tarea específica utilizando su ID.

        :param id_tarea: Identificador de la tarea que se desea eliminar.
        :return: True si se eliminó, False si no se encontró.
        """

        if self.esta_vacia():
            return False

        id_buscado = int(id_tarea)

        if getattr(self._frente.dato, "id_tarea", None) == id_buscado:
            self._frente = self._frente.siguiente

            if self._frente is None:
                self._final = None

            self._tamano -= 1
            return True

        actual = self._frente

        while actual.siguiente:
            if getattr(
                actual.siguiente.dato,
                "id_tarea",
                None
            ) == id_buscado:

                if actual.siguiente == self._final:
                    self._final = actual

                actual.siguiente = actual.siguiente.siguiente
                self._tamano -= 1

                return True

            actual = actual.siguiente

        return False

    def incrementar_ciclos_y_extraer_escaladas(
        self,
        max_ciclos: int
    ) -> list:
        """
        Incrementa los ciclos de espera de las tareas y extrae
        aquellas que alcanzaron el límite establecido.

        :param max_ciclos: Cantidad máxima de ciclos permitidos.
        :return: Lista de tareas que fueron escaladas.
        """

        escaladas = []

        if self.esta_vacia():
            return escaladas

        actual = self._frente
        previo = None

        while actual:

            tarea = actual.dato

            if hasattr(tarea, "incrementar_ciclo_espera"):
                tarea.incrementar_ciclo_espera()

            ciclos = getattr(tarea, "ciclos_espera", 0)

            if ciclos >= max_ciclos:

                escaladas.append(tarea)

                if previo is None:
                    self._frente = actual.siguiente

                    if self._frente is None:
                        self._final = None

                else:
                    previo.siguiente = actual.siguiente

                    if actual == self._final:
                        self._final = previo

                self._tamano -= 1
                actual = actual.siguiente

            else:
                previo = actual
                actual = actual.siguiente

        return escaladas

    def __len__(self):
        """
        Retorna la cantidad de elementos almacenados.

        :return: Cantidad de elementos de la cola.
        """

        return self._tamano