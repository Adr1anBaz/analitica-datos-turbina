"""Comprueba imports, kernel y archivos, sin ajustar modelos ni transformar datos."""

import importlib
import json
import platform
from importlib.metadata import version

from scripts.datos import verificar_directorio

PACKAGES = {
    "numpy": "numpy", "pandas": "pandas", "matplotlib": "matplotlib",
    "seaborn": "seaborn", "scikit-learn": "sklearn", "jupyterlab": "jupyterlab",
    "ipykernel": "ipykernel",
}


def main() -> None:
    print(f"Python {platform.python_version()}")
    if platform.python_version_tuple()[:2] != ("3", "12"):
        raise SystemExit("Se requiere Python 3.12. Ejecuta primero uv sync --locked.")
    for distribution, module in PACKAGES.items():
        importlib.import_module(module)
        print(f"OK {distribution}=={version(distribution)}")
    from jupyter_client.kernelspec import KernelSpecManager
    kernels = KernelSpecManager().find_kernel_specs()
    if "python3" not in kernels:
        raise SystemExit("No se encontró el kernel python3 dentro del entorno Jupyter.")
    print("OK kernel Jupyter python3")
    try:
        summary = verificar_directorio()
    except (OSError, ValueError) as error:
        raise SystemExit(str(error)) from error
    print(json.dumps(summary, indent=2, ensure_ascii=False))
    print("Setup y datos verificados. Sin entrenamiento ni evaluación predictiva.")


if __name__ == "__main__":
    main()
