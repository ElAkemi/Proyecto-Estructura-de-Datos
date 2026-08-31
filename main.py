"""
Punto de entrada del Sistema Gestor de Flujos de Trabajo.

Proyecto de Investigación Aplicada #1
Estructuras de Datos

Incluye:
- Autenticación y control de acceso.
- Gestión de usuarios.
- Gestión de tareas.
- Colas FIFO y de prioridad.
- Árbol de tareas y subtareas.
- Deshacer y rehacer.
- Escalamiento por SLA.
- Auditoría.
- Persistencia CSV.
- Algoritmos de ordenamiento.
"""

from getpass import getpass

from services.sistema_service import SistemaService


# ============================================================
# UTILIDADES DE ENTRADA
# ============================================================

def leer_entero(mensaje):
    """Solicita un número entero hasta recibir uno válido."""

    while True:
        try:
            return int(input(mensaje).strip())
        except ValueError:
            print(" Error: debe ingresar un número entero.")


def leer_entero_positivo(mensaje):
    """Solicita un entero positivo."""

    while True:
        numero = leer_entero(mensaje)

        if numero > 0:
            return numero

        print(" El número debe ser positivo.")


def leer_texto(mensaje):
    """Solicita texto no vacío."""

    while True:
        texto = input(mensaje).strip()

        if texto:
            return texto

        print(" El campo no puede estar vacío.")


def pausar():
    """Pausa la ejecución hasta que el usuario presione Enter."""

    input("\nPresione ENTER para continuar...")


def mostrar_tarea(tarea):
    """Muestra la información de una tarea."""

    print("\n----------------------------------------")
    print(f"ID:              {tarea.id}")
    print(f"Descripción:     {tarea.descripcion}")
    print(f"Prioridad:       {tarea.prioridad}")
    print(f"Responsable:     {tarea.responsable_id}")
    print(f"Estado:          {tarea.estado}")
    print(f"Padre:           {tarea.padre_id}")
    print(f"Ciclos de espera:{tarea.ciclos_espera}")
    print("----------------------------------------")


def mostrar_usuario(usuario):
    """Muestra la información de un usuario."""

    print("\n----------------------------------------")
    print(f"ID:       {usuario.id}")
    print(f"Nombre:   {usuario.nombre}")
    print(f"Rol:      {usuario.rol}")
    print("----------------------------------------")


# ============================================================
# LOGIN
# ============================================================

def iniciar_sesion(sistema):
    """Solicita las credenciales del usuario."""

    print("\n========================================")
    print("       WORKFLOW MANAGER")
    print("========================================")
    print("             INICIO DE SESIÓN")
    print("========================================")

    while True:
        id_usuario = leer_entero_positivo(
            "ID de usuario: "
        )

        # getpass evita mostrar la contraseña en pantalla.
        password = getpass("Contraseña: ")

        try:
            usuario = sistema.iniciar_sesion(
                id_usuario,
                password
            )
        except ValueError as error:
            print(f" {error}")
            continue

        if usuario is not None:
            print(
                f"\n✅ Bienvenido, {usuario.nombre}."
            )
            print(f"Rol: {usuario.rol}")
            return usuario

        print(
            "\n Usuario o contraseña incorrectos."
        )

        opcion = input(
            "¿Desea intentar nuevamente? (s/n): "
        ).strip().lower()

        if opcion != "s":
            return None


# ============================================================
# MENÚ DE USUARIOS
# ============================================================

def menu_usuarios(sistema):
    """Menú administrativo de gestión de usuarios."""

    while True:
        print("\n========================================")
        print("         GESTIÓN DE USUARIOS")
        print("========================================")
        print("1. Agregar usuario")
        print("2. Actualizar usuario")
        print("3. Eliminar usuario")
        print("4. Listar usuarios")
        print("5. Buscar usuario por ID")
        print("0. Volver")
        print("========================================")

        opcion = input("Seleccione una opción: ").strip()

        try:

            if opcion == "1":
                agregar_usuario(sistema)

            elif opcion == "2":
                modificar_usuario(sistema)

            elif opcion == "3":
                eliminar_usuario(sistema)

            elif opcion == "4":
                listar_usuarios(sistema)

            elif opcion == "5":
                buscar_usuario(sistema)

            elif opcion == "0":
                return

            else:
                print(" Opción inválida.")

        except (ValueError, PermissionError) as error:
            print(f"\n {error}")

        pausar()


