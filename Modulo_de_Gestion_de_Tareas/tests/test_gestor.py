import unittest
import os

import sys

# Determine the root path of the 'Modulo_de_Gestion_de_Tareas' package
# (one level up from the 'Pruebas' folder)
RAIZ_MODULO = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

# Add the root path to sys.path if it's not already present
# This ensures that imports like 'from Modulo_de_Gestion_de_Tareas...' work
# when the test file is run directly, without relying on __init__.py being loaded.
if RAIZ_MODULO not in sys.path:
    sys.path.insert(0, RAIZ_MODULO)

from Servicios.Gestor_tareas import GestorTareas
from Models.Prioridad import Prioridad
from Models.Tarea import Tarea

class TestGestorTareas(unittest.TestCase):
    """
    Clase de pruebas unitarias para GestorTareas.
    Cada método de prueba verifica una funcionalidad específica del gestor.
    """

    def setUp(self):
        """
        Configuración inicial para cada prueba.
        Se ejecuta antes de cada método de prueba.
        Crea un gestor de tareas nuevo y define una ruta para un CSV de prueba.
        """
        self.ruta_csv_prueba = "test_tareas.csv"
        self.ruta_auditoria_prueba = "test_auditoria_log.csv"
        self.gestor = GestorTareas(ruta_csv=self.ruta_csv_prueba, ruta_log_auditoria=self.ruta_auditoria_prueba)

    def tearDown(self):
        """
        Limpieza después de cada prueba.
        Se ejecuta después de cada método de prueba.
        Elimina los archivos CSV de prueba si existen para no dejar basura.
        """
        if os.path.exists(self.ruta_csv_prueba):
            os.remove(self.ruta_csv_prueba)
        if os.path.exists(self.ruta_auditoria_prueba):
            os.remove(self.ruta_auditoria_prueba)


    def test_crear_tarea(self):
        """
        Prueba la creación de tareas, tanto regulares como urgentes.
        Verifica que las tareas se añadan a las colas correctas y que
        no se puedan crear tareas con IDs duplicados.
        """
        # Crear una tarea regular
        self.gestor.crear_tarea(1, "NORMAL", 100, "Tarea de prueba 1")
        self.assertEqual(len(self.gestor.obtener_todas_tareas()), 1)
        self.assertFalse(self.gestor.cola_regular.esta_vacia())
        self.assertTrue(self.gestor.cola_urgente.esta_vacia())

        # Crear una tarea urgente
        self.gestor.crear_tarea(2, "ALTA", 101, "Tarea urgente")
        self.assertEqual(len(self.gestor.obtener_todas_tareas()), 2)
        self.assertFalse(self.gestor.cola_urgente.esta_vacia())

        # Intentar crear tarea con ID duplicado
        with self.assertRaises(ValueError):
            self.gestor.crear_tarea(1, "NORMAL", 102, "Duplicada")

    def test_actualizar_tarea(self):
        """
        Prueba la actualización de los atributos de una tarea.
        Verifica que se puedan cambiar la descripción, el usuario y la prioridad.
        También confirma que un cambio de prioridad mueva la tarea a la cola correcta.
        """
        self.gestor.crear_tarea(1, "NORMAL", 100, "Descripción original")
        
        # Actualizar descripción y usuario
        self.gestor.actualizar_tarea(1, nueva_descripcion="Nueva descripción", nuevo_id_usuario=105)
        tarea = self.gestor.buscar_tarea(1)
        self.assertEqual(tarea.descripcion, "Nueva descripción")
        self.assertEqual(tarea.id_usuario, 105)

        # Cambiar prioridad a ALTA (debería moverla a la cola de urgentes)
        self.gestor.actualizar_tarea(1, nueva_prioridad_str="ALTA")
        self.assertTrue(self.gestor.cola_regular.esta_vacia())
        self.assertFalse(self.gestor.cola_urgente.esta_vacia())
        self.assertEqual(self.gestor.buscar_tarea(1).prioridad, Prioridad.ALTA)

    def test_eliminar_tarea(self):
        """
        Prueba la eliminación de una tarea.
        Verifica que la tarea sea eliminada del sistema y de las colas.
        """
        self.gestor.crear_tarea(1, "NORMAL", 100, "Para eliminar")
        self.assertTrue(self.gestor.eliminar_tarea(1))
        self.assertIsNone(self.gestor.buscar_tarea(1))
        self.assertEqual(len(self.gestor.obtener_todas_tareas()), 0)
        self.assertFalse(self.gestor.eliminar_tarea(99)) # ID no existente

    def test_agregar_subtarea(self):
        """
        Prueba la adición de una subtarea a una tarea padre existente.
        Verifica que la subtarea se añada correctamente al árbol de la tarea padre.
        """
        self.gestor.crear_tarea(1, "NORMAL", 100, "Tarea Padre")
        self.assertTrue(self.gestor.agregar_subtarea(10, 1, "Subtarea 1"))
        
        # Verificar que la subtarea existe en el árbol
        arbol_padre = self.gestor.arboles_subtareas[1]
        self.assertIsNotNone(arbol_padre.buscar_nodo(10))
        
        # Intentar agregar subtarea a un padre no existente
        self.assertFalse(self.gestor.agregar_subtarea(20, 99, "Subtarea huérfana"))

    def test_procesar_siguiente(self):
        """
        Prueba la lógica de procesamiento de tareas.
        Verifica que las tareas urgentes se procesen antes que las regulares.
        """
        self.gestor.crear_tarea(1, "NORMAL", 100, "Regular 1")
        self.gestor.crear_tarea(2, "ALTA", 101, "Urgente 1")
        self.gestor.crear_tarea(3, "NORMAL", 102, "Regular 2")

        # La primera tarea procesada debe ser la urgente
        primera = self.gestor.procesar_siguiente()
        self.assertEqual(primera.id_tarea, 2)
        
        # La siguiente debe ser la primera regular
        segunda = self.gestor.procesar_siguiente()
        self.assertEqual(segunda.id_tarea, 1)

        # Y así sucesivamente
        tercera = self.gestor.procesar_siguiente()
        self.assertEqual(tercera.id_tarea, 3)
        
        # Finalmente, la cola debe estar vacía
        self.assertIsNone(self.gestor.procesar_siguiente())

    def test_listar_pendientes(self):
        """
        Prueba el filtrado de tareas pendientes.
        Verifica que solo devuelva tareas que no están completadas.
        """
        self.gestor.crear_tarea(1, "NORMAL", 100, "Pendiente 1", completada=False)
        self.gestor.crear_tarea(2, "ALTA", 101, "Completada 1", completada=True)
        self.gestor.crear_tarea(3, "NORMAL", 102, "Pendiente 2", completada=False)

        pendientes = self.gestor.listar_pendientes()
        self.assertEqual(len(pendientes), 2)
        self.assertTrue(all(not t.completada for t in pendientes))

    def test_listar_por_usuario(self):
        """
        Prueba el filtrado de tareas por ID de usuario.
        Verifica que devuelva todas las tareas asignadas a un usuario específico.
        """
        self.gestor.crear_tarea(1, "NORMAL", 100, "Tarea A")
        self.gestor.crear_tarea(2, "ALTA", 101, "Tarea B")
        self.gestor.crear_tarea(3, "NORMAL", 100, "Tarea C")

        tareas_usuario_100 = self.gestor.listar_por_usuario(100)
        self.assertEqual(len(tareas_usuario_100), 2)
        self.assertTrue(all(t.id_usuario == 100 for t in tareas_usuario_100))
        
        tareas_usuario_999 = self.gestor.listar_por_usuario(999)
        self.assertEqual(len(tareas_usuario_999), 0)

    def test_cambiar_estado_tarea(self):
        """
        Prueba el cambio de estado de una tarea (pendiente/completada).
        Verifica la lógica de permisos: un usuario solo puede cambiar sus propias tareas
        a menos que sea administrador.
        """
        self.gestor.crear_tarea(1, "NORMAL", 100, "Tarea para cambiar estado")
        
        # Usuario correcto cambia su propia tarea
        self.assertTrue(self.gestor.cambiar_estado_tarea(1, "Completada", id_usuario_solicitante=100))
        self.assertTrue(self.gestor.buscar_tarea(1).completada)

        # Usuario incorrecto intenta cambiar tarea ajena (debe fallar)
        with self.assertRaises(PermissionError):
            self.gestor.cambiar_estado_tarea(1, "Pendiente", id_usuario_solicitante=101)

        # Administrador puede cambiar cualquier tarea
        self.assertTrue(self.gestor.cambiar_estado_tarea(1, "Pendiente", es_admin=True))
        self.assertFalse(self.gestor.buscar_tarea(1).completada)

    def test_guardado_y_cargado_csv(self):
        """
        Prueba la persistencia de datos guardando y cargando desde un archivo CSV.
        Verifica que el estado del gestor se pueda restaurar correctamente.
        """
        # 1. Preparar estado inicial
        self.gestor.crear_tarea(1, "NORMAL", 100, "Tarea 1 a guardar", auto_guardar=False)
        self.gestor.crear_tarea(2, "ALTA", 101, "Tarea 2 urgente", auto_guardar=False)
        self.gestor.agregar_subtarea(10, 1, "Subtarea de 1", auto_guardar=False)

        # 2. Guardar estado en CSV
        self.assertTrue(self.gestor.guardar_csv())
        self.assertTrue(os.path.exists(self.ruta_csv_prueba))

        # 3. Crear un nuevo gestor y cargar el estado
        nuevo_gestor = GestorTareas(ruta_csv=self.ruta_csv_prueba)
        self.assertTrue(nuevo_gestor.cargar_csv())

        # 4. Verificar que el estado cargado es idéntico al original
        self.assertEqual(len(self.gestor.obtener_todas_tareas()), len(nuevo_gestor.obtener_todas_tareas()))
        
        # Comprobar tarea 1
        t1_original = self.gestor.buscar_tarea(1)
        t1_cargada = nuevo_gestor.buscar_tarea(1)
        self.assertIsNotNone(t1_cargada)
        self.assertEqual(t1_original.descripcion, t1_cargada.descripcion)
        self.assertEqual(t1_original.prioridad, t1_cargada.prioridad)

        # Comprobar tarea 2
        t2_original = self.gestor.buscar_tarea(2)
        t2_cargada = nuevo_gestor.buscar_tarea(2)
        self.assertIsNotNone(t2_cargada)
        self.assertEqual(t2_original.descripcion, t2_cargada.descripcion)
        
        # Comprobar subtarea
        self.assertIsNotNone(nuevo_gestor.arboles_subtareas[1].buscar_nodo(10))

    def test_prevencion_inanicion_escalamiento(self):
        """
        Prueba la regla de negocio de prevención de inanición (starvation prevention).
        Verifica que al saturar la cola urgente, una tarea en la cola regular acumule ciclos de espera
        y al alcanzar el límite configurado (max_ciclos_espera=3) sea escalada automáticamente a la cola urgente.
        """
        gestor_anti_inanicion = GestorTareas(ruta_csv=self.ruta_csv_prueba, max_ciclos_espera=3)

        # 1. Crear 1 tarea regular y 3 tareas urgentes
        gestor_anti_inanicion.crear_tarea(1, "NORMAL", 100, "Tarea Regular Olvidada", auto_guardar=False)
        gestor_anti_inanicion.crear_tarea(2, "ALTA", 101, "Urgente A", auto_guardar=False)
        gestor_anti_inanicion.crear_tarea(3, "ALTA", 102, "Urgente B", auto_guardar=False)
        gestor_anti_inanicion.crear_tarea(4, "ALTA", 103, "Urgente C", auto_guardar=False)

        # La tarea regular 1 está inicialmente en la cola regular
        self.assertFalse(gestor_anti_inanicion.cola_regular.esta_vacia())
        tarea_1 = gestor_anti_inanicion.buscar_tarea(1)
        self.assertEqual(tarea_1.ciclos_espera, 0)

        # 2. Procesar primera urgente (Urgente A). Tarea 1 acumula 1 ciclo de espera
        p1 = gestor_anti_inanicion.procesar_siguiente()
        self.assertEqual(p1.id_tarea, 2)
        self.assertEqual(tarea_1.ciclos_espera, 1)

        # 3. Procesar segunda urgente (Urgente B). Tarea 1 acumula 2 ciclos de espera
        p2 = gestor_anti_inanicion.procesar_siguiente()
        self.assertEqual(p2.id_tarea, 3)
        self.assertEqual(tarea_1.ciclos_espera, 2)

        # 4. Procesar tercera urgente (Urgente C). Tarea 1 alcanza 3 ciclos de espera
        # y debe ser promovida automáticamente a la cola urgente
        p3 = gestor_anti_inanicion.procesar_siguiente()
        self.assertEqual(p3.id_tarea, 4)
        self.assertEqual(tarea_1.ciclos_espera, 3)
        self.assertEqual(tarea_1.prioridad, Prioridad.ALTA)
        self.assertTrue(gestor_anti_inanicion.cola_regular.esta_vacia())

        # 5. La siguiente tarea a procesar debe ser Tarea 1 (escalada a la cola urgente)
        p4 = gestor_anti_inanicion.procesar_siguiente()
        self.assertEqual(p4.id_tarea, 1)

    def test_auditoria_log_y_deshacer_rehacer(self):
        """
        Prueba la generación de la bitácora inmutable (auditoria_log.csv)
        y la pila de Deshacer / Rehacer.
        """
        # 1. Crear tarea y cambiar estado
        self.gestor.crear_tarea(50, "NORMAL", 200, "Tarea para Auditoría", auto_guardar=False)
        self.assertTrue(self.gestor.cambiar_estado_tarea(50, "Completada", id_usuario_solicitante=200, auto_guardar=False))
        self.assertEqual(self.gestor.buscar_tarea(50).estado, "Completada")

        # 2. Ejecutar Deshacer (Stack LIFO)
        self.assertTrue(self.gestor.deshacer(id_usuario_ejecutor=200))
        self.assertEqual(self.gestor.buscar_tarea(50).estado, "Pendiente")

        # 3. Ejecutar Rehacer (Stack LIFO)
        self.assertTrue(self.gestor.rehacer(id_usuario_ejecutor=200))
        self.assertEqual(self.gestor.buscar_tarea(50).estado, "Completada")

        # 4. Verificar que se creó el archivo auditoria_log.csv inmutable con el formato exacto
        self.assertTrue(os.path.exists(self.ruta_auditoria_prueba))
        with open(self.ruta_auditoria_prueba, "r", encoding="utf-8") as f:
            lineas = f.readlines()

        self.assertGreaterEqual(len(lineas), 3)
        # Formato esperado: [Fecha y Hora] | [ID Usuario que ejecutó] | [Acción Realizada] | [ID Tarea Afectada]
        for linea in lineas:
            partes = [p.strip() for p in linea.split("|")]
            self.assertEqual(len(partes), 4)

        self.assertIn("Cambio de Estado", lineas[0])
        self.assertIn("Deshacer", lineas[1])
        self.assertIn("Rehacer", lineas[2])



if __name__ == '__main__':
    """
    Punto de entrada para ejecutar las pruebas.
    Permite correr el archivo directamente como un script.
    """
    unittest.main(verbosity=2)
