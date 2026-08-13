"""
Nombre: ColaFIFO
Autor: Valeria Cordero Murillo
"""

from __future__ import annotations
from typing import Any, Optional


class ColaVaciaError(Exception):

    def __init__(self, mensaje: str = "La cola de tareas está vacía.") -> None:
        self.mensaje = mensaje
        super().__init__(self.mensaje)


class _NodoTarea:


    __slots__ = ("tarea", "siguiente")

    def __init__(self, tarea: Any) -> None:
        self.tarea: Any = tarea
        self.siguiente: Optional["_NodoTarea"] = None


class ColaFIFO:


    def __init__(self) -> None:
        self._frente: Optional[_NodoTarea] = None
        self._final: Optional[_NodoTarea] = None
        self._tamano: int = 0

    def encolar(self, tarea: Any) -> None:
        if tarea is None:
            raise ValueError("No se puede encolar una tarea con valor None.")

        nuevo_nodo = _NodoTarea(tarea)

        if self.esta_vacia():
            # La cola no tiene elementos: el nuevo nodo es frente y final.
            self._frente = nuevo_nodo
            self._final = nuevo_nodo
        else:
            # Se enlaza el nuevo nodo al final actual y se actualiza el final.
            self._final.siguiente = nuevo_nodo
            self._final = nuevo_nodo

        self._tamano += 1

    def desencolar(self) -> Any:

        if self.esta_vacia():
            raise ColaVaciaError(
                "No es posible desencolar: la cola de tareas está vacía."
            )

        nodo_frente = self._frente
        self._frente = nodo_frente.siguiente

        # Si tras remover el frente la cola quedó vacía, el final
        # también debe quedar en None para mantener el estado consistente.
        if self._frente is None:
            self._final = None

        self._tamano -= 1

        # Se libera explícitamente la referencia al siguiente nodo para
        # facilitar la recolección de basura del nodo extraído.
        nodo_frente.siguiente = None

        return nodo_frente.tarea

    def frente(self) -> Any:
        if self.esta_vacia():
            raise ColaVaciaError(
                "No es posible consultar el frente: la cola de tareas está vacía."
            )

        return self._frente.tarea

    def esta_vacia(self) -> bool:
        return self._frente is None

    def tamano(self) -> int:
        return self._tamano

    def __len__(self) -> int:
        return self._tamano

    def __str__(self) -> str:
        elementos = []
        nodo_actual = self._frente
        while nodo_actual is not None:
            elementos.append(str(nodo_actual.tarea))
            nodo_actual = nodo_actual.siguiente
        return "ColaFIFO([" + " -> ".join(elementos) + "])"

    def __repr__(self) -> str:
        return self.__str__()


if __name__ == "__main__":
    # Auto-prueba rápida para validar el comportamiento de la ColaFIFO.
    cola = ColaFIFO()

    print("¿Está vacía al inicio?", cola.esta_vacia())

    cola.encolar("Tarea 1: Revisar backlog")
    cola.encolar("Tarea 2: Actualizar documentación")
    cola.encolar("Tarea 3: Desplegar a producción")

    print("Estado de la cola:", cola)
    print("Cantidad de tareas:", len(cola))
    print("Tarea al frente (sin remover):", cola.frente())

    print("Desencolando:", cola.desencolar())
    print("Estado de la cola:", cola)

    print("Desencolando:", cola.desencolar())
    print("Desencolando:", cola.desencolar())

    print("¿Está vacía al final?", cola.esta_vacia())

    try:
        cola.desencolar()
    except ColaVaciaError as error:
        print("Excepción capturada correctamente:", error)

    try:
        cola.frente()
    except ColaVaciaError as error:
        print("Excepción capturada correctamente:", error)

    try:
        cola.encolar(None)
    except ValueError as error:
        print("Excepción capturada correctamente:", error)
