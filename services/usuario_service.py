from copy import copy

from models.usuario import Usuario
from models.accion import Accion
from structures.lista_doble import ListaDoble
from services.historial_service import HistorialService
from persistence.usuario_repository import UsuarioRepository

class UsuarioService:
    def __init__(self, archivo_csv="data/usuarios.csv"):
        self.lista_usuarios = ListaDoble()
        self.repository = UsuarioRepository(archivo_csv)
        self.historial = HistorialService(self.lista_usuarios, self.repository)
        #Cargar los usuarios desde el archivo CSV al iniciar
        self.repository.cargar_usuarios(self.lista_usuarios)

    def agregar_usuario(self, id, nombre, rol):
        # Validar que el ID sea un número entero
        if not isinstance(id, int) or id <= 0:
            raise ValueError("El ID debe ser un número entero mayor a cero.")
        # Validar que el ID sea único
        if self.lista_usuarios.buscar(id) is not None:
            raise ValueError("El ID ya existe.")
        # Validar que el nombre no esté vacío
        if not isinstance(nombre, str) or not nombre.strip():
            raise ValueError("El nombre no puede estar vacío.")
        # Validar que el rol sea válido
        if rol not in ("Administrador", "Usuario"):
            raise ValueError("Rol inválido.")

        usuario = Usuario(id, nombre, rol)

        self.lista_usuarios.insertar(usuario)

        accion = Accion("AGREGAR", f"Se agregó el usuario: {id}", usuario)

        self.historial.registrar_accion(accion)

        self.repository.guardar_usuarios(self.lista_usuarios)
        
        return True
    
    def modificar_usuario(self, id, nuevo_nombre, nuevo_rol):
        #Buscar el usuario por su ID
        usuario = self.lista_usuarios.buscar(id)
        # Validar que el usuario exista
        if usuario is None:
            raise ValueError("El usuario no existe.")

        # Validar que el nuevo nombre no esté vacío
        if not isinstance(nuevo_nombre, str) or not nuevo_nombre.strip():
            raise ValueError("El nombre no puede estar vacío.")

        # Validar que el nuevo rol sea válido
        if nuevo_rol not in ("Administrador", "Usuario"):
            raise ValueError("Rol inválido.")

        # Guardar el estado anterior del usuario para poder deshacer la acción
        usuario_anterior = copy(usuario)

        self.lista_usuarios.modificar(id, nuevo_nombre, nuevo_rol)

        usuario_modificado = copy(usuario)

        accion = Accion("MODIFICAR", f"Se modificó el usuario: {id}", {"anterior": usuario_anterior, "nuevo": usuario_modificado})

        self.historial.registrar_accion(accion)

        self.repository.guardar_usuarios(self.lista_usuarios)

        return True

    def eliminar_usuario(self, id):
        #Buscar el usuario por su ID
        usuario = self.lista_usuarios.buscar(id)

        # Validar que el usuario exista
        if usuario is None:
            raise ValueError("El usuario no existe.")

        # Guardar el usuario antes de eliminarlo
        usuario_eliminado = copy(usuario)

        self.lista_usuarios.eliminar(id)

        accion = Accion("ELIMINAR", f"Se eliminó el usuario: {id}", usuario_eliminado)

        self.historial.registrar_accion(accion)

        self.repository.guardar_usuarios(self.lista_usuarios)

        return True

    def buscar_usuario(self, id):
        usuario = self.lista_usuarios.buscar(id)
        if usuario is None:
            raise ValueError("El usuario no existe.")
        return usuario
    
    def mostrar_usuarios(self):
        self.lista_usuarios.mostrar()