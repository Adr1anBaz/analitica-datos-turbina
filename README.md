# Scania APS · Proyecto de Analítica de Datos

Proyecto académico de **clasificación de fallas relacionadas con el sistema neumático APS** en camiones Scania, con futura evaluación sensible al costo de los errores.

**Estado actual: únicamente setup y descarga.** No hay modelos entrenados, imputación, balanceo, selección de variables ni resultados predictivos.

## Requisitos

- Git y conexión a internet para clonar, instalar y descargar los datos.
- [uv](https://docs.astral.sh/uv/getting-started/installation/), gestor del entorno Python. En macOS con Homebrew: `brew install uv`; en Windows: `winget install --id=astral-sh.uv -e`.
- Acceso al repositorio privado. El propietario debe invitar a cada integrante desde **Settings → Collaborators**. No basta con recibir el enlace.

El proyecto fija **Python 3.12.12** en `.python-version`. `uv sync --locked` puede descargarlo si no está instalado. Las dependencias exactas están en `uv.lock`; no hace falta instalar Python o paquetes globalmente ni activar manualmente `.venv`.

## Arranque desde cero

En Terminal, PowerShell o la terminal de VS Code, ejecutar cada comando desde la carpeta del proyecto:

```sh
git clone git@github.com:Adr1anBaz/analitica-datos-scania-aps.git
cd analitica-datos-scania-aps
uv sync --locked
uv run python -m scripts.descargar_datos
uv run python -m scripts.verificar_setup
uv run python -m unittest discover -s tests -v
```

El clon por SSH requiere una llave autorizada en la cuenta de GitHub con acceso. Como alternativa, clonar con la autenticación HTTPS de tu cliente Git:

```sh
git clone https://github.com/Adr1anBaz/analitica-datos-scania-aps.git
```

No pongas tokens, contraseñas o llaves privadas en comandos guardados, archivos del proyecto o commits.

### Qué debe pasar

1. `uv sync --locked` crea `.venv/` y usa las versiones de `uv.lock` sin modificarlo.
2. La descarga obtiene los **tres originales** de UCI y los guarda en `data/raw/`. Verifica SHA-256 del ZIP y de cada archivo.
3. La verificación importa las siete dependencias principales, comprueba el kernel de Jupyter y valida archivos, columnas y etiquetas. No ajusta ningún modelo.
4. Las pruebas unitarias deben terminar en `OK`.

El ZIP descargado tiene aproximadamente **56.6 MB**; los originales suman aproximadamente **56.6 MB**. Además, reservar espacio para el entorno y sus dependencias. El descargador lee el ZIP en memoria y no conserva una copia adicional.

## Abrir Jupyter

Desde la raíz del repositorio:

```sh
uv run jupyter lab
```

Se abrirá JupyterLab en el navegador. Si no abre automáticamente, usar la URL que imprime la terminal. Dentro de `notebooks/`, crear un notebook con **Python 3 (ipykernel)**. Mantener esa terminal abierta; para detener el servidor, usar `Ctrl+C` y confirmar si lo solicita. No compartir la URL que contiene el token de sesión.

No se instala un kernel global: Jupyter y Python se ejecutan en `.venv/` mediante `uv run`. En VS Code también puedes seleccionar el intérprete `.venv` del proyecto (en Windows, `.venv\Scripts\python.exe`).

## Archivos y datos

```text
.
├── pyproject.toml             # Dependencias directas y versión de Python
├── uv.lock                    # Versiones exactas resueltas
├── .python-version
├── scripts/
│   ├── datos.py               # Fuente, hashes y validaciones
│   ├── descargar_datos.py     # Descarga los originales
│   └── verificar_setup.py     # Comprueba entorno y datos
├── tests/test_setup.py
├── notebooks/                 # Reservado para trabajo futuro
├── data/raw/                  # Originales locales, fuera de Git
├── data/processed/            # Reservado; no contiene datos transformados
├── outputs/                   # Reservado para resultados futuros
└── docs/plans/
```

| Original | Filas | Columnas | Etiquetas |
|---|---:|---:|---|
| `aps_failure_training_set.csv` | 60,000 | 171 | 59,000 `neg`, 1,000 `pos` |
| `aps_failure_test_set.csv` | 16,000 | 171 | 15,625 `neg`, 375 `pos` |
| `aps_failure_description.txt` | — | — | Descripción y condiciones originales |

Las 171 columnas incluyen **170 predictores y `class`**. Los archivos CSV llevan un preámbulo antes del encabezado; no leerlos como si su primera línea fuera el nombre de las columnas. El código de verificación localiza la línea que empieza por `class,`. `na` representa un faltante; los originales no se modifican.

**`pos`** identifica fallas del componente APS; **`neg`** corresponde a fallas no relacionadas con APS, no necesariamente vehículos sanos. Las variables están anonimizadas: no atribuirles significados físicos no documentados. El dataset no fija un horizonte como «fallará en siete días».

## Fuente, integridad y uso

- [Ficha original UCI](https://archive.ics.uci.edu/dataset/421/aps+failure+at+scania+trucks).
- [DOI: 10.24432/C51S51](https://doi.org/10.24432/C51S51).
- Descarga: `https://archive.ics.uci.edu/static/public/421/aps+failure+at+scania+trucks.zip`.
- SHA-256 del ZIP: `5504d0402f54faaf97ac0ca085a621645763f5cfea2eb29c592b057d43d4db89`.
- Los hashes de cada original están fijados en `scripts/datos.py`.

El archivo original de descripción incluye condiciones GPL v3 o posterior, mientras que la ficha actual de UCI muestra CC BY 4.0. Conservamos la descripción sin alterarla y no redistribuimos los CSV en este repositorio. Consultar las condiciones de la fuente antes de redistribuir; este setup no cambia ni resuelve esa discrepancia de licencias.

## Qué se sube a GitHub

Se versionan código, documentación, pruebas, configuración y `uv.lock`. **No se suben** `.venv/`, datos originales o procesados, resultados locales, cachés ni secretos. Cada integrante descarga sus propios originales con el comando documentado.

Conservar la separación original de desarrollo y prueba. La prueba se reserva para la futura evaluación: no utilizarla para elegir imputación, variables, umbral o hiperparámetros. La verificación actual sólo confirma integridad y estructura, no explora relaciones predictivas.

## Problemas frecuentes

- **`uv` no se reconoce:** instalar uv y abrir una terminal nueva.
- **El clon dice `Repository not found`:** comprobar invitación aceptada, cuenta autenticada y acceso SSH/HTTPS; el repo es privado.
- **Faltan datos:** ejecutar `uv run python -m scripts.descargar_datos` desde la raíz.
- **Hash inesperado:** detenerse. Puede haber un archivo local modificado o un cambio en la fuente. El script no sobrescribe archivos existentes diferentes; revisar y respaldar antes de decidir qué hacer. No cambiar los hashes para ocultar el error.
- **Ya descargué los datos:** volver a ejecutar es seguro; verifica los originales existentes y no vuelve a descargarlos si están completos.
- **Error de conexión:** comprobar acceso a UCI y reintentar. Los archivos finales sólo se escriben después de verificar el ZIP y sus contenidos.
- **Jupyter usa otro Python:** detenerlo y arrancar con `uv run jupyter lab` desde esta carpeta, no con un comando global.
- **`uv.lock` no coincide:** no regenerarlo sin revisar cambios; usar el archivo del commit correspondiente junto con `pyproject.toml`.

## Próxima etapa (no implementada)

Definir la pregunta principal y protocolo de evaluación, y después comenzar la exploración únicamente con desarrollo. La idea candidata es comparar decisiones de revisión usando la penalización del desafío: **10 × falsas alarmas + 500 × fallas APS omitidas**. Es una escala del benchmark, no un costo en pesos ni un ahorro demostrado.
