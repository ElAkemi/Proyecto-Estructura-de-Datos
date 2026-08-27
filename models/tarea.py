"""Módulo para la gestión de tareas."""

from models.prioridad import Prioridad


class Tarea:
    """Clase que representa una tarea dentro del sistema."""

    def __init__(
        self,
        id_tarea: int,
        descripcion: str,
        prioridad: Prioridad,
        id_usuario: int,
        estado: str = "Pendiente",
        ciclos_espera: int = 0
    ):
        """
        Inicializa una tarea con sus atributos.

        :param id_tarea: Identificador único de la tarea.
        :param descripcion: Descripción de la tarea.
        :param prioridad: Nivel de prioridad.
        :param id_usuario: ID del usuario responsable.
        :param estado: Estado actual de la tarea.
        :param ciclos_espera: Cantidad de ciclos de espera.
        """

        self.id_tarea = int(id_tarea)
        self.descripcion = str(descripcion)

        self.prioridad = (
            Prioridad.desde_texto(prioridad)
            if not isinstance(prioridad, Prioridad)
            else prioridad
        )

        self.id_usuario = int(id_usuario)

        self.estado = estado
        self.ciclos_espera = int(ciclos_espera)

    @property
    def estado(self):
        """
        Obtiene el estado actual de la tarea.

        :return: Estado de la tarea.
        """

        return self._estado

    @estado.setter
    def estado(self, valor):
        """
        Establece el estado de la tarea.

        :param valor: Nuevo estado.
        :return: None.
        :raises ValueError: Si el estado no es válido.
        """

        estados_validos = (
            "Pendiente",
            "En Proceso",
            "Finalizada"
        )

        if valor not in estados_validos:
            raise ValueError(
                "El estado debe ser Pendiente, En Proceso o Finalizada."
            )

        self._estado = valor

    def incrementar_ciclo_espera(self):
        """
        Incrementa el contador de ciclos de espera.

        :return: None.
        """

        self.ciclos_espera += 1

    def __repr__(self):
        """
        Genera una representación textual de la tarea.

        :return: Cadena con la información principal.
        """

        return (
            f"Tarea("
            f"ID={self.id_tarea}, "
            f"Prioridad={self.prioridad.name}, "
            f"Usuario={self.id_usuario}, "
            f"Estado={self.estado}, "
            f"Ciclos={self.ciclos_espera}, "
            f"Desc='{self.descripcion}')"
        )