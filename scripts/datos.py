"""Origen y verificaciones de los archivos originales Scania APS."""

import csv
import hashlib
import io
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw"
URL = "https://archive.ics.uci.edu/static/public/421/aps+failure+at+scania+trucks.zip"
ZIP_SHA256 = "5504d0402f54faaf97ac0ca085a621645763f5cfea2eb29c592b057d43d4db89"
FILES = {
    "aps_failure_training_set.csv": {
        "sha256": "bb484302e3a3a1c8ef5e1f0129c4dc7cbd58f350867f95b575461ca21ab6b9da",
        "rows": 60000,
        "classes": {"neg": 59000, "pos": 1000},
    },
    "aps_failure_test_set.csv": {
        "sha256": "2cdf6f7661c7b4c63333c93cdec36a3a82350176b604a2312cf82799fb2712f3",
        "rows": 16000,
        "classes": {"neg": 15625, "pos": 375},
    },
    "aps_failure_description.txt": {
        "sha256": "57b1eb3c551a678ffc1c8112e5b34c566dd16457642563f58aeb3ca65beeb820",
    },
}


def sha256_bytes(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def verificar_hash(payload: bytes, expected: str, name: str) -> None:
    if sha256_bytes(payload) != expected:
        raise ValueError(f"Hash SHA-256 inesperado: {name}. No se usará ni sobrescribirá el archivo.")


def resumir_csv(payload: bytes) -> dict:
    """Lee el encabezado real después del preámbulo, sin alterar los datos."""
    stream = io.StringIO(payload.decode("utf-8-sig"))
    for line in stream:
        if line.startswith("class,"):
            header = next(csv.reader([line]))
            break
    else:
        raise ValueError("No se encontró el encabezado class, en el CSV.")
    if len(header) != 171 or len(set(header)) != 171:
        raise ValueError("Se esperaban 171 columnas únicas: etiqueta y 170 predictores.")
    labels = Counter()
    rows = 0
    missing = 0
    for row in csv.reader(stream):
        if len(row) != len(header):
            raise ValueError(f"Fila de datos {rows + 1}: ancho distinto del encabezado.")
        if row[0] not in ("pos", "neg"):
            raise ValueError(f"Etiqueta no reconocida en fila de datos {rows + 1}.")
        labels[row[0]] += 1
        missing += row[1:].count("na")
        rows += 1
    return {"rows": rows, "columns": len(header), "classes": dict(labels), "missing_cells": missing}


def verificar_directorio(directory: Path = RAW) -> dict:
    summaries = {}
    for name, expected in FILES.items():
        path = directory / name
        if not path.is_file():
            raise FileNotFoundError(f"Falta {path}. Ejecuta: uv run python -m scripts.descargar_datos")
        payload = path.read_bytes()
        verificar_hash(payload, expected["sha256"], name)
        if name.endswith(".csv"):
            summary = resumir_csv(payload)
            if summary["rows"] != expected["rows"] or summary["classes"] != expected["classes"]:
                raise ValueError(f"Conteos inesperados: {name}")
            summaries[name] = summary
    return summaries
