import csv
import os
from datetime import datetime


class AuditoriaService:
    """
    Gestiona la bitácora inmutable del sistema.

    El archivo solamente recibe nuevas líneas.
    Nunca se sobrescribe ni se eliminan registros.
    """

    ENCABEZADOS = [
        "fecha_hora",
        "usuario_id",
        "accion",
        "tarea_id",
    ]

    def __init__(self, ruta="data/auditoria_log.csv"):
        self.ruta = ruta
        self._asegurar_archivo()

    def _asegurar_archivo(self):
        """Crea el archivo de auditoría si no existe."""

        directorio = os.path.dirname(self.ruta)

        if directorio:
            os.makedirs(directorio, exist_ok=True)

        if not os.path.exists(self.ruta):
            with open(
                self.ruta,
                "w",
                newline="",
                encoding="utf-8"
            ) as archivo:

                escritor = csv.writer(archivo)
                escritor.writerow(self.ENCABEZADOS)

    def registrar(
        self,
        usuario_id,
        accion,
        tarea_id=None
    ):
        """
        Agrega un nuevo registro a la bitácora.

        El archivo se abre en modo append ('a'), por lo que
        los registros anteriores nunca son modificados.
        """

        fecha_hora = datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )

        with open(
            self.ruta,
            "a",
            newline="",
            encoding="utf-8"
        ) as archivo:

            escritor = csv.writer(archivo)

            escritor.writerow([
                fecha_hora,
                usuario_id,
                accion,
                "" if tarea_id is None else tarea_id,
            ])

   
    def listar(self):
        """Devuelve todas las líneas de la bitácora de auditoría."""

        try:
            with open(
                self.ruta,
                "r",
                encoding="utf-8"
            ) as archivo:

                lector = csv.reader(
                    archivo,
                    delimiter=","
                )

                registros = []

                for fila in lector:
                    if not fila:
                        continue

                    registros.append(
                        " | ".join(campo.strip() for campo in fila)
                    )

                return registros

        except FileNotFoundError:
            return []

