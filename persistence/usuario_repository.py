import csv
from models.usuario import Usuario

class UsuarioRepository:
    def __init__(self, archivo_csv):
        self.archivo_csv = archivo_csv

    def guardar_usuarios(self, lista_usuarios):
        with open(self.archivo_csv, mode="w", newline="", encoding="utf-8") as archivo:
            writer = csv.writer(archivo)

            for nodo in self.recorrer_lista_usuarios(lista_usuarios):
                usuario = nodo.usuario
                writer.writerow([usuario.id, usuario.nombre, usuario.rol])

    def cargar_usuarios(self, lista_usuarios):
        try:
            with open(self.archivo_csv, "r", newline="", encoding="utf-8") as archivo:
                reader = csv.reader(archivo)

                for row in reader:

                    # La fila debe tener ID, nombre y rol
                    if len(row) != 3:
                        continue

                    try:
                        id = int(row[0])
                        nombre = row[1]
                        rol = row[2]

                        usuario = Usuario(id, nombre, rol)
                        lista_usuarios.insertar(usuario)

                    except ValueError:
                        # Ignorar registros inválidos del CSV
                        continue

        except FileNotFoundError:
            # Si el archivo no existe, no hay usuarios que cargar
            pass
                
    def recorrer_lista_usuarios(self, lista_usuarios):
        # Este método debería recorrer la lista de usuarios y devolver los nodos
        # Aquí se asume que self.lista_usuarios es una instancia de ListaDoble
        nodo_actual = lista_usuarios.cabeza

        while nodo_actual is not None:
            yield nodo_actual
            nodo_actual = nodo_actual.siguiente