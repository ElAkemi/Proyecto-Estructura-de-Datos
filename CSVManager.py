# Importamos csv para poder trabajar con archivos .csv
import csv

# Importamos os para comprobar si un archivo existe
import os


# =========================================================
# GUARDAR USUARIOS
# =========================================================

def guardar_usuarios(usuarios):

    # Abrimos el archivo donde vamos a guardar los usuarios.
    # "w" significa que vamos a escribir en el archivo.
    archivo = open("usuarios.csv", "w", newline="", encoding="utf-8")

    # Creamos el escritor del CSV.
    escritor = csv.writer(archivo)

    # Escribimos los títulos de las columnas.
    escritor.writerow(["id", "nombre"])

    # Recorremos todos los usuarios.
    for usuario in usuarios:

        # Guardamos cada usuario en una fila.
        escritor.writerow([
            usuario["id"],
            usuario["nombre"]
        ])

    # Cerramos el archivo cuando terminamos.
    archivo.close()


# =========================================================
# CARGAR USUARIOS
# =========================================================

def cargar_usuarios():

    # Creamos una lista vacía para guardar los usuarios.
    usuarios = []

    # Si el archivo todavía no existe,
    # simplemente devolvemos la lista vacía.
    if not os.path.exists("usuarios.csv"):
        return usuarios

    # Abrimos el archivo para leerlo.
    archivo = open("usuarios.csv", "r", encoding="utf-8")

    # DictReader nos permite leer cada usuario
    # usando los nombres de las columnas.
    lector = csv.DictReader(archivo)

    # Recorremos los usuarios del archivo.
    for fila in lector:

        # Creamos un usuario.
        usuario = {
            "id": fila["id"],
            "nombre": fila["nombre"]
        }

        # Lo agregamos a la lista.
        usuarios.append(usuario)

    # Cerramos el archivo.
    archivo.close()

    # Devolvemos la lista de usuarios.
    return usuarios


# =========================================================
# GUARDAR TAREAS
# =========================================================

def guardar_tareas(tareas):

    # Abrimos el archivo de tareas.
    archivo = open("tareas.csv", "w", newline="", encoding="utf-8")

    # Creamos el escritor.
    escritor = csv.writer(archivo)

    # Escribimos los títulos de las columnas.
    escritor.writerow([
        "id",
        "prioridad",
        "usuario_id",
        "descripcion"
    ])

    # Recorremos todas las tareas.
    for tarea in tareas:

        # Guardamos cada tarea.
        escritor.writerow([
            tarea["id"],
            tarea["prioridad"],
            tarea["usuario_id"],
            tarea["descripcion"]
        ])

    # Cerramos el archivo.
    archivo.close()


# =========================================================
# CARGAR TAREAS
# =========================================================

def cargar_tareas():

    # Creamos una lista vacía.
    tareas = []

    # Comprobamos si existe el archivo.
    if not os.path.exists("tareas.csv"):
        return tareas

    # Abrimos el archivo para leerlo.
    archivo = open("tareas.csv", "r", encoding="utf-8")

    # Leemos el CSV.
    lector = csv.DictReader(archivo)

    # Recorremos todas las tareas.
    for fila in lector:

        # Creamos una tarea.
        tarea = {
            "id": fila["id"],
            "prioridad": fila["prioridad"],
            "usuario_id": fila["usuario_id"],
            "descripcion": fila["descripcion"]
        }

        # Agregamos la tarea a la lista.
        tareas.append(tarea)

    # Cerramos el archivo.
    archivo.close()

    # Devolvemos las tareas.
    return tareas