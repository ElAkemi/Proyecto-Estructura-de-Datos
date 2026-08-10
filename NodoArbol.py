"""
Nombre: ColaFIFO
Autor: Valeria Cordero Murillo
"""

from __future__ import annotations
from typing import Any
from Tarea import Tarea, ESTADO_EN_PROCESO, ESTADO_HECHA


class DependenciaNoResueltaError(Exception):
    def __init__(self, mensaje: str):
        super().__init__(mensaje)


class NodoArbol:
    __slots__ = ("tarea", "hijos")

    def __init__(self, tarea: Tarea):
        if not isinstance(tarea, Tarea):
            raise TypeError("El nodo debe ser inicializado con un objeto de clase Tarea.")
        self.tarea: Tarea = tarea
        self.hijos: list[NodoArbol] = []

    @property
    def id(self) -> Any:
        return self.tarea.id

    def agregar_hijo(self, nodo_hijo: NodoArbol) -> None:
        self.hijos.append(nodo_hijo)

    def marcar_como_en_proceso(self) -> None:
        self.tarea.estado = ESTADO_EN_PROCESO
        print(f"INFO: Tarea '{self.id}' marcada como '{ESTADO_EN_PROCESO}'.")

    def puede_completarse(self) -> bool:
        return all(hijo.tarea.estado == ESTADO_HECHA for hijo in self.hijos)

    def marcar_como_hecha(self) -> None:
        if not self.puede_completarse():
            subtareas_pendientes = [h.id for h in self.hijos if h.tarea.estado != ESTADO_HECHA]
            raise DependenciaNoResueltaError(
                f"No se puede completar la tarea '{self.id}'. "
                f"Subtareas pendientes: {subtareas_pendientes}"
            )

        self.tarea.estado = ESTADO_HECHA
        print(f"INFO: Tarea '{self.id}' marcada como '{ESTADO_HECHA}'.")

    def __repr__(self) -> str:
        return f"<NodoArbol id='{self.id}' estado='{self.tarea.estado}'>"