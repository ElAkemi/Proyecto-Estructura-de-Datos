# =========================================================
#                  WORKFLOW MANAGER
# =========================================================

# Importamos las funciones que hicimos en CSVManager.py.
# Estas funciones nos permiten cargar y guardar información.
from CSVManager import cargar_usuarios
from CSVManager import guardar_usuarios
from CSVManager import cargar_tareas
from CSVManager import guardar_tareas

# Importamos nuestros tres algoritmos de ordenamiento.
from Ordenamientos import burbuja
from Ordenamientos import merge_sort
from Ordenamientos import quick_sort


# =========================================================
#               LISTAS TEMPORALES
# =========================================================

# Aquí vamos a guardar temporalmente los usuarios
# mientras el programa esté funcionando.
usuarios = []

# Aquí vamos a guardar temporalmente las tareas.
tareas = []


# =========================================================
#                 MENÚ DE USUARIOS
# =========================================================

def menu_usuarios():

    # El menú se repite hasta seleccionar "Volver".
    while True:

        print("\n============================")
        print("     GESTIÓN DE USUARIOS")
        print("============================")
        print("1. Registrar usuario")
        print("2. Actualizar usuario")
        print("3. Eliminar usuario")
        print("4. Mostrar usuarios")
        print("5. Buscar usuario por ID")
        print("6. Volver")

        # Pedimos al usuario que seleccione una opción.
        opcion = input("Seleccione una opción: ")

        # Estas funciones todavía no están conectadas
        # porque corresponden al trabajo de José.

        if opcion == "1":
            print("\nRegistrar usuario - Pendiente de integrar.")

        elif opcion == "2":
            print("\nActualizar usuario - Pendiente de integrar.")

        elif opcion == "3":
            print("\nEliminar usuario - Pendiente de integrar.")

        elif opcion == "4":
            print("\nMostrar usuarios - Pendiente de integrar.")

        elif opcion == "5":
            print("\nBuscar usuario - Pendiente de integrar.")

        # Regresamos al menú principal.
        elif opcion == "6":
            break

        # Si escribe algo diferente a las opciones anteriores.
        else:
            print("\nOpción inválida. Intente nuevamente.")


# =========================================================
#                  MENÚ DE TAREAS
# =========================================================

def menu_tareas():

    while True:

        print("\n============================")
        print("      GESTIÓN DE TAREAS")
        print("============================")
        print("1. Crear tarea")
        print("2. Ejecutar tarea")
        print("3. Mostrar tareas")
        print("4. Mostrar subtareas")
        print("5. Volver")

        opcion = input("Seleccione una opción: ")

        # Estas opciones todavía quedan pendientes
        # porque dependen del módulo de Valeria.

        if opcion == "1":
            print("\nCrear tarea - Pendiente de integrar.")

        elif opcion == "2":
            print("\nEjecutar tarea - Pendiente de integrar.")

        elif opcion == "3":
            print("\nMostrar tareas - Pendiente de integrar.")

        elif opcion == "4":
            print("\nMostrar subtareas - Pendiente de integrar.")

        # Regresamos al menú principal.
        elif opcion == "5":
            break

        else:
            print("\nOpción inválida. Intente nuevamente.")


# =========================================================
#               MENÚ DE ORDENAMIENTOS
# =========================================================

def menu_ordenamientos():

    while True:

        print("\n============================")
        print("       ORDENAMIENTOS")
        print("============================")
        print("1. Burbuja")
        print("2. Merge Sort")
        print("3. Quick Sort")
        print("4. Volver")

        opcion = input("Seleccione una opción: ")

        # Antes de ordenar comprobamos que existan tareas.
        if opcion != "4" and len(tareas) == 0:

            print("\nNo hay tareas para ordenar.")

            # Volvemos al inicio del menú.
            continue

        # Ordenamiento Burbuja.
        if opcion == "1":

            resultado = burbuja(tareas)

            print("\nResultado:")
            print(resultado)

        # Ordenamiento Merge Sort.
        elif opcion == "2":

            resultado = merge_sort(tareas)

            print("\nResultado:")
            print(resultado)

        # Ordenamiento Quick Sort.
        elif opcion == "3":

            resultado = quick_sort(tareas)

            print("\nResultado:")
            print(resultado)

        # Regresamos al menú principal.
        elif opcion == "4":
            break

        else:
            print("\nOpción inválida. Intente nuevamente.")


# =========================================================
#                   CARGAR DATOS
# =========================================================

def cargar_datos():

    # Indicamos que queremos utilizar las listas
    # que fueron creadas al inicio del programa.
    global usuarios
    global tareas

    # Leemos los usuarios desde usuarios.csv.
    usuarios = cargar_usuarios()

    # Leemos las tareas desde tareas.csv.
    tareas = cargar_tareas()

    print("\nDatos cargados correctamente.")

    # Mostramos cuántos datos fueron encontrados.
    print("Usuarios cargados:", len(usuarios))
    print("Tareas cargadas:", len(tareas))


# =========================================================
#                   GUARDAR DATOS
# =========================================================

def guardar_datos():

    # Guardamos los usuarios actuales.
    guardar_usuarios(usuarios)

    # Guardamos las tareas actuales.
    guardar_tareas(tareas)

    print("\nDatos guardados correctamente.")


# =========================================================
#                    MENÚ PRINCIPAL
# =========================================================

def menu_principal():

    # Este ciclo mantiene funcionando el programa
    # hasta que el usuario seleccione "Salir".
    while True:

        print("\n================================")
        print("        WORKFLOW MANAGER")
        print("================================")
        print("1. Gestión de usuarios")
        print("2. Gestión de tareas")
        print("3. Ordenamientos")
        print("4. Cargar datos")
        print("5. Guardar datos")
        print("6. Salir")

        opcion = input("Seleccione una opción: ")

        # Abrimos el menú de usuarios.
        if opcion == "1":

            menu_usuarios()

        # Abrimos el menú de tareas.
        elif opcion == "2":

            menu_tareas()

        # Abrimos nuestro menú de ordenamientos.
        elif opcion == "3":

            menu_ordenamientos()

        # Cargamos la información de los CSV.
        elif opcion == "4":

            cargar_datos()

        # Guardamos la información en los CSV.
        elif opcion == "5":

            guardar_datos()

        # Terminamos el programa.
        elif opcion == "6":

            print("\nPrograma finalizado.")
            break

        # Evitamos que una opción incorrecta cierre el programa.
        else:

            print("\nOpción inválida. Intente nuevamente.")


# =========================================================
#                   INICIO DEL PROGRAMA
# =========================================================

# Esta línea inicia nuestro programa.
menu_principal()