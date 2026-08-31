from models.accion import Accion
from services.historial_service import HistorialService


def test_registrar_accion():
    historial = HistorialService()

    accion = Accion(
        "AGREGAR",
        "Se agregó el usuario: 1",
        None
    )

    historial.registrar_accion(accion)

    assert not historial.pila_deshacer.esta_vacia()


def test_deshacer_accion():
    historial = HistorialService()

    accion = Accion(
        "AGREGAR",
        "Se agregó el usuario: 1",
        None
    )

    historial.registrar_accion(accion)

    resultado = historial.deshacer_accion()

    assert resultado is not None
    assert historial.pila_deshacer.esta_vacia()


def test_redo_despues_de_undo():
    historial = HistorialService()

    accion = Accion(
        "AGREGAR",
        "Se agregó el usuario: 1",
        None
    )

    historial.registrar_accion(accion)

    historial.deshacer_accion()

    assert not historial.pila_rehacer.esta_vacia()
