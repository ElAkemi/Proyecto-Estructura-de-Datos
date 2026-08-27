"""
Este archivo tiene la funcion de tomar una lista de tareas y devolver una
lista ordenada segun el criterio especificado y en la direccion deseada.
"""


class OrdenadorTareas:

    @staticmethod
    def mergesort(
        lista_tareas,
        clave=lambda x: x.id_tarea,
        reverso=False
    ):
        if len(lista_tareas) <= 1:
            return list(lista_tareas)

        medio = len(lista_tareas) // 2

        izquierda = OrdenadorTareas.mergesort(
            lista_tareas[:medio],
            clave,
            reverso
        )

        derecha = OrdenadorTareas.mergesort(
            lista_tareas[medio:],
            clave,
            reverso
        )

        return OrdenadorTareas._mezclar(
            izquierda,
            derecha,
            clave,
            reverso
        )

    @staticmethod
    def _mezclar(izq, der, clave, reverso):
        resultado = []
        i = j = 0

        """
        Recorre ambas listas comparando elemento por elemento según el
        criterio (clave) y el sentido (reverso). Inserta el elemento
        correspondiente en resultado e incrementa el puntero adecuado.
        """

        while i < len(izq) and j < len(der):

            val_izq = clave(izq[i])
            val_der = clave(der[j])

            condicion = (
                val_izq >= val_der
                if reverso
                else val_izq <= val_der
            )

            if condicion:
                resultado.append(izq[i])
                i += 1
            else:
                resultado.append(der[j])
                j += 1

        """
        Copia cualquier elemento restante que haya quedado sin comparar
        en la lista izquierda o derecha y retorna el resultado combinado.
        """

        resultado.extend(izq[i:])
        resultado.extend(der[j:])

        return resultado

    @staticmethod
    def bubblesort(
        lista_tareas,
        clave=lambda x: x.id_tarea,
        reverso=False
    ):
        copia = list(lista_tareas)
        n = len(copia)

        """
        Repasa la lista varias veces. En cada pasada (controlada por 'i'),
        compara pares adyacentes e intercambia si están en el orden incorrecto,
        moviendo los elementos más "grandes" (o pequeños, según 'reverso') hacia el final.
        """

        for i in range(n):

            intercambio = False

            for j in range(0, n - i - 1):

                val_actual = clave(copia[j])
                val_siguiente = clave(copia[j + 1])

                condicion = (
                    val_actual < val_siguiente
                    if reverso
                    else val_actual > val_siguiente
                )

                if condicion:
                    copia[j], copia[j + 1] = (
                        copia[j + 1],
                        copia[j]
                    )

                    intercambio = True

            if not intercambio:
                break

        return copia

    @staticmethod
    def quicksort(
        lista_tareas,
        clave=lambda x: x.id_tarea,
        reverso=False
    ):
        """
        Toma un elemento como "pivote" y divide el resto en dos grupos:
        menores y mayores. Luego se repite el proceso en cada subgrupo
        hasta que todo esté ordenado.
        """

        if len(lista_tareas) <= 1:
            return list(lista_tareas)

        pivote = lista_tareas[len(lista_tareas) // 2]
        val_pivote = clave(pivote)

        menores = []
        iguales = []
        mayores = []

        for elem in lista_tareas:

            v = clave(elem)

            if v == val_pivote:
                iguales.append(elem)

            elif v < val_pivote:
                menores.append(elem)

            else:
                mayores.append(elem)

        if reverso:

            return (
                OrdenadorTareas.quicksort(
                    mayores,
                    clave,
                    reverso
                )
                + iguales
                + OrdenadorTareas.quicksort(
                    menores,
                    clave,
                    reverso
                )
            )

        return (
            OrdenadorTareas.quicksort(
                menores,
                clave,
                reverso
            )
            + iguales
            + OrdenadorTareas.quicksort(
                mayores,
                clave,
                reverso
            )
        )