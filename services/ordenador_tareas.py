class OrdenadorTareas:
    """
    Implementa tres algoritmos de ordenamiento:

    1. Burbuja
    2. Merge Sort
    3. Quick Sort
    """

    @staticmethod
    def burbuja(tareas, clave):
        """
        Ordenamiento Bubble Sort.

        Complejidad:
            Mejor caso: O(n)
            Caso promedio: O(n²)
            Peor caso: O(n²)

        Espacio adicional:
            O(1)
        """

        resultado = list(tareas)
        n = len(resultado)

        for i in range(n):

            intercambio = False

            for j in range(0, n - i - 1):

                if clave(resultado[j]) > clave(
                    resultado[j + 1]
                ):
                    resultado[j], resultado[j + 1] = (
                        resultado[j + 1],
                        resultado[j]
                    )

                    intercambio = True

            if not intercambio:
                break

        return resultado

    @classmethod
    def merge_sort(cls, tareas, clave):
        """
        Ordenamiento Merge Sort.

        Complejidad:
            Mejor caso: O(n log n)
            Caso promedio: O(n log n)
            Peor caso: O(n log n)

        Espacio adicional:
            O(n)
        """

        if len(tareas) <= 1:
            return list(tareas)

        mitad = len(tareas) // 2

        izquierda = cls.merge_sort(
            tareas[:mitad],
            clave
        )

        derecha = cls.merge_sort(
            tareas[mitad:],
            clave
        )

        return cls._mezclar(
            izquierda,
            derecha,
            clave
        )

    @staticmethod
    def _mezclar(izquierda, derecha, clave):

        resultado = []

        i = 0
        j = 0

        while i < len(izquierda) and j < len(derecha):

            if clave(izquierda[i]) <= clave(derecha[j]):
                resultado.append(izquierda[i])
                i += 1

            else:
                resultado.append(derecha[j])
                j += 1

        while i < len(izquierda):
            resultado.append(izquierda[i])
            i += 1

        while j < len(derecha):
            resultado.append(derecha[j])
            j += 1

        return resultado

    @classmethod
    def quick_sort(cls, tareas, clave):
        """
        Ordenamiento Quick Sort.

        Complejidad:
            Mejor caso: O(n log n)
            Caso promedio: O(n log n)
            Peor caso: O(n²)

        Espacio:
            O(n) debido a las listas auxiliares
            utilizadas en esta implementación.
        """

        if len(tareas) <= 1:
            return list(tareas)

        pivote = tareas[len(tareas) // 2]

        valor_pivote = clave(pivote)

        menores = [
            tarea
            for tarea in tareas
            if clave(tarea) < valor_pivote
        ]

        iguales = [
            tarea
            for tarea in tareas
            if clave(tarea) == valor_pivote
        ]

        mayores = [
            tarea
            for tarea in tareas
            if clave(tarea) > valor_pivote
        ]

        return (
            cls.quick_sort(menores, clave)
            + iguales
            + cls.quick_sort(mayores, clave)
        )