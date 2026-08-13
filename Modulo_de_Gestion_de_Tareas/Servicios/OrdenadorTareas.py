""" 
Este archivo tiene la funcion de tomar una lista detareas y devolver una
lista de ordenada segun el criterio especificado y en la direccion deseada.  
"""
class OrdenadorTareas:
    @staticmethod # Todos los metodos son estaticos
    def mergesort(lista_tareas, clave=lambda x: x.id_tarea, reverso=False): #Una función que extrae el valor por el cual se compararán los objetos. Por defecto, busca la propiedad id_tarea.
        if len(lista_tareas) <= 1:
            return list(lista_tareas) #Si la lista tiene 0 o 1 elementos, ya está ordenada, por lo que la devuelve convertida en lista.

        #Encuentra el punto medio y divide la lista en dos mitades izquierda y derecha, ordenando cada mitad recursivamente.
        medio = len(lista_tareas) // 2
        izquierda = OrdenadorTareas.mergesort(lista_tareas[:medio], clave, reverso)
        derecha = OrdenadorTareas.mergesort(lista_tareas[medio:], clave, reverso)

        #Combina las dos listas ordenadas utilizando el método privado auxiliar _mezclar.
        return OrdenadorTareas._mezclar(izquierda, derecha, clave, reverso)

    @staticmethod
    def _mezclar(izq, der, clave, reverso):
        resultado = []
        i = j = 0 #Inicializa la lista resultante y los punteros i y j.

        """ 
        Recorre ambas listas comparando elemento por elemento según el 
        criterio (clave) y el sentido (reverso). Inserta el elemento 
        correspondiente en resultado e incrementa el puntero adecuado.
        """
        while i < len(izq) and j < len(der):
            val_izq = clave(izq[i])
            val_der = clave(der[j])
            condicion = (val_izq >= val_der) if reverso else (val_izq <= val_der)
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
    def bubblesort(lista_tareas, clave=lambda x: x.id_tarea, reverso=False):
        copia = list(lista_tareas) # Crea una copia d la lista para no modificar la original. 
        n = len(copia)
        for i in range(n):
            intercambio = False
            for j in range(0, n - i - 1):
                val_actual = clave(copia[j])
                val_siguiente = clave(copia[j + 1])
                condicion = (val_actual < val_siguiente) if reverso else (val_actual > val_siguiente)
                if condicion:
                    copia[j], copia[j + 1] = copia[j + 1], copia[j]
                    intercambio = True
            if not intercambio:
                break
        return copia

    @staticmethod
    def quicksort(lista_tareas, clave=lambda x: x.id_tarea, reverso=False):
        # Primer caso si tiene 0 o 1 elemento y retorna la lista tal y como es.
        if len(lista_tareas) <= 1:
            return list(lista_tareas)

        # Selecciona el elemento central como pivote, calcula su valor con clave y crea tres listas para clasificar los elementos respecto al pivote.
        pivote = lista_tareas[len(lista_tareas) // 2]
        val_pivote = clave(pivote)

        menores = []
        iguales = []
        mayores = []


        #Recorre todos los elementos y los distribuye en menores, iguales o mayores según su valor comparado contra el pivote.
        for elem in lista_tareas:
            v = clave(elem)
            if v == val_pivote:
                iguales.append(elem)
            elif v < val_pivote:
                menores.append(elem)
            else:
                mayores.append(elem)
        
        # Llama recursivamente a quicksort sobre las sublistas y las concatena.
        if reverso:
            return OrdenadorTareas.quicksort(mayores, clave, reverso) + iguales + OrdenadorTareas.quicksort(menores, clave, reverso)
        else:
            return OrdenadorTareas.quicksort(menores, clave, reverso) + iguales + OrdenadorTareas.quicksort(mayores, clave, reverso)