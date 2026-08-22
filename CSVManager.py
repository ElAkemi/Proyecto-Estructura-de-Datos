# =========================================================
#                    CSVMANAGER.PY
# =========================================================

# Importamos csv para trabajar con archivos CSV.
import csv

# Importamos os para comprobar si existen archivos.
import os

# Importamos datetime para obtener
# la fecha y hora actual.
from datetime import datetime


# =========================================================
#                  GUARDAR USUARIOS
# =========================================================

def guardar_usuarios(usuarios):

    # Abrimos usuarios.csv en modo escritura.
    archivo = open(
        "usuarios.csv",
        "w",
        newline="",
        encoding="utf-8"
    )

    # Creamos el escritor del CSV.
    escritor = csv.writer(archivo)

    # Escribimos los títulos.
    escritor.writerow([
        "id",
        "nombre"
    ])

    # Recorremos los usuarios.
    for usuario in usuarios:

        # Si estamos utilizando diccionarios.
        if isinstance(usuario, dict):

            escritor.writerow([
                usuario.get("id", ""),
                usuario.get("nombre", "")
            ])

        # Si José utiliza objetos Usuario,
        # intentamos obtener sus atributos.
        else:

            escritor.writerow([
                getattr(usuario, "id", ""),
                getattr(usuario, "nombre", "")
            ])

    # Cerramos el archivo.
    archivo.close()


# =========================================================
#                  CARGAR USUARIOS
# =========================================================

def cargar_usuarios():

    # Lista donde guardaremos los usuarios.
    usuarios = []

    # Comprobamos si el archivo existe.
    if not os.path.exists("usuarios.csv"):
        return usuarios

    # Abrimos el archivo.
    archivo = open(
        "usuarios.csv",
        "r",
        encoding="utf-8"
    )

    # Leemos el CSV.
    lector = csv.DictReader(archivo)

    # Recorremos las filas.
    for fila in lector:

        usuario = {
            "id": fila["id"],
            "nombre": fila["nombre"]
        }

        usuarios.append(usuario)

    # Cerramos el archivo.
    archivo.close()

    # Devolvemos los usuarios.
    return usuarios


# =========================================================
#                   GUARDAR TAREAS
# =========================================================

def guardar_tareas(tareas):

    # Abrimos tareas.csv.
    archivo = open(
        "tareas.csv",
        "w",
        newline="",
        encoding="utf-8"
    )

    # Creamos el escritor.
    escritor = csv.writer(archivo)

    # Escribimos los encabezados.
    escritor.writerow([
        "id",
        "prioridad",
        "usuario_id",
        "descripcion"
    ])

    # Recorremos las tareas.
    for tarea in tareas:

        # Si la tarea es un diccionario.
        if isinstance(tarea, dict):

            escritor.writerow([
                tarea.get("id", ""),
                tarea.get("prioridad", ""),
                tarea.get("usuario_id", ""),
                tarea.get("descripcion", "")
            ])

        # Si Valeria utiliza objetos Tarea.
        else:

            escritor.writerow([
                getattr(tarea, "id", ""),
                getattr(tarea, "prioridad", ""),
                getattr(tarea, "usuario_id", ""),
                getattr(tarea, "descripcion", "")
            ])

    # Cerramos el archivo.
    archivo.close()


# =========================================================
#                    CARGAR TAREAS
# =========================================================

def cargar_tareas():

    # Lista vacía.
    tareas = []

    # Comprobamos si existe tareas.csv.
    if not os.path.exists("tareas.csv"):
        return tareas

    # Abrimos el archivo.
    archivo = open(
        "tareas.csv",
        "r",
        encoding="utf-8"
    )

    # Leemos el CSV.
    lector = csv.DictReader(archivo)

    # Recorremos las tareas.
    for fila in lector:

        tarea = {
            "id": fila["id"],
            "prioridad": fila["prioridad"],
            "usuario_id": fila["usuario_id"],
            "descripcion": fila["descripcion"]
        }

        tareas.append(tarea)

    # Cerramos el archivo.
    archivo.close()

    # Devolvemos las tareas.
    return tareas


# =========================================================
#                 REGISTRAR AUDITORÍA
# =========================================================

def registrar_auditoria(
        id_usuario,
        accion,
        id_tarea="-"):

    # Obtenemos la fecha y hora actuales.
    fecha_hora = datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )

    # IMPORTANTE:
    # Utilizamos "a" y NO "w".
    #
    # "a" significa agregar.
    # De esta manera nunca borramos los
    # registros anteriores de auditoría.
    archivo = open(
        "auditoria_log.csv",
        "a",
        encoding="utf-8"
    )

    # Creamos la línea que vamos a guardar.
    linea = (
        fecha_hora
        + " | "
        + str(id_usuario)
        + " | "
        + str(accion)
        + " | "
        + str(id_tarea)
        + "\n"
    )

    # Agregamos la línea.
    archivo.write(linea)

    # Cerramos el archivo.
    archivo.close()