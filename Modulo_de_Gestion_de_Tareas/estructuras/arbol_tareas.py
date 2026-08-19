"""Módulo para la gestión de la estructura de árbol de tareas."""
from modelos.nodo_arbol import NodoArbolTarea
class ArbolTareas:
    """Clase para la representación y gestión de la estructura de árbol de tareas."""

    def __init__(self, id_raiz: int, descripcion: str):
        """Inicializa la raíz del árbol con su identificador y descripción.

        Como es la raíz, su id_padre es None.
        """
        self.raiz = NodoArbolTarea(

            id_subtarea=id_raiz,
            descripcion=descripcion,
            id_padre=None
        )

    def agregar_subtarea(
        self,
        id_subtarea: int,
        id_padre: int,
        descripcion: str,
        completada: bool = False
    ) -> bool:
        """Inserta una nueva subtarea de forma recursiva desde la raíz."""
        return self.raiz.agregar_subtarea(
            id_padre,
            id_subtarea,
            descripcion,
            completada
        )

    def buscar_nodo(self, id_subtarea: int):
        """Busca y retorna un nodo dentro del árbol según su ID."""
        return self.raiz.buscar_nodo(id_subtarea)

    def obtener_todas(self) -> list:
        """Retorna todas las tareas del árbol."""
        return self.raiz.obtener_todas() if self.raiz else []

    