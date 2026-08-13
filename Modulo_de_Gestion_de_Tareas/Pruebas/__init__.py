import os
import sys

# Determina la ruta raíz del paquete 'Modulo de Gestion de Tareas'
# (sube un nivel desde la carpeta 'Pruebas')
RAIZ_MODULO = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

# Agrega la ruta raíz al sys.path si aún no está presente
if RAIZ_MODULO not in sys.path:
    sys.path.insert(0, RAIZ_MODULO)