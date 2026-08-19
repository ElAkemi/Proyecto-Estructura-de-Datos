# Implementación manual de Pila (LIFO) mediante nodos simplemente enlazados.
class NodoPila:
    def __init__(self, dato):
        self.dato = dato
        self.siguiente = None

class Pila:
    def __init__(self):
        self.tope = None
        self._tamano = 0

    def apilar(self, dato):
        """Inserta un elemento en el tope de la pila."""
        nuevo_nodo = NodoPila(dato)
        nuevo_nodo.siguiente = self.tope
        self.tope = nuevo_nodo
        self._tamano += 1

    def desapilar(self):
        """Extrae y retorna el elemento en el tope de la pila."""
        if self.esta_vacia():
            raise IndexError("La pila está vacía.")
        dato = self.tope.dato
        self.tope = self.tope.siguiente
        self._tamano -= 1
        return dato

    def ver_tope(self):
        """Retorna el elemento en el tope sin extraerlo."""
        if self.esta_vacia():
            return None
        return self.tope.dato

    def esta_vacia(self) -> bool:
        """Verifica si la pila no contiene elementos."""
        return self.tope is None

    def limpiar(self):
        """Vacía todos los elementos de la pila."""
        self.tope = None
        self._tamano = 0

    def __len__(self):
        return self._tamano
