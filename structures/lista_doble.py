"""Módulo que implementa una lista doblemente enlazada."""

from structures.nodo_usuario import NodoUsuario


class ListaDoble:
    """Implementa una lista doblemente enlazada de usuarios."""

    def __init__(self):
        """
        Inicializa una lista doblemente enlazada vacía.

        :return: None.
        """

        self.cabeza = None
        self.cola = None

    def insertar(self, usuario):
        """
        Inserta un usuario al final de la lista.

        :param usuario: Usuario que se desea insertar.
        :return: True si se inserta correctamente, False si ya existe.
        """

        if self.buscar(usuario.id) is not None:
            return False

        nuevo_nodo = NodoUsuario(usuario)

        if self.cabeza is None:
            self.cabeza = nuevo_nodo
            self.cola = nuevo_nodo

        else:
            nuevo_nodo.anterior = self.cola
            self.cola.siguiente = nuevo_nodo
            self.cola = nuevo_nodo

        return True

    def mostrar(self):
        """
        Muestra todos los usuarios de la lista.

        :return: None.
        """

        if self.cabeza is None:
            print("La lista está vacía")
            return

        nodo_actual = self.cabeza

        while nodo_actual is not None:
            print(
                f"ID: {nodo_actual.usuario.id}, "
                f"Nombre: {nodo_actual.usuario.nombre}, "
                f"Rol: {nodo_actual.usuario.rol}"
            )

            nodo_actual = nodo_actual.siguiente

    def buscar(self, id):
        """
        Busca un usuario por su ID.

        :param id: ID del usuario.
        :return: Usuario encontrado o None.
        """

        nodo_actual = self.cabeza

        while nodo_actual is not None:

            if nodo_actual.usuario.id == id:
                return nodo_actual.usuario

            nodo_actual = nodo_actual.siguiente

        return None

    def modificar(self, id, nuevo_nombre, nuevo_rol):
        """
        Modifica los datos de un usuario.

        :param id: ID del usuario.
        :param nuevo_nombre: Nuevo nombre.
        :param nuevo_rol: Nuevo rol.
        :return: True si se modificó, False si no existe.
        """

        usuario = self.buscar(id)

        if usuario is None:
            return False

        usuario.nombre = nuevo_nombre
        usuario.rol = nuevo_rol

        return True

    def eliminar(self, id):
        """
        Elimina un usuario de la lista.

        :param id: ID del usuario.
        :return: True si se eliminó, False si no existe.
        """

        actual = self.cabeza

        while actual is not None:

            if actual.usuario.id == id:

                if actual == self.cabeza and actual == self.cola:
                    self.cabeza = None
                    self.cola = None

                elif actual == self.cabeza:
                    self.cabeza = actual.siguiente
                    self.cabeza.anterior = None

                elif actual == self.cola:
                    self.cola = actual.anterior
                    self.cola.siguiente = None

                else:
                    actual.anterior.siguiente = actual.siguiente
                    actual.siguiente.anterior = actual.anterior

                return True

            actual = actual.siguiente

        return False