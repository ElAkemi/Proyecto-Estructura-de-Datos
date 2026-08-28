"""Módulo encargado de administrar Deshacer, Rehacer y Auditoría."""

from copy import deepcopy
import csv

from structures.pila import Pila
from structures.nodo_arbol import NodoArbolTarea


class HistorialService:
    """Gestiona el historial de acciones del sistema."""

    def __init__(
        self,
        tarea_service=None,
        usuario_service=None,
        archivo_auditoria=None
    ):
        self.tarea_service = tarea_service
        self.usuario_service = usuario_service
        self.archivo_auditoria = archivo_auditoria

        self.pila_deshacer = Pila()
        self.pila_rehacer = Pila()

    # =========================================================
    # CONFIGURACIÓN
    # =========================================================

    def establecer_tarea_service(self, tarea_service):
        """Establece el servicio de tareas."""

        self.tarea_service = tarea_service

    def establecer_usuario_service(self, usuario_service):
        """Establece el servicio de usuarios."""

        self.usuario_service = usuario_service

    def establecer_archivo_auditoria(self, archivo_auditoria):
        """Establece el archivo donde se guarda la auditoría."""

        self.archivo_auditoria = archivo_auditoria

    # =========================================================
    # AUDITORÍA
    # =========================================================

    def guardar_auditoria(self, accion):
        """Guarda una acción en el archivo de auditoría."""

        if self.archivo_auditoria is None:
            return

        with open(
            self.archivo_auditoria,
            mode="a",
            newline="",
            encoding="utf-8"
        ) as archivo:

            writer = csv.writer(archivo)

            writer.writerow([
                accion.tipo,
                accion.descripcion
            ])

    # =========================================================
    # REGISTRAR
    # =========================================================

    def registrar_accion(self, accion):
        """
        Registra una nueva acción.

        Una nueva acción elimina el historial de rehacer
        y guarda la acción en la auditoría.
        """

        self.pila_deshacer.apilar(
            accion
        )

        self.pila_rehacer = Pila()

        self.guardar_auditoria(
            accion
        )

    # =========================================================
    # DESHACER
    # =========================================================

    def deshacer_accion(self):
        """
        Deshace la última acción registrada.

        :return: Acción deshecha o None.
        """

        accion = self.pila_deshacer.desapilar()

        if accion is None:
            return None

        try:

            self._aplicar_deshacer(
                accion
            )

            self.pila_rehacer.apilar(
                accion
            )

            return accion

        except Exception:

            self.pila_deshacer.apilar(
                accion
            )

            return None

    # =========================================================
    # REHACER
    # =========================================================

    def rehacer_accion(self):
        """
        Rehace la última acción deshecha.

        :return: Acción rehecha o None.
        """

        accion = self.pila_rehacer.desapilar()

        if accion is None:
            return None

        try:

            self._aplicar_rehacer(
                accion
            )

            self.pila_deshacer.apilar(
                accion
            )

            return accion

        except Exception:

            self.pila_rehacer.apilar(
                accion
            )

            return None

    # =========================================================
    # APLICAR DESHACER
    # =========================================================

    def _aplicar_deshacer(self, accion):
        """Aplica la operación inversa de una acción."""

        tipo = accion.tipo

        # =====================================================
        # AGREGAR TAREA
        # =====================================================

        if tipo == "AGREGAR_TAREA":

            tarea = accion.datos

            self.tarea_service.tareas = [
                t
                for t in self.tarea_service.tareas
                if t.id_tarea != tarea.id_tarea
            ]

            self.tarea_service.arboles_subtareas.pop(
                tarea.id_tarea,
                None
            )

            self.tarea_service.guardar_datos()

        # =====================================================
        # ELIMINAR TAREA
        # =====================================================

        elif tipo == "ELIMINAR_TAREA":

            tarea = accion.datos["tarea"]
            arbol = accion.datos["arbol"]

            if self.tarea_service.buscar_tarea(
                tarea.id_tarea
            ) is None:

                self.tarea_service.tareas.append(
                    deepcopy(tarea)
                )

                if arbol is not None:

                    self.tarea_service.arboles_subtareas[
                        tarea.id_tarea
                    ] = deepcopy(arbol)

                self.tarea_service.guardar_datos()

        # =====================================================
        # MODIFICAR TAREA
        # =====================================================

        elif tipo == "MODIFICAR_TAREA":

            id_tarea = accion.datos["id_tarea"]
            anterior = accion.datos["anterior"]

            tarea = self.tarea_service.buscar_tarea(
                id_tarea
            )

            if tarea is None:
                raise ValueError(
                    "La tarea no existe."
                )

            tarea.descripcion = anterior["descripcion"]
            tarea.prioridad = anterior["prioridad"]
            tarea.id_usuario = anterior["id_usuario"]

            raiz = (
                self.tarea_service
                .arboles_subtareas
                .get(id_tarea)
            )

            if raiz is not None:
                raiz.descripcion = tarea.descripcion

            self.tarea_service.guardar_datos()

        # =====================================================
        # AGREGAR SUBTAREA
        # =====================================================

        elif tipo == "AGREGAR_SUBTAREA":

            id_subtarea = accion.datos["id_subtarea"]

            resultado = self._eliminar_subtarea(
                id_subtarea
            )

            if resultado is None:
                raise ValueError(
                    "No se encontró la subtarea."
                )

            self.tarea_service.guardar_datos()

        # =====================================================
        # ELIMINAR SUBTAREA
        # =====================================================

        elif tipo == "ELIMINAR_SUBTAREA":

            nodo = accion.datos["nodo"]

            if nodo.id_padre is None:
                raise ValueError(
                    "La subtarea no tiene padre."
                )

            padre = self.tarea_service.buscar_subtarea(
                nodo.id_padre
            )

            if padre is None:
                raise ValueError(
                    "No se encontró el padre de la subtarea."
                )

            if self.tarea_service.buscar_subtarea(
                nodo.id_subtarea
            ) is not None:
                raise ValueError(
                    "La subtarea ya existe."
                )

            padre.subtareas.append(
                deepcopy(nodo)
            )

            self.tarea_service.guardar_datos()

        # =====================================================
        # AGREGAR USUARIO
        # =====================================================

        elif tipo == "AGREGAR_USUARIO":

            usuario = accion.datos

            if self.usuario_service.lista_usuarios.buscar(
                usuario.id
            ) is not None:

                self.usuario_service.lista_usuarios.eliminar(
                    usuario.id
                )

                self.usuario_service.repository.guardar_usuarios(
                    self.usuario_service.lista_usuarios
                )

        # =====================================================
        # ELIMINAR USUARIO
        # =====================================================

        elif tipo == "ELIMINAR_USUARIO":

            usuario = accion.datos

            if self.usuario_service.lista_usuarios.buscar(
                usuario.id
            ) is None:

                self.usuario_service.lista_usuarios.insertar(
                    deepcopy(usuario)
                )

                self.usuario_service.repository.guardar_usuarios(
                    self.usuario_service.lista_usuarios
                )

        # =====================================================
        # MODIFICAR USUARIO
        # =====================================================

        elif tipo == "MODIFICAR_USUARIO":

            anterior = accion.datos["anterior"]

            usuario = self.usuario_service.lista_usuarios.buscar(
                anterior.id
            )

            if usuario is None:
                raise ValueError(
                    "El usuario no existe."
                )

            self.usuario_service.lista_usuarios.modificar(
                anterior.id,
                anterior.nombre,
                anterior.rol
            )

            self.usuario_service.repository.guardar_usuarios(
                self.usuario_service.lista_usuarios
            )

        else:

            raise ValueError(
                f"Tipo de acción no soportado: {tipo}"
            )

    # =========================================================
    # APLICAR REHACER
    # =========================================================

    def _aplicar_rehacer(self, accion):
        """Vuelve a aplicar la acción original."""

        tipo = accion.tipo

        # =====================================================
        # AGREGAR TAREA
        # =====================================================

        if tipo == "AGREGAR_TAREA":

            tarea = accion.datos

            if self.tarea_service.buscar_tarea(
                tarea.id_tarea
            ) is None:

                tarea_nueva = deepcopy(
                    tarea
                )

                self.tarea_service.tareas.append(
                    tarea_nueva
                )

                self.tarea_service.arboles_subtareas[
                    tarea.id_tarea
                ] = NodoArbolTarea(
                    id_subtarea=tarea.id_tarea,
                    descripcion=tarea.descripcion,
                    id_padre=None,
                    completada=(
                        tarea.estado == "Finalizada"
                    )
                )

                self.tarea_service.guardar_datos()

        # =====================================================
        # ELIMINAR TAREA
        # =====================================================

        elif tipo == "ELIMINAR_TAREA":

            tarea = accion.datos["tarea"]

            self.tarea_service.tareas = [
                t
                for t in self.tarea_service.tareas
                if t.id_tarea != tarea.id_tarea
            ]

            self.tarea_service.arboles_subtareas.pop(
                tarea.id_tarea,
                None
            )

            self.tarea_service.guardar_datos()

        # =====================================================
        # MODIFICAR TAREA
        # =====================================================

        elif tipo == "MODIFICAR_TAREA":

            id_tarea = accion.datos["id_tarea"]
            nuevo = accion.datos["nuevo"]

            tarea = self.tarea_service.buscar_tarea(
                id_tarea
            )

            if tarea is None:
                raise ValueError(
                    "La tarea no existe."
                )

            tarea.descripcion = nuevo["descripcion"]
            tarea.prioridad = nuevo["prioridad"]
            tarea.id_usuario = nuevo["id_usuario"]

            raiz = (
                self.tarea_service
                .arboles_subtareas
                .get(id_tarea)
            )

            if raiz is not None:
                raiz.descripcion = tarea.descripcion

            self.tarea_service.guardar_datos()

        # =====================================================
        # AGREGAR SUBTAREA
        # =====================================================

        elif tipo == "AGREGAR_SUBTAREA":

            id_subtarea = accion.datos["id_subtarea"]
            id_padre = accion.datos["id_padre"]
            nodo = accion.datos["subtarea"]

            if self.tarea_service.buscar_subtarea(
                id_subtarea
            ) is not None:
                raise ValueError(
                    "La subtarea ya existe."
                )

            padre = self.tarea_service.buscar_subtarea(
                id_padre
            )

            if padre is None:
                raise ValueError(
                    "No se encontró el padre."
                )

            padre.subtareas.append(
                deepcopy(nodo)
            )

            self.tarea_service.guardar_datos()

        # =====================================================
        # ELIMINAR SUBTAREA
        # =====================================================

        elif tipo == "ELIMINAR_SUBTAREA":

            nodo = accion.datos["nodo"]

            resultado = self._eliminar_subtarea(
                nodo.id_subtarea
            )

            if resultado is None:
                raise ValueError(
                    "No se encontró la subtarea."
                )

            self.tarea_service.guardar_datos()

        # =====================================================
        # AGREGAR USUARIO
        # =====================================================

        elif tipo == "AGREGAR_USUARIO":

            usuario = accion.datos

            if self.usuario_service.lista_usuarios.buscar(
                usuario.id
            ) is None:

                self.usuario_service.lista_usuarios.insertar(
                    deepcopy(usuario)
                )

                self.usuario_service.repository.guardar_usuarios(
                    self.usuario_service.lista_usuarios
                )

        # =====================================================
        # ELIMINAR USUARIO
        # =====================================================

        elif tipo == "ELIMINAR_USUARIO":

            usuario = accion.datos

            if self.usuario_service.lista_usuarios.buscar(
                usuario.id
            ) is not None:

                self.usuario_service.lista_usuarios.eliminar(
                    usuario.id
                )

                self.usuario_service.repository.guardar_usuarios(
                    self.usuario_service.lista_usuarios
                )

        # =====================================================
        # MODIFICAR USUARIO
        # =====================================================

        elif tipo == "MODIFICAR_USUARIO":

            nuevo = accion.datos["nuevo"]

            usuario = self.usuario_service.lista_usuarios.buscar(
                nuevo.id
            )

            if usuario is None:
                raise ValueError(
                    "El usuario no existe."
                )

            self.usuario_service.lista_usuarios.modificar(
                nuevo.id,
                nuevo.nombre,
                nuevo.rol
            )

            self.usuario_service.repository.guardar_usuarios(
                self.usuario_service.lista_usuarios
            )

        else:

            raise ValueError(
                f"Tipo de acción no soportado: {tipo}"
            )

    # =========================================================
    # ELIMINAR SUBTAREA AUXILIAR
    # =========================================================

    def _eliminar_subtarea(self, id_subtarea):
        """
        Busca y elimina una subtarea de cualquier árbol.

        :param id_subtarea: ID de la subtarea.
        :return: Nodo eliminado o None.
        """

        for raiz in (
            self.tarea_service.arboles_subtareas.values()
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
        """Busca y elimina recursivamente un nodo hijo."""

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

    # =========================================================
    # MOSTRAR HISTORIAL
    # =========================================================

    def mostrar_deshacer(self):
        """Muestra las acciones disponibles para deshacer."""

        self.pila_deshacer.mostrar()

    def mostrar_rehacer(self):
        """Muestra las acciones disponibles para rehacer."""

        self.pila_rehacer.mostrar()