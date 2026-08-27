"""Definición de Nodo del Árbol de Subtareas."""


class NodoArbolTarea:
    """Representa un nodo dentro del árbol de subtareas."""

    def __init__(
        self,
        id_subtarea: int,
        descripcion: str,
        id_padre: int = None,
        completada: bool = False
    ):
        """
        Inicializa un nodo del árbol con sus atributos.

        :param id_subtarea: Identificador único de la subtarea.
        :param descripcion: Descripción de la subtarea.
        :param id_padre: Identificador del nodo padre.
        :param completada: Indica si la subtarea está completada.
        """
        self.id_subtarea = int(id_subtarea)
        self.descripcion = str(descripcion)
        self.id_padre = int(id_padre) if id_padre is not None else None
        self.completada = bool(completada)
        self.subtareas = []  # Lista de hijos en el árbol general

    def agregar_subtarea(
        self,
        id_padre: int,
        id_subtarea: int,
        descripcion: str,
        completada: bool = False
    ) -> bool:
        """
        Busca recursivamente el nodo padre y agrega una nueva subtarea.

        :param id_padre: ID del nodo al que se agregará la subtarea.
        :param id_subtarea: ID de la nueva subtarea.
        :param descripcion: Descripción de la nueva subtarea.
        :param completada: Estado inicial de la subtarea.
        :return: True si se agregó correctamente, False si no se encontró
                 el padre o existe un ID duplicado.
        """

        if self.id_subtarea == id_padre:
            # Evita IDs duplicados dentro del árbol.
            if self.buscar_nodo(id_subtarea) is not None:
                return False

            self.subtareas.append(
                NodoArbolTarea(
                    id_subtarea,
                    descripcion,
                    id_padre,
                    completada
                )
            )
            return True

        for hijo in self.subtareas:
            if hijo.agregar_subtarea(
                id_padre,
                id_subtarea,
                descripcion,
                completada
            ):
                return True

        return False

    def buscar_nodo(self, id_subtarea: int):
        """
        Busca recursivamente un nodo por su ID.

        :param id_subtarea: ID del nodo que se desea buscar.
        :return: El nodo encontrado o None si no existe.
        """

        if self.id_subtarea == id_subtarea:
            return self

        for hijo in self.subtareas:
            encontrado = hijo.buscar_nodo(id_subtarea)

            if encontrado:
                return encontrado

        return None

    def obtener_todas(self) -> list:
        """
        Recorre recursivamente el árbol y obtiene todas las subtareas.

        :return: Lista de tuplas con ID, descripción, estado e ID del padre.
        """

        resultado = [
            (
                self.id_subtarea,
                self.descripcion,
                self.completada,
                self.id_padre
            )
        ]

        for hijo in self.subtareas:
            resultado.extend(hijo.obtener_todas())

        return resultado

    def __repr__(self):
        """
        Genera una representación textual del nodo.

        :return: Cadena con la información principal del nodo.
        """

        estado = "Completada" if self.completada else "Pendiente"

        return (
            f"NodoArbolTarea("
            f"ID={self.id_subtarea}, "
            f"Desc='{self.descripcion}', "
            f"Estado={estado}, "
            f"Subtareas={len(self.subtareas)})"
        )