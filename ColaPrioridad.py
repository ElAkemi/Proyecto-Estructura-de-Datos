"""
ColaPrioridad.py

Implementación de una Cola de Prioridad (Priority Queue) construida
desde cero con nodos enlazados, destinada a la gestión de tareas
urgentes dentro del proyecto Workflow Manager (sistema XDE).

Diseño:
    - No se utilizan colecciones integradas de Python (list, heapq,
      queue.PriorityQueue, etc.). La estructura se implementa mediante
      una lista enlazada simple cuyos nodos (`_NodoPrioridad`) se
      mantienen siempre ORDENADOS por nivel de prioridad en el momento
      de la inserción (inserción ordenada mediante punteros), de modo
      que la cabeza de la lista siempre referencia a la tarea más
      urgente pendiente.
    - Niveles de prioridad soportados (de mayor a menor urgencia):
          1. Alta  -> se procesa primero
          2. Media
          3. Baja  -> se procesa al final
      Cada nivel se traduce internamente a un "peso" numérico
      (0, 1, 2 respectivamente) que determina el orden de la lista.
    - Entre tareas con el mismo nivel de prioridad se conserva el
      orden de llegada (comportamiento FIFO estable), evitando así
      que una tarea "Alta" recién insertada adelante a otra "Alta"
      que ya esperaba en la cola.
    - Se reutiliza la excepción `ColaVaciaError`, definida en
      `ColaFIFO.py`, para que el módulo `Program.py` pueda manejar de
      forma uniforme los errores de "cola vacía", sin importar si
      trabaja con la ColaFIFO (tareas normales) o con la ColaPrioridad
      (tareas urgentes).

Autor: Workflow Manager Team
"""

from __future__ import annotations
from typing import Any, Optional, Tuple

from ColaFIFO import ColaVaciaError


# Niveles de prioridad soportados por el sistema XDE, expuestos como
# constantes para evitar el uso de "cadenas mágicas" en Program.py.
PRIORIDAD_ALTA = "Alta"
PRIORIDAD_MEDIA = "Media"
PRIORIDAD_BAJA = "Baja"

# Mapeo interno de cada nivel de prioridad a un peso numérico.
# A menor peso, mayor urgencia (0 = más urgente, se atiende primero).
_PESOS_PRIORIDAD = {
    PRIORIDAD_ALTA: 0,
    PRIORIDAD_MEDIA: 1,
    PRIORIDAD_BAJA: 2,
}


class _NodoPrioridad:
    """
    Nodo interno utilizado por ColaPrioridad para construir la lista
    enlazada simple, ordenada por prioridad, que sostiene las tareas
    urgentes en memoria dinámica.

    No está pensado para ser instanciado ni utilizado fuera de este
    módulo, de ahí el prefijo con guion bajo (convención de "privado"
    en Python).
    """

    __slots__ = ("tarea", "prioridad", "peso", "siguiente")

    def __init__(self, tarea: Any, prioridad: str, peso: int) -> None:
        self.tarea: Any = tarea
        self.prioridad: str = prioridad
        self.peso: int = peso
        self.siguiente: Optional["_NodoPrioridad"] = None


