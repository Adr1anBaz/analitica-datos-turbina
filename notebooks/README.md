# Notebooks

Empezar con **`01_carga_y_variables.ipynb`**. Contiene la carga y unión de los cinco CSV, el diccionario de variables y la exploración realizada: tipos, faltantes, boxplots, histogramas, comparación anual, correlación y dispersión AT/NOX. Las gráficas usan únicamente 2011 y 2012. El código sigue las herramientas de los ejemplos del profesor y cada resultado tiene una interpretación escrita.

Desde la raíz del repositorio: `uv run jupyter lab`. Al crear un notebook, usar el kernel **Python 3 (ipykernel)** del entorno iniciado con ese comando.

Abrir el notebook y ejecutar sus celdas de arriba hacia abajo con `Shift+Enter`, o usar **Run → Run All Cells**. Los cinco originales completos están incluidos en `data/raw/`; `uv run python -m scripts.descargar_datos` permite verificarlos o recuperarlos desde UCI si faltan.

El notebook conserva las figuras y tablas de una ejecución completa para consultarlas en GitHub. Todavía no define `X` e `y`, no ajusta escaladores y no entrena modelos. Ver [avance y pendientes](../README.md#objetivo-y-avance).
