"""Módulo para la gestión de la estructura de árbol de tareas."""

from structures.nodo_arbol import NodoArbolTarea


class ArbolTareas:
    """Clase para la representación y gestión de la estructura
    de árbol de tareas.
    """

    def __init__(self, id_raiz: int, descripcion: str):
        """
        Inicializa la raíz del árbol.

        :param id_raiz: Identificador de la tarea raíz.
        :param descripcion: Descripción de la tarea raíz.
        :return: None.
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
        """
        Inserta una nueva subtarea de forma recursiva desde la raíz.

        :param id_subtarea: Identificador de la nueva subtarea.
        :param id_padre: Identificador de la tarea padre.
        :param descripcion: Descripción de la subtarea.
        :param completada: Estado inicial de la subtarea.
        :return: True si se agregó correctamente, False en caso contrario.
        """

        return self.raiz.agregar_subtarea(
            id_padre,
            id_subtarea,
            descripcion,
            completada
        )

    def buscar_nodo(self, id_subtarea: int):
        """
        Busca un nodo dentro del árbol según su ID.

        :param id_subtarea: Identificador del nodo que se desea buscar.
        :return: Nodo encontrado o None si no existe.
        """

        return self.raiz.buscar_nodo(id_subtarea)

    def obtener_todas(self) -> list:
        """
        Obtiene todas las tareas almacenadas en el árbol.

        :return: Lista con la información de todas las tareas.
        """

        return self.raiz.obtener_todas() if self.raiz else []