def agregar_usuario(sistema):
    """Agrega un usuario."""

    print("\n--- AGREGAR USUARIO ---")

    id_usuario = leer_entero_positivo(
        "ID: "
    )

    nombre = leer_texto(
        "Nombre: "
    )

    print("\nRoles disponibles:")
    print("1. Administrador")
    print("2. Usuario")

    while True:
        opcion = input(
            "Seleccione el rol: "
        ).strip()

        if opcion == "1":
            rol = "Administrador"
            break

        if opcion == "2":
            rol = "Usuario"
            break

        print(" Rol inválido.")

    password = getpass(
        "Contraseña: "
    )

    if not password:
        raise ValueError(
            "La contraseña no puede estar vacía."
        )

    usuario = sistema.usuario_service.agregar_usuario(
        id_usuario,
        nombre,
        rol,
        password
    )

    print(
        f"\n Usuario {usuario.id} agregado correctamente."
    )


def modificar_usuario(sistema):
    """Modifica un usuario existente."""

    print("\n--- ACTUALIZAR USUARIO ---")

    id_usuario = leer_entero_positivo(
        "ID del usuario: "
    )

    usuario = sistema.usuario_service.buscar_usuario(
        id_usuario
    )

    if usuario is None:
        raise ValueError(
            "No existe un usuario con ese ID."
        )

    mostrar_usuario(usuario)

    nombre = leer_texto(
        "Nuevo nombre: "
    )

    print("\nRoles disponibles:")
    print("1. Administrador")
    print("2. Usuario")

    while True:
        opcion = input(
            "Nuevo rol: "
        ).strip()

        if opcion == "1":
            rol = "Administrador"
            break

        if opcion == "2":
            rol = "Usuario"
            break

        print(" Rol inválido.")

    cambiar_password = input(
        "¿Desea cambiar la contraseña? (s/n): "
    ).strip().lower()

    if cambiar_password == "s":
        password = getpass(
            "Nueva contraseña: "
        )

        if not password:
            raise ValueError(
                "La contraseña no puede estar vacía."
            )
    else:
        password = usuario.password

    sistema.usuario_service.modificar_usuario(
        id_usuario,
        nombre,
        rol,
        password
    )

    print("\n Usuario actualizado correctamente.")


def eliminar_usuario(sistema):
    """Elimina un usuario."""

    print("\n--- ELIMINAR USUARIO ---")

    id_usuario = leer_entero_positivo(
        "ID del usuario: "
    )

    usuario = sistema.usuario_service.buscar_usuario(
        id_usuario
    )

    if usuario is None:
        raise ValueError(
            "No existe un usuario con ese ID."
        )

    mostrar_usuario(usuario)

    confirmar = input(
        "\n¿Confirma la eliminación? (s/n): "
    ).strip().lower()

    if confirmar != "s":
        print("Operación cancelada.")
        return

    sistema.usuario_service.eliminar_usuario(
        id_usuario
    )

    print("\n Usuario eliminado correctamente.")


def listar_usuarios(sistema):
    """Lista todos los usuarios."""

    print("\n--- LISTA DE USUARIOS ---")

    usuarios = sistema.usuario_service.listar_usuarios()

    if not usuarios:
        print("No existen usuarios registrados.")
        return

    for usuario in usuarios:
        mostrar_usuario(usuario)


def buscar_usuario(sistema):
    """Busca un usuario por ID."""

    print("\n--- BUSCAR USUARIO ---")

    id_usuario = leer_entero_positivo(
        "ID: "
    )

    usuario = sistema.usuario_service.buscar_usuario(
        id_usuario
    )

    if usuario is None:
        print("\n Usuario no encontrado.")
        return

    mostrar_usuario(usuario)


