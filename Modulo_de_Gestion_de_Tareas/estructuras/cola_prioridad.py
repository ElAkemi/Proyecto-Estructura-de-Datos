class NodoPrioridad:
    def __init__(self, tarea):
        # Guarda el objeto Tarea (el cual posee el atributo de prioridad)
        self.tarea = tarea
        
        # Referencia al siguiente NodoPrioridad (None si es el último nodo)
        self.siguiente = None
class ColaPrioridad:
    def __init__(self):
        # Puntero/Referencia al primer elemento de la cola (nodo con mayor prioridad)
        self.cabeza = None
        
        # Contador interno del número total de elementos en la cola
        self._tamano = 0

    def encolar(self, tarea):
        # Instancia un nuevo nodo con la tarea a insertar
        nuevo_nodo = NodoPrioridad(tarea)
        
        # Mayor valor numérico en Enum Prioridad = Mayor urgencia
        # Si la cola está vacía O la nueva tarea tiene mayor prioridad que la cabeza actual
        if self.cabeza is None or tarea.prioridad.value > self.cabeza.tarea.prioridad.value:
            # Apunta el nuevo nodo a la antigua cabeza
            nuevo_nodo.siguiente = self.cabeza
            
            # El nuevo nodo se convierte en la nueva cabeza de la lista
            self.cabeza = nuevo_nodo
        else:
            # La nueva tarea debe insertarse en el cuerpo o al final de la lista
            actual = self.cabeza
            
            # Recorre la lista mientras exista un nodo siguiente Y la prioridad del nodo siguiente
            # sea mayor o igual a la nueva tarea (mantiene estabilidad FIFO para prioridades iguales)
            while actual.siguiente and actual.siguiente.tarea.prioridad.value >= tarea.prioridad.value:
                actual = actual.siguiente
                
            # Intercala el nuevo nodo entre 'actual' y 'actual.siguiente'
            nuevo_nodo.siguiente = actual.siguiente
            actual.siguiente = nuevo_nodo
            
        # Incrementa el contador de elementos
        self._tamano += 1

    def desencolar(self):
        # Comprueba que la cola contenga elementos antes de extraer
        if self.esta_vacia():
            # Lanza excepción si se intenta extraer de una cola vacía
            raise IndexError("La cola de prioridad está vacía.")
            
        # Obtiene la tarea alojada en el nodo cabeza
        tarea = self.cabeza.tarea
        
        # Desplaza la cabeza al siguiente nodo en la lista
        self.cabeza = self.cabeza.siguiente
        
        # Decrementa el contador global de elementos
        self._tamano -= 1
        
        # Retorna la tarea extraída
        return tarea

    def esta_vacia(self) -> bool:
        # Verifica si el puntero de la cabeza es None
        return self.cabeza is None

    def obtener_lista(self) -> list:
        # Lista temporal para recopilar los objetos Tarea
        elementos = []
        
        # Comienza el recorrido desde el primer nodo (cabeza)
        actual = self.cabeza
        
        # Avanza nodo por nodo añadiendo la tarea correspondiente
        while actual:
            elementos.append(actual.tarea)
            actual = actual.siguiente
            
        # Retorna la lista con todas las tareas
        return elementos

    def buscar_por_id(self, id_tarea: int):
        # Comienza la inspección desde la cabeza
        actual = self.cabeza
        
        # Recorre la lista mientras existan nodos
        while actual:
            # Comprueba si el objeto tarea tiene el atributo 'id_tarea' y coincide con el parametro
            if hasattr(actual.tarea, "id_tarea") and actual.tarea.id_tarea == id_tarea:
                # Retorna el objeto tarea si lo encuentra
                return actual.tarea
                
            # Avanza al siguiente nodo
            actual = actual.siguiente
            
        # Retorna None si no se encontró la tarea
        return None

    def eliminar_por_id(self, id_tarea: int) -> bool:
        # Si la cola está vacía, no se puede realizar la eliminación
        if self.esta_vacia():
            return False

        # El nodo a eliminar es la cabeza actual
        if hasattr(self.cabeza.tarea, "id_tarea") and self.cabeza.tarea.id_tarea == id_tarea:
            # Mueve la cabeza al segundo nodo
            self.cabeza = self.cabeza.siguiente
            
            # Decrementa el contador global
            self._tamano -= 1
            
            # Retorna True indicando éxito
            return True

        # El nodo a eliminar se encuentra más adelante en la lista
        actual = self.cabeza
        
        # Revisa el nodo siguiente (actual.siguiente) mientras no sea None
        while actual.siguiente:
            # Comprueba si el nodo subsiguiente tiene el ID buscado
            if hasattr(actual.siguiente.tarea, "id_tarea") and actual.siguiente.tarea.id_tarea == id_tarea:
                # Desvincula el nodo saltándose la referencia hacia 'actual.siguiente.siguiente'
                actual.siguiente = actual.siguiente.siguiente
                
                # Decrementa el contador de elementos
                self._tamano -= 1
                
                # Retorna True indicando que fue eliminado
                return True
                
            # Avanza al siguiente nodo en la lista
            actual = actual.siguiente
            
        # Retorna False si no se encontró el ID en la cola
        return False

    def __len__(self):
        # Retorna la variable entera que rastrea el tamaño
        return self._tamano