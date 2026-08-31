import pytest

from services.usuario_service import UsuarioService


class HistorialMock:
    """Historial simulado para las pruebas."""

    def __init__(self):
        self.acciones = []

    def registrar_accion(self, accion):
        self.acciones.append(accion)


class RepositoryMock:
    """Repositorio simulado para las pruebas."""

    def __init__(self):
        self.usuarios = []
        self.guardados = []

    def cargar(self):
        """Devuelve los usuarios persistidos."""

        return self.usuarios.copy()

    def guardar(self, usuarios):
        """Simula la persistencia de usuarios."""

        self.usuarios = usuarios.copy()
        self.guardados.append(usuarios.copy())


@pytest.fixture
def servicio():
    repository = RepositoryMock()
    historial = HistorialMock()

    return UsuarioService(
        repository,
        historial
    )


def test_agregar_usuario(servicio):
    usuario = servicio.agregar_usuario(
        1,
        "Ana Rojas",
        "Usuario",
        "1234"
    )

    assert usuario.id == 1
    assert usuario.nombre == "Ana Rojas"
    assert usuario.rol == "Usuario"


def test_buscar_usuario(servicio):
    servicio.agregar_usuario(
        1,
        "Ana Rojas",
        "Usuario",
        "1234"
    )

    usuario = servicio.buscar_usuario(1)

    assert usuario is not None
    assert usuario.nombre == "Ana Rojas"


def test_no_permite_id_duplicado(servicio):
    servicio.agregar_usuario(
        1,
        "Ana Rojas",
        "Usuario",
        "1234"
    )

    with pytest.raises(ValueError):
        servicio.agregar_usuario(
            1,
            "Carlos Pérez",
            "Usuario",
            "5678"
        )


def test_no_permite_id_invalido(servicio):
    with pytest.raises(ValueError):
        servicio.agregar_usuario(
            0,
            "Ana Rojas",
            "Usuario",
            "1234"
        )


def test_no_permite_nombre_vacio(servicio):
    with pytest.raises(ValueError):
        servicio.agregar_usuario(
            2,
            "",
            "Usuario",
            "1234"
        )


def test_no_permite_rol_invalido(servicio):
    with pytest.raises(ValueError):
        servicio.agregar_usuario(
            3,
            "Ana Rojas",
            "Gerente",
            "1234"
        )


def test_modificar_usuario(servicio):
    servicio.agregar_usuario(
        1,
        "Ana Rojas",
        "Usuario",
        "1234"
    )

    servicio.modificar_usuario(
        1,
        "Ana María Rojas",
        "Administrador",
        "5678"
    )

    usuario = servicio.buscar_usuario(1)

    assert usuario.nombre == "Ana María Rojas"
    assert usuario.rol == "Administrador"
    assert usuario.password == "5678"


def test_eliminar_usuario(servicio):
    servicio.agregar_usuario(
        1,
        "Ana Rojas",
        "Usuario",
        "1234"
    )

    servicio.eliminar_usuario(1)

    assert servicio.buscar_usuario(1) is None


def test_listar_usuarios(servicio):
    servicio.agregar_usuario(
        1,
        "Ana Rojas",
        "Usuario",
        "1234"
    )

    servicio.agregar_usuario(
        2,
        "Carlos Pérez",
        "Administrador",
        "5678"
    )

    usuarios = servicio.listar_usuarios()

    assert len(usuarios) == 2

