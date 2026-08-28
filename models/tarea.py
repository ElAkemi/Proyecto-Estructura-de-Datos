from models.prioridad import Prioridad


class Tarea:
    """Representa una tarea del Workflow Manager."""

    ESTADOS_VALIDOS = (
        "Pendiente",
        "En ejecución",
        "Completada",
        "Cancelada",
    )

    def __init__(
        self,
        id,
        prioridad,
        responsable_id,
        descripcion,
        estado="Pendiente",
        padre_id=None,
        ciclos_espera=0,
    ):
        if not isinstance(id, int) or id <= 0:
            raise ValueError(
                "El ID de la tarea debe ser un entero positivo."
            )

        if not isinstance(responsable_id, int) or responsable_id <= 0:
            raise ValueError(
                "El responsable debe tener un ID válido."
            )

        if not isinstance(descripcion, str) or not descripcion.strip():
            raise ValueError(
                "La descripción no puede estar vacía."
            )

        if estado not in self.ESTADOS_VALIDOS:
            raise ValueError("Estado inválido.")

        self.id = id
        self.prioridad = Prioridad.desde_texto(prioridad)
        self.responsable_id = responsable_id
        self.descripcion = descripcion.strip()
        self.estado = estado
        self.padre_id = padre_id
        self.ciclos_espera = max(0, int(ciclos_espera))

    def copiar(self):
        """Devuelve una copia independiente de la tarea."""
        return Tarea(
            self.id,
            self.prioridad,
            self.responsable_id,
            self.descripcion,
            self.estado,
            self.padre_id,
            self.ciclos_espera,
        )

    def __repr__(self):
        return (
            f"Tarea("
            f"id={self.id}, "
            f"prioridad={self.prioridad.name}, "
            f"responsable={self.responsable_id}, "
            f"estado='{self.estado}'"
            f")"
        )