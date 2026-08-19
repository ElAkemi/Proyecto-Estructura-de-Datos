"""Módulo para la gestión principal de tareas, colas y auditoría."""

from estructuras.arbol_tareas import ArbolTareas
from estructuras.cola_fifo import ColaFIFO
from estructuras.cola_prioridad import ColaPrioridad
from estructuras.pila import Pila
from modelos.nodo_arbol import NodoArbolTarea
from modelos.prioridad import Prioridad
from modelos.tarea import Tarea
from persistencia.gestor_csv import AuditoriaLogger, GestorCSV


class GestorTareas:
    # Constructor de __init__ y Auxiliar de guardado.
    def __init__(self, ruta_csv: str = "tareas.csv", max_ciclos_espera: int = 3, ruta_log_auditoria: str = "auditoria_log.csv"):
        self.cola_regular = ColaFIFO() # Tareas no urgentes
        self.cola_urgente = ColaPrioridad() # Tareas urgentes
        self.arboles_subtareas = {} # Relaciona el id_tarea con la raíz de un árbol donde se gestionan las subtareas dependientes.
        self.ruta_csv = ruta_csv # Establece el archivo de alamccenamiento.
        self.max_ciclos_espera = int(max_ciclos_espera) # Límite de ciclos de espera antes de promover a cola urgente para evitar inanición.
        self.ruta_log_auditoria = ruta_log_auditoria # Archivo de bitácora inmutable (auditoria_log.csv)
        self.pila_deshacer = Pila() # Pila para función Deshacer
        self.pila_rehacer = Pila() # Pila para función Rehacer

    def registrar_auditoria(self, id_usuario, accion: str, id_tarea):
        """Registra una nueva línea en la bitácora inmutable auditoria_log.csv."""
        if self.ruta_log_auditoria:
            try:
                try:
                    from ..Persistencia.Gestor_csv import AuditoriaLogger
                except (ImportError, ValueError):
                    from Persistencia.Gestor_csv import AuditoriaLogger
                AuditoriaLogger.registrar_evento(self.ruta_log_auditoria, id_usuario, accion, id_tarea)
            except Exception as e:
                print(f"Advertencia: No se pudo registrar auditoría: {e}")



    """
    Evalua si auto_guardar es True e importa GestorCSV y guarda el estado actual 
    para no perder informacion, a la vez que captura cualquier error. 
    """
    def _guardar_si_es_necesario(self, auto_guardar: bool):
        if auto_guardar and self.ruta_csv:
            try:
                try:
                    from ..Persistencia.Gestor_csv import GestorCSV
                except (ImportError, ValueError):
                    from Persistencia.Gestor_csv import GestorCSV
                GestorCSV.guardar_en_csv(self.ruta_csv, self)
            except Exception as e:
                print(f"Advertencia: No se pudo guardar la información en CSV: {e}")

        """
        Convierte el ID a entero y realiza una búsqueda secuencial primero
        en la cola urgente; si no la encuentra, busca en la cola regular.
        """
    def buscar_tarea(self, id_tarea: int) -> Tarea:
        id_tarea = int(id_tarea)
        # Buscar en cola urgente
        tarea = self.cola_urgente.buscar_por_id(id_tarea)
        if tarea:
            return tarea
        # Buscar en cola regular
        return self.cola_regular.buscar_por_id(id_tarea)

        """
        Une las listas de ambas colas urgentes 
        primero, para entregar el catálogo completo de tareas.
        """
    def obtener_todas_tareas(self) -> list:
        # Devuelve la combinación de urgente + regular
        return self.cola_urgente.obtener_lista() + self.cola_regular.obtener_lista()

    def crear_tarea(self, id_tarea: int, prioridad_str: str, id_usuario: int, descripcion: str, completada: bool = False, auto_guardar: bool = True) -> Tarea:
        id_tarea = int(id_tarea)
        
        # Validar duplicados
        if self.buscar_tarea(id_tarea) is not None or id_tarea in self.arboles_subtareas:
            raise ValueError(f"Ya existe una tarea registrada con el ID {id_tarea}.")

        # Asigna la tarea a la cola urgente, caso contrario a la regular.
        prioridad = Prioridad.desde_texto(prioridad_str)
        nueva_tarea = Tarea(id_tarea, descripcion, prioridad, id_usuario, completada=completada)
        
        if prioridad == Prioridad.ALTA:
            self.cola_urgente.encolar(nueva_tarea)
        else:
            self.cola_regular.encolar(nueva_tarea)

        # Inicializa la raíz del árbol de subtareas
        self.arboles_subtareas[id_tarea] = NodoArbolTarea(id_tarea, descripcion, completada=completada)

        # Guarda automaticamente la informacion.
        self._guardar_si_es_necesario(auto_guardar)
        return nueva_tarea


    # Permite actualizar la descripcion en la tarea y su nodo raiz, asignacion de usuario y prioridad.
    def actualizar_tarea(self, id_tarea: int, nueva_descripcion: str = None, nueva_prioridad_str: str = None, nuevo_id_usuario: int = None, auto_guardar: bool = True) -> bool:
        tarea = self.buscar_tarea(id_tarea)
        if not tarea:
            return False

        if nueva_descripcion:
            tarea.descripcion = str(nueva_descripcion)
            if id_tarea in self.arboles_subtareas:
                self.arboles_subtareas[id_tarea].descripcion = str(nueva_descripcion)

        if nuevo_id_usuario is not None:
            tarea.id_usuario = int(nuevo_id_usuario)

        # Si la prioridad cambia, la remueve de la cola anterior y la inserta en la nueva.
        if nueva_prioridad_str:
            nueva_prio = Prioridad.desde_texto(nueva_prioridad_str)
            if nueva_prio != tarea.prioridad:
                # Re-encolar si cambia de cola urgente/regular
                self.cola_urgente.eliminar_por_id(id_tarea)
                self.cola_regular.eliminar_por_id(id_tarea)
                tarea.prioridad = nueva_prio
                if nueva_prio == Prioridad.ALTA:
                    self.cola_urgente.encolar(tarea)
                else:
                    self.cola_regular.encolar(tarea)

        self._guardar_si_es_necesario(auto_guardar)
        return True

    # Elimina el registro de la tarea de ambas colas y borra de memoria su subarbol.
    def eliminar_tarea(self, id_tarea: int, auto_guardar: bool = True) -> bool:
        id_tarea = int(id_tarea)
        eliminado_urgente = self.cola_urgente.eliminar_por_id(id_tarea)
        eliminado_regular = self.cola_regular.eliminar_por_id(id_tarea)
        
        if id_tarea in self.arboles_subtareas:
            del self.arboles_subtareas[id_tarea]

        exito = eliminado_urgente or eliminado_regular
        if exito:
            self._guardar_si_es_necesario(auto_guardar)
        return exito

    def agregar_subtarea(self, id_subtarea: int, id_padre: int, descripcion: str, completada: bool = False, auto_guardar: bool = True) -> bool:
        id_subtarea = int(id_subtarea)
        id_padre = int(id_padre)

        # Buscar en las raíces de los árboles de subtareas
        if id_padre in self.arboles_subtareas:
            exito = self.arboles_subtareas[id_padre].agregar_subtarea(id_padre, id_subtarea, descripcion, completada)
            if exito:
                self._guardar_si_es_necesario(auto_guardar)
            return exito
        
        # Buscar recursivamente en todas las subtareas existentes
        for raiz in self.arboles_subtareas.values():
            if raiz.agregar_subtarea(id_padre, id_subtarea, descripcion, completada):
                self._guardar_si_es_necesario(auto_guardar)
                return True
        return False

    def _aplicar_escalamiento_por_inanicion(self):
        """
        Incrementa los ciclos de espera de las tareas en la cola regular
        y promueve a la cola urgente a aquellas que alcancen max_ciclos_espera.
        """
        escaladas = self.cola_regular.incrementar_ciclos_y_extraer_escaladas(self.max_ciclos_espera)
        for tarea in escaladas:
            tarea.prioridad = Prioridad.ALTA
            self.cola_urgente.encolar(tarea)
            self.registrar_auditoria("SISTEMA", f"Escalamiento por SLA a Cola Urgente (Ciclos={tarea.ciclos_espera})", tarea.id_tarea)
            print(f"⚡ Escalamiento Automático (Anti-Inanición): La tarea ID={tarea.id_tarea} ('{tarea.descripcion}') superó {tarea.ciclos_espera} ciclos de espera y fue promovida a la Cola Urgente.")


    def procesar_siguiente(self) -> Tarea:
        tarea_procesada = None
        # Desencola primero las tareas urgentes
        if not self.cola_urgente.esta_vacia():
            tarea_procesada = self.cola_urgente.desencolar()
        # Si la cola urgente está vacía, atiende la cola regular
        elif not self.cola_regular.esta_vacia():
            tarea_procesada = self.cola_regular.desencolar()

        if tarea_procesada is not None:
            # Aplica el incremento de ciclos de espera y el escalamiento por inanición a las tareas restantes en la cola regular
            self._aplicar_escalamiento_por_inanicion()
            self._guardar_si_es_necesario(True)

        return tarea_procesada


    # Filtra tareas activas no completadas
    def listar_pendientes(self) -> list:
        todas = self.obtener_todas_tareas()
        return [t for t in todas if not t.completada]

    # Filta asociadas a un ID de usuario
    def listar_por_usuario(self, id_usuario: int) -> list:
        id_usuario = int(id_usuario)
        todas = self.obtener_todas_tareas()
        return [t for t in todas if t.id_usuario == id_usuario]

    # Verifica que el cambio viene de un usuario administrador o usuario responsable.
    def cambiar_estado_tarea(self, id_tarea: int, nuevo_estado: str, id_usuario_solicitante: int = None, es_admin: bool = False, auto_guardar: bool = True) -> bool:
        tarea = self.buscar_tarea(id_tarea)
        if not tarea:
            return False

        # Validación de permisos: un usuario normal sólo modifica sus propias tareas asignadas
        if not es_admin and id_usuario_solicitante is not None:
            if tarea.id_usuario != int(id_usuario_solicitante):
                raise PermissionError("No tiene permisos para modificar una tarea asignada a otro usuario.")

        estado_anterior = tarea.estado
        tarea.estado = nuevo_estado

        usr_ejecutor = id_usuario_solicitante if id_usuario_solicitante is not None else (0 if es_admin else tarea.id_usuario)

        # Registrar en la bitácora inmutable de auditoría (auditoria_log.csv)
        self.registrar_auditoria(usr_ejecutor, f"Cambio de Estado de '{estado_anterior}' a '{nuevo_estado}'", id_tarea)

        # Guardar acción en la Pila de Deshacer
        def _deshacer_cambio_estado():
            t = self.buscar_tarea(id_tarea)
            if t:
                t.estado = estado_anterior

        def _rehacer_cambio_estado():
            t = self.buscar_tarea(id_tarea)
            if t:
                t.estado = nuevo_estado

        self.pila_deshacer.apilar({
            "accion": _rehacer_cambio_estado,
            "undo": _deshacer_cambio_estado,
            "descripcion": f"Cambio de Estado de '{estado_anterior}' a '{nuevo_estado}'",
            "id_tarea": id_tarea,
            "id_usuario": usr_ejecutor
        })
        self.pila_rehacer.limpiar()

        self._guardar_si_es_necesario(auto_guardar)
        return True

    def deshacer(self, id_usuario_ejecutor = "SISTEMA") -> bool:
        """Deshace la última acción registrada en la Pila de Deshacer y escribe en auditoria_log.csv."""
        if self.pila_deshacer.esta_vacia():
            return False

        evento = self.pila_deshacer.desapilar()
        evento["undo"]()
        self.pila_rehacer.apilar(evento)

        usr = id_usuario_ejecutor if id_usuario_ejecutor != "SISTEMA" else evento.get("id_usuario", "SISTEMA")
        self.registrar_auditoria(usr, f"Deshacer: {evento['descripcion']}", evento["id_tarea"])
        self._guardar_si_es_necesario(True)
        return True

    def rehacer(self, id_usuario_ejecutor = "SISTEMA") -> bool:
        """Rehace la última acción deshecha de la Pila de Rehacer y escribe en auditoria_log.csv."""
        if self.pila_rehacer.esta_vacia():
            return False

        evento = self.pila_rehacer.desapilar()
        evento["accion"]()
        self.pila_deshacer.apilar(evento)

        usr = id_usuario_ejecutor if id_usuario_ejecutor != "SISTEMA" else evento.get("id_usuario", "SISTEMA")
        self.registrar_auditoria(usr, f"Rehacer: {evento['descripcion']}", evento["id_tarea"])
        self._guardar_si_es_necesario(True)
        return True


def cargar_csv(self, ruta_csv: str = None) -> bool:
        """Carga el estado de las tareas desde un archivo CSV."""
        ruta = ruta_csv or self.ruta_csv
        if not ruta:
            return False

        self.ruta_csv = ruta
        return GestorCSV.cargar_desde_csv(ruta, self)

def guardar_csv(self, ruta_csv: str = None) -> bool:
        """Guarda el estado actual de las tareas en un archivo CSV."""
        ruta = ruta_csv or self.ruta_csv
        if not ruta:
            return False

        self.ruta_csv = ruta
        return GestorCSV.guardar_en_csv(ruta, self)