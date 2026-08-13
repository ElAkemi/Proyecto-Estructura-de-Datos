# Representa un nodo individual en una lista simplemente enlazada.
# Cada nodo almacena un dato y una referencia al siguiente nodo.
class NodoCola:
    def __init__(self, dato):
        # Almacena la información o el objeto principal que guarda el nodo
        self.dato = dato
        
        # Puntero hacia el siguiente NodoCola en la lista (None si es el último)
        self.siguiente = None

class ColaFIFO:
    def __init__(self):
        # Referencia al primer elemento de la cola 
        self._frente = None
        
        # Referencia al último elemento de la cola 
        self._final = None
        
        # Contador interno del número total de elementos almacenados en la cola
        self._tamano = 0

    def encolar(self, dato):
        # Instancia un nuevo nodo envolviendo el dato recibido
        nuevo_nodo = NodoCola(dato)
        
        # Si la cola está completamente vacía
        if self.esta_vacia():
            # El nuevo nodo se convierte simultáneamente en la cabeza (frente) y cola (final)
            self._frente = nuevo_nodo
            self._final = nuevo_nodo
        else:
            # Si la cola ya contiene elementos
            self._final.siguiente = nuevo_nodo # Enlaza el nodo que estaba al final con el nuevo nodo
            
            # Actualiza el puntero del final para que apunte al nuevo nodo recien insertado
            self._final = nuevo_nodo
            
        # Incrementa en 1 el contador global de elementos
        self._tamano += 1

    def desencolar(self):
        # Verifica que la cola tenga elementos antes de intentar extraer
        if self.esta_vacia():
            # Lanza una excepción si se intenta extraer de una cola vacía
            raise IndexError("La cola está vacía.")
            
        # Guarda temporalmente el dato almacenado en el nodo del frente
        dato = self._frente.dato
        
        # Desplaza el puntero del frente al siguiente nodo de la lista
        self._frente = self._frente.siguiente
        
        # Si al mover el frente la lista queda vacía (el frente es None)
        if self._frente is None:
            # Resetea también la referencia del final a None para mantener consistencia
            self._final = None
            
        # Decrementa en 1 el contador global de elementos
        self._tamano -= 1
        
        # Retorna el dato que fue extraído
        return dato

    def ver_frente(self):
        # Si la cola está vacía, no hay nada que retornar
        if self.esta_vacia():
            return None
        # Retorna la información almacenada en el nodo frontal
        return self._frente.dato

    def esta_vacia(self) -> bool:
        # Retorna True si la referencia al frente es None; de lo contrario, False
        return self._frente is None

    def obtener_lista(self) -> list:
        # Inicializa un arreglo vacío para almacenar los elementos
        elementos = []
        
        # Inicializa un puntero de recorrido comenzando por el frente
        actual = self._frente
        
        # Recorre la lista enlazada nodo por nodo hasta llegar a None
        while actual:
            # Añade el dato del nodo actual a la lista resultante
            elementos.append(actual.dato)
            
            # Avanza la posición del puntero al siguiente nodo
            actual = actual.siguiente
            
        # Retorna la lista con todos los objetos recolectados
        return elementos

    def buscar_por_id(self, id_tarea: int):
        # Asegura la conversión del ID de búsqueda a entero para evitar fallos de tipo
        id_buscado = int(id_tarea)
        
        # Comienza el recorrido desde el nodo inicial (frente)
        actual = self._frente
        
        # Itera sobre los nodos mientras no se alcance el final (None)
        while actual:
            # Utiliza getattr para verificar de forma segura si el dato tiene la propiedad 'id_tarea'
            if getattr(actual.dato, "id_tarea", None) == id_buscado:
                # Si los IDs coinciden, retorna inmediatamente el objeto encontrado
                return actual.dato
                
            # Avanza hacia el nodo subsiguiente
            actual = actual.siguiente
            
        # Retorna None si finalizó el recorrido sin encontrar ningún nodo coincidente
        return None

    def eliminar_por_id(self, id_tarea: int) -> bool:
        # Si la cola no contiene elementos, no hay nada que eliminar
        if self.esta_vacia():
            return False

        # Normaliza el parámetro a número entero
        id_buscado = int(id_tarea)

        # El elemento a eliminar está en el frente (primer nodo)
        if getattr(self._frente.dato, "id_tarea", None) == id_buscado:
            # Hace que el frente apunte directamente al segundo nodo
            self._frente = self._frente.siguiente
            
            # Si tras eliminar la cabeza no quedan más elementos en la cola
            if self._frente is None:
                # Resetea también el puntero del final a None
                self._final = None
                
            # Reduce el contador de tamaño
            self._tamano -= 1
            
            # Retorna True indicando que la eliminación fue exitosa
            return True

        # El elemento está en el cuerpo de la cola o al final
        actual = self._frente
        
        # Evalúa el nodo siguiente (actual.siguiente) mientras exista
        while actual.siguiente:
            # Comprueba si el nodo hijo/siguiente contiene el ID buscado
            if getattr(actual.siguiente.dato, "id_tarea", None) == id_buscado:
                # Si el nodo a eliminar resulta ser el último nodo (final)
                if actual.siguiente == self._final:
                    # Actualiza la referencia del final al nodo previo (actual)
                    self._final = actual
                    
                # "Salta" el nodo objetivo enlazando 'actual' directamente con el posterior al objetivo
                actual.siguiente = actual.siguiente.siguiente
                
                # Decrementa el contador global de elementos
                self._tamano -= 1
                
                # Confirma la eliminación exitosa
                return True
                
            # Avanza el puntero de inspección al siguiente nodo
            actual = actual.siguiente
            
        # Si terminó todo el bucle sin coincidencias, retorna False
        return False

    def __len__(self):
        # Retorna el entero que almacena el conteo actual de elementos
        return self._tamano