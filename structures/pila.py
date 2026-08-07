from structures.nodo_pila import NodoPila

class Pila:
    def __init__(self):
        self.cima = None

    def apilar(self, accion):
        nuevo_nodo = NodoPila(accion)

        #El nuevo nodo apunta al que estaba arriba
        nuevo_nodo.siguiente = self.cima

        #La cima ahora es el nuevo nodo
        self.cima = nuevo_nodo

    def desapilar(self):
        # La pila está vacía
        if self.cima is None:
            return None  

        # Guardar el nodo que está en la cima
        nodo_desapilado = self.cima

        # La cima ahora es el siguiente nodo
        self.cima = self.cima.siguiente
        
        nodo_desapilado.siguiente = None
        # Retornar la acción del nodo desapilado
        return nodo_desapilado.accion
        
    def peek(self):
        # La pila está vacía
        if self.cima is None:
            return None  

        # Retornar la acción del nodo en la cima sin desapilarlo
        return self.cima.accion
    
    def esta_vacia(self):
        return self.cima is None

    def mostrar(self):
        if self.cima is None:
            print("La pila está vacía")
            return

        actual = self.cima

        while actual is not None:
            print(f"Tipo: {actual.accion.tipo}, Descripción: {actual.accion.descripcion}")
            actual = actual.siguiente