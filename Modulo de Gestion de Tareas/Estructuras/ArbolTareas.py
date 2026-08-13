"""
Nombre: ArbolTareas
Autor: Valeria Cordero Murillo
"""

from __future__ import annotations
from typing import Any, Optional

from NodoArbol import NodoArbol, DependenciaNoResueltaError
from Models.Tarea import Tarea, ESTADO_HECHA


class ArbolTareas:
    def __init__(self, tarea_raiz: Any):
        if not isinstance(tarea_raiz, Tarea):
            raise TypeError("La tarea raíz debe ser una instancia de la clase Tarea.")
        self._raiz: NodoArbol = NodoArbol(tarea_raiz)

    @property
    def raiz(self) -> Any:
        """Retorna la tarea raíz del árbol."""
        return self._raiz.tarea

    def _buscar_recursivo(
        self,
        nodo_actual: Optional[NodoArbol],
        id_tarea: Any
    ) -> Optional[NodoArbol]:
        # Caso base 1: El nodo actual es nulo, la rama se agotó.
        if nodo_actual is None:
            return None

        # Caso base 2: El ID del nodo actual coincide con el buscado.
        if nodo_actual.id == id_tarea:
            return nodo_actual

        # Paso recursivo: Buscar en los hijos.
        for hijo in nodo_actual.hijos:
            nodo_encontrado = self._buscar_recursivo(hijo, id_tarea)
            if nodo_encontrado:
                return nodo_encontrado

        # Si no se encontró en ninguna rama de los hijos.
        return None

    def buscar_nodo(self, id_tarea: Any) -> Optional[NodoArbol]:
        return self._buscar_recursivo(self._raiz, id_tarea)

    def buscar_tarea(self, id_tarea: Any) -> Optional[Any]:
        """
        Busca los datos de una tarea por su ID.

        Returns:
            El objeto de la tarea si se encuentra, o None si no existe.
        """
        nodo_encontrado = self.buscar_nodo(id_tarea)
        return nodo_encontrado.tarea if nodo_encontrado else None

    def _agregar_recursivo(
        self,
        nodo_actual: NodoArbol,
        id_padre: Any,
        nueva_subtarea: Any
    ) -> bool:
        # Si el nodo actual es el padre, agregar la nueva subtarea como hijo.
        if nodo_actual.id == id_padre:
            if nodo_actual.tarea.estado == ESTADO_HECHA:
                raise ValueError(
                    f"No se puede agregar una subtarea a una tarea ya completada ('{id_padre}')."
                )
            nodo_actual.agregar_hijo(NodoArbol(nueva_subtarea))
            return True

        # Continuar la búsqueda en los hijos.
        for hijo in nodo_actual.hijos:
            if self._agregar_recursivo(hijo, id_padre, nueva_subtarea):
                return True

        return False

    def agregar_subtarea(self, id_padre: Any, nueva_subtarea: Any) -> None:
        if not isinstance(nueva_subtarea, Tarea):
            raise TypeError("La nueva subtarea debe ser una instancia de la clase Tarea.")

        id_nueva_tarea = nueva_subtarea.id
        if id_padre == id_nueva_tarea:
            raise ValueError("Una tarea no puede ser subtarea de sí misma (dependencia circular).")

        if self.buscar_tarea(id_nueva_tarea) is not None:
            raise ValueError(f"El ID de tarea '{id_nueva_tarea}' ya existe en el árbol.")

        if not self._agregar_recursivo(self._raiz, id_padre, nueva_subtarea):
            raise ValueError(f"No se encontró la tarea padre con ID '{id_padre}'.")

    def _eliminar_recursivo(self, nodo_actual: NodoArbol, id_tarea_a_eliminar: Any) -> bool:
        # Recorrer los hijos del nodo actual para encontrar el que se debe eliminar.
        for i, hijo in enumerate(nodo_actual.hijos):
            if hijo.id == id_tarea_a_eliminar:
                # Eliminar el hijo de la lista de hijos del padre.
                del nodo_actual.hijos[i]
                return True

            # Si no es el hijo, continuar la búsqueda recursivamente en el subárbol.
            if self._eliminar_recursivo(hijo, id_tarea_a_eliminar):
                return True

        return False

    def eliminar_subarbol(self, id_tarea: Any) -> None:
        """
        Elimina una tarea y todas sus subtareas descendientes del árbol.

        Args:
            id_tarea: El ID de la tarea que encabeza el subárbol a eliminar.

        Raises:
            ValueError: Si se intenta eliminar la tarea raíz o si la tarea
                        no se encuentra en el árbol.
        """
        if self._raiz.id == id_tarea:
            raise ValueError("No se puede eliminar la tarea raíz del árbol.")

        if not self._eliminar_recursivo(self._raiz, id_tarea):
            raise ValueError(f"No se encontró la tarea con ID '{id_tarea}' para eliminar.")

    def __str__(self) -> str:
        lineas = []

        def construir_str(nodo: NodoArbol, prefijo: str = "", es_ultimo: bool = True):
            conector = "└── " if es_ultimo else "├── "
            descripcion = nodo.tarea.descripcion
            lineas.append(f"{prefijo}{conector}[{nodo.tarea.estado}] {nodo.id}: {descripcion}")

            nuevo_prefijo = prefijo + ("    " if es_ultimo else "│   ")
            num_hijos = len(nodo.hijos)
            for i, hijo in enumerate(nodo.hijos):
                construir_str(hijo, nuevo_prefijo, i == num_hijos - 1)

        lineas.append(
            f"[{self._raiz.tarea.estado}] {self._raiz.id}: {self._raiz.tarea.descripcion}"
        )
        num_hijos_raiz = len(self._raiz.hijos)
        for i, hijo in enumerate(self._raiz.hijos):
            construir_str(hijo, "", i == num_hijos_raiz - 1)

        return "\n".join(lineas)


