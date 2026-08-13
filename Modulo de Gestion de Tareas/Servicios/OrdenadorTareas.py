"""
Nombre: OrdenadorTareas
Autor: Valeria Cordero Murillo
"""
from __future__ import annotations
from typing import List, Any, TYPE_CHECKING

if TYPE_CHECKING:
    from Models.Tarea import Tarea
    from ArbolTareas import ArbolTareas
    from NodoArbol import NodoArbol

# Reutilizamos el mapeo de prioridades para mantener la consistencia.
# A menor peso, mayor urgencia (0 = Alta, 1 = Media, 2 = Baja).
from ColaPrioridad import _PESOS_PRIORIDAD, PRIORIDAD_ALTA, PRIORIDAD_MEDIA, PRIORIDAD_BAJA


def _heapify(arr: List[Tarea], n: int, i: int) -> None:
    """
    Convierte un subárbol con raíz en el índice `i` en un max-heap.
    `n` es el tamaño del heap.
    Convierte un subárbol con raíz en el índice `i` en un max-heap
    basado en el peso de la prioridad (a menor peso, mayor prioridad,
    por lo que en realidad se comporta como un min-heap).
    `n` es el tamaño del heap. `i` es el índice de la raíz del subárbol.
    """
    mayor = i  # Inicializa el mayor como la raíz
    # En lugar de 'mayor', usamos 'extremo_idx' para evitar confusión.
    # Buscamos el índice del elemento con el menor peso (mayor prioridad).
    extremo_idx = i
    izquierda = 2 * i + 1
    derecha = 2 * i + 2

    # Obtener pesos de prioridad para la comparación
    peso_mayor = _PESOS_PRIORIDAD.get(arr[mayor].prioridad, 99)
    peso_extremo = _PESOS_PRIORIDAD.get(arr[extremo_idx].prioridad, 99)

    # Si el hijo izquierdo existe y es mayor que la raíz
    # Si el hijo izquierdo existe y tiene mayor prioridad (menor peso) que la raíz
    if izquierda < n:
        peso_izquierda = _PESOS_PRIORIDAD.get(arr[izquierda].prioridad, 99)
        # En Heap Sort estándar se busca el máximo. Para ordenar de mayor a
        # menor prioridad (menor peso numérico), necesitamos un min-heap.
        if peso_izquierda < peso_mayor:
            mayor = izquierda
            peso_mayor = peso_izquierda
        if peso_izquierda < peso_extremo:
            extremo_idx = izquierda
            # Actualizamos el peso extremo para la siguiente comparación
            peso_extremo = peso_izquierda

    # Si el hijo derecho existe y es mayor que el hasta ahora mayor
    # Si el hijo derecho existe y tiene mayor prioridad (menor peso) que el extremo actual
    if derecha < n:
        peso_derecha = _PESOS_PRIORIDAD.get(arr[derecha].prioridad, 99)
        if peso_derecha < peso_mayor:
            mayor = derecha
        if peso_derecha < peso_extremo:
            extremo_idx = derecha

    # Si el mayor no es la raíz, intercambiarlos y continuar heapify
    if mayor != i:
        arr[i], arr[mayor] = arr[mayor], arr[i]
        _heapify(arr, n, mayor)
    # Si el nodo con mayor prioridad no es la raíz, intercambiarlos y
    # continuar aplicando heapify recursivamente en el subárbol afectado.
    if extremo_idx != i:
        arr[i], arr[extremo_idx] = arr[extremo_idx], arr[i]
        _heapify(arr, n, extremo_idx)


def heap_sort_tareas(tareas: List[Tarea]) -> None:
    """
    Ordena una lista de objetos Tarea en su lugar (in-place) utilizando
    el algoritmo Heap Sort, basado en la prioridad de las tareas.
    Las tareas de mayor prioridad (ej. 'Alta') aparecerán primero.
    Las tareas de mayor prioridad (ej. 'Alta') aparecerán al inicio de la lista.

    Args:
        tareas: Una lista de objetos Tarea a ordenar.
    """
    n = len(tareas)

    # 1. Construir un min-heap. El rango va desde el último nodo no-hoja
    #    hacia atrás hasta la raíz.
    # 1. Construir un "min-heap" (basado en el peso)
    for i in range(n // 2 - 1, -1, -1):
        _heapify(tareas, n, i)

    # 2. Extraer elementos uno por uno del heap.
    for i in range(n - 1, 0, -1):
        # Mover la raíz actual (el elemento de menor peso/mayor prioridad)
        # al final del array ordenado.
        # Mover la raíz actual (tarea de mayor prioridad) al final de la
        # porción no ordenada de la lista.
        tareas[i], tareas[0] = tareas[0], tareas[i]
        # Llamar a heapify en el heap reducido.
        # Reconstruir el heap en el rango reducido.
        _heapify(tareas, i, 0)
    tareas.reverse()


def extraer_tareas_del_arbol(arbol: ArbolTareas) -> List[Tarea]:
    """
    Recorre un ArbolTareas y extrae todas las tareas a una lista plana.

    Args:
        arbol: La instancia de ArbolTareas de donde se extraerán las tareas.

    Returns:
        Una lista con todos los objetos Tarea contenidos en el árbol.
    """
    lista_tareas = []

    def _recorrer(nodo: NodoArbol):
        if nodo:
            lista_tareas.append(nodo.tarea)
            for hijo in nodo.hijos:
                _recorrer(hijo)

    # El nodo raíz se accede a través del atributo _raiz
    if hasattr(arbol, '_raiz'):
        _recorrer(arbol._raiz)

    return lista_tareas
