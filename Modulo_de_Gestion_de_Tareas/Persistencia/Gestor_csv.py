import csv # Modulo para leer y escribir archivos en formato separado por comas.
import os # Modulo para interactuar con el sistema operativo.

class GestorCSV:
    @staticmethod # Metodos estaticos 
    def cargar_desde_csv(ruta_archivo: str, gestor):
        if not os.path.exists(ruta_archivo): # Verifica que le archivo exista en el disco.
            return False # No existe False.

        # Abre el archivo en modo lectura "r".
        # Usa codificacion "utf-8".
        # Asegura que el archivo se cierre al terminar "with".
        with open(ruta_archivo, mode='r', encoding='utf-8') as archivo: 
            lector = csv.reader(archivo) # Lee el archivo y devuelve una lista de cadenas por cada fila.
            for fila in lector: #Procesa la fila actual de csv.
                if not fila or len(fila) < 2: # Ignora las lineas vacias.
                    continue
                comando = fila[0].strip().upper() # Toma la primera columna (fila[0]), limpia los espacios de los extremos (.strip()) y la pasa a mayúsculas (.upper()).
                
                if comando in ["CREAR_TAREA", "CREAR TAREA"]:
                    # Formato: CREAR_TAREA, id, prioridad, id_usuario, descripcion, [estado]
                    try:
                        id_tarea = int(fila[1].strip())
                        prio = fila[2].strip()
                        id_usr = int(fila[3].strip())
                        desc = fila[4].strip()
                        completada = False
                        if len(fila) >= 6:
                            estado_str = fila[5].strip().lower()
                            completada = (estado_str in ["completada", "done", "true", "1"]) # Si existe la sexta linea, revisa si corresponde a un estado completada.

                        # Ejecuta el metodo para recrear la tarea en memoria
                        gestor.crear_tarea(id_tarea, prio, id_usr, desc, completada=completada, auto_guardar=False)
                    except Exception as e:
                        print(f"Error al procesar línea CSV (Tarea): {fila} -> {e}")
                
                elif comando in ["AGREGAR_SUBTAREA", "AGREGAR SUBTAREA"]:
                    # Formato: AGREGAR_SUBTAREA, id_subtarea, id_padre, descripcion, [completada]
                    try:
                        id_sub = int(fila[1].strip())
                        id_padre = int(fila[2].strip())
                        desc = fila[3].strip()
                        completada = False
                        if len(fila) >= 5:
                            estado_str = fila[4].strip().lower()
                            completada = (estado_str in ["completada", "done", "true", "1"])

                        # Rearma el arbol jerarquico.
                        gestor.agregar_subtarea(id_sub, id_padre, desc, completada=completada, auto_guardar=False)
                    except Exception as e:
                        print(f"Error al procesar línea CSV (Subtarea): {fila} -> {e}")

        return True

    @staticmethod # Metodo estatico.
    def guardar_en_csv(ruta_archivo: str, gestor):
        # Escribe todas las tareas y subtareas al archivo CSV
        filas = [] # Inicializa la lista.
        # Recorre todas las tareas obtenidas del gestor y las fomratea como comandos.
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
            
        # Subtareas desde el diccionario de árboles
        for id_raiz, raiz in gestor.arboles_subtareas.items():
            subtareas_tuplas = raiz.obtener_todas()
            # La primera tupla es la raíz misma, las demás son subtareas hijas
            for sub_tuple in subtareas_tuplas[1:]:
                id_sub, desc, completada, id_padre = sub_tuple
                filas.append([
                    "AGREGAR_SUBTAREA",
                    str(id_sub),
                    str(id_padre),
                    desc,
                    "Completada" if completada else "Pendiente"
                ])

        # Asegurar directorio de destino si aplica
        directorio = os.path.dirname(ruta_archivo) # Extrae la ruta de la carpeta emisora.
        if directorio and not os.path.exists(directorio):
            os.makedirs(directorio, exist_ok=True) # Crea la estructura de carpetas

        # Abre el archivo en moddo escritura "w".
        # Evita la inserción de saltos de línea dobles innecesarios en plataformas como Windows "newline+''".
        with open(ruta_archivo, mode='w', encoding='utf-8', newline='') as archivo:
            escritor = csv.writer(archivo)
            escritor.writerows(filas) # Escribe en bloque de filas generadas.

        return True

class AuditoriaLogger:
    """
    Gestiona la bitácora inmutable de auditoría (auditoria_log.csv).
    Solo permite agregar líneas (modo append) en formato:
    [Fecha y Hora] | [ID Usuario que ejecutó] | [Acción Realizada] | [ID Tarea Afectada]
    """
    @staticmethod
    def registrar_evento(ruta_log: str, id_usuario, accion: str, id_tarea):
        import datetime
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        usuario_str = str(id_usuario) if id_usuario is not None else "SISTEMA"
        tarea_str = str(id_tarea) if id_tarea is not None else "N/A"
        linea = f"{timestamp} | {usuario_str} | {accion} | {tarea_str}\n"

        directorio = os.path.dirname(ruta_log)
        if directorio and not os.path.exists(directorio):
            os.makedirs(directorio, exist_ok=True)

        # Abre en modo 'a' (append) para garantizar la inmutabilidad de los registros previos
        with open(ruta_log, mode='a', encoding='utf-8') as archivo:
            archivo.write(linea)