# ============================================================
# MENÚ DE TAREAS
# ============================================================

def menu_tareas(sistema, usuario):
    """Menú de administración de tareas."""

    while True:
        print("\n========================================")
        print("           GESTIÓN DE TAREAS")
        print("========================================")
        print("1. Agregar tarea")
        print("2. Actualizar tarea")
        print("3. Eliminar tarea")
        print("4. Listar tareas pendientes")
        print("5. Buscar tarea por ID")
        print("6. Agregar subtarea")
        print("7. Mostrar árbol de tareas")
        print("8. Procesar siguiente tarea")
        print("9. Aplicar ciclo SLA")
        print("10. Cambiar estado")
        print("11. Ordenar tareas")
        print("0. Volver")
        print("========================================")

        opcion = input(
            "Seleccione una opción: "
        ).strip()

        try:

            if opcion == "1":
                agregar_tarea(sistema)

            elif opcion == "2":
                modificar_tarea(sistema)

            elif opcion == "3":
                eliminar_tarea(sistema)

            elif opcion == "4":
                listar_tareas_pendientes(sistema)

            elif opcion == "5":
                buscar_tarea(sistema)

            elif opcion == "6":
                agregar_subtarea(sistema)

            elif opcion == "7":
                mostrar_arbol(sistema)

            elif opcion == "8":
                procesar_tarea(sistema, usuario)

            elif opcion == "9":
                aplicar_sla(sistema, usuario)

            elif opcion == "10":
                cambiar_estado(sistema, usuario)

            elif opcion == "11":
                menu_ordenamiento(sistema)

            elif opcion == "0":
                return

            else:
                print(" Opción inválida.")

        except (
            ValueError,
            PermissionError,
            AttributeError
        ) as error:
            print(f"\n {error}")

        pausar()


def seleccionar_prioridad():
    """Solicita una prioridad válida."""

    print("\nPrioridades disponibles:")
    print("1. URGENTE")
    print("2. ALTA")
    print("3. MEDIA")
    print("4. BAJA")

    while True:
        opcion = input(
            "Seleccione la prioridad: "
        ).strip()

        prioridades = {
            "1": "URGENTE",
            "2": "ALTA",
            "3": "MEDIA",
            "4": "BAJA",
        }

        if opcion in prioridades:
            return prioridades[opcion]

        print(" Prioridad inválida.")


def seleccionar_responsable(sistema):
    """Solicita un usuario responsable existente."""

    while True:
        responsable_id = leer_entero_positivo(
            "ID del responsable: "
        )

        usuario = sistema.usuario_service.buscar_usuario(
            responsable_id
        )

        if usuario is not None:
            return responsable_id

        print(
            " No existe un usuario con ese ID."
        )


def agregar_tarea(sistema):
    """Agrega una tarea."""

    print("\n--- AGREGAR TAREA ---")

    id_tarea = leer_entero_positivo(
        "ID de la tarea: "
    )

    descripcion = leer_texto(
        "Descripción: "
    )

    prioridad = seleccionar_prioridad()

    responsable_id = seleccionar_responsable(
        sistema
    )

    tiene_padre = input(
        "¿Es una subtarea? (s/n): "
    ).strip().lower()

    padre_id = None

    if tiene_padre == "s":

        padre_id = leer_entero_positivo(
            "ID de la tarea padre: "
        )

        if sistema.tarea_service.buscar_tarea(
            padre_id
        ) is None:
            raise ValueError(
                "La tarea padre no existe."
            )

    tarea = sistema.tarea_service.agregar_tarea(
        id_tarea,
        prioridad,
        responsable_id,
        descripcion,
        padre_id
    )

    print(
        f"\n Tarea {tarea.id} creada correctamente."
    )


