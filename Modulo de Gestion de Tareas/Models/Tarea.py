"""
Nombre: Tarea
Autor: Valeria Cordero Murillo
"""

from __future__ import annotations
from typing import List, Dict, Any, TYPE_CHECKING

if TYPE_CHECKING:
    import ArbolTareas 

ESTADO_POR_HACER = "Por hacer"
ESTADO_EN_PROCESO = "En proceso"
ESTADO_HECHA = "Hecha"
ESTADOS_KANBAN = [ESTADO_POR_HACER, ESTADO_EN_PROCESO, ESTADO_HECHA]

PRIORIDAD_ALTA = "Alta"
PRIORIDAD_MEDIA = "Media"
PRIORIDAD_BAJA = "Baja"


class Tarea:
    __slots__ = ("id", "descripcion", "prioridad", "asignado", "estado")

    def __init__(
        self,
        id_tarea: Any,
        descripcion: str,
        prioridad: str = PRIORIDAD_MEDIA,
        asignado: str = "N/A"
    ):
        self.id: Any = id_tarea
        self.descripcion: str = descripcion
        self.prioridad: str = prioridad
        self.asignado: str = asignado
        self.estado: str = ESTADO_POR_HACER

    def __repr__(self) -> str:
        return f"Tarea(id={self.id}, desc='{self.descripcion}', estado='{self.estado}')"


def renderizar_kanban(arbol: Any) -> str:

    tareas_por_estado: Dict[str, List[str]] = {estado: [] for estado in ESTADOS_KANBAN}

    def _recorrer_y_formatear(nodo: Any, profundidad: int = 0):
        """Función interna recursiva para construir las líneas de texto."""
        prefijo = "    " * profundidad
        conector = "|-- " if profundidad > 0 else ""

        # Accedemos a la tarea a través del nodo
        tarea_actual: Tarea = nodo.tarea

        linea = (
            f"{prefijo}{conector}{tarea_actual.id}: "
            f"{tarea_actual.descripcion} [{tarea_actual.asignado}]"
        )

        # Agregamos la línea a la columna de estado correspondiente
        if tarea_actual.estado in tareas_por_estado:
            tareas_por_estado[tarea_actual.estado].append(linea)

        # Recursión sobre los hijos
        for hijo in nodo.hijos:
            _recorrer_y_formatear(hijo, profundidad + 1)

    # Iniciar el recorrido desde la raíz del árbol (usando propiedad pública o atributo)
    raiz = getattr(arbol, "raiz", getattr(arbol, "_raiz", None))
    if raiz:
        _recorrer_y_formatear(raiz)

    # Construir la salida final del tablero
    salida = ["=" * 80, "TABLERO KANBAN DE TAREAS".center(80), "=" * 80]

    for estado in ESTADOS_KANBAN:
        salida.append(f"\n--- {estado.upper()} ---\n")
        if tareas_por_estado[estado]:
            salida.extend(tareas_por_estado[estado])
        else:
            salida.append("(Ninguna tarea en este estado)")

    salida.append("\n" + "=" * 80)

    return "\n".join(salida)
