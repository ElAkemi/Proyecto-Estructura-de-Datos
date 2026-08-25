"""Módulo que implementa una cola FIFO con nodos."""

class NodoCola:
    """Representa un nodo individual en una lista simplemente enlazada."""

    def __init__(self, dato):
        """Inicializa un nuevo nodo con el dato recibido y puntero vacio."""
        self.dato = dato
        self.siguiente = None

class ColaFIFO:
    """Implementa una estructura de datos Cola FIFO basada en nodos."""

    def __init__(self):
        """Inicializa una cola vacia con punteros al frente, final y tamaño 0."""
        self._frente = None
        self._final = None
        self._tamano = 0

    def encolar(self, dato):
        """Agrega un nuevo elemento al final de la cola."""
        nuevo_nodo = NodoCola(dato)

        if self.esta_vacia():
            self._frente = nuevo_nodo
            self._final = nuevo_nodo
        else:
            self._final.siguiente = nuevo_nodo
            self._final = nuevo_nodo

        self._tamano += 1

    def desencolar(self):
        """Extrae y retorna el elemento en el frente de la cola."""
        if self.esta_vacia():
            raise IndexError("La cola está vacía.")

        dato = self._frente.dato
        self._frente = self._frente.siguiente

        if self._frente is None:
            self._final = None

        self._tamano -= 1
        return dato

    def ver_frente(self):
        """Retorna el dato en el frente de la cola sin removerlo."""
        if self.esta_vacia():
            return None
        return self._frente.dato

    def esta_vacia(self) -> bool:
        """Verifica si la cola no contiene elementos."""
        return self._frente is None

    def obtener_lista(self) -> list:
        """Retorna todos los elementos de la cola en una lista."""
        elementos = []
        actual = self._frente
        while actual:
            elementos.append(actual.dato)
            actual = actual.siguiente
        return elementos

    def buscar_por_id(self, id_tarea: int):
        """Busca y retorna un elemento por su atributo id_tarea."""
        id_buscado = int(id_tarea)
        actual = self._frente
        while actual:
            if getattr(actual.dato, "id_tarea", None) == id_buscado:
                return actual.dato
            actual = actual.siguiente
        return None

    def eliminar_por_id(self, id_tarea: int) -> bool:
        """Elimina un nodo especifico buscando por su id_tarea."""
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
            if getattr(actual.siguiente.dato, "id_tarea", None) == id_buscado:
                if actual.siguiente == self._final:
                    self._final = actual
                actual.siguiente = actual.siguiente.siguiente
                self._tamano -= 1
                return True
            actual = actual.siguiente

        return False

    def incrementar_ciclos_y_extraer_escaladas(self, max_ciclos: int) -> list:
        """Incrementa los ciclos de espera y remueve las tareas que superan el maximo."""
        escaladas = []
        if self.esta_vacia():
            return escaladas

        actual = self._frente
        previo = None

        while actual:
            tarea = actual.dato
            if hasattr(tarea, "incrementar_ciclo_espera"):
                tarea.incrementar_ciclo_espera()
            elif hasattr(tarea, "ciclos_espera"):
                tarea.ciclos_espera += 1

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
        """Retorna la cantidad de elementos en la cola."""
        return self._tamano
    