try:
    from ..Models.NodoArbol import NodoArbolTarea
except (ImportError, ValueError):
    from Models.NodoArbol import NodoArbolTarea

class ArbolTareas:
    # Contructor de la clase
    def __init__(self, id_raiz: int, descripcion: str):
        # Instancia la raíz del árbol guardándolo en el atributo self.raiz. Como es la raíz, su id_padre es None.
        self.raiz = NodoArbolTarea(id_subtarea=id_raiz, descripcion=descripcion, id_padre=None)

    # Metodo para insertar una nueva tarea, lo resive por defecto como False y retorna un booleano
    def agregar_subtarea(self, id_subtarea: int, id_padre: int, descripcion: str, completada: bool = False) -> bool:
        # Le da la responsabilidad de insercion a la raiz, el cual buscara recursivamente al padre para poner la nueva tarea
        return self.raiz.agregar_subtarea(id_padre, id_subtarea, descripcion, completada)

    # Metodo de busqueda de una subtarea por su ID
    def buscar_nodo(self, id_subtarea: int):
        # Retorna el nodo encontrado
        return self.raiz.buscar_nodo(id_subtarea)

    # Metodo para mostrar todas las subtareas en forma de lista
    def obtener_todas(self) -> list:
        return self.raiz.obtener_todas()
