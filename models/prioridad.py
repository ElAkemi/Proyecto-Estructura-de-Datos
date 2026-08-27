"""Definición de Prioridad."""

from enum import Enum


class Prioridad(Enum):
    """Clase que representa la prioridad de una tarea."""

    BAJA = 1
    MEDIA = 2
    ALTA = 3

    @classmethod
    def desde_texto(cls, texto: str):
        """
        Crea una instancia de Prioridad a partir de un texto.

        :param texto: Texto que representa el nivel de prioridad.
        :return: Valor correspondiente del Enum Prioridad.
        :raises ValueError: Si la prioridad proporcionada no es válida.
        """

        if isinstance(texto, cls):
            return texto

        mapping = {
            "BAJA": cls.BAJA,
            "MEDIA": cls.MEDIA,
            "ALTA": cls.ALTA,
            "NORMAL": cls.MEDIA
        }

        texto_normalizado = str(texto).upper().strip()

        if texto_normalizado not in mapping:
            raise ValueError(
                "La prioridad debe ser BAJA, MEDIA o ALTA."
            )

        return mapping[texto_normalizado]

    def __str__(self):
        """
        Devuelve el nombre de la prioridad.

        :return: Nombre de la prioridad como texto.
        """

        return self.name