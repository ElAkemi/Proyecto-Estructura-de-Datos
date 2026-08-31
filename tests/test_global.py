from models.usuario import Usuario
from structures.lista_doble import ListaDoble
from structures.pila import Pila
from structures.cola_fifo import ColaFIFO
from structures.cola_prioridad import ColaPrioridad
from models.tarea import Tarea

def test_lista_doble_insertar_y_buscar():
    lista = ListaDoble()

    usuario1 = Usuario(
        1,
        "Ana",
        "Usuario",
        "1234"
    )

    usuario2 = Usuario(
        2,
        "Carlos",
        "Usuario",
        "5678"
    )

    lista.insertar(usuario1)
    lista.insertar(usuario2)

    assert lista.buscar(1) is not None
    assert lista.buscar(2) is not None


def test_lista_doble_eliminar():
    lista = ListaDoble()

    usuario = Usuario(
        1,
        "Ana",
        "Usuario",
        "1234"
    )

    lista.insertar(usuario)
    lista.eliminar(1)

    assert lista.buscar(1) is None


def test_pila_lifo():
    pila = Pila()

    pila.apilar("A")
    pila.apilar("B")

    assert pila.desapilar() == "B"
    assert pila.desapilar() == "A"


def test_cola_fifo():
    cola = ColaFIFO()

    cola.encolar("A")
    cola.encolar("B")

    assert cola.desencolar() == "A"
    assert cola.desencolar() == "B"


def test_cola_prioridad():
    cola = ColaPrioridad()

    tarea_baja = Tarea(
        1,
        "BAJA",
        10,
        "Tarea baja"
    )

    tarea_urgente = Tarea(
        2,
        "URGENTE",
        10,
        "Tarea urgente"
    )

    tarea_media = Tarea(
        3,
        "MEDIA",
        10,
        "Tarea media"
    )

    cola.encolar(tarea_baja)
    cola.encolar(tarea_urgente)
    cola.encolar(tarea_media)

    assert cola.desencolar().prioridad.name == "URGENTE"


def test_pila_vacia():
    pila = Pila()

    assert pila.esta_vacia() is True


def test_cola_vacia():
    cola = ColaFIFO()

    assert cola.esta_vacia() is True
