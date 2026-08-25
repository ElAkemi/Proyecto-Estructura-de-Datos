"""Módulo para la gestión de tareas."""
try:
    from .prioridad import Prioridad
except (ImportError, ValueError):
    from modelos.prioridad import prioridad

class Tarea:
    """Clase para la gestión de tareas."""
    def __init__(self, id_tarea: int, descripcion: str, prioridad: Prioridad, id_usuario: int, completada: bool = False, ciclos_espera: int = 0):
        self.id_tarea = int(id_tarea)
        self.descripcion = str(descripcion)
        self.prioridad = Prioridad.desde_texto(prioridad) if not isinstance(prioridad, Prioridad) else prioridad
        self.id_usuario = int(id_usuario)
        self.completada = bool(completada)
        self.ciclos_espera = int(ciclos_espera)

    def incrementar_ciclo_espera(self):
        """Incrementa el contador de ciclos de espera."""
        self.ciclos_espera += 1

    @property
    def estado(self) -> str:
        """Obtiene el estado de la tarea."""
        return "Completada" if self.completada else "Pendiente"

    @estado.setter
    def estado(self, valor: str):
        """Establece el estado de la tarea."""
        if isinstance(valor, bool):
            self.completada = valor
        elif isinstance(valor, str):
            self.completada = (valor.strip().lower() in ["completada", "done", "true", "1"])
            
    def to_csv_row(self) -> list:
        """Convierte la tarea a una fila CSV."""
        return ["CREAR_TAREA", str(self.id_tarea), self.prioridad.name, str(self.id_usuario), self.descripcion, self.estado]

    def __repr__(self):
        """Representación oficial de la tarea."""
        return f"Tarea(ID={self.id_tarea}, Prioridad={self.prioridad.name}, Usuario={self.id_usuario}, Estado={self.estado}, Desc='{self.descripcion}')"
