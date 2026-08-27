"""Módulo que implementa una pila."""


from structures.nodo_pila import NodoPila


class Pila:
    """Implementa una estructura de datos tipo pila."""

    def __init__(self):
        """
        Inicializa una pila vacía.

        :return: None.
        """

        self.cima = None

    def apilar(self, accion):
        """
        Agrega una acción a la cima de la pila.

        :param accion: Acción que se desea almacenar.
        :return: None.
        """

        nuevo_nodo = NodoPila(accion)

        # El nuevo nodo apunta al que estaba arriba
        nuevo_nodo.siguiente = self.cima

        # La cima ahora es el nuevo nodo
        self.cima = nuevo_nodo

    def desapilar(self):
        """
        Retira y retorna la acción ubicada en la cima.

        :return: Acción retirada o None si la pila está vacía.
        """

        # La pila está vacía
        if self.cima is None:
            return None

        # Guardar el nodo que está en la cima
        nodo_desapilado = self.cima

        # La cima ahora es el siguiente nodo
        self.cima = self.cima.siguiente

        nodo_desapilado.siguiente = None

        # Retornar la acción del nodo desapilado
        return nodo_desapilado.accion

    def peek(self):
        """
        Consulta la acción ubicada en la cima sin eliminarla.

        :return: Acción en la cima o None.
        """

        # La pila está vacía
        if self.cima is None:
            return None

        return self.cima.accion

    def esta_vacia(self):
        """
        Verifica si la pila está vacía.

        :return: True si está vacía, False en caso contrario.
        """

        return self.cima is None

    def mostrar(self):
        """
        Muestra las acciones almacenadas en la pila.

        :return: None.
        """

        if self.cima is None:
            print("La pila está vacía")
            return

        actual = self.cima

        while actual is not None:
            print(
                f"Tipo: {actual.accion.tipo}, "
                f"Descripción: {actual.accion.descripcion}"
            )

            actual = actual.siguiente