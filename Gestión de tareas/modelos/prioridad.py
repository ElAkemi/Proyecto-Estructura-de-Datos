"""Definición de Prioridad"""

from enum import Enum

class Prioridad(Enum):
    """Clase que representa la prioridad de una tarea."""

    BAJA = 1
    MEDIA = 2
    ALTA = 3
    """Método que crea una instancia de Prioridad a partir de un texto."""
    @classmethod
    def desde_texto(cls, texto: str):
        """Método que crea una instancia de Prioridad a partir de un texto."""
        if isinstance(texto, cls):
            return texto
        mapping = {
            "BAJA": cls.BAJA,
            "MEDIA": cls.MEDIA,
            "ALTA": cls.ALTA
        }
        return mapping.get(str(texto).upper().strip(), cls.BAJA)

    def __str__(self):
        """Representación de la prioridad en formato de cadena."""
        return self.name
        