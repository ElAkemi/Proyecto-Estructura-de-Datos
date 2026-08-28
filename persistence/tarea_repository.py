import csv
import os

from models.tarea import Tarea


class TareaRepository:
    """Gestiona la persistencia de tareas mediante CSV."""

    ENCABEZADOS = [
        "id",
        "prioridad",
        "responsable_id",
        "descripcion",
        "estado",
        "padre_id",
        "ciclos_espera",
    ]

    def __init__(self, ruta="data/tareas.csv"):
        self.ruta = ruta
        self._asegurar_archivo()

    def _asegurar_archivo(self):
        """Crea el directorio y archivo si no existen."""

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

    def guardar(self, tareas):
        """
        Sobrescribe el archivo con todas las tareas actuales.

        Args:
            tareas: iterable de objetos Tarea.
        """

        self._asegurar_archivo()

        with open(
            self.ruta,
            "w",
            newline="",
            encoding="utf-8"
        ) as archivo:

            escritor = csv.writer(archivo)

            escritor.writerow(self.ENCABEZADOS)

            for tarea in tareas:

                padre_id = (
                    ""
                    if tarea.padre_id is None
                    else tarea.padre_id
                )

                escritor.writerow([
                    tarea.id,
                    tarea.prioridad.name,
                    tarea.responsable_id,
                    tarea.descripcion,
                    tarea.estado,
                    padre_id,
                    tarea.ciclos_espera,
                ])

    def cargar(self):
        """
        Carga todas las tareas almacenadas.

        Retorna:
            Lista de objetos Tarea.
        """

        self._asegurar_archivo()

        tareas = []

        with open(
            self.ruta,
            "r",
            newline="",
            encoding="utf-8"
        ) as archivo:

            lector = csv.DictReader(archivo)

            for fila in lector:

                if not fila.get("id"):
                    continue

                try:
                    padre_id = fila.get("padre_id")

                    if padre_id in ("", None):
                        padre_id = None
                    else:
                        padre_id = int(padre_id)

                    ciclos = fila.get(
                        "ciclos_espera",
                        "0"
                    )

                    tarea = Tarea(
                        id=int(fila["id"]),
                        prioridad=fila["prioridad"],
                        responsable_id=int(
                            fila["responsable_id"]
                        ),
                        descripcion=fila["descripcion"],
                        estado=fila.get(
                            "estado",
                            "Pendiente"
                        ),
                        padre_id=padre_id,
                        ciclos_espera=int(ciclos),
                    )

                    tareas.append(tarea)

                except (ValueError, KeyError):
                    # Si existe una fila corrupta,
                    # se ignora y se continúa con las demás.
                    continue

        return tareas

    def obtener_por_id(self, id_tarea):
        """
        Busca una tarea por ID.

        Retorna:
            Tarea o None.
        """

        tareas = self.cargar()

        for tarea in tareas:

            if tarea.id == id_tarea:
                return tarea

        return None