"""Módulo que contiene la lógica de negocio de las tareas."""

from copy import deepcopy

from models.tarea import Tarea
from models.prioridad import Prioridad
from models.accion import Accion
from structures.nodo_arbol import NodoArbolTarea


class TareaService:
    """Gestiona las tareas y sus árboles de subtareas."""

    def __init__(
        self,
        tarea_repository,
        historial_service=None
    ):
        """Inicializa el servicio de tareas."""

        self.tarea_repository = tarea_repository
        self.historial_service = historial_service

        self.tareas = []
        self.arboles_subtareas = {}

        self.cargar_datos()

    # =========================================================
    # CONFIGURACIÓN
    # =========================================================

    def establecer_historial(self, historial_service):
        """Establece el servicio de historial compartido."""

        self.historial_service = historial_service

    # =========================================================
    # PERSISTENCIA
    # =========================================================

    def cargar_datos(self):
        """Carga las tareas y subtareas desde el repositorio."""

        resultado = self.tarea_repository.cargar_tareas()

        self.tareas, self.arboles_subtareas = resultado

    def guardar_datos(self):
        """Guarda las tareas y subtareas en el repositorio."""

        self.tarea_repository.guardar_tareas(
            self.tareas,
            self.arboles_subtareas
        )

    # =========================================================
    # BUSCAR TAREA
    # =========================================================

    def buscar_tarea(self, id_tarea):
        """
        Busca una tarea por ID.

        :param id_tarea: ID de la tarea.
        :return: Tarea encontrada o None.
        """

        try:
            id_tarea = int(id_tarea)

        except (ValueError, TypeError):
            return None

        for tarea in self.tareas:

            if tarea.id_tarea == id_tarea:
                return tarea

        return None

    # =========================================================
    # AGREGAR TAREA
    # =========================================================

    def agregar_tarea(
        self,
        id_tarea,
        descripcion,
        prioridad,
        id_usuario,
        estado="Pendiente",
        ciclos_espera=0,
        id_usuario_ejecutor=None
    ):
        """
        Agrega una nueva tarea.

        :return: True si se agregó correctamente.
        """

        try:
            id_tarea = int(id_tarea)
            id_usuario = int(id_usuario)
            ciclos_espera = int(ciclos_espera)

            if id_tarea <= 0:
                return False

            if id_usuario <= 0:
                return False

            if ciclos_espera < 0:
                return False

            if self.buscar_tarea(id_tarea) is not None:
                return False

            if (
                not isinstance(descripcion, str)
                or not descripcion.strip()
            ):
                return False

            prioridad = (
                prioridad
                if isinstance(prioridad, Prioridad)
                else Prioridad.desde_texto(prioridad)
            )

            tarea = Tarea(
                id_tarea=id_tarea,
                descripcion=descripcion.strip(),
                prioridad=prioridad,
                id_usuario=id_usuario,
                estado=estado,
                ciclos_espera=ciclos_espera
            )

        except (ValueError, TypeError):
            return False

        self.tareas.append(tarea)

        self.arboles_subtareas[id_tarea] = NodoArbolTarea(
            id_subtarea=id_tarea,
            descripcion=tarea.descripcion,
            id_padre=None,
            completada=tarea.estado == "Finalizada"
        )

        self.guardar_datos()

        if self.historial_service is not None:

            accion = Accion(
                "AGREGAR_TAREA",
                f"Se agregó la tarea: {id_tarea}",
                deepcopy(tarea),
                id_usuario_ejecutor
            )

            self.historial_service.registrar_accion(
                accion
            )

        return True

    # =========================================================
    # MODIFICAR TAREA
    # =========================================================

    def modificar_tarea(
        self,
        id_tarea,
        nueva_descripcion=None,
        nueva_prioridad=None,
        nuevo_id_usuario=None,
        id_usuario_ejecutor=None
    ):
        """
        Modifica una tarea existente.

        :return: True si se modificó correctamente.
        """

        tarea = self.buscar_tarea(id_tarea)

        if tarea is None:
            return False

        datos_anterior = {
            "descripcion": tarea.descripcion,
            "prioridad": tarea.prioridad,
            "id_usuario": tarea.id_usuario
        }

        # =====================================================
        # VALIDAR TODO ANTES DE MODIFICAR
        # =====================================================

        descripcion_final = tarea.descripcion
        prioridad_final = tarea.prioridad
        id_usuario_final = tarea.id_usuario

        try:

            if nueva_descripcion is not None:

                if (
                    not isinstance(nueva_descripcion, str)
                    or not nueva_descripcion.strip()
                ):
                    return False

                descripcion_final = nueva_descripcion.strip()

            if nueva_prioridad is not None:

                prioridad_final = (
                    nueva_prioridad
                    if isinstance(
                        nueva_prioridad,
                        Prioridad
                    )
                    else Prioridad.desde_texto(
                        nueva_prioridad
                    )
                )

            if nuevo_id_usuario is not None:

                id_usuario_final = int(
                    nuevo_id_usuario
                )

                if id_usuario_final <= 0:
                    return False

        except (ValueError, TypeError):
            return False

        # =====================================================
        # APLICAR MODIFICACIÓN
        # =====================================================

        tarea.descripcion = descripcion_final
        tarea.prioridad = prioridad_final
        tarea.id_usuario = id_usuario_final

        raiz = self.arboles_subtareas.get(
            tarea.id_tarea
        )

        if raiz is not None:
            raiz.descripcion = tarea.descripcion

        datos_nuevo = {
            "descripcion": tarea.descripcion,
            "prioridad": tarea.prioridad,
            "id_usuario": tarea.id_usuario
        }

        self.guardar_datos()

        # =====================================================
        # HISTORIAL
        # =====================================================

        if self.historial_service is not None:

            accion = Accion(
                "MODIFICAR_TAREA",
                f"Se modificó la tarea: {id_tarea}",
                {
                    "id_tarea": id_tarea,
                    "anterior": deepcopy(datos_anterior),
                    "nuevo": deepcopy(datos_nuevo)
                },
                id_usuario_ejecutor
            )

            self.historial_service.registrar_accion(
                accion
            )

        return True

    # =========================================================
    # ELIMINAR TAREA
    # =========================================================

    def eliminar_tarea(
        self,
        id_tarea,
        id_usuario_ejecutor=None
    ):
        """
        Elimina una tarea y todo su árbol de subtareas.

        :return: True si se eliminó correctamente.
        """

        tarea = self.buscar_tarea(id_tarea)

        if tarea is None:
            return False

        tarea_eliminada = deepcopy(tarea)

        arbol = self.arboles_subtareas.get(
            tarea.id_tarea
        )

        arbol_eliminado = (
            deepcopy(arbol)
            if arbol is not None
            else None
        )

        self.tareas.remove(tarea)

        self.arboles_subtareas.pop(
            tarea.id_tarea,
            None
        )

        self.guardar_datos()

        if self.historial_service is not None:

            accion = Accion(
                "ELIMINAR_TAREA",
                f"Se eliminó la tarea: {id_tarea}",
                {
                    "tarea": tarea_eliminada,
                    "arbol": arbol_eliminado
                },
                id_usuario_ejecutor
            )

            self.historial_service.registrar_accion(
                accion
            )

        return True

    # =========================================================
    # AGREGAR SUBTAREA
    # =========================================================

    def agregar_subtarea(
        self,
        id_padre,
        id_subtarea,
        descripcion,
        completada=False,
        id_usuario_ejecutor=None
    ):
        """
        Agrega una subtarea a una tarea o subtarea existente.

        :return: True si se agregó correctamente.
        """

        try:
            id_padre = int(id_padre)
            id_subtarea = int(id_subtarea)

        except (ValueError, TypeError):
            return False

        if id_subtarea <= 0:
            return False

        if (
            not isinstance(descripcion, str)
            or not descripcion.strip()
        ):
            return False

        # =====================================================
        # VERIFICAR ID ÚNICO
        # =====================================================

        for raiz in self.arboles_subtareas.values():

            if raiz.buscar_nodo(id_subtarea) is not None:
                return False

        # =====================================================
        # BUSCAR PADRE
        # =====================================================

        padre = None

        for raiz in self.arboles_subtareas.values():

            encontrado = raiz.buscar_nodo(
                id_padre
            )

            if encontrado is not None:
                padre = encontrado
                break

        if padre is None:
            return False

        # =====================================================
        # CREAR SUBTAREA
        # =====================================================

        nueva_subtarea = NodoArbolTarea(
            id_subtarea=id_subtarea,
            descripcion=descripcion.strip(),
            id_padre=id_padre,
            completada=bool(completada)
        )

        padre.subtareas.append(
            nueva_subtarea
        )

        self.guardar_datos()

        # =====================================================
        # HISTORIAL
        # =====================================================

        if self.historial_service is not None:

            accion = Accion(
                "AGREGAR_SUBTAREA",
                f"Se agregó la subtarea: {id_subtarea}",
                {
                    "id_subtarea": id_subtarea,
                    "id_padre": id_padre,
                    "subtarea": deepcopy(
                        nueva_subtarea
                    )
                },
                id_usuario_ejecutor
            )

            self.historial_service.registrar_accion(
                accion
            )

        return True

    # =========================================================
    # ELIMINAR SUBTAREA
    # =========================================================

    def eliminar_subtarea(
        self,
        id_subtarea,
        id_usuario_ejecutor=None
    ):
        """
        Elimina una subtarea de cualquier árbol.

        Guarda una copia completa del nodo antes de eliminarlo
        para permitir las operaciones de deshacer y rehacer.

        :return: True si se eliminó correctamente.
        """

        try:
            id_subtarea = int(id_subtarea)

        except (ValueError, TypeError):
            return False

        if id_subtarea <= 0:
            return False

        # =====================================================
        # BUSCAR SUBTAREA
        # =====================================================

        subtarea = self.buscar_subtarea(
            id_subtarea
        )

        if subtarea is None:
            return False

        # =====================================================
        # GUARDAR COPIA ANTES DE ELIMINAR
        # =====================================================

        subtarea_eliminada = deepcopy(
            subtarea
        )

        # =====================================================
        # ELIMINAR SUBTAREA
        # =====================================================

        resultado = self._eliminar_subtarea(
            id_subtarea
        )

        if resultado is None:
            return False

        self.guardar_datos()

        # =====================================================
        # HISTORIAL
        # =====================================================

        if self.historial_service is not None:

            accion = Accion(
                "ELIMINAR_SUBTAREA",
                f"Se eliminó la subtarea: {id_subtarea}",
                {
                    "nodo": deepcopy(
                        subtarea_eliminada
                    )
                },
                id_usuario_ejecutor
            )

            self.historial_service.registrar_accion(
                accion
            )

        return True

    # =========================================================
    # BUSCAR SUBTAREA
    # =========================================================

    def buscar_subtarea(self, id_subtarea):
        """
        Busca una subtarea en todos los árboles.

        :return: Nodo encontrado o None.
        """

        try:
            id_subtarea = int(id_subtarea)

        except (ValueError, TypeError):
            return None

        for raiz in self.arboles_subtareas.values():

            encontrado = raiz.buscar_nodo(
                id_subtarea
            )

            if encontrado is not None:
                return encontrado

        return None

    # =========================================================
    # COMPLETAR SUBTAREA
    # =========================================================

    def completar_subtarea(self, id_subtarea):
        """
        Marca una subtarea como completada.

        :return: True si se realizó correctamente.
        """

        subtarea = self.buscar_subtarea(
            id_subtarea
        )

        if subtarea is None:
            return False

        subtarea.completada = True

        self.guardar_datos()

        return True

    # =========================================================
    # LISTAR SUBTAREAS
    # =========================================================

    def listar_subtareas(self, id_tarea):
        """
        Obtiene todas las subtareas de una tarea.

        :return: Lista de tuplas.
        """

        try:
            id_tarea = int(id_tarea)

        except (ValueError, TypeError):
            return []

        raiz = self.arboles_subtareas.get(
            id_tarea
        )

        if raiz is None:
            return []

        return raiz.obtener_todas()

    # =========================================================
    # MÉTODOS AUXILIARES PARA SUBTAREAS
    # =========================================================

    def _eliminar_subtarea(self, id_subtarea):
        """
        Busca y elimina una subtarea de cualquier árbol.

        :param id_subtarea: ID de la subtarea.
        :return: Nodo eliminado o None.
        """

        for raiz in (
            self.arboles_subtareas.values()
        ):

            resultado = self._eliminar_de_nodo(
                raiz,
                id_subtarea
            )

            if resultado is not None:
                return resultado

        return None

    def _eliminar_de_nodo(
        self,
        nodo,
        id_subtarea
    ):
        """
        Busca y elimina recursivamente un nodo hijo.

        :return: Nodo eliminado o None.
        """

        for indice, hijo in enumerate(
            nodo.subtareas
        ):

            if hijo.id_subtarea == id_subtarea:

                return nodo.subtareas.pop(
                    indice
                )

            resultado = self._eliminar_de_nodo(
                hijo,
                id_subtarea
            )

            if resultado is not None:
                return resultado

        return None