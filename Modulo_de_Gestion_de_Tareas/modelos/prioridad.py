from enum import Enum # Para crear tipos de enumeración con un conjunto fijo de constantes.

class Prioridad(Enum):
    BAJA = 1
    MEDIA = 2
    ALTA = 3

    @classmethod # El método recibe la propia clase (cls) como primer parámetro en lugar de una instancia.
    def desde_texto(cls, texto: str):
        if isinstance(texto, cls): # Si el argumento recibido ya es un objeto de tipo Prioridad. De ser así, lo retorna directamente sin necesidad de transformarlo.
            return texto
        mapping = { # Relaciona las cadenas de texto en mayúsculas con sus miembros correspondientes de la enumeración.
            "BAJA": cls.BAJA,
            "MEDIA": cls.MEDIA,
            "ALTA": cls.ALTA
        }
        #Convierte a texto con str().
        #Pasa todo a mayúsculas con .upper().
        #Quita espacios innecesarios al inicio o final con .strip().
        return mapping.get(str(texto).upper().strip(), cls.BAJA)

    def __str__(self): # Define cómo se representará el objeto cuando se convierta a texto.
        return self.name # Retorna el nombre del miembro de la enumeración como cadena.