if __name__ == "__main__":
    from Models.Tarea import renderizar_kanban, PRIORIDAD_ALTA
    from OrdenadorTareas import heap_sort_tareas, extraer_tareas_del_arbol

    # Crear tarea raíz
    raiz = Tarea(
        id_tarea="proyecto_alpha",
        descripcion="Lanzamiento del sistema XDE",
        prioridad=PRIORIDAD_ALTA,
        asignado="Valeria Cordero"
    )
    arbol = ArbolTareas(raiz)

    print("Árbol inicial:")
    print(arbol)
    print("-" * 30)

    # Agregar subtareas
    arbol.agregar_subtarea(
        "proyecto_alpha",
        Tarea(id_tarea="fase_1", descripcion="Análisis de requisitos", asignado="Equipo A")
    )
    arbol.agregar_subtarea(
        "proyecto_alpha",
        Tarea(id_tarea="fase_2", descripcion="Desarrollo", asignado="Equipo B")
    )
    arbol.agregar_subtarea(
        "fase_2",
        Tarea(
            id_tarea="backend",
            descripcion="Implementar API REST",
            prioridad=PRIORIDAD_ALTA,
            asignado="Dev1"
        )
    )
    arbol.agregar_subtarea(
        "fase_2",
        Tarea(id_tarea="frontend", descripcion="Diseñar interfaz de usuario", asignado="UI/UX")
    )
    arbol.agregar_subtarea(
        "backend",
        Tarea(
            id_tarea="auth",
            descripcion="Módulo de autenticación",
            prioridad=PRIORIDAD_ALTA,
            asignado="Dev1"
        )
    )

    print("Árbol con subtareas:")
    print(arbol)
    print("-" * 30)

    # Buscar una tarea
    tarea_encontrada = arbol.buscar_tarea("backend")
    print(f"Buscando 'backend': {tarea_encontrada}")
    tarea_no_existente = arbol.buscar_tarea("inexistente")
    print(f"Buscando 'inexistente': {tarea_no_existente}")
    print("-" * 30)

    # --- Lógica de ejecución de tareas ---
    print("Ejecutando flujo de tareas...")

    try:
        nodo_fase_2 = arbol.buscar_nodo("fase_2")
        if nodo_fase_2:
            nodo_fase_2.marcar_como_hecha()
    except DependenciaNoResueltaError as e:
        print(f"Error esperado capturado: {e}")

    # Ejecutar tareas en el orden correcto
    n_fase_1 = arbol.buscar_nodo("fase_1")
    if n_fase_1:
        n_fase_1.marcar_como_hecha()

    n_frontend = arbol.buscar_nodo("frontend")
    if n_frontend:
        n_frontend.marcar_como_hecha()

    n_auth = arbol.buscar_nodo("auth")
    if n_auth:
        n_auth.marcar_como_hecha()

    n_backend = arbol.buscar_nodo("backend")
    if n_backend:
        n_backend.marcar_como_hecha()

    n_fase_2 = arbol.buscar_nodo("fase_2")
    if n_fase_2:
        n_fase_2.marcar_como_hecha()

    # Visualizar el estado final con el tablero Kanban
    print(renderizar_kanban(arbol))
    print("-" * 30)

    # Eliminar subárbol 'fase_1'
    print("Eliminando el subárbol 'fase_1'...")
    arbol.eliminar_subarbol("fase_1")
    print("\nÁrbol después de la eliminación:")
    print(arbol)
    print("-" * 30)

    # Validar errores
    try:
        arbol.agregar_subtarea("proyecto_alpha", Tarea(id_tarea="frontend", descripcion="Tarea duplicada"))
    except ValueError as e:
        print(f"Error capturado correctamente: {e}")

    try:
        arbol.agregar_subtarea("fase_3", Tarea(id_tarea="nueva", descripcion="Padre no existe"))
    except ValueError as e:
        print(f"Error capturado correctamente: {e}")

    try:
        arbol.eliminar_subarbol("proyecto_alpha")
    except ValueError as e:
        print(f"Error capturado correctamente: {e}")

    print("-" * 30)
    print("Probando Heap Sort para ordenar tareas por prioridad...")

    todas_las_tareas = extraer_tareas_del_arbol(arbol)
    print("\nLista de tareas antes de ordenar:")
    print([f"'{t.descripcion}' (Prioridad: {t.prioridad})" for t in todas_las_tareas])

    heap_sort_tareas(todas_las_tareas)
    print("\nLista de tareas después de ordenar con Heap Sort (de mayor a menor prioridad):")
    print([f"'{t.descripcion}' (Prioridad: {t.prioridad})" for t in todas_las_tareas])