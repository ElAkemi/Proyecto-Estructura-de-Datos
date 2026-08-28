class Usuario:
    def __init__(self, id, nombre, rol):
        self.id = id
        self.nombre = nombre
        # Validar que el rol sea "Administrador" o "Usuario"
        if rol not in ("Administrador", "Usuario"):
            raise ValueError("Rol inválido.")
        
        self.rol = rol