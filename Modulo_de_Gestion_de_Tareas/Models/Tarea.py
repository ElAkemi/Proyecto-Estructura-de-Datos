try:
    from .Prioridad import Prioridad
except (ImportError, ValueError):
    from .Prioridad import Prioridad
class Tarea:
    def __init__(self, id_tarea: int, descripcion: str, prioridad: Prioridad, id_usuario: int, completada: bool = False):
        self.id_tarea = int(id_tarea) # Conversión a entero para garantizar que el ID sea numérico.
        self.descripcion = str(descripcion) # Asegura que la descripción se almacene como texto.
        # Si prioridad ya es un objeto de tipo Prioridad, lo asigna directamente; de lo contrario, usa el método de conversión Prioridad.desde_texto(...) para transformar una cadena.
        self.prioridad = Prioridad.desde_texto(prioridad) if not isinstance(prioridad, Prioridad) else prioridad
        self.id_usuario = int(id_usuario) # Asigna el ID del usuario responsable asegurando tipo entero.
        self.completada = bool(completada) # Booleano que rastrea el estado de avance de la tarea.

    @property # Permite acceder al atributo tarea.estado.
    def estado(self) -> str:
        return "Completada" if self.completada else "Pendiente"

    @estado.setter # Permite reasignar el estado mediante sintaxis de atribución.
    def estado(self, valor: str):
        if isinstance(valor, bool):
            self.completada = valor # Actualiza self.completada directamente.
        elif isinstance(valor, str):
            self.completada = (valor.strip().lower() in ["completada", "done", "true", "1"])
            
    def to_csv_row(self) -> list:
        # Formato: CREAR_TAREA, id_tarea, prioridad, id_usuario, descripcion, estado.
        return ["CREAR_TAREA", str(self.id_tarea), self.prioridad.name, str(self.id_usuario), self.descripcion, self.estado]

    # Define como como se imprime el objeto cuando se llama en consola.
    def __repr__(self):
        return f"Tarea(ID={self.id_tarea}, Prioridad={self.prioridad.name}, Usuario={self.id_usuario}, Estado={self.estado}, Desc='{self.descripcion}')"