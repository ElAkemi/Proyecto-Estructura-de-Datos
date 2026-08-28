import csv
import os

from models.usuario import Usuario


class UsuarioRepository:
    """Gestiona la persistencia de usuarios mediante CSV."""

    ENCABEZADOS = [
        "id",
        "nombre",
        "rol",
        "password",
    ]

    def __init__(self, ruta="data/usuarios.csv"):
        self.ruta = ruta
        self._asegurar_archivo()

    def _asegurar_archivo(self):
        """Crea el directorio y archivo si no existen."""

        directorio = os.path.dirname(self.ruta)

        if directorio:
            os.makedirs(directorio, exist_ok=True)

        if not os.path.exists(self.ruta):
            with open(
                self.ruta,
                "w",
                newline="",
                encoding="utf-8"
            ) as archivo:

                escritor = csv.writer(archivo)
                escritor.writerow(self.ENCABEZADOS)

    def guardar(self, usuarios):
        """
        Sobrescribe el archivo con el estado actual de usuarios.

        Args:
            usuarios: iterable de objetos Usuario.
        """

        self._asegurar_archivo()

        with open(
            self.ruta,
            "w",
            newline="",
            encoding="utf-8"
        ) as archivo:

            escritor = csv.writer(archivo)

            escritor.writerow(self.ENCABEZADOS)

            for usuario in usuarios:
                escritor.writerow([
                    usuario.id,
                    usuario.nombre,
                    usuario.rol,
                    usuario.password,
                ])

    def cargar(self):
        """
        Carga todos los usuarios almacenados en el CSV.

        Retorna:
            Lista de objetos Usuario.
        """

        self._asegurar_archivo()

        usuarios = []

        with open(
            self.ruta,
            "r",
            newline="",
            encoding="utf-8"
        ) as archivo:

            lector = csv.DictReader(archivo)

            for fila in lector:

                if not fila.get("id"):
                    continue

                try:
                    usuario = Usuario(
                        id=int(fila["id"]),
                        nombre=fila["nombre"],
                        rol=fila["rol"],
                        password=fila["password"],
                    )

                    usuarios.append(usuario)

                except (ValueError, KeyError):
                    # Una fila corrupta no debe provocar
                    # que todo el sistema se cierre.
                    continue

        return usuarios

    def obtener_por_id(self, id_usuario):
        """
        Busca un usuario directamente en el archivo.

        Retorna:
            Usuario o None.
        """

        usuarios = self.cargar()

        for usuario in usuarios:
            if usuario.id == id_usuario:
                return usuario

        return None