from structures.pila import Pila


class HistorialService:
    def __init__(self, lista_usuarios, repository):
        self.lista_usuarios = lista_usuarios
        self.repository = repository

        self.pila_deshacer = Pila()  # Acciones que se pueden deshacer
        self.pila_rehacer = Pila()  # Acciones que se pueden rehacer
        

    def registrar_accion(self, accion):
       self.pila_deshacer.apilar(accion)
       self.pila_rehacer = Pila()  # Limpiar la pila de rehacer al registrar una nueva acción

    def deshacer_accion(self):
        # No hay acciones para deshacer
        if self.pila_deshacer.esta_vacia():
            return None

        accion = self.pila_deshacer.desapilar()

        if accion.tipo == "AGREGAR":
           self.lista_usuarios.eliminar(accion.datos.id)
        elif accion.tipo == "ELIMINAR":
           self.lista_usuarios.insertar(accion.datos)
        elif accion.tipo == "MODIFICAR":
            usuario = accion.datos["anterior"]
            self.lista_usuarios.modificar(
                usuario.id,
                usuario.nombre,
                usuario.rol
            )

        self.pila_rehacer.apilar(accion)

        self.repository.guardar_usuarios(self.lista_usuarios)

        return accion

    def rehacer_accion(self):
        # No hay acciones para rehacer
        if self.pila_rehacer.esta_vacia():
            return None

        accion = self.pila_rehacer.desapilar()

        if accion.tipo == "AGREGAR":
           self.lista_usuarios.insertar(accion.datos)
        elif accion.tipo == "ELIMINAR":
           self.lista_usuarios.eliminar(accion.datos.id)
        elif accion.tipo == "MODIFICAR":
            usuario = accion.datos["nuevo"]
            self.lista_usuarios.modificar(
                usuario.id,
                usuario.nombre,
                usuario.rol
            )

        self.pila_deshacer.apilar(accion)

        self.repository.guardar_usuarios(self.lista_usuarios)

        return accion