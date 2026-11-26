# Datos originales y atribución

Este repositorio incluye los cinco CSV completos de **Gas Turbine CO and NOx Emission Data Set**, publicado en UCI Machine Learning Repository por Heysem Kaya, Pınar Tüfekci y Erdinç Uzun.

- Dataset: https://archive.ics.uci.edu/dataset/551/gas+turbine+co+and+nox+emission+data+set
- DOI del dataset: https://doi.org/10.24432/C5WC95
- Artículo: Kaya, Tüfekci y Uzun (2019), https://doi.org/10.3906/elk-1807-87
- Licencia publicada por UCI: Creative Commons Attribution 4.0 International, https://creativecommons.org/licenses/by/4.0/

Los archivos `raw/gt_2011.csv` a `raw/gt_2015.csv` se redistribuyen sin cambios de valores, columnas ni unidades. Suman 36,733 registros y tienen once columnas cada uno. Su integridad se verifica con los SHA-256 fijados en `scripts/datos.py` mediante `uv run python -m scripts.verificar_setup` desde la raíz del proyecto.

La columna `anio` se añade sólo en memoria al unir las tablas en el notebook. No forma parte de los CSV originales. Las discrepancias documentales de CDP y TEY se explican en [el diccionario de variables](../docs/VARIABLES.md).

Al reutilizar los datos, conservar la atribución a sus autores, el enlace a la fuente y a la licencia, e indicar cualquier modificación. La licencia de los datos no implica respaldo de sus autores a este proyecto.
