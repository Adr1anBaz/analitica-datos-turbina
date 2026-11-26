# Emisiones de una turbina de gas · Analítica de Datos

Proyecto académico con **mediciones reales e interpretables** de operación y emisiones de una turbina de gas. Ruta candidata: estimar la concentración de NOx mediante regresión y evaluar la utilidad de las mediciones operativas frente a usar sólo variables ambientales.

**Estado actual:** entorno reproducible, descarga verificada y notebook inicial de carga. No se han limpiado datos, convertido unidades, generado gráficas, separado X/y ni entrenado modelos.

## Requisitos

- Git, acceso al repositorio privado y conexión para instalar y descargar.
- [uv](https://docs.astral.sh/uv/getting-started/installation/). En macOS con Homebrew: `brew install uv`. En Windows: `winget install --id=astral-sh.uv -e`.
- Python **3.12.12**, fijado en `.python-version`; uv puede descargarlo si falta. No hace falta instalar paquetes globales ni activar manualmente `.venv`.

Cada integrante necesita aceptar una invitación desde **Settings → Collaborators**. El enlace solo no concede acceso al repositorio privado.

## Instalar, descargar y verificar

```sh
git clone git@github.com:Adr1anBaz/analitica-datos-turbina.git
cd analitica-datos-turbina
uv sync --locked
uv run python -m scripts.descargar_datos
uv run python -m scripts.verificar_setup
uv run python -m unittest discover -s tests -v
```

El clon SSH requiere una llave autorizada. Alternativa con la autenticación HTTPS de tu cliente Git:

```sh
git clone https://github.com/Adr1anBaz/analitica-datos-turbina.git
```

No guardar credenciales o llaves privadas en el proyecto. `uv.lock` fija las versiones exactas de pandas, NumPy, matplotlib, seaborn, scikit-learn, JupyterLab, ipykernel y sus dependencias.

## Abrir el archivo de trabajo

Desde la raíz del proyecto:

```sh
uv run jupyter lab
```

Abrir **`notebooks/01_carga_y_variables.ipynb`** con el kernel **Python 3 (ipykernel)**. Ejecutar de arriba hacia abajo con `Shift+Enter` o **Run → Run All Cells**.

El notebook:

1. Importa las librerías habituales de clase.
2. Carga cada CSV con `pd.read_csv` y añade el año del archivo.
3. Apila los cinco años con `pd.concat`, sin reordenar ni eliminar observaciones.
4. Deja un único DataFrame **`df` de 36,733 filas y 12 columnas**: once variables originales y `anio` como procedencia.
5. Muestra sus dimensiones, primeras filas y lista de columnas, con un diccionario de significados y dudas documentales.

No se guarda un CSV unido: por ahora trabajamos con `df` en memoria y conservamos los originales intactos. Unir filas no obliga a mezclarlas aleatoriamente para evaluar modelos después.

Jupyter se ejecuta dentro de `.venv` gracias a `uv run`. Si no abre el navegador, usar la URL de la terminal; no compartir su token de sesión. Para detenerlo, `Ctrl+C` y confirmar si lo solicita. En VS Code, seleccionar el intérprete `.venv` del proyecto.

## Datos

| Archivo original | Filas | Columnas originales |
|---|---:|---:|
| `gt_2011.csv` | 7,411 | 11 |
| `gt_2012.csv` | 7,628 | 11 |
| `gt_2013.csv` | 7,152 | 11 |
| `gt_2014.csv` | 7,158 | 11 |
| `gt_2015.csv` | 7,384 | 11 |
| **Total** | **36,733** | **11** |

Columnas originales: `AT`, `AP`, `AH`, `AFDP`, `GTEP`, `TIT`, `TAT`, `TEY`, `CDP`, `CO`, `NOX`. Ver [diccionario y sentido de ingeniería](docs/VARIABLES.md).

Cada registro corresponde a datos agregados de una hora de operación de una instalación en Turquía, no a una turbina distinta. Los archivos no publican fechas completas por fila. El año se conoce por el nombre del archivo, no por una medición adicional.

**Unidades pendientes de aclaración:** CDP presenta una contradicción entre tabla y esquema del artículo. TEY se conserva como producción energética con la unidad publicada, sin asumir que sea potencia o eficiencia. No corregimos números por suposición; ambas cuestiones se detallan en el diccionario.

## Fuente e integridad

- [UCI: Gas Turbine CO and NOx Emission Data Set](https://archive.ics.uci.edu/dataset/551/gas+turbine+co+and+nox+emission+data+set).
- [DOI del dataset: 10.24432/C5WC95](https://doi.org/10.24432/C5WC95).
- [Artículo original: Kaya, Tüfekci y Uzun (2019)](https://journals.tubitak.gov.tr/elektrik/vol27/iss6/53), [DOI 10.3906/elk-1807-87](https://doi.org/10.3906/elk-1807-87).
- Licencia publicada por UCI: **CC BY 4.0**; citar y atribuir la fuente al utilizar los datos.
- ZIP: aproximadamente **1.09 MB**; los cinco CSV suman aproximadamente **2.78 MB**. Reservar espacio adicional para el entorno Python.
- SHA-256 del ZIP: `55fdb1acc25f05bd9c77aac285c424e9154ffb0dbf1bbadb56b69a1142231295`.

El script verifica el ZIP y cada CSV con hashes fijados en `scripts/datos.py`. Comprueba encabezados, conteos y valores numéricos finitos. **No cambia unidades ni rellena valores.** Volver a ejecutar con los cinco originales presentes sólo verifica; no descarga de nuevo. Un archivo existente diferente no se sobrescribe.

## Estructura

```text
.
├── pyproject.toml / uv.lock / .python-version
├── scripts/
│   ├── datos.py
│   ├── descargar_datos.py
│   └── verificar_setup.py
├── tests/test_setup.py
├── notebooks/01_carga_y_variables.ipynb
├── docs/VARIABLES.md
├── docs/plans/
├── data/raw/          # Cinco originales locales, fuera de Git
├── data/processed/    # Reservado; sin datos transformados
└── outputs/           # Reservado; sin resultados de modelos
```

Git versiona código, notebook sin salidas guardadas, documentación, pruebas y configuración. Excluye los CSV, `.venv`, resultados, cachés y secretos. Cada integrante descarga sus originales.

## Solución de problemas

- **`uv` no se reconoce:** instalarlo y abrir otra terminal.
- **Repositorio no encontrado:** revisar cuenta autenticada, invitación aceptada y acceso SSH/HTTPS.
- **Falta un CSV:** ejecutar `uv run python -m scripts.descargar_datos` desde la raíz.
- **Hash inesperado:** detenerse y revisar si cambió la fuente o el archivo local. No modificar hashes para ocultar el error ni sobrescribir trabajo sin revisarlo.
- **Error de conexión:** comprobar acceso a UCI y reintentar; sólo se escriben originales tras verificar el contenido descargado.
- **Jupyter usa otro entorno:** detenerlo y arrancar con `uv run jupyter lab` desde esta carpeta.
- **Lock incompatible:** usar `pyproject.toml` y `uv.lock` del mismo commit; no regenerarlo sin revisar cambios.

## Límites y siguiente etapa

El primer trabajo es entender las variables. Más adelante se elegirá una respuesta principal y un protocolo de regresión. La partición temporal publicada es 2011–2012 para entrenamiento, 2013 para validación y 2014–2015 para prueba; aún no está implementada.

Estimar emisiones de la misma hora no es pronosticar el futuro, demostrar causalidad ni sustituir legalmente un analizador certificado. No se promete precisión antes de entrenar y evaluar.
