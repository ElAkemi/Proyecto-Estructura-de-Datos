from structures.nodo_usuario import NodoUsuario

class ListaDoble:
    def __init__(self):
        self.cabeza = None
        self.cola = None

    def insertar(self, usuario):
        nuevo_nodo = NodoUsuario(usuario)

        #Si la lista está vacía, el nuevo nodo se convierte en la cabeza y la cola
        if self.cabeza is None:
            self.cabeza = nuevo_nodo
            self.cola = nuevo_nodo
        else:
            #Conectar el nuevo nodo al final de la lista
            nuevo_nodo.anterior = self.cola
            self.cola.siguiente = nuevo_nodo

            #Actualizar la cola para que apunte al nuevo nodo
            self.cola = nuevo_nodo 
        return True

    def mostrar(self):
        if self.cabeza is None:
            print("La lista está vacía")
            return
        
        nodo_actual = self.cabeza
        #Recorre la lista desde la cabeza hasta la cola y muestra los datos de cada usuario
        while nodo_actual is not None:
            print(f"ID: {nodo_actual.usuario.id}, Nombre: {nodo_actual.usuario.nombre}, Rol: {nodo_actual.usuario.rol}")
            nodo_actual = nodo_actual.siguiente

    def buscar(self, id):
        nodo_actual = self.cabeza
        #Recorre la lista desde la cabeza hasta la cola para buscar un usuario por su ID
        while nodo_actual is not None:

            if nodo_actual.usuario.id == id:
                return nodo_actual.usuario

            nodo_actual = nodo_actual.siguiente
            # Retorna None si no se encuentra el usuario con el ID especificado
        return None  

    def modificar(self, id, nuevo_nombre, nuevo_rol):
        usuario = self.buscar(id)

        usuario.nombre = nuevo_nombre
        usuario.rol = nuevo_rol

        return True

    def eliminar(self, id):
        actual = self.cabeza

        while actual is not None:
            if actual.usuario.id == id:

                 # Si el nodo a eliminar es el único nodo en la lista
                if actual == self.cabeza and actual == self.cola:
                    self.cabeza = None
                    self.cola = None

                # Si el nodo a eliminar es la cabeza
                elif actual == self.cabeza:
                    self.cabeza = actual.siguiente
                    self.cabeza.anterior = None

                # Si el nodo a eliminar es la cola
                elif actual == self.cola:
                    self.cola = actual.anterior
                    self.cola.siguiente = None

                else:
                    # Conectar el nodo anterior con el siguiente, eliminando el nodo actual de la lista (esta entre la cabeza y la cola)
                    actual.anterior.siguiente = actual.siguiente
                    actual.siguiente.anterior = actual.anterior
                # Retorna True si el usuario fue eliminado
                return True
            actual = actual.siguiente
            # Retorna False si no se encontró el usuario con el ID especificado
        return False