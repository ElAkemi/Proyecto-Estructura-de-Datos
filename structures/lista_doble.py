from models import usuario
from structures.nodo_usuario import NodoUsuario

class ListaDoble:
    def __init__(self):
        self.cabeza = None
        self.cola = None

    def insertar(self, usuario):
        #Verificar si el ID del usuario ya existe en la lista
        if self.buscar(usuario.id):
            print("Ese ID ya existe.")
            return False
    
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
        actual = self.cabeza

        #Recorre la lista desde la cabeza hasta la cola para buscar un usuario por su ID y modificar su nombre
        while actual is not None:
            if actual.usuario.id == id:
                actual.usuario.nombre = nuevo_nombre
                actual.usuario.rol = nuevo_rol
                
                # Retorna True si se modificó el usuario
                return True  
            actual = actual.siguiente

         # Retorna False si no se encontró el usuario con el ID especificado
        return False  # Retorna False si no se encontró el usuario con el ID especificado

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
                    # Si la nueva cabeza no es None, actualizar su puntero anterior a None
                    if self.cabeza is not None:
                        self.cabeza.anterior = None

                # Si el nodo a eliminar es la cola
                elif actual == self.cola:
                    self.cola = actual.anterior
                    # Si la nueva cola no es None, actualizar su puntero siguiente a None
                    if self.cola is not None:
                        self.cola.siguiente = None

                else:
                    # Conectar el nodo anterior con el siguiente, eliminando el nodo actual de la lista (esta entre la cabeza y la cola)
                    actual.anterior.siguiente = actual.siguiente
                    # Si el nodo siguiente no es None, actualizar su puntero anterior
                    if actual.siguiente is not None:
                        actual.siguiente.anterior = actual.anterior

                # Retorna True si se eliminó el usuario, como quedo aislado python lo elimina automáticamente de la memoria
                return True
            actual = actual.siguiente
            # Retorna False si no se encontró el usuario con el ID especificado
        return False