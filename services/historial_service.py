from structures.pila import Pila
from models.accion import Accion


class HistorialService:
    """Gestiona las operaciones de Deshacer y Rehacer."""

    def __init__(self, auditoria_service=None):
        self.pila_deshacer = Pila()
        self.pila_rehacer = Pila()
        self.usuario_service = None
        self.tarea_service = None
        self.auditoria_service = auditoria_service

    def configurar(
        self,
        usuario_service=None,
        tarea_service=None
    ):
        """Conecta el historial con los servicios del sistema."""

        self.usuario_service = usuario_service
        self.tarea_service = tarea_service

    def registrar_accion(self, accion):
        """Registra una nueva acción."""

        self.pila_deshacer.apilar(accion)
        self.pila_rehacer.limpiar()

    def deshacer_accion(self, usuario_id=None):
        """Deshace la última acción."""

        if self.pila_deshacer.esta_vacia():
            return None

        accion = self.pila_deshacer.desapilar()

        try:
            self._deshacer(accion)
        except Exception:
            self.pila_deshacer.apilar(accion)
            raise

        self.pila_rehacer.apilar(accion)

        self._auditar(
            usuario_id,
            "DESHACER",
            accion
        )

        return accion

    def rehacer_accion(self, usuario_id=None):
        """Rehace la última acción."""

        if self.pila_rehacer.esta_vacia():
            return None

        accion = self.pila_rehacer.desapilar()

        try:
            self._rehacer(accion)
        except Exception:
            self.pila_rehacer.apilar(accion)
            raise

        self.pila_deshacer.apilar(accion)

        self._auditar(
            usuario_id,
            "REHACER",
            accion
        )

        return accion

    def _deshacer(self, accion):

        if accion.tipo == Accion.AGREGAR:
            self._deshacer_agregar(accion)

        elif accion.tipo == Accion.ELIMINAR:
            self._deshacer_eliminar(accion)

        elif accion.tipo == Accion.MODIFICAR:
            self._deshacer_modificar(accion)

        elif accion.tipo == Accion.CAMBIAR_ESTADO:
            self._deshacer_estado(accion)

        else:
            raise ValueError(
                f"Tipo de acción no soportado: {accion.tipo}"
            )

    def _rehacer(self, accion):

        if accion.tipo == Accion.AGREGAR:
            self._rehacer_agregar(accion)

        elif accion.tipo == Accion.ELIMINAR:
            self._rehacer_eliminar(accion)

        elif accion.tipo == Accion.MODIFICAR:
            self._rehacer_modificar(accion)

        elif accion.tipo == Accion.CAMBIAR_ESTADO:
            self._rehacer_estado(accion)

        else:
            raise ValueError(
                f"Tipo de acción no soportado: {accion.tipo}"
            )

    def _es_usuario(self, objeto):
        return (
            self.usuario_service is not None
            and self.usuario_service.buscar_usuario(
                objeto.id
            ) is not None
        )

    def _deshacer_agregar(self, accion):

        objeto = accion.datos

        if self.usuario_service is not None:
            usuario = self.usuario_service.buscar_usuario(
                objeto.id
            )

            if usuario is not None:
                self.usuario_service.eliminar_usuario(
                    objeto.id,
                    registrar_historial=False
                )
                return

        if self.tarea_service is not None:
            self.tarea_service.eliminar_tarea(
                objeto.id,
                registrar_historial=False
            )

    def _deshacer_eliminar(self, accion):

        objeto = accion.datos

        if self.usuario_service is not None:
            if (
                self.usuario_service.buscar_usuario(
                    objeto.id
                )
                is None
                and hasattr(objeto, "password")
            ):
                self.usuario_service.restaurar_usuario(
                    objeto
                )
                return

        if self.tarea_service is not None:
            self.tarea_service.restaurar_tarea(
                objeto
            )

    def _deshacer_modificar(self, accion):

        anterior = accion.datos["anterior"]

        if hasattr(anterior, "password"):
            self.usuario_service.restaurar_usuario(
                anterior
            )
            return

        self.tarea_service.restaurar_tarea(
            anterior
        )

    def _deshacer_estado(self, accion):

        datos = accion.datos

        self.tarea_service.cambiar_estado(
            datos["tarea_id"],
            datos["estado_anterior"],
            datos.get("usuario_id"),
            registrar_historial=False,
            registrar_auditoria=False
        )

    def _rehacer_agregar(self, accion):

        objeto = accion.datos

        if hasattr(objeto, "password"):
            self.usuario_service.restaurar_usuario(
                objeto
            )
        else:
            self.tarea_service.restaurar_tarea(
                objeto
            )

    def _rehacer_eliminar(self, accion):

        objeto = accion.datos

        if hasattr(objeto, "password"):
            self.usuario_service.eliminar_usuario(
                objeto.id,
                registrar_historial=False
            )
        else:
            self.tarea_service.eliminar_tarea(
                objeto.id,
                registrar_historial=False
            )

    def _rehacer_modificar(self, accion):

        nuevo = accion.datos["nuevo"]

        if hasattr(nuevo, "password"):
            self.usuario_service.restaurar_usuario(
                nuevo
            )
        else:
            self.tarea_service.restaurar_tarea(
                nuevo
            )

    def _rehacer_estado(self, accion):

        datos = accion.datos

        self.tarea_service.cambiar_estado(
            datos["tarea_id"],
            datos["estado_nuevo"],
            datos.get("usuario_id"),
            registrar_historial=False,
            registrar_auditoria=False
        )

    def _auditar(self, usuario_id, accion_nombre, accion):

        if self.auditoria_service is None:
            return

        tarea_id = None

        if accion.tipo == Accion.CAMBIAR_ESTADO:
            tarea_id = accion.datos.get("tarea_id")

        elif hasattr(accion.datos, "padre_id"):
            tarea_id = accion.datos.id

        self.auditoria_service.registrar(
            usuario_id,
            accion_nombre,
            tarea_id
        )