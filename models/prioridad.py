from enum import IntEnum


class Prioridad(IntEnum):
    """Niveles de prioridad de las tareas."""

    BAJA = 1
    MEDIA = 2
    ALTA = 3
    URGENTE = 4

    @classmethod
    def desde_texto(cls, valor):
        """Convierte un texto o número en una prioridad válida."""

        texto = str(valor).strip().upper()

        equivalencias = {
            "1": cls.BAJA,
            "2": cls.MEDIA,
            "3": cls.ALTA,
            "4": cls.URGENTE,
        }

        if texto in equivalencias:
            return equivalencias[texto]

        try:
            return cls[texto]
        except KeyError as exc:
            raise ValueError(
                "Prioridad inválida. "
                "Use BAJA, MEDIA, ALTA o URGENTE."
            ) from exc

    def __str__(self):
        return self.name