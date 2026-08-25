"""Módulo para la gestión principal de tareas, colas y auditoría."""

from estructuras.cola_fifo import ColaFIFO
from estructuras.cola_prioridad import ColaPrioridad
from estructuras.pila import Pila
from modelos.nodo_arbol import NodoArbolTarea
from modelos.prioridad import Prioridad
from modelos.tarea import Tarea
from persistencia.gestor_csv import AuditoriaLogger, GestorCSV

class GestorTareas:
    """Clase principal para la gestión de tareas, colas y persistencia."""

    def __init__(
        self,
        ruta_csv: str = "tareas.csv",
        max_ciclos_espera: int = 3,
        ruta_log_auditoria: str = "auditoria_log.csv"
    ):
        """Inicializa las estructuras principales del gestor."""
        self.cola_regular = ColaFIFO()
        self.cola_urgente = ColaPrioridad()
        self.arboles_subtareas = {}
        self.ruta_csv = ruta_csv
        self.max_ciclos_espera = int(max_ciclos_espera)
        self.ruta_log_auditoria = ruta_log_auditoria
        self.pila_deshacer = Pila()
        self.pila_rehacer = Pila()

    def registrar_auditoria(self, id_usuario, accion: str, id_tarea):
        """Registra una nueva línea en la bitácora inmutable auditoria_log.csv."""
        if self.ruta_log_auditoria:
            try:
                AuditoriaLogger.registrar_evento(
                    self.ruta_log_auditoria, id_usuario, accion, id_tarea
                )
            except Exception as e:
                print(f"Advertencia: No se pudo registrar auditoría: {e}")

    def _guardar_si_es_necesario(self, auto_guardar: bool):
        """Guarda el estado actual si auto_guardar es True y hay una ruta definida."""
        if auto_guardar and self.ruta_csv:
            try:
                GestorCSV.guardar_en_csv(self.ruta_csv, self)
            except Exception as e:
                print(f"Advertencia: No se pudo guardar la información en CSV: {e}")

    def buscar_tarea(self, id_tarea: int) -> Tarea:
        """Realiza una búsqueda secuencial primero en la cola urgente y luego en la regular."""
        id_tarea = int(id_tarea)
        tarea = self.cola_urgente.buscar_por_id(id_tarea)
        if tarea:
            return tarea
        return self.cola_regular.buscar_por_id(id_tarea)

    def obtener_todas_tareas(self) -> list:
        """Entrega el catálogo completo de tareas (urgentes + regulares)."""
        return self.cola_urgente.obtener_lista() + self.cola_regular.obtener_lista()

    def crear_tarea(
        self,
        id_tarea: int,
        prioridad_str: str,
        id_usuario: int,
        descripcion: str,
        completada: bool = False,
        auto_guardar: bool = True
    ) -> Tarea:
        """Crea una nueva tarea, la asigna a la cola correspondiente e inicializa su árbol."""
        id_tarea = int(id_tarea)

        if self.buscar_tarea(id_tarea) is not None or id_tarea in self.arboles_subtareas:
            raise ValueError(f"Ya existe una tarea registrada con el ID {id_tarea}.")

        prioridad = Prioridad.desde_texto(prioridad_str)
        nueva_tarea = Tarea(
            id_tarea, descripcion, prioridad, id_usuario, completada=completada
        )

        if prioridad == Prioridad.ALTA:
            self.cola_urgente.encolar(nueva_tarea)
        else:
            self.cola_regular.encolar(nueva_tarea)

        self.arboles_subtareas[id_tarea] = NodoArbolTarea(
            id_tarea, descripcion, completada=completada
        )

        self._guardar_si_es_necesario(auto_guardar)
        return nueva_tarea

    def actualizar_tarea(
        self,
        id_tarea: int,
        nueva_descripcion: str = None,
        nueva_prioridad_str: str = None,
        nuevo_id_usuario: int = None,
        auto_guardar: bool = True
    ) -> bool:
        """Actualiza la descripción, usuario o prioridad de una tarea existente."""
        tarea = self.buscar_tarea(id_tarea)
        if not tarea:
            return False

        if nueva_descripcion:
            tarea.descripcion = str(nueva_descripcion)
            if id_tarea in self.arboles_subtareas:
                self.arboles_subtareas[id_tarea].descripcion = str(nueva_descripcion)

        if nuevo_id_usuario is not None:
            tarea.id_usuario = int(nuevo_id_usuario)

        if nueva_prioridad_str:
            nueva_prio = Prioridad.desde_texto(nueva_prioridad_str)
            if nueva_prio != tarea.prioridad:
                self.cola_urgente.eliminar_por_id(id_tarea)
                self.cola_regular.eliminar_por_id(id_tarea)
                tarea.prioridad = nueva_prio
                if nueva_prio == Prioridad.ALTA:
                    self.cola_urgente.encolar(tarea)
                else:
                    self.cola_regular.encolar(tarea)

        self._guardar_si_es_necesario(auto_guardar)
        return True

    def eliminar_tarea(self, id_tarea: int, auto_guardar: bool = True) -> bool:
        """Elimina el registro de la tarea de las colas y borra su subárbol."""
        id_tarea = int(id_tarea)
        eliminado_urgente = self.cola_urgente.eliminar_por_id(id_tarea)
        eliminado_regular = self.cola_regular.eliminar_por_id(id_tarea)

        if id_tarea in self.arboles_subtareas:
            del self.arboles_subtareas[id_tarea]

        exito = eliminado_urgente or eliminado_regular
        if exito:
            self._guardar_si_es_necesario(auto_guardar)
        return exito

    def agregar_subtarea(
        self,
        id_subtarea: int,
        id_padre: int,
        descripcion: str,
        completada: bool = False,
        auto_guardar: bool = True
    ) -> bool:
        """Agrega una subtarea buscando al padre en las raíces o de forma recursiva."""
        id_subtarea = int(id_subtarea)
        id_padre = int(id_padre)

        if id_padre in self.arboles_subtareas:
            exito = self.arboles_subtareas[id_padre].agregar_subtarea(
                id_padre, id_subtarea, descripcion, completada
            )
            if exito:
                self._guardar_si_es_necesario(auto_guardar)
            return exito

        for raiz in self.arboles_subtareas.values():
            if raiz.agregar_subtarea(id_padre, id_subtarea, descripcion, completada):
                self._guardar_si_es_necesario(auto_guardar)
                return True
        return False

    def _aplicar_escalamiento_por_inanicion(self):
        """Promueve a la cola urgente las tareas regulares que superen max_ciclos_espera."""
        escaladas = self.cola_regular.incrementar_ciclos_y_extraer_escaladas(
            self.max_ciclos_espera
        )
        for tarea in escaladas:
            tarea.prioridad = Prioridad.ALTA
            self.cola_urgente.encolar(tarea)
            self.registrar_auditoria(
                "SISTEMA",
                f"Escalamiento por SLA a Cola Urgente (Ciclos={tarea.ciclos_espera})",
                tarea.id_tarea
            )
            print(
                f"⚡ Escalamiento Automático (Anti-Inanición): La tarea ID={tarea.id_tarea} "
                f"('{tarea.descripcion}') superó {tarea.ciclos_espera} ciclos de espera "
                "y fue promovida a la Cola Urgente."
            )

    def procesar_siguiente(self) -> Tarea:
        """Procesa la siguiente tarea en orden de prioridad e incrementa ciclos de espera."""
        tarea_procesada = None
        if not self.cola_urgente.esta_vacia():
            tarea_procesada = self.cola_urgente.desencolar()
        elif not self.cola_regular.esta_vacia():
            tarea_procesada = self.cola_regular.desencolar()

        if tarea_procesada is not None:
            self._aplicar_escalamiento_por_inanicion()
            self._guardar_si_es_necesario(True)

        return tarea_procesada

    def listar_pendientes(self) -> list:
        """Filtra y retorna las tareas que aún no han sido completadas."""
        todas = self.obtener_todas_tareas()
        return [t for t in todas if not t.completada]

    def listar_por_usuario(self, id_usuario: int) -> list:
        """Filtra y retorna las tareas asociadas a un ID de usuario específico."""
        id_usuario = int(id_usuario)
        todas = self.obtener_todas_tareas()
        return [t for t in todas if t.id_usuario == id_usuario]

    def cambiar_estado_tarea(
        self,
        id_tarea: int,
        nuevo_estado: str,
        id_usuario_solicitante: int = None,
        es_admin: bool = False,
        auto_guardar: bool = True
    ) -> bool:
        """Cambia el estado de una tarea validando permisos y apilando la acción."""
        tarea = self.buscar_tarea(id_tarea)
        if not tarea:
            return False

        if not es_admin and id_usuario_solicitante is not None:
            if tarea.id_usuario != int(id_usuario_solicitante):
                raise PermissionError(
                    "No tiene permisos para modificar una tarea asignada a otro usuario."
                )

        estado_anterior = tarea.estado
        tarea.estado = nuevo_estado

        usr_ejecutor = (
            id_usuario_solicitante
            if id_usuario_solicitante is not None
            else (0 if es_admin else tarea.id_usuario)
        )

        self.registrar_auditoria(
            usr_ejecutor,
            f"Cambio de Estado de '{estado_anterior}' a '{nuevo_estado}'",
            id_tarea
        )

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

    def deshacer(self, id_usuario_ejecutor="SISTEMA") -> bool:
        """Deshace la última acción registrada en la Pila de Deshacer."""
        if self.pila_deshacer.esta_vacia():
            return False

        evento = self.pila_deshacer.desapilar()
        evento["undo"]()
        self.pila_rehacer.apilar(evento)

        usr = (
            id_usuario_ejecutor
            if id_usuario_ejecutor != "SISTEMA"
            else evento.get("id_usuario", "SISTEMA")
        )
        self.registrar_auditoria(
            usr, f"Deshacer: {evento['descripcion']}", evento["id_tarea"]
        )
        self._guardar_si_es_necesario(True)
        return True

    def rehacer(self, id_usuario_ejecutor="SISTEMA") -> bool:
        """Rehace la última acción deshecha de la Pila de Rehacer."""
        if self.pila_rehacer.esta_vacia():
            return False

        evento = self.pila_rehacer.desapilar()
        evento["accion"]()
        self.pila_deshacer.apilar(evento)

        usr = (
            id_usuario_ejecutor
            if id_usuario_ejecutor != "SISTEMA"
            else evento.get("id_usuario", "SISTEMA")
        )
        self.registrar_auditoria(
            usr, f"Rehacer: {evento['descripcion']}", evento["id_tarea"]
        )
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
    