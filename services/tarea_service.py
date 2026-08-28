from models.tarea import Tarea
from models.prioridad import Prioridad
from models.accion import Accion

from structures.cola_fifo import ColaFIFO
from structures.cola_prioridad import ColaPrioridad
from structures.arbol_tareas import ArbolTareas

from services.ordenador_tareas import OrdenadorTareas


class TareaService:
    """Gestiona las tareas y sus estructuras de datos."""

    LIMITE_SLA = 3

    def __init__(
        self,
        tarea_repository,
        historial_service=None,
        auditoria_service=None,
        usuario_service=None
    ):
        self.tarea_repository = tarea_repository
        self.historial = historial_service
        self.auditoria = auditoria_service
        self.usuario_service = usuario_service

        self.cola_fifo = ColaFIFO()
        self.cola_prioridad = ColaPrioridad()
        self.arbol = ArbolTareas()

        self._cargar_tareas()

    def _cargar_tareas(self):
        """Carga las tareas desde el CSV."""

        tareas = self.tarea_repository.cargar()

        # Primero construimos el árbol.
        # Las tareas padre deben existir antes
        # que sus subtareas.
        pendientes = list(tareas)

        while pendientes:

            progreso = False

            for tarea in pendientes[:]:

                if tarea.padre_id is None:
                    self.arbol.agregar(tarea)
                    pendientes.remove(tarea)
                    progreso = True

                elif self.arbol.buscar(
                    tarea.padre_id
                ) is not None:

                    self.arbol.agregar(tarea)
                    pendientes.remove(tarea)
                    progreso = True

            if not progreso:
                # Evita un ciclo infinito si existe
                # información inconsistente.
                break

        # Reconstruimos las colas.
        for tarea in tareas:

            if tarea.estado != "Pendiente":
                continue

            if tarea.prioridad == Prioridad.URGENTE:
                self.cola_prioridad.encolar(tarea)

            else:
                self.cola_fifo.encolar(tarea)

    def _guardar(self):
        """Guarda todas las tareas."""

        self.tarea_repository.guardar(
            self.arbol.listar()
        )

    def _validar_responsable(self, responsable_id):
        """Comprueba que el responsable exista."""

        if self.usuario_service is None:
            return

        usuario = self.usuario_service.buscar_usuario(
            responsable_id
        )

        if usuario is None:
            raise ValueError(
                "El usuario responsable no existe."
            )

    def _obtener_tarea(self, tarea_id):
        """Busca una tarea."""

        tarea = self.arbol.buscar(tarea_id)

        if tarea is None:
            raise ValueError(
                "No existe una tarea con ese ID."
            )

        return tarea

    def agregar_tarea(
        self,
        id_tarea,
        prioridad,
        responsable_id,
        descripcion,
        padre_id=None,
        registrar_historial=True
    ):
        """Crea y agrega una tarea."""

        if not isinstance(id_tarea, int):
            raise ValueError(
                "El ID debe ser un número entero."
            )

        if id_tarea <= 0:
            raise ValueError(
                "El ID debe ser positivo."
            )

        if self.arbol.buscar(id_tarea) is not None:
            raise ValueError(
                "Ya existe una tarea con ese ID."
            )

        if not isinstance(responsable_id, int):
            raise ValueError(
                "El responsable debe tener un ID válido."
            )

        self._validar_responsable(responsable_id)

        if padre_id is not None:

            if self.arbol.buscar(padre_id) is None:
                raise ValueError(
                    "La tarea padre no existe."
                )

            if padre_id == id_tarea:
                raise ValueError(
                    "Una tarea no puede ser su propia padre."
                )

        prioridad = Prioridad.desde_texto(
            prioridad
        )

        tarea = Tarea(
            id=id_tarea,
            prioridad=prioridad,
            responsable_id=responsable_id,
            descripcion=descripcion,
            padre_id=padre_id
        )

        if not self.arbol.agregar(tarea):
            raise ValueError(
                "No se pudo agregar la tarea al árbol."
            )

        if prioridad == Prioridad.URGENTE:
            self.cola_prioridad.encolar(tarea)

        else:
            self.cola_fifo.encolar(tarea)

        self._guardar()

        if registrar_historial and self.historial is not None:

            accion = Accion(
                Accion.AGREGAR,
                f"Se agregó la tarea {id_tarea}",
                tarea.copiar()
            )

            self.historial.registrar_accion(
                accion
            )

        return tarea

    def buscar_tarea(self, id_tarea):
        """Busca una tarea por ID."""

        return self.arbol.buscar(id_tarea)

    def listar_tareas(self):
        """Devuelve todas las tareas."""

        return self.arbol.listar()

    def listar_pendientes(self):
        """Devuelve únicamente las tareas pendientes."""

        return [
            tarea
            for tarea in self.arbol.listar()
            if tarea.estado == "Pendiente"
        ]

    def modificar_tarea(
        self,
        id_tarea,
        descripcion=None,
        prioridad=None,
        responsable_id=None,
        registrar_historial=True
    ):
        """Modifica una tarea."""

        tarea = self._obtener_tarea(id_tarea)

        anterior = tarea.copiar()

        if descripcion is not None:

            if not isinstance(
                descripcion,
                str
            ) or not descripcion.strip():

                raise ValueError(
                    "La descripción no puede estar vacía."
                )

            tarea.descripcion = descripcion.strip()

        if prioridad is not None:

            tarea.prioridad = Prioridad.desde_texto(
                prioridad
            )

        if responsable_id is not None:

            if not isinstance(
                responsable_id,
                int
            ):
                raise ValueError(
                    "El responsable debe ser un ID válido."
                )

            self._validar_responsable(
                responsable_id
            )

            tarea.responsable_id = responsable_id

        self._reconstruir_colas()
        self._guardar()

        if registrar_historial and self.historial is not None:

            accion = Accion(
                Accion.MODIFICAR,
                f"Se modificó la tarea {id_tarea}",
                {
                    "anterior": anterior,
                    "nuevo": tarea.copiar(),
                }
            )

            self.historial.registrar_accion(
                accion
            )

        return tarea

    def eliminar_tarea(
        self,
        id_tarea,
        registrar_historial=True
    ):
        """Elimina una tarea y sus subtareas."""

        tarea = self._obtener_tarea(id_tarea)

        copia = tarea.copiar()

        if not self.arbol.eliminar(id_tarea):
            raise ValueError(
                "No se pudo eliminar la tarea."
            )

        self.cola_fifo.remover_por_id(
            id_tarea
        )

        self.cola_prioridad.remover_por_id(
            id_tarea
        )

        self._guardar()

        if registrar_historial and self.historial is not None:

            accion = Accion(
                Accion.ELIMINAR,
                f"Se eliminó la tarea {id_tarea}",
                copia
            )

            self.historial.registrar_accion(
                accion
            )

        return True

    def restaurar_tarea(self, tarea):
        """Restaura una tarea eliminada."""

        if self.arbol.buscar(tarea.id) is not None:
            return False

        # Si tiene padre, este debe existir.
        if tarea.padre_id is not None:

            if self.arbol.buscar(
                tarea.padre_id
            ) is None:

                raise ValueError(
                    "No existe la tarea padre."
                )

        self.arbol.agregar(tarea)

        if tarea.estado == "Pendiente":

            if tarea.prioridad == Prioridad.URGENTE:
                self.cola_prioridad.encolar(
                    tarea
                )

            else:
                self.cola_fifo.encolar(
                    tarea
                )

        self._guardar()

        return True

    def cambiar_estado(
        self,
        id_tarea,
        nuevo_estado,
        usuario_id=None,
        registrar_historial=True,
        registrar_auditoria=True
    ):
        """Cambia el estado de una tarea."""

        tarea = self._obtener_tarea(id_tarea)

        if nuevo_estado not in Tarea.ESTADOS_VALIDOS:
            raise ValueError(
                "Estado inválido."
            )

        estado_anterior = tarea.estado

        tarea.estado = nuevo_estado

        self._reconstruir_colas()
        self._guardar()

        if registrar_historial and self.historial is not None:

            accion = Accion(
                Accion.CAMBIAR_ESTADO,
                (
                    f"Tarea {id_tarea}: "
                    f"{estado_anterior} -> "
                    f"{nuevo_estado}"
                ),
                {
                    "tarea_id": id_tarea,
                    "estado_anterior": estado_anterior,
                    "estado_nuevo": nuevo_estado,
                    "usuario_id": usuario_id,
                },
                usuario_id
            )

            self.historial.registrar_accion(
                accion
            )

        if registrar_auditoria and self.auditoria is not None:

            self.auditoria.registrar(
                usuario_id,
                f"CAMBIAR_ESTADO:{nuevo_estado}",
                id_tarea
            )

        return tarea

    def puede_modificar_estado(
        self,
        tarea,
        usuario_id
    ):
        """
        Determina si un usuario puede cambiar
        el estado de una tarea.

        Administrador:
            Puede modificar cualquier tarea.

        Usuario normal:
            Solo puede modificar tareas asignadas a él.
        """

        if self.usuario_service is None:
            return False

        usuario = self.usuario_service.buscar_usuario(
            usuario_id
        )

        if usuario is None:
            return False

        if usuario.rol == "Administrador":
            return True

        return (
            usuario.rol == "Usuario"
            and tarea.responsable_id == usuario_id
        )

    def procesar_siguiente(
        self,
        usuario_id=None
    ):
        """
        Procesa la siguiente tarea.

        Las tareas urgentes tienen prioridad sobre
        las tareas regulares.
        """

        if not self.cola_prioridad.esta_vacia():

            tarea = self.cola_prioridad.desencolar()

        elif not self.cola_fifo.esta_vacia():

            tarea = self.cola_fifo.desencolar()

        else:
            return None

        tarea.estado = "En ejecución"

        self._guardar()

        return tarea

    def aplicar_sla(self, usuario_id=None):
        """
        Incrementa los ciclos de espera de las tareas
        regulares.

        Si una tarea alcanza LIMITE_SLA, se escala
        automáticamente a la cola de prioridad.
        """

        escaladas = []

        tareas_regulares = self.cola_fifo.listar()

        # Reconstruimos la cola para modificarla
        # de forma segura.
        nueva_cola = ColaFIFO()

        for tarea in tareas_regulares:

            tarea.ciclos_espera += 1

            if tarea.ciclos_espera >= self.LIMITE_SLA:

                tarea.ciclos_espera = 0

                tarea.prioridad = Prioridad.ALTA

                self.cola_prioridad.encolar(
                    tarea
                )

                escaladas.append(tarea)

                if self.auditoria is not None:

                    self.auditoria.registrar(
                        usuario_id,
                        "ESCALAMIENTO_SLA",
                        tarea.id
                    )

            else:
                nueva_cola.encolar(tarea)

        self.cola_fifo = nueva_cola

        self._guardar()

        return escaladas

    def _reconstruir_colas(self):
        """Reconstruye ambas colas desde las tareas actuales."""

        self.cola_fifo = ColaFIFO()
        self.cola_prioridad = ColaPrioridad()

        for tarea in self.arbol.listar():

            if tarea.estado != "Pendiente":
                continue

            if tarea.prioridad == Prioridad.URGENTE:

                self.cola_prioridad.encolar(
                    tarea
                )

            else:

                self.cola_fifo.encolar(
                    tarea
                )

    def listar_arbol(self):
        """Devuelve la representación jerárquica del árbol."""

        return self.arbol.mostrar_arbol()

    def obtener_subtareas(self, id_tarea):
        """Devuelve las subtareas de una tarea."""

        return self.arbol.obtener_subtareas(
            id_tarea
        )

    def ordenar_por_id(self, algoritmo="merge"):
        """Ordena las tareas por ID."""

        tareas = self.arbol.listar()

        clave = lambda tarea: tarea.id

        if algoritmo == "burbuja":
            return OrdenadorTareas.burbuja(
                tareas,
                clave
            )

        if algoritmo == "merge":
            return OrdenadorTareas.merge_sort(
                tareas,
                clave
            )

        if algoritmo == "quick":
            return OrdenadorTareas.quick_sort(
                tareas,
                clave
            )

        raise ValueError(
            "Algoritmo inválido."
        )

    def ordenar_por_prioridad(
        self,
        algoritmo="merge"
    ):
        """Ordena las tareas por prioridad."""

        tareas = self.arbol.listar()

        clave = lambda tarea: -int(
            tarea.prioridad
        )

        if algoritmo == "burbuja":
            return OrdenadorTareas.burbuja(
                tareas,
                clave
            )

        if algoritmo == "merge":
            return OrdenadorTareas.merge_sort(
                tareas,
                clave
            )

        if algoritmo == "quick":
            return OrdenadorTareas.quick_sort(
                tareas,
                clave
            )

        raise ValueError(
            "Algoritmo inválido."
        )