"""Definición de Nodo del Árbol de Subtareas"""

class NodoArbolTarea:
    def __init__(self, id_subtarea: int, descripcion: str, id_padre: int = None, completada: bool = False):
        """Inicializa un nodo del árbol con sus atributos."""
        self.id_subtarea = int(id_subtarea)
        self.descripcion = str(descripcion)
        self.id_padre = int(id_padre) if id_padre is not None else None
        self.completada = bool(completada)
        self.subtareas = [] # Lista de hijos en el árbol general

    def agregar_subtarea(self, id_padre: int, id_subtarea: int, descripcion: str, completada: bool = False) -> bool:
        """Busca recursivamente el nodo padre y le agrega el nuevo nodo hijo."""
        
        if self.id_subtarea == id_padre:
            self.subtareas.append(NodoArbolTarea(id_subtarea, descripcion, id_padre, completada))
            return True
        
        for hijo in self.subtareas:
            if hijo.agregar_subtarea(id_padre, id_subtarea, descripcion, completada):
                return True
        return False

    def buscar_nodo(self, id_subtarea: int):
        """Busca un nodo recursivamente por su ID."""
        
        if self.id_subtarea == id_subtarea:
            return self
        for hijo in self.subtareas:
            encontrado = hijo.buscar_nodo(id_subtarea)
            if encontrado:
                return encontrado
        return None

    def obtener_todas(self) -> list:
        """Recorrido recursivo para obtener todas las subtareas en formato de tupla."""
        
        resultado = [(self.id_subtarea, self.descripcion, self.completada, self.id_padre)]
        for hijo in self.subtareas:
            resultado.extend(hijo.obtener_todas())
        return resultado

    def __repr__(self):
        """Representación del nodo en formato de cadena."""
        estado = "Completada" if self.completada else "Pendiente"
        return f"NodoArbolTarea(ID={self.id_subtarea}, Desc='{self.descripcion}', Estado={estado}, Subtareas={len(self.subtareas)})"
    