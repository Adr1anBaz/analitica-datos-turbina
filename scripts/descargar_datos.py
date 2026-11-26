"""Descarga reproducible: uv run python -m scripts.descargar_datos."""

import io
import json
import os
import tempfile
import urllib.request
import zipfile
from pathlib import Path

from scripts.datos import FILES, RAW, URL, ZIP_SHA256, verificar_directorio, verificar_hash


def descargar(directory: Path = RAW) -> dict:
    directory.mkdir(parents=True, exist_ok=True)
    # Un archivo existente diferente se respeta: requiere intervención humana.
    for name, expected in FILES.items():
        path = directory / name
        if path.exists():
            verificar_hash(path.read_bytes(), expected["sha256"], name)
    if all((directory / name).is_file() for name in FILES):
        print("Los tres archivos ya existen; verificando sin volver a descargarlos.")
        return verificar_directorio(directory)

    print(f"Descargando originales desde {URL}")
    request = urllib.request.Request(URL, headers={"User-Agent": "ScaniaAPS-AcademicSetup/0.1"})
    with urllib.request.urlopen(request, timeout=180) as response:
        payload = response.read()
    verificar_hash(payload, ZIP_SHA256, "ZIP original UCI")
    with zipfile.ZipFile(io.BytesIO(payload)) as archive:
        contents = {name: archive.read(name) for name in FILES}
    # Validar todos los contenidos antes de escribir; no hacer extractall.
    for name, data in contents.items():
        verificar_hash(data, FILES[name]["sha256"], name)
    with tempfile.TemporaryDirectory(prefix=".descarga-", dir=directory) as temporary:
        for name, data in contents.items():
            candidate = Path(temporary) / name
            candidate.write_bytes(data)
        for name in contents:
            os.replace(Path(temporary) / name, directory / name)
    return verificar_directorio(directory)


def main() -> None:
    try:
        summary = descargar()
    except (OSError, ValueError, KeyError, zipfile.BadZipFile) as error:
        raise SystemExit(f"No se completó la descarga: {error}") from error
    print(json.dumps(summary, indent=2, ensure_ascii=False))
    print("Datos originales locales verificados. No se limpiaron ni se entrenaron modelos.")


if __name__ == "__main__":
    main()
