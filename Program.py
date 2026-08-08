def menu_principal():
    while True:
        print("\n========================================")
        print("          WORKFLOW MANAGER")
        print("========================================")
        print("1. Usuarios")
        print("2. Tareas")
        print("3. Kanban")
        print("0. Salir")
        print("========================================")

        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            menu_usuarios()

        elif opcion == "2":
            menu_tareas()

        elif opcion == "3":
            menu_kanban()

        elif opcion == "0":
            print("\nSaliendo del sistema...")
            break

        else:
            print("\nOpción inválida. Intente nuevamente.")


def menu_usuarios():
    while True:
        print("\n========================================")
        print("           MENÚ DE USUARIOS")
        print("========================================")
        print("1. Registrar usuario")
        print("2. Actualizar usuario")
        print("3. Eliminar usuario")
        print("4. Listar usuarios")
        print("5. Buscar usuario por ID")
        print("6. Permisos y roles")
        print("0. Volver al menú principal")
        print("========================================")

        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            print("\nRegistrar usuario - Pendiente de integrar.")

        elif opcion == "2":
            print("\nActualizar usuario - Pendiente de integrar.")

        elif opcion == "3":
            print("\nEliminar usuario - Pendiente de integrar.")

        elif opcion == "4":
            print("\nLista de usuarios - Pendiente de integrar.")

        elif opcion == "5":
            print("\nBuscar usuario por ID - Pendiente de integrar.")

        elif opcion == "6":
            menu_roles()

        elif opcion == "0":
            break

        else:
            print("\nOpción inválida. Intente nuevamente.")


def menu_roles():
    while True:
        print("\n========================================")
        print("         PERMISOS Y ROLES")
        print("========================================")
        print("1. Administrador")
        print("2. Colaborador regular")
        print("0. Volver")
        print("========================================")

        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            print("\nRol Administrador - Pendiente de integrar.")

        elif opcion == "2":
            print("\nRol Colaborador regular - Pendiente de integrar.")

        elif opcion == "0":
            break

        else:
            print("\nOpción inválida. Intente nuevamente.")


def menu_tareas():
    while True:
        print("\n========================================")
        print("            MENÚ DE TAREAS")
        print("========================================")
        print("1. Crear tarea")
        print("2. Mostrar tareas")
        print("3. Asignar prioridad")
        print("4. Asignar responsable")
        print("5. Mostrar subtareas")
        print("0. Volver al menú principal")
        print("========================================")

        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            print("\nCrear tarea - Pendiente de integrar.")

        elif opcion == "2":
            print("\nMostrar tareas - Pendiente de integrar.")

        elif opcion == "3":
            menu_prioridad()

        elif opcion == "4":
            print("\nAsignar responsable - Pendiente de integrar.")
            print("Una tarea podrá tener ninguno, uno o varios responsables.")

        elif opcion == "5":
            print("\nMostrar subtareas - Pendiente de integrar.")

        elif opcion == "0":
            break

        else:
            print("\nOpción inválida. Intente nuevamente.")


def menu_prioridad():
    while True:
        print("\n========================================")
        print("          PRIORIDAD DE TAREA")
        print("========================================")
        print("1. Alta")
        print("2. Media")
        print("3. Baja")
        print("4. Mostrar tareas ordenadas por prioridad")
        print("0. Volver")
        print("========================================")

        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            print("\nPrioridad ALTA seleccionada.")

        elif opcion == "2":
            print("\nPrioridad MEDIA seleccionada.")

        elif opcion == "3":
            print("\nPrioridad BAJA seleccionada.")

        elif opcion == "4":
            print("\nOrdenamiento por prioridad - Pendiente de desarrollar.")

        elif opcion == "0":
            break

        else:
            print("\nOpción inválida. Intente nuevamente.")


def menu_kanban():
    while True:
        print("\n========================================")
        print("              MENÚ KANBAN")
        print("========================================")
        print("1. Ver tareas por hacer")
        print("2. Ver tareas en proceso")
        print("3. Ver tareas hechas")
        print("4. Cambiar estado de una tarea")
        print("5. Deshacer último cambio")
        print("6. Rehacer último cambio")
        print("0. Volver al menú principal")
        print("========================================")

        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            print("\nTareas POR HACER - Pendiente de integrar.")

        elif opcion == "2":
            print("\nTareas EN PROCESO - Pendiente de integrar.")

        elif opcion == "3":
            print("\nTareas HECHAS - Pendiente de integrar.")

        elif opcion == "4":
            menu_cambiar_estado()

        elif opcion == "5":
            print("\nDeshacer - Pendiente de integrar con la pila.")

        elif opcion == "6":
            print("\nRehacer - Pendiente de integrar con la pila.")

        elif opcion == "0":
            break

        else:
            print("\nOpción inválida. Intente nuevamente.")


def menu_cambiar_estado():
    while True:
        print("\n========================================")
        print("        CAMBIAR ESTADO DE TAREA")
        print("========================================")
        print("1. Por hacer")
        print("2. En proceso")
        print("3. Hecha")
        print("0. Cancelar")
        print("========================================")

        opcion = input("Seleccione el nuevo estado: ")

        if opcion == "1":
            print("\nNuevo estado: POR HACER")
            break

        elif opcion == "2":
            print("\nNuevo estado: EN PROCESO")
            break

        elif opcion == "3":
            print("\nNuevo estado: HECHA")
            break

        elif opcion == "0":
            print("\nCambio cancelado.")
            break

        else:
            print("\nOpción inválida. Intente nuevamente.")


if __name__ == "__main__":
    menu_principal()