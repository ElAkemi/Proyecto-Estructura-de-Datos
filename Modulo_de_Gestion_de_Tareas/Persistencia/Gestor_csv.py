"""Módulo para la gestión de carga, guardado y auditoría de tareas en CSV."""

import csv  # Modulo para leer y escribir archivos en formato CSV.
import datetime
import os  # Modulo para interactuar con el sistema operativo.


class GestorCSV:
    """Clase encargada de la persistencia de tareas y subtareas en formato CSV."""

    @staticmethod
    def cargar_desde_csv(ruta_archivo: str, gestor):
        """Carga las tareas y subtareas desde un archivo CSV al gestor en memoria."""
        if not os.path.exists(ruta_archivo):
            return False

        with open(ruta_archivo, mode='r', encoding='utf-8') as archivo:
            lector = csv.reader(archivo)
            for fila in lector:
                if not fila or len(fila) < 2:
                    continue
                comando = fila[0].strip().upper()

                if comando in ["CREAR_TAREA", "CREAR TAREA"]:
                    GestorCSV._procesar_crear_tarea(fila, gestor)
                elif comando in ["AGREGAR_SUBTAREA", "AGREGAR SUBTAREA"]:
                    GestorCSV._procesar_agregar_subtarea(fila, gestor)

        return True

    @staticmethod
    def _procesar_crear_tarea(fila, gestor):
        """Procesa una línea del CSV con la orden de crear tarea."""
        try:
            id_tarea = int(fila[1].strip())
            prio = fila[2].strip()
            id_usr = int(fila[3].strip())
            desc = fila[4].strip()
            completada = False
            if len(fila) >= 6:
                estado_str = fila[5].strip().lower()
                completada = estado_str in ["completada", "done", "true", "1"]

            gestor.crear_tarea(
                id_tarea, prio, id_usr, desc,
                completada=completada, auto_guardar=False
            )
        except (ValueError, IndexError) as e:
            print(f"Error al procesar línea CSV (Tarea): {fila} -> {e}")

    @staticmethod
    def _procesar_agregar_subtarea(fila, gestor):
        """Procesa una línea del CSV con la orden de agregar subtarea."""
        try:
            id_sub = int(fila[1].strip())
            id_padre = int(fila[2].strip())
            desc = fila[3].strip()
            completada = False
            if len(fila) >= 5:
                estado_str = fila[4].strip().lower()
                completada = estado_str in ["completada", "done", "true", "1"]

            gestor.agregar_subtarea(
                id_sub, id_padre, desc,
                completada=completada, auto_guardar=False
            )
        except (ValueError, IndexError) as e:
            print(f"Error al procesar línea CSV (Subtarea): {fila} -> {e}")

    @staticmethod
    def guardar_en_csv(ruta_archivo: str, gestor):
        """Escribe todas las tareas y subtareas en el archivo CSV."""
        filas = []
        todas_tareas = gestor.obtener_todas_tareas()
        for t in todas_tareas:
            filas.append([
                "CREAR_TAREA",
                str(t.id_tarea),
                t.prioridad.name,
                str(t.id_usuario),
                t.descripcion,
                t.estado
            ])

        for _, raiz in gestor.arboles_subtareas.items():
            subtareas_tuplas = raiz.obtener_todas()
            for sub_tuple in subtareas_tuplas[1:]:
                id_sub, desc, completada, id_padre = sub_tuple
                filas.append([
                    "AGREGAR_SUBTAREA",
                    str(id_sub),
                    str(id_padre),
                    desc,
                    "Completada" if completada else "Pendiente"
                ])

        directorio = os.path.dirname(ruta_archivo)
        if directorio and not os.path.exists(directorio):
            os.makedirs(directorio, exist_ok=True)

        with open(
            ruta_archivo, mode='w', encoding='utf-8', newline=''
        ) as archivo:
            escritor = csv.writer(archivo)
            escritor.writerows(filas)

        return True


class AuditoriaLogger:
    """Gestiona la bitácora inmutable de auditoría (auditoria_log.csv)."""

    @staticmethod
    def registrar_evento(ruta_log: str, id_usuario, accion: str, id_tarea):
        """Registra un evento individual en el log de auditoría."""
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        usuario_str = str(id_usuario) if id_usuario is not None else "SISTEMA"
        tarea_str = str(id_tarea) if id_tarea is not None else "N/A"
        linea = f"{timestamp} | {usuario_str} | {accion} | {tarea_str}\n"

        directorio = os.path.dirname(ruta_log)
        if directorio and not os.path.exists(directorio):
            os.makedirs(directorio, exist_ok=True)

        with open(ruta_log, mode='a', encoding='utf-8') as archivo:
            archivo.write(linea)
