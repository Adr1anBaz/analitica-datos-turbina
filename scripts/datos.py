"""Fuente e integridad de los cinco CSV originales de la turbina de gas."""

import csv
import hashlib
import io
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw"
URL = "https://archive.ics.uci.edu/static/public/551/gas+turbine+co+and+nox+emission+data+set.zip"
ZIP_SHA256 = "55fdb1acc25f05bd9c77aac285c424e9154ffb0dbf1bbadb56b69a1142231295"
COLUMNS = ["AT", "AP", "AH", "AFDP", "GTEP", "TIT", "TAT", "TEY", "CDP", "CO", "NOX"]
FILES = {
    "gt_2011.csv": {
        "sha256": "d87ceef9aa59533cc7d924d10de241b1b06ecd11f9b26bab59191ea0f8a76b9a",
        "rows": 7411, "year": 2011,
    },
    "gt_2012.csv": {
        "sha256": "be54b9d0e1a7de40c55d32fa489e75de892b000c066b5a09f09a19124ee29100",
        "rows": 7628, "year": 2012,
    },
    "gt_2013.csv": {
        "sha256": "13c437bb440ec2045bd12057e6654c41dd4107a661eac16ba2e878e897a08f9e",
        "rows": 7152, "year": 2013,
    },
    "gt_2014.csv": {
        "sha256": "c2a03c92c9c3207aad0c6be7de8d9b5b4bfa4720ad0efb2c1f21b6cec4d3f3fa",
        "rows": 7158, "year": 2014,
    },
    "gt_2015.csv": {
        "sha256": "9b08f35fde0d4b138232a605db4093c2b8bf9d6757e6f1fbd9534ad616c13591",
        "rows": 7384, "year": 2015,
    },
}


def sha256_bytes(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def verificar_hash(payload: bytes, expected: str, name: str) -> None:
    if sha256_bytes(payload) != expected:
        raise ValueError(f"Hash SHA-256 inesperado: {name}. No se usará ni sobrescribirá el archivo.")


def resumir_csv(payload: bytes) -> dict:
    """Verifica estructura y números sin modificar, imputar ni convertir unidades."""
    reader = csv.reader(io.StringIO(payload.decode("utf-8-sig")))
    header = next(reader, None)
    if header != COLUMNS:
        raise ValueError("Encabezado inesperado: se requieren las once columnas originales en orden.")
    rows = 0
    for row in reader:
        if len(row) != len(header):
            raise ValueError(f"Fila de datos {rows + 1}: ancho distinto del encabezado.")
        for name, value in zip(header, row):
            try:
                number = float(value)
            except ValueError as error:
                raise ValueError(f"Fila {rows + 1}, {name}: falta un valor numérico válido.") from error
            if not math.isfinite(number):
                raise ValueError(f"Fila {rows + 1}, {name}: valor no finito.")
        rows += 1
    return {"rows": rows, "columns": len(header), "missing_cells": 0}


def verificar_directorio(directory: Path = RAW) -> dict:
    summaries = {}
    for name, expected in FILES.items():
        path = directory / name
        if not path.is_file():
            raise FileNotFoundError(f"Falta {path}. Ejecuta: uv run python -m scripts.descargar_datos")
        payload = path.read_bytes()
        verificar_hash(payload, expected["sha256"], name)
        summary = resumir_csv(payload)
        if summary["rows"] != expected["rows"]:
            raise ValueError(f"Conteo de filas inesperado: {name}")
        summaries[name] = {"year": expected["year"], **summary}
    return summaries