class ColaPrioridad:

    def __init__(self) -> None:
        self._cabeza: Optional[_NodoPrioridad] = None
        self._tamano: int = 0

    @staticmethod
    def _normalizar_prioridad(prioridad: str) -> Tuple[str, int]:
        """
        Valida y normaliza el nivel de prioridad recibido, devolviendo
        una tupla (nombre_normalizado, peso_numerico).

        Args:
            prioridad: nivel de prioridad como texto. Se acepta en
                cualquier combinación de mayúsculas/minúsculas
                (por ejemplo "alta", "ALTA" o "Alta").

        Raises:
            ValueError: si la prioridad no es un texto o no corresponde
                a ninguno de los niveles soportados (Alta, Media, Baja).
        """
        if not isinstance(prioridad, str) or not prioridad.strip():
            raise ValueError(
                "La prioridad debe ser un texto no vacío: 'Alta', 'Media' o 'Baja'."
            )

        prioridad_normalizada = prioridad.strip().capitalize()

        if prioridad_normalizada not in _PESOS_PRIORIDAD:
            raise ValueError(
                f"Prioridad '{prioridad}' inválida. "
                f"Valores permitidos: {PRIORIDAD_ALTA}, {PRIORIDAD_MEDIA}, {PRIORIDAD_BAJA}."
            )

        return prioridad_normalizada, _PESOS_PRIORIDAD[prioridad_normalizada]

    def insertar_con_prioridad(self, tarea: Any, prioridad: str) -> None:
        """
        Inserta una tarea urgente en la cola, ubicándola en la posición
        que le corresponde según su nivel de prioridad (Alta, Media o
        Baja), de modo que la lista se mantenga siempre ordenada de
        mayor a menor urgencia.

        Entre tareas con el mismo nivel de prioridad se respeta el
        orden de llegada (FIFO estable): la nueva tarea se inserta
        después de todas las que ya tengan el mismo peso.

        Args:
            tarea: elemento a insertar. Puede ser cualquier objeto
                (dict, str, una instancia de una clase Tarea, etc.).
            prioridad: nivel de urgencia de la tarea. Debe ser uno de
                'Alta', 'Media' o 'Baja' (sin distinción de mayúsculas).

        Raises:
            ValueError: si `tarea` es None o si `prioridad` no es un
                nivel de prioridad válido.
        """
        if tarea is None:
            raise ValueError("No se puede insertar una tarea con valor None.")

        prioridad_normalizada, peso = self._normalizar_prioridad(prioridad)
        nuevo_nodo = _NodoPrioridad(tarea, prioridad_normalizada, peso)

        # Caso 1: cola vacía o la nueva tarea es más urgente que la cabeza.
        if self._cabeza is None or peso < self._cabeza.peso:
            nuevo_nodo.siguiente = self._cabeza
            self._cabeza = nuevo_nodo
            self._tamano += 1
            return

        # Caso 2: se recorre la lista hasta encontrar el punto de
        # inserción, es decir, el último nodo cuyo peso sea menor o
        # igual al de la nueva tarea (para mantener el FIFO estable
        # entre tareas de igual prioridad).
        actual = self._cabeza
        while actual.siguiente is not None and actual.siguiente.peso <= peso:
            actual = actual.siguiente

        nuevo_nodo.siguiente = actual.siguiente
        actual.siguiente = nuevo_nodo
        self._tamano += 1

    def extraer_urgente(self) -> Any:
        """
        Extrae y retorna la tarea más urgente de la cola, es decir,
        la que se encuentra a la cabeza de la lista enlazada (mayor
        prioridad y, en caso de empate, la más antigua).

        Returns:
            La tarea más urgente actualmente en la cola.

        Raises:
            ColaVaciaError: si la cola no contiene elementos.
        """
        if self.esta_vacia():
            raise ColaVaciaError(
                "No es posible extraer: la cola de prioridad está vacía."
            )

        nodo_cabeza = self._cabeza
        self._cabeza = nodo_cabeza.siguiente
        self._tamano -= 1

        # Se libera explícitamente la referencia al siguiente nodo para
        # facilitar la recolección de basura del nodo extraído.
        nodo_cabeza.siguiente = None

        return nodo_cabeza.tarea

    def obtener_siguiente(self) -> Any:
        """
        Retorna la tarea más urgente de la cola sin removerla, es
        decir, consulta la cabeza de la lista enlazada.

        Returns:
            La tarea más urgente actualmente en la cola.

        Raises:
            ColaVaciaError: si la cola no contiene elementos.
        """
        if self.esta_vacia():
            raise ColaVaciaError(
                "No es posible consultar: la cola de prioridad está vacía."
            )

        return self._cabeza.tarea

    def esta_vacia(self) -> bool:
        """
        Indica si la cola de prioridad no tiene elementos.

        Returns:
            True si la cola está vacía, False en caso contrario.
        """
        return self._cabeza is None

    def tamano(self) -> int:
        """
        Retorna la cantidad de tareas urgentes actualmente almacenadas
        en la cola.

        Returns:
            Número entero de elementos en la cola.
        """
        return self._tamano

    def __len__(self) -> int:
        return self._tamano

    def __str__(self) -> str:
        elementos = []
        nodo_actual = self._cabeza
        while nodo_actual is not None:
            elementos.append(f"[{nodo_actual.prioridad}] {nodo_actual.tarea}")
            nodo_actual = nodo_actual.siguiente
        return "ColaPrioridad([" + " -> ".join(elementos) + "])"

    def __repr__(self) -> str:
        return self.__str__()


if __name__ == "__main__":
    # Auto-prueba rápida para validar el comportamiento de la ColaPrioridad.
    cola = ColaPrioridad()

    print("¿Está vacía al inicio?", cola.esta_vacia())

    cola.insertar_con_prioridad("Tarea A: Corregir bug en login", PRIORIDAD_MEDIA)
    cola.insertar_con_prioridad("Tarea B: Servidor caído", PRIORIDAD_ALTA)
    cola.insertar_con_prioridad("Tarea C: Actualizar changelog", PRIORIDAD_BAJA)
    cola.insertar_con_prioridad("Tarea D: Fuga de datos detectada", "alta")
    cola.insertar_con_prioridad("Tarea E: Revisar métricas", "media")

    print("Estado de la cola:", cola)
    print("Cantidad de tareas:", len(cola))
    print("Siguiente tarea a atender (sin remover):", cola.obtener_siguiente())

    print("Extraída:", cola.extraer_urgente())
    print("Extraída:", cola.extraer_urgente())
    print("Estado de la cola:", cola)

    print("Extraída:", cola.extraer_urgente())
    print("Extraída:", cola.extraer_urgente())
    print("Extraída:", cola.extraer_urgente())

    print("¿Está vacía al final?", cola.esta_vacia())

    try:
        cola.extraer_urgente()
    except ColaVaciaError as error:
        print("Excepción capturada correctamente:", error)

    try:
        cola.obtener_siguiente()
    except ColaVaciaError as error:
        print("Excepción capturada correctamente:", error)

    try:
        cola.insertar_con_prioridad("Tarea inválida", "Urgentísima")
    except ValueError as error:
        print("Excepción capturada correctamente:", error)

    try:
        cola.insertar_con_prioridad(None, PRIORIDAD_ALTA)
    except ValueError as error:
        print("Excepción capturada correctamente:", error)
