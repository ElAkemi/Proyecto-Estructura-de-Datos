import csv

from pathlib import Path


def test_escritura_csv(tmp_path):

    archivo = tmp_path / "usuarios.csv"

    datos = [
        ["1", "Administrador", "Administrador"],
        ["2", "Ana Rojas", "Usuario"],
    ]

    with open(
        archivo,
        "w",
        newline="",
        encoding="utf-8"
    ) as salida:

        escritor = csv.writer(salida)

        for fila in datos:
            escritor.writerow(fila)

    assert archivo.exists()

    with open(
        archivo,
        "r",
        newline="",
        encoding="utf-8"
    ) as entrada:

        lector = list(csv.reader(entrada))

    assert len(lector) == 2
    assert lector[0][0] == "1"
    assert lector[1][1] == "Ana Rojas"


def test_auditoria_es_append_only(tmp_path):

    archivo = tmp_path / "auditoria_log.csv"

    primera_linea = (
        "2026-08-31 10:00:00|1|"
        "CAMBIAR_ESTADO:Completada|10\n"
    )

    segunda_linea = (
        "2026-08-31 10:01:00|1|"
        "DESHACER|10\n"
    )

    with open(
        archivo,
        "a",
        encoding="utf-8"
    ) as salida:
        salida.write(primera_linea)

    with open(
        archivo,
        "a",
        encoding="utf-8"
    ) as salida:
        salida.write(segunda_linea)

    contenido = archivo.read_text(
        encoding="utf-8"
    )

    assert primera_linea in contenido
    assert segunda_linea in contenido
    assert contenido.count("\n") == 2

