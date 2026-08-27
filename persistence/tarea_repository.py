"""Módulo encargado de la persistencia de tareas y subtareas en CSV."""

import csv
import os

from models.tarea import Tarea
from models.prioridad import Prioridad
from structures.nodo_arbol import NodoArbolTarea


class TareaRepository:
    """Gestiona la lectura y escritura de tareas y subtareas en CSV."""

    def __init__(self, archivo_csv="data/tareas.csv"):
        """Inicializa el repositorio de tareas."""

        self.archivo_csv = archivo_csv

    def guardar_tareas(
        self,
        tareas,
        arboles_subtareas=None
    ):
        """
        Guarda las tareas y sus subtareas en el archivo CSV.

        :param tareas: Lista de objetos Tarea.
        :param arboles_subtareas: Diccionario de árboles de subtareas.
        :return: None.
        """

        directorio = os.path.dirname(
            self.archivo_csv
        )

        if directorio:
            os.makedirs(
                directorio,
                exist_ok=True
            )

        if arboles_subtareas is None:
            arboles_subtareas = {}

        with open(
            self.archivo_csv,
            mode="w",
            newline="",
            encoding="utf-8"
        ) as archivo:

            writer = csv.writer(archivo)

            writer.writerow([
                "tipo",
                "id_tarea",
                "descripcion",
                "prioridad",
                "id_usuario",
                "estado",
                "ciclos_espera",
                "id_subtarea",
                "id_padre",
                "completada"
            ])

            for tarea in tareas:

                writer.writerow([
                    "TAREA",
                    tarea.id_tarea,
                    tarea.descripcion,
                    tarea.prioridad.name,
                    tarea.id_usuario,
                    tarea.estado,
                    tarea.ciclos_espera,
                    "",
                    "",
                    ""
                ])

                raiz = arboles_subtareas.get(
                    tarea.id_tarea
                )

                if raiz is not None:
                    self._guardar_subtareas(
                        writer,
                        raiz
                    )

    def _guardar_subtareas(
        self,
        writer,
        nodo
    ):
        """
        Guarda recursivamente todas las subtareas.

        :param writer: Escritor CSV.
        :param nodo: Nodo padre actual.
        :return: None.
        """

        for hijo in nodo.subtareas:

            writer.writerow([
                "SUBTAREA",
                "",
                hijo.descripcion,
                "",
                "",
                "",
                "",
                hijo.id_subtarea,
                hijo.id_padre,
                hijo.completada
            ])

            self._guardar_subtareas(
                writer,
                hijo
            )

    def cargar_tareas(self):
        """
        Carga las tareas y reconstruye los árboles de subtareas.

        :return:
            Tupla con:
            - lista de tareas
            - diccionario de árboles de subtareas
        """

        tareas = []
        arboles_subtareas = {}
        subtareas = []

        if not os.path.exists(
            self.archivo_csv
        ):
            return tareas, arboles_subtareas

        with open(
            self.archivo_csv,
            mode="r",
            newline="",
            encoding="utf-8"
        ) as archivo:

            reader = csv.DictReader(
                archivo
            )

            for fila in reader:

                try:

                    tipo = fila.get(
                        "tipo",
                        ""
                    ).strip().upper()

                    if tipo == "TAREA":

                        id_tarea = int(
                            fila["id_tarea"]
                        )

                        if any(
                            tarea.id_tarea == id_tarea
                            for tarea in tareas
                        ):
                            continue

                        tarea = Tarea(
                            id_tarea=id_tarea,
                            descripcion=fila[
                                "descripcion"
                            ],
                            prioridad=Prioridad.desde_texto(
                                fila["prioridad"]
                            ),
                            id_usuario=int(
                                fila["id_usuario"]
                            ),
                            estado=fila["estado"],
                            ciclos_espera=int(
                                fila.get(
                                    "ciclos_espera",
                                    0
                                )
                            )
                        )

                        tareas.append(
                            tarea
                        )

                        arboles_subtareas[
                            id_tarea
                        ] = NodoArbolTarea(
                            id_subtarea=id_tarea,
                            descripcion=tarea.descripcion,
                            id_padre=None,
                            completada=(
                                tarea.estado
                                == "Finalizada"
                            )
                        )

                    elif tipo == "SUBTAREA":

                        id_subtarea = int(
                            fila["id_subtarea"]
                        )

                        id_padre = int(
                            fila["id_padre"]
                        )

                        descripcion = fila.get(
                            "descripcion",
                            ""
                        ).strip()

                        if not descripcion:
                            descripcion = (
                                "Subtarea sin descripción"
                            )

                        completada = (
                            fila.get(
                                "completada",
                                "False"
                            ).strip().lower()
                            == "true"
                        )

                        subtareas.append({
                            "id_subtarea": id_subtarea,
                            "id_padre": id_padre,
                            "descripcion": descripcion,
                            "completada": completada
                        })

                except (
                    ValueError,
                    KeyError,
                    TypeError
                ):
                    continue

        pendientes = subtareas[:]

        while pendientes:

            progreso = False
            restantes = []

            for subtarea in pendientes:

                id_subtarea = subtarea[
                    "id_subtarea"
                ]

                id_padre = subtarea[
                    "id_padre"
                ]

                existe = False

                for raiz in arboles_subtareas.values():

                    if raiz.buscar_nodo(
                        id_subtarea
                    ) is not None:

                        existe = True
                        break

                if existe:
                    continue

                padre_encontrado = None

                for raiz in arboles_subtareas.values():

                    encontrado = raiz.buscar_nodo(
                        id_padre
                    )

                    if encontrado is not None:
                        padre_encontrado = encontrado
                        break

                if padre_encontrado is None:

                    restantes.append(
                        subtarea
                    )

                    continue

                nuevo_nodo = NodoArbolTarea(
                    id_subtarea=id_subtarea,
                    descripcion=subtarea[
                        "descripcion"
                    ],
                    id_padre=id_padre,
                    completada=subtarea[
                        "completada"
                    ]
                )

                padre_encontrado.subtareas.append(
                    nuevo_nodo
                )

                progreso = True

            if not progreso:
                break

            pendientes = restantes

        return (
            tareas,
            arboles_subtareas
        )