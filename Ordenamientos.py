# ============================================================
# ORDENAMIENTOS.PY
# Sistema Gestor de Flujos de Trabajo - Workflow Manager
#
# Este archivo contiene los algoritmos de ordenamiento
# utilizados para ordenar las tareas según su prioridad.
#
# Algoritmos implementados:
# 1. Burbuja
# 2. Merge Sort
# 3. QuickSort
# ============================================================


# ------------------------------------------------------------
# PRIORIDADES
# ------------------------------------------------------------
# Se asigna un número a cada nivel de prioridad.
#
# Mientras menor sea el número, mayor es la prioridad.
#
# Esto permite que los algoritmos puedan comparar fácilmente
# las prioridades de las tareas.
#
# ALTA  -> 1
# MEDIA -> 2
# BAJA  -> 3

PRIORIDADES = {
    "ALTA": 1,
    "MEDIA": 2,
    "BAJA": 3
}


# ------------------------------------------------------------
# OBTENER PRIORIDAD
# ------------------------------------------------------------
def obtener_prioridad(tarea):
    """
    Recibe una tarea y devuelve el valor numérico
    correspondiente a su prioridad.

    Ejemplo:
    Si la prioridad de la tarea es "ALTA",
    esta función devuelve 1.
    """

    # Obtenemos la prioridad de la tarea.
    # upper() convierte el texto a mayúsculas para evitar
    # problemas si llega "alta", "Alta" o "ALTA".
    prioridad = tarea["prioridad"].upper()

    # Buscamos la prioridad dentro del diccionario PRIORIDADES.
    #
    # Si por alguna razón la prioridad no existe,
    # se devuelve 4 para colocarla después de ALTA, MEDIA y BAJA.
    return PRIORIDADES.get(prioridad, 4)


# ============================================================
# ALGORITMO BURBUJA
# ============================================================
def burbuja(lista):
    """
    Ordena una lista de tareas según su prioridad
    utilizando el algoritmo de ordenamiento Burbuja.

    El orden será:
    ALTA -> MEDIA -> BAJA
    """

    # Guardamos la cantidad de elementos que tiene la lista.
    n = len(lista)

    # El primer ciclo controla cuántas veces debemos
    # recorrer la lista.
    for i in range(n - 1):

        # El segundo ciclo compara elementos consecutivos.
        #
        # Se resta "i" porque al finalizar cada recorrido,
        # los elementos del final ya se encuentran ordenados.
        for j in range(n - 1 - i):

            # Obtenemos la prioridad de la tarea actual.
            prioridad_actual = obtener_prioridad(lista[j])

            # Obtenemos la prioridad de la siguiente tarea.
            prioridad_siguiente = obtener_prioridad(lista[j + 1])

            # Si la tarea actual tiene menor prioridad
            # que la siguiente, intercambiamos sus posiciones.
            #
            # Por ejemplo:
            # BAJA (3) > ALTA (1)
            #
            # Entonces ALTA debe colocarse primero.
            if prioridad_actual > prioridad_siguiente:

                lista[j], lista[j + 1] = lista[j + 1], lista[j]

    # Devolvemos la lista ya ordenada.
    return lista


# ============================================================
# ALGORITMO MERGE SORT
# ============================================================
def merge_sort(lista):
    """
    Ordena una lista de tareas según su prioridad
    utilizando el algoritmo Merge Sort.

    Merge Sort divide la lista en partes más pequeñas,
    las ordena y después vuelve a unirlas.
    """

    # CASO BASE DE LA RECURSIVIDAD
    #
    # Si la lista tiene un elemento o está vacía,
    # ya se considera ordenada.
    if len(lista) <= 1:
        return lista

    # Buscamos la posición central de la lista.
    mitad = len(lista) // 2

    # Dividimos la lista en dos partes.
    izquierda = lista[:mitad]
    derecha = lista[mitad:]

    # Llamamos nuevamente a merge_sort para ordenar
    # cada mitad de forma recursiva.
    izquierda = merge_sort(izquierda)
    derecha = merge_sort(derecha)

    # Cuando las dos partes están ordenadas,
    # utilizamos la función mezclar para unirlas.
    return mezclar(izquierda, derecha)


# ------------------------------------------------------------
# FUNCIÓN AUXILIAR PARA MERGE SORT
# ------------------------------------------------------------
def mezclar(izquierda, derecha):
    """
    Recibe dos listas previamente ordenadas y las combina
    en una nueva lista respetando la prioridad de las tareas.
    """

    # Aquí guardaremos el resultado final.
    resultado = []

    # Estos índices permiten recorrer las dos listas.
    i = 0
    j = 0

    # Mientras todavía existan elementos en ambas listas,
    # seguimos comparando sus prioridades.
    while i < len(izquierda) and j < len(derecha):

        # Obtenemos la prioridad del elemento de la izquierda.
        prioridad_izquierda = obtener_prioridad(izquierda[i])

        # Obtenemos la prioridad del elemento de la derecha.
        prioridad_derecha = obtener_prioridad(derecha[j])

        # Si el elemento izquierdo tiene una prioridad
        # mayor o igual en importancia, lo agregamos primero.
        if prioridad_izquierda <= prioridad_derecha:

            resultado.append(izquierda[i])

            # Avanzamos al siguiente elemento de la izquierda.
            i += 1

        else:

            # Si el elemento derecho tiene mayor prioridad,
            # agregamos ese elemento.
            resultado.append(derecha[j])

            # Avanzamos al siguiente elemento de la derecha.
            j += 1

    # Si quedaron elementos sin agregar en la lista izquierda,
    # los agregamos al resultado.
    resultado.extend(izquierda[i:])

    # Si quedaron elementos sin agregar en la lista derecha,
    # también los agregamos.
    resultado.extend(derecha[j:])

    # Devolvemos la lista combinada y ordenada.
    return resultado


# ============================================================
# ALGORITMO QUICK SORT
# ============================================================
def quick_sort(lista):
    """
    Ordena una lista de tareas según su prioridad
    utilizando el algoritmo QuickSort.

    QuickSort selecciona un elemento llamado pivote
    y divide los demás elementos según su prioridad.
    """

    # CASO BASE DE LA RECURSIVIDAD
    #
    # Una lista vacía o con un solo elemento
    # ya está ordenada.
    if len(lista) <= 1:
        return lista

    # Seleccionamos como pivote el elemento
    # ubicado en el centro de la lista.
    pivote = lista[len(lista) // 2]

    # Obtenemos el valor numérico de la prioridad del pivote.
    prioridad_pivote = obtener_prioridad(pivote)

    # Creamos tres listas.
    #
    # menores:
    # tareas con mayor importancia que el pivote.
    #
    # iguales:
    # tareas con la misma prioridad que el pivote.
    #
    # mayores:
    # tareas con menor importancia que el pivote.
    menores = []
    iguales = []
    mayores = []

    # Recorremos todas las tareas.
    for tarea in lista:

        # Obtenemos la prioridad de la tarea actual.
        prioridad_tarea = obtener_prioridad(tarea)

        # Si el número es menor que el del pivote,
        # significa que tiene una prioridad más alta.
        if prioridad_tarea < prioridad_pivote:

            menores.append(tarea)

        # Si tiene la misma prioridad que el pivote,
        # se guarda en la lista de iguales.
        elif prioridad_tarea == prioridad_pivote:

            iguales.append(tarea)

        # Si el número es mayor, significa que
        # tiene una prioridad más baja.
        else:

            mayores.append(tarea)

    # Ordenamos recursivamente las listas de menores
    # y mayores y después unimos todos los resultados.
    return quick_sort(menores) + iguales + quick_sort(mayores)

