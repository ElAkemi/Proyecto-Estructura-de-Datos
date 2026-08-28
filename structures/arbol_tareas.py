from structures.nodo_arbol import NodoArbol


class ArbolTareas:
    """
    Árbol general utilizado para representar
    tareas y sus subtareas.
    """

    def __init__(self):
        self.raices = []

    def agregar(self, tarea):
        """
        Agrega una tarea al árbol.

        Si no tiene padre, se agrega como raíz.
        Si tiene padre, se agrega como hijo de ese nodo.
        """

        nuevo_nodo = NodoArbol(tarea)

        # Tarea principal.
        if tarea.padre_id is None:
            self.raices.append(nuevo_nodo)
            return True

        # Buscar el padre.
        nodo_padre = self.buscar_nodo(tarea.padre_id)

        if nodo_padre is None:
            return False

        nodo_padre.hijos.append(nuevo_nodo)

        return True

    def buscar_nodo(self, tarea_id, nodos=None):
        """
        Busca un nodo utilizando RECURSIVIDAD.

        Este método recorre todos los niveles del árbol.
        """

        if nodos is None:
            nodos = self.raices

        for nodo in nodos:

            # Encontramos la tarea.
            if nodo.tarea.id == tarea_id:
                return nodo

            # Buscar recursivamente dentro de sus hijos.
            encontrado = self.buscar_nodo(
                tarea_id,
                nodo.hijos
            )

            if encontrado is not None:
                return encontrado

        return None

    def buscar(self, tarea_id):
        """Busca una tarea y devuelve el objeto Tarea."""

        nodo = self.buscar_nodo(tarea_id)

        if nodo is None:
            return None

        return nodo.tarea

    def listar_recursivo(self, nodos=None, nivel=0):
        """
        Recorre recursivamente todo el árbol.

        Devuelve tuplas:
            (nivel, tarea)

        Esto permite representar visualmente
        la jerarquía de subtareas.
        """

        if nodos is None:
            nodos = self.raices

        resultado = []

        for nodo in nodos:

            resultado.append(
                (nivel, nodo.tarea)
            )

            # Recorrido recursivo.
            resultado.extend(
                self.listar_recursivo(
                    nodo.hijos,
                    nivel + 1
                )
            )

        return resultado

    def eliminar(self, tarea_id, nodos=None):
        """
        Elimina una tarea del árbol utilizando recursividad.

        Si la tarea tiene subtareas, se elimina
        el subárbol completo.
        """

        if nodos is None:
            nodos = self.raices

        for indice, nodo in enumerate(nodos):

            if nodo.tarea.id == tarea_id:
                nodos.pop(indice)
                return True

            # Buscar recursivamente en los hijos.
            if self.eliminar(
                tarea_id,
                nodo.hijos
            ):
                return True

        return False

    def listar(self):
        """Devuelve todas las tareas mediante recorrido recursivo."""

        resultado = self.listar_recursivo()

        return [
            tarea
            for _, tarea in resultado
        ]

    def obtener_subtareas(self, tarea_id):
        """
        Devuelve directamente las subtareas de una tarea.
        """

        nodo = self.buscar_nodo(tarea_id)

        if nodo is None:
            return []

        return [
            hijo.tarea
            for hijo in nodo.hijos
        ]

    def mostrar_arbol(self):
        """
        Genera una representación textual del árbol.
        """

        resultado = []

        for nivel, tarea in self.listar_recursivo():

            sangria = "    " * nivel

            resultado.append(
                f"{sangria}- "
                f"[{tarea.id}] "
                f"{tarea.descripcion}"
            )

        return resultado

    def esta_vacio(self):
        """Indica si el árbol está vacío."""

        return len(self.raices) == 0