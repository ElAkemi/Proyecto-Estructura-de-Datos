# =========================================================
#                  ORDENAMIENTOS.PY
# =========================================================
#
# Este archivo contiene los tres métodos de ordenamiento
# pedidos en el proyecto.
#
# Según la aclaratoria nueva del profesor, los métodos
# llamados Merge Sort y Quick Sort deben conservar esos
# nombres, pero internamente deben usar el algoritmo
# Burbuja.
#
# Por eso:
# - burbuja() hace el ordenamiento real.
# - merge_sort() llama a burbuja().
# - quick_sort() llama a burbuja().
# =========================================================


# =========================================================
#              FUNCIÓN: obtener_prioridad
# =========================================================

def obtener_prioridad(tarea):

    # En el proyecto las tareas pueden tener prioridades
    # como ALTA, MEDIA o BAJA.
    #
    # Para poder ordenarlas fácilmente, convertimos esas
    # palabras a números.
    #
    # ALTA = 1 porque queremos que aparezca primero.
    # MEDIA = 2.
    # BAJA = 3 porque queremos que aparezca después.
    prioridades = {
        "ALTA": 1,
        "MEDIA": 2,
        "BAJA": 3
    }

    # Mientras todavía no está integrado el código de
    # Valeria, las tareas pueden estar representadas como
    # diccionarios.
    #
    # Ejemplo:
    #
    # {
    #     "id": 1,
    #     "prioridad": "ALTA",
    #     "descripcion": "Respaldar datos"
    # }
    #
    # Por eso primero preguntamos si "tarea" es un
    # diccionario.
    if isinstance(tarea, dict):

        # get() busca el dato llamado "prioridad".
        #
        # Si por alguna razón no existe ese dato,
        # usamos "BAJA" como valor por defecto para evitar
        # que el programa se caiga.
        prioridad = tarea.get("prioridad", "BAJA")

    else:

        # Más adelante Valeria puede entregar una clase
        # llamada Tarea.
        #
        # En ese caso ya no tendríamos algo como:
        #
        # tarea["prioridad"]
        #
        # sino algo como:
        #
        # tarea.prioridad
        #
        # getattr() nos permite obtener ese atributo.
        #
        # También usamos "BAJA" si no existe.
        prioridad = getattr(tarea, "prioridad", "BAJA")

    # Convertimos la prioridad a texto y luego a mayúsculas.
    #
    # Esto evita problemas si alguien escribió:
    #
    # alta
    # Alta
    # ALTA
    #
    # Todas terminarán siendo "ALTA".
    prioridad = str(prioridad).upper()

    # Buscamos la prioridad en el diccionario.
    #
    # Por ejemplo:
    #
    # "ALTA" devuelve 1.
    # "MEDIA" devuelve 2.
    # "BAJA" devuelve 3.
    #
    # Si aparece una prioridad desconocida, usamos 3
    # para tratarla como prioridad baja.
    return prioridades.get(prioridad, 3)


# =========================================================
#                 ORDENAMIENTO BURBUJA
# =========================================================

def burbuja(lista):

    # copy() crea una copia de la lista recibida.
    #
    # Esto es importante porque así podemos ordenar los
    # elementos sin cambiar directamente la lista original.
    lista_ordenada = lista.copy()

    # len() nos dice cuántos elementos hay en la lista.
    #
    # Por ejemplo:
    #
    # [Tarea1, Tarea2, Tarea3]
    #
    # tendría una cantidad de 3.
    cantidad = len(lista_ordenada)

    # El algoritmo Burbuja necesita recorrer la lista
    # varias veces.
    #
    # La variable "i" representa el número del recorrido
    # que estamos realizando.
    for i in range(cantidad):

        # Esta variable sirve para saber si durante un
        # recorrido tuvimos que mover algún elemento.
        #
        # Si nadie se mueve, significa que la lista ya
        # está ordenada y podemos terminar antes.
        hubo_cambio = False

        # En cada recorrido comparamos elementos que están
        # uno al lado del otro.
        #
        # Por ejemplo:
        #
        # ALTA - BAJA - MEDIA
        #
        # primero compara ALTA con BAJA,
        # después BAJA con MEDIA.
        #
        # "cantidad - i - 1" evita volver a revisar
        # posiciones que ya quedaron ordenadas al final.
        for j in range(0, cantidad - i - 1):

            # Obtenemos el valor numérico de la prioridad
            # de la tarea actual.
            prioridad_actual = obtener_prioridad(
                lista_ordenada[j]
            )

            # Obtenemos la prioridad de la tarea que está
            # inmediatamente después.
            prioridad_siguiente = obtener_prioridad(
                lista_ordenada[j + 1]
            )

            # Recordemos:
            #
            # ALTA = 1
            # MEDIA = 2
            # BAJA = 3
            #
            # Entonces, si prioridad_actual es mayor,
            # significa que tiene MENOS prioridad y debe
            # ir después.
            #
            # Ejemplo:
            #
            # BAJA = 3
            # ALTA = 1
            #
            # Como 3 > 1, intercambiamos sus posiciones.
            if prioridad_actual > prioridad_siguiente:

                # Guardamos temporalmente la tarea actual.
                #
                # Esto es necesario para no perderla cuando
                # hagamos el intercambio.
                temporal = lista_ordenada[j]

                # Colocamos la tarea siguiente en la
                # posición actual.
                lista_ordenada[j] = lista_ordenada[j + 1]

                # Colocamos la tarea que habíamos guardado
                # en la posición siguiente.
                lista_ordenada[j + 1] = temporal

                # Indicamos que sí ocurrió al menos un
                # intercambio durante este recorrido.
                hubo_cambio = True

        # Si terminamos todo el recorrido y no hubo ningún
        # intercambio, significa que ya todo está en el
        # orden correcto.
        #
        # Entonces usamos break para salir del ciclo
        # y evitar hacer recorridos innecesarios.
        if hubo_cambio == False:
            break

    # Finalmente devolvemos la nueva lista ya ordenada.
    return lista_ordenada


# =========================================================
#                    MERGE SORT
# =========================================================

def merge_sort(lista):

    # Normalmente Merge Sort tiene su propio algoritmo.
    #
    # Sin embargo, la aclaratoria oficial del profesor
    # indica que este método debe mantener el nombre
    # "Merge Sort", pero utilizar internamente únicamente
    # el algoritmo Burbuja.
    #
    # Por eso simplemente enviamos la lista a burbuja().
    lista_ordenada = burbuja(lista)

    # Devolvemos la lista que Burbuja ya ordenó.
    return lista_ordenada


# =========================================================
#                    QUICK SORT
# =========================================================

def quick_sort(lista):

    # Igual que con Merge Sort, normalmente Quick Sort
    # tendría su propio procedimiento.
    #
    # Pero por la aclaratoria del proyecto debemos mantener
    # el nombre quick_sort() y utilizar Burbuja internamente.
    lista_ordenada = burbuja(lista)

    # Devolvemos el resultado ya ordenado.
    return lista_ordenada