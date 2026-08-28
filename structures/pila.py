from structures.nodo_pila import NodoPila


class Pila:
    """Implementación de una pila utilizando nodos enlazados."""

    def __init__(self):
        self.tope = None
        self.tamano = 0

    def apilar(self, dato):
        """Agrega un elemento en el tope de la pila."""

        nuevo_nodo = NodoPila(dato)

        nuevo_nodo.siguiente = self.tope
        self.tope = nuevo_nodo

        self.tamano += 1

    def desapilar(self):
        """
        Elimina y devuelve el elemento del tope.

        Retorna:
            El dato del tope o None si está vacía.
        """

        if self.esta_vacia():
            return None

        dato = self.tope.dato

        self.tope = self.tope.siguiente

        self.tamano -= 1

        return dato

    def peek(self):
        """Devuelve el elemento del tope sin eliminarlo."""

        if self.esta_vacia():
            return None

        return self.tope.dato

    def esta_vacia(self):
        """Indica si la pila está vacía."""

        return self.tope is None

    def mostrar(self):
        """Devuelve los elementos de la pila de arriba hacia abajo."""

        elementos = []

        actual = self.tope

        while actual is not None:
            elementos.append(actual.dato)
            actual = actual.siguiente

        return elementos

    def limpiar(self):
        """Vacía completamente la pila."""

        self.tope = None
        self.tamano = 0

    def __len__(self):
        """Devuelve la cantidad de elementos."""

        return self.tamano