def modificar_tarea(sistema):
    """Modifica una tarea."""

    print("\n--- ACTUALIZAR TAREA ---")

    id_tarea = leer_entero_positivo(
        "ID de la tarea: "
    )

    tarea = sistema.tarea_service.buscar_tarea(
        id_tarea
    )

    if tarea is None:
        raise ValueError(
            "No existe una tarea con ese ID."
        )

    mostrar_tarea(tarea)

    descripcion = leer_texto(
        "Nueva descripción: "
    )

    prioridad = seleccionar_prioridad()

    responsable_id = seleccionar_responsable(
        sistema
    )

    sistema.tarea_service.modificar_tarea(
        id_tarea,
        descripcion,
        prioridad,
        responsable_id
    )

    print("\n Tarea actualizada correctamente.")


def eliminar_tarea(sistema):
    """Elimina una tarea."""

    print("\n--- ELIMINAR TAREA ---")

    id_tarea = leer_entero_positivo(
        "ID: "
    )

    tarea = sistema.tarea_service.buscar_tarea(
        id_tarea
    )

    if tarea is None:
        raise ValueError(
            "No existe una tarea con ese ID."
        )

    mostrar_tarea(tarea)

    confirmar = input(
        "\n¿Confirma la eliminación? (s/n): "
    ).strip().lower()

    if confirmar != "s":
        print("Operación cancelada.")
        return

    sistema.tarea_service.eliminar_tarea(
        id_tarea
    )

    print("\n Tarea eliminada correctamente.")


def listar_tareas_pendientes(sistema):
    """Lista las tareas pendientes."""

    print("\n--- TAREAS PENDIENTES ---")

    tareas = sistema.tarea_service.listar_pendientes()

    if not tareas:
        print("No existen tareas pendientes.")
        return

    for tarea in tareas:
        mostrar_tarea(tarea)


def buscar_tarea(sistema):
    """Busca una tarea."""

    print("\n--- BUSCAR TAREA ---")

    id_tarea = leer_entero_positivo(
        "ID: "
    )

    tarea = sistema.tarea_service.buscar_tarea(
        id_tarea
    )

    if tarea is None:
        print("\n Tarea no encontrada.")
        return

    mostrar_tarea(tarea)


def agregar_subtarea(sistema):
    """Agrega una subtarea a una tarea existente."""

    print("\n--- AGREGAR SUBTAREA ---")

    padre_id = leer_entero_positivo(
        "ID de la tarea padre: "
    )

    padre = sistema.tarea_service.buscar_tarea(
        padre_id
    )

    if padre is None:
        raise ValueError(
            "La tarea padre no existe."
        )

    id_tarea = leer_entero_positivo(
        "ID de la subtarea: "
    )

    descripcion = leer_texto(
        "Descripción: "
    )

    prioridad = seleccionar_prioridad()

    responsable_id = seleccionar_responsable(
        sistema
    )

    tarea = sistema.tarea_service.agregar_tarea(
        id_tarea,
        prioridad,
        responsable_id,
        descripcion,
        padre_id
    )

    print(
        f"\n Subtarea {tarea.id} agregada."
    )


def mostrar_arbol(sistema):
    """Muestra la jerarquía de tareas."""

    print("\n--- ÁRBOL DE TAREAS ---")

    try:
        arbol = sistema.tarea_service.listar_arbol()

        if arbol:
            print(arbol)
        else:
            print("No existen tareas.")

    except AttributeError:
        # Compatibilidad si la estructura devuelve
        # directamente una lista.
        tareas = sistema.tarea_service.listar_tareas()

        if not tareas:
            print("No existen tareas.")
            return

        for tarea in tareas:
            print(
                f"- [{tarea.id}] "
                f"{tarea.descripcion}"
            )


def procesar_tarea(sistema, usuario):
    """Procesa la siguiente tarea de las colas."""

    print("\n--- PROCESAR SIGUIENTE TAREA ---")

    tarea = sistema.tarea_service.procesar_siguiente(
        usuario.id
    )

    if tarea is None:
        print("No hay tareas pendientes.")
        return

    print("\n Tarea seleccionada para ejecución:")
    mostrar_tarea(tarea)


