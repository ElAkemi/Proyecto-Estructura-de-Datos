from structures.nodo_usuario import NodoUsuario


class ListaDoble:
    """Implementación de una lista doblemente enlazada."""

    def __init__(self):
        self.cabeza = None
        self.cola = None
        self.tamano = 0

    def insertar(self, usuario):
        """
        Inserta un usuario al final de la lista.

        Retorna:
            True si se insertó correctamente.
            False si ya existe un usuario con el mismo ID.
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

        self.tamano += 1
        return True

    def buscar(self, id_usuario):
        """
        Busca un usuario por su ID.

        Retorna:
            El usuario encontrado o None.
        """

        actual = self.cabeza

        while actual is not None:
            if actual.usuario.id == id_usuario:
                return actual.usuario

            actual = actual.siguiente

        return None

    def eliminar(self, id_usuario):
        """
        Elimina un usuario por su ID.

        Retorna:
            True si se eliminó.
            False si no existe.
        """

        actual = self.cabeza

        while actual is not None:

            if actual.usuario.id == id_usuario:

                # Si tiene nodo anterior.
                if actual.anterior is not None:
                    actual.anterior.siguiente = actual.siguiente
                else:
                    # Es la cabeza.
                    self.cabeza = actual.siguiente

                # Si tiene nodo siguiente.
                if actual.siguiente is not None:
                    actual.siguiente.anterior = actual.anterior
                else:
                    # Es la cola.
                    self.cola = actual.anterior

                self.tamano -= 1
                return True

            actual = actual.siguiente

        return False

    def modificar(self, usuario):
        """
        Modifica los datos de un usuario existente.

        Retorna:
            True si se modificó.
            False si no existe.
        """

        usuario_existente = self.buscar(usuario.id)

        if usuario_existente is None:
            return False

        usuario_existente.nombre = usuario.nombre
        usuario_existente.rol = usuario.rol
        usuario_existente.password = usuario.password

        return True

    def listar(self):
        """Devuelve todos los usuarios en una lista de Python."""

        usuarios = []
        actual = self.cabeza

        while actual is not None:
            usuarios.append(actual.usuario)
            actual = actual.siguiente

        return usuarios

    def esta_vacia(self):
        """Indica si la lista está vacía."""

        return self.cabeza is None

    def __len__(self):
        """Devuelve la cantidad de usuarios."""

        return self.tamano