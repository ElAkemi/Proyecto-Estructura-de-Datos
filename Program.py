# =========================================================
#                   PROGRAM.PY
# =========================================================
#
# Este es el archivo principal del sistema.
# Desde aquí se controlan los diferentes módulos.
# =========================================================


# Importamos las funciones del CSV.
from CSVManager import cargar_usuarios
from CSVManager import guardar_usuarios
from CSVManager import cargar_tareas
from CSVManager import guardar_tareas
from CSVManager import registrar_auditoria


# Importamos los algoritmos.
from Ordenamientos import burbuja
from Ordenamientos import merge_sort
from Ordenamientos import quick_sort


# =========================================================
#               DATOS DEL PROGRAMA
# =========================================================

# Listas temporales.
usuarios = []
tareas = []


# =========================================================
#                 LEER UNA OPCIÓN
# =========================================================

def leer_opcion():

    # Pedimos una opción.
    opcion = input(
        "Seleccione una opción: "
    )

    # Quitamos espacios innecesarios.
    opcion = opcion.strip()

    # Devolvemos la opción.
    return opcion


# =========================================================
#                 MENÚ DE USUARIOS
# =========================================================

def menu_usuarios():

    while True:

        print("\n================================")
        print("       MENÚ DE USUARIOS")
        print("================================")
        print("1. Registrar usuario")
        print("2. Actualizar usuario")
        print("3. Eliminar usuario")
        print("4. Listar usuarios")
        print("5. Buscar usuario por ID")
        print("6. Deshacer")
        print("7. Rehacer")
        print("0. Volver")
        print("================================")

        opcion = leer_opcion()

        # Estas opciones se conectarán
        # posteriormente con el código de José.

        if opcion == "1":

            print(
                "\nRegistrar usuario "
                "- Pendiente de integrar."
            )

        elif opcion == "2":

            print(
                "\nActualizar usuario "
                "- Pendiente de integrar."
            )

        elif opcion == "3":

            print(
                "\nEliminar usuario "
                "- Pendiente de integrar."
            )

        elif opcion == "4":

            print(
                "\nListar usuarios "
                "- Pendiente de integrar."
            )

        elif opcion == "5":

            print(
                "\nBuscar usuario "
                "- Pendiente de integrar."
            )

        elif opcion == "6":

            print(
                "\nDeshacer "
                "- Pendiente de integrar."
            )

        elif opcion == "7":

            print(
                "\nRehacer "
                "- Pendiente de integrar."
            )

        elif opcion == "0":

            break

        else:

            print(
                "\nOpción inválida. "
                "Intente nuevamente."
            )


# =========================================================
#                   MENÚ DE TAREAS
# =========================================================

def menu_tareas():

    while True:

        print("\n================================")
        print("        MENÚ DE TAREAS")
        print("================================")
        print("1. Crear tarea")
        print("2. Ejecutar siguiente tarea")
        print("3. Mostrar tareas")
        print("4. Mostrar subtareas")
        print("5. Revisar SLA")
        print("0. Volver")
        print("================================")

        opcion = leer_opcion()

        # Estas funciones se conectarán
        # posteriormente con el módulo de Valeria.

        if opcion == "1":

            print(
                "\nCrear tarea "
                "- Pendiente de integrar."
            )

        elif opcion == "2":

            print(
                "\nEjecutar tarea "
                "- Pendiente de integrar."
            )

        elif opcion == "3":

            print(
                "\nMostrar tareas "
                "- Pendiente de integrar."
            )

        elif opcion == "4":

            print(
                "\nMostrar subtareas "
                "- Pendiente de integrar."
            )

        elif opcion == "5":

            # El control real del SLA corresponde
            # al módulo de colas.
            print(
                "\nControl SLA "
                "- Pendiente de integrar."
            )

        elif opcion == "0":

            break

        else:

            print(
                "\nOpción inválida. "
                "Intente nuevamente."
            )


# =========================================================
#               MENÚ DE ORDENAMIENTOS
# =========================================================

def menu_ordenamientos():

    while True:

        print("\n================================")
        print("          ORDENAMIENTOS")
        print("================================")
        print("1. Burbuja")
        print("2. Merge Sort")
        print("3. Quick Sort")
        print("0. Volver")
        print("================================")

        opcion = leer_opcion()

        # Si selecciona volver.
        if opcion == "0":
            break

        # Validamos las opciones.
        if opcion not in ["1", "2", "3"]:

            print(
                "\nOpción inválida. "
                "Intente nuevamente."
            )

            continue

        # Comprobamos que existan tareas.
        if len(tareas) == 0:

            print(
                "\nNo hay tareas para ordenar."
            )

            continue

        # ---------------------------------------------
        # BURBUJA
        # ---------------------------------------------

        if opcion == "1":

            resultado = burbuja(tareas)

            print("\nResultado:")
            print(resultado)

        # ---------------------------------------------
        # MERGE SORT
        # ---------------------------------------------

        elif opcion == "2":

            resultado = merge_sort(tareas)

            print("\nResultado:")
            print(resultado)

        # ---------------------------------------------
        # QUICK SORT
        # ---------------------------------------------

        elif opcion == "3":

            resultado = quick_sort(tareas)

            print("\nResultado:")
            print(resultado)


# =========================================================
#                     CARGAR DATOS
# =========================================================

def cargar_datos():

    global usuarios
    global tareas

    # try intenta ejecutar el código.
    try:

        usuarios = cargar_usuarios()
        tareas = cargar_tareas()

        print(
            "\nDatos cargados correctamente."
        )

        print(
            "Usuarios cargados:",
            len(usuarios)
        )

        print(
            "Tareas cargadas:",
            len(tareas)
        )

    # Si ocurre un error, el programa
    # no se cierra inesperadamente.
    except Exception as error:

        print(
            "\nNo se pudieron cargar los datos."
        )

        print("Error:", error)


# =========================================================
#                    GUARDAR DATOS
# =========================================================

def guardar_datos():

    try:

        guardar_usuarios(usuarios)
        guardar_tareas(tareas)

        print(
            "\nDatos guardados correctamente."
        )

    except Exception as error:

        print(
            "\nNo se pudieron guardar los datos."
        )

        print("Error:", error)


# =========================================================
#                    MENÚ PRINCIPAL
# =========================================================

def menu_principal():

    while True:

        print("\n================================")
        print("        WORKFLOW MANAGER")
        print("================================")
        print("1. Gestión de usuarios")
        print("2. Gestión de tareas")
        print("3. Ordenamientos")
        print("4. Cargar datos")
        print("5. Guardar datos")
        print("0. Salir")
        print("================================")

        opcion = leer_opcion()

        if opcion == "1":

            menu_usuarios()

        elif opcion == "2":

            menu_tareas()

        elif opcion == "3":

            menu_ordenamientos()

        elif opcion == "4":

            cargar_datos()

        elif opcion == "5":

            guardar_datos()

        elif opcion == "0":

            print(
                "\nPrograma finalizado."
            )

            break

        else:

            print(
                "\nOpción inválida. "
                "Intente nuevamente."
            )


# =========================================================
#                  INICIAR PROGRAMA
# =========================================================

menu_principal()