def aplicar_sla(sistema, usuario):
    """Aplica el mecanismo de escalamiento SLA."""

    print("\n--- ESCALAMIENTO SLA ---")

    escaladas = sistema.tarea_service.aplicar_sla(
        usuario.id
    )

    if not escaladas:
        print(
            "No se escaló ninguna tarea."
        )
        return

    print(
        f"\n Se escalaron "
        f"{len(escaladas)} tarea(s):"
    )

    for tarea in escaladas:
        print(
            f"- Tarea {tarea.id}: "
            f"{tarea.descripcion}"
        )


def seleccionar_estado():
    """Solicita un estado válido."""

    print("\nEstados disponibles:")
    print("1. Pendiente")
    print("2. En ejecución")
    print("3. Completada")
    print("4. Cancelada")

    estados = {
        "1": "Pendiente",
        "2": "En ejecución",
        "3": "Completada",
        "4": "Cancelada",
    }

    while True:
        opcion = input(
            "Seleccione el estado: "
        ).strip()

        if opcion in estados:
            return estados[opcion]

        print(" Estado inválido.")


def cambiar_estado(sistema, usuario):
    """Cambia el estado de una tarea."""

    print("\n--- CAMBIAR ESTADO ---")

    id_tarea = leer_entero_positivo(
        "ID de la tarea: "
    )

    tarea = sistema.tarea_service.buscar_tarea(
        id_tarea
    )

    if tarea is None:
        raise ValueError(
            "No existe una tarea con ese ID."
        )

    if not sistema.tarea_service.puede_modificar_estado(
        tarea,
        usuario.id
    ):
        raise PermissionError(
            "No tiene permisos para cambiar "
            "el estado de esta tarea."
        )

    nuevo_estado = seleccionar_estado()

    sistema.tarea_service.cambiar_estado(
        id_tarea,
        nuevo_estado,
        usuario.id
    )

    print(
        "\n Estado actualizado correctamente."
    )


# ============================================================
# ORDENAMIENTOS
# ============================================================

def menu_ordenamiento(sistema):
    """Menú de algoritmos de ordenamiento."""

    print("\n========================================")
    print("       ORDENAMIENTO DE TAREAS")
    print("========================================")
    print("1. Bubble Sort")
    print("2. Merge Sort")
    print("3. Quick Sort")
    print("0. Volver")

    opcion = input(
        "Seleccione un algoritmo: "
    ).strip()

    algoritmos = {
        "1": "burbuja",
        "2": "merge",
        "3": "quick",
    }

    if opcion == "0":
        return

    if opcion not in algoritmos:
        print(" Opción inválida.")
        return

    algoritmo = algoritmos[opcion]

    print("\nCriterio:")
    print("1. ID")
    print("2. Prioridad")

    criterio = input(
        "Seleccione el criterio: "
    ).strip()

    try:

        if criterio == "1":
            tareas = sistema.tarea_service.ordenar_por_id(
                algoritmo
            )

        elif criterio == "2":
            tareas = (
                sistema.tarea_service.ordenar_por_prioridad(
                    algoritmo
                )
            )

        else:
            print(" Criterio inválido.")
            return

        print(
            f"\n--- RESULTADO ({algoritmo.upper()}) ---"
        )

        for tarea in tareas:
            print(
                f"ID: {tarea.id} | "
                f"Prioridad: {tarea.prioridad} | "
                f"{tarea.descripcion}"
            )

    except ValueError as error:
        print(f" {error}")


# ============================================================
# MENÚ DE USUARIO NORMAL
# ============================================================

def menu_usuario(sistema, usuario):
    """Menú para usuarios normales."""

    while True:
        print("\n========================================")
        print("          MENÚ DE USUARIO")
        print("========================================")
        print(f"Usuario: {usuario.nombre}")
        print("========================================")
        print("1. Ver tareas")
        print("2. Buscar tarea")
        print("3. Ver mis tareas")
        print("4. Cambiar estado de una tarea asignada")
        print("5. Ver árbol de tareas")
        print("0. Cerrar sesión")
        print("========================================")

        opcion = input(
            "Seleccione una opción: "
        ).strip()

        try:

            if opcion == "1":
                listar_tareas_pendientes(sistema)

            elif opcion == "2":
                buscar_tarea(sistema)

            elif opcion == "3":
                listar_mis_tareas(
                    sistema,
                    usuario
                )

            elif opcion == "4":
                cambiar_estado(
                    sistema,
                    usuario
                )

            elif opcion == "5":
                mostrar_arbol(sistema)

            elif opcion == "0":
                return

            else:
                print(" Opción inválida.")

        except (
            ValueError,
            PermissionError,
            AttributeError
        ) as error:
            print(f"\n {error}")

        pausar()


def listar_mis_tareas(sistema, usuario):
    """Lista las tareas asignadas al usuario."""

    print("\n--- MIS TAREAS ---")

    tareas = sistema.tarea_service.listar_tareas()

    encontradas = False

    for tarea in tareas:

        if tarea.responsable_id == usuario.id:
            mostrar_tarea(tarea)
            encontradas = True

    if not encontradas:
        print(
            "No tiene tareas asignadas."
        )


# ============================================================
# MENÚ ADMINISTRADOR
# ============================================================

def menu_administrador(sistema, usuario):
    """Menú completo del administrador."""

    while True:
        print("\n========================================")
        print("       MENÚ DE ADMINISTRADOR")
        print("========================================")
        print(f"Administrador: {usuario.nombre}")
        print("========================================")
        print("1. Gestión de usuarios")
        print("2. Gestión de tareas")
        print("3. Deshacer última acción")
        print("4. Rehacer última acción")
        print("5. Ver auditoría")
        print("0. Cerrar sesión")
        print("========================================")

        opcion = input(
            "Seleccione una opción: "
        ).strip()

        try:

            if opcion == "1":
                menu_usuarios(sistema)

            elif opcion == "2":
                menu_tareas(
                    sistema,
                    usuario
                )

            elif opcion == "3":
                deshacer(sistema, usuario)

            elif opcion == "4":
                rehacer(sistema, usuario)

            elif opcion == "5":
                mostrar_auditoria(sistema)

            elif opcion == "0":
                return

            else:
                print(" Opción inválida.")

        except (
            ValueError,
            PermissionError,
            AttributeError
        ) as error:
            print(f"\n {error}")

        pausar()


def deshacer(sistema, usuario):
    """Ejecuta Undo."""

    accion = sistema.deshacer(usuario)

    if accion is None:
        print(
            "\n No hay acciones para deshacer."
        )
        return

    print(
        "\n Acción deshecha correctamente:"
    )

    print(
        f"Tipo: {accion.tipo}"
    )

    print(
        f"Descripción: {accion.descripcion}"
    )


def rehacer(sistema, usuario):
    """Ejecuta Redo."""

    accion = sistema.rehacer(usuario)

    if accion is None:
        print(
            "\n No hay acciones para rehacer."
        )
        return

    print(
        "\n Acción rehecha correctamente:"
    )

    print(
        f"Tipo: {accion.tipo}"
    )

    print(
        f"Descripción: {accion.descripcion}"
    )



def mostrar_auditoria(sistema):
    """Muestra la bitácora de auditoría."""

    print("\n========================================")
    print("            AUDITORÍA")
    print("========================================")

    try:
        registros = sistema.auditoria.listar()
    except AttributeError:
        registros = []

    if not registros:
        print("No existen registros de auditoría.")
        return

    for registro in registros:
        print(registro)




# ============================================================
# PROGRAMA PRINCIPAL
# ============================================================

def main():
    """Ejecuta el programa."""

    try:
        sistema = SistemaService()

    except Exception as error:
        print(
            "\n Error al iniciar el sistema:"
        )
        print(error)
        return

    while True:

        usuario = iniciar_sesion(sistema)

        if usuario is None:
            print(
                "\n Programa finalizado."
            )
            break

        if sistema.puede_administrar(usuario):
            menu_administrador(
                sistema,
                usuario
            )

        else:
            menu_usuario(
                sistema,
                usuario
            )

        print(
            "\n Sesión cerrada."
        )


if __name__ == "__main__":
    main()

