# Emisiones de una turbina de gas · Analítica de Datos

Proyecto final de regresión y monitoreo operativo para estimar la concentración contemporánea de **NOX** (`mg/m³`) de una turbina de gas industrial a partir de sus condiciones ambientales y operativas, evaluando su desempeño en años posteriores (`2014–2015`).

**Integrantes:** José Adrián Bazaldua Huerta · Sebastián de Jesús Enguilo Ruiz  
**Materia:** Aplicaciones de Analítica de Datos · Universidad Iberoamericana

---

## Pregunta de investigación y resultados principales

> **¿Cuánto mejora la estimación horaria de `NOX` al incorporar variables internas de la turbina (`Set B`: 9 sensores) frente a emplear únicamente variables ambientales (`Set A`: `AT`, `AP`, `AH`), y se conserva esa mejora en años posteriores (`2014–2015`)?**

### Protocolo temporal sin fuga de datos
- **Entrenamiento (`2011–2012`):** `15,039` registros horarios (único bloque donde se ajustan escaladores, `PCA`, `K-Means`, `Isolation Forest` y pesos de regresión).
- **Validación (`2013`):** `7,152` registros horarios (comparación de arquitecturas y ajuste de hiperparámetros).
- **Prueba final (`2014–2015`):** `14,542` registros horarios (`7,158` en 2014 + `7,384` en 2015), evaluados una única vez con modelos congelados en `2011–2012`.
- **Exclusiones estrictas en `X`:** Se excluyen `CO` (para no depender de otro analizador de gases), `NOX` y `anio`.

### Resumen de desempeño obtenido

| Modelo / Configuración | Sensores (`X`) | Val 2013 MAE | Val 2013 RMSE | Val 2013 $R^2$ | Prueba 2014–2015 MAE | Prueba 2014–2015 RMSE | Prueba 2014–2015 $R^2$ | Corr. Dinámica $r$ (14–15) |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Baseline (Media `2011–2012`) | — | 8.931 | 12.184 | -0.0227 | 11.512 | 13.391 | -0.6031 | 0.0000 |
| Regresión Lineal MCO (`Set A`) | 3 vars | 6.956 | 9.746 | 0.3456 | 10.521 | 12.173 | -0.3246 | 0.6418 |
| Random Forest (`Set A`) | 3 vars | 6.715 | 9.470 | 0.3820 | 10.194 | 11.918 | -0.2697 | 0.5980 |
| SVR Kernel RBF (`Set A`) | 3 vars | 6.582 | 9.342 | 0.3986 | 10.325 | 11.951 | -0.2767 | 0.5984 |
| Regresión Lineal MCO (`Set B`) | 9 vars | 7.690 | 10.628 | 0.2218 | 7.431 | 10.102 | 0.0877 | 0.5472 |
| Poly Grado 2 + Ridge (`Set B`) | 9 vars | 5.557 | 7.658 | 0.5959 | 7.286 | 8.951 | 0.2837 | 0.7482 |
| Random Forest `mf=sqrt` (`Set B`) | 9 vars | 5.692 | 7.520 | 0.6104 | 10.153 | 11.428 | -0.1674 | 0.8053 |
| SVR Kernel RBF (`Set B`) | 9 vars | 5.472 | 7.498 | 0.6126 | 11.579 | 12.669 | -0.4348 | 0.8162 |
| **Ensamble No Lineal (`SVR+RF+PolyRidge`, `Set B`)** | **9 vars** | **5.485** | **7.409** | **0.6218** | 9.206 | 10.404 | 0.0324 | **0.8217** |
| **Ensamble Híbrido Extrapolable (`PolyRidge+RF+Ridge`, `Set B`)** | **9 vars** | 5.730 | 7.757 | 0.5854 | **7.103** | **8.612** | **0.3370** | 0.7930 |

### Hallazgos centrales de ingeniería
1. **Valor incremental de los sensores internos:** En operación sin cambio de planta (`2013`), incorporar las 6 señales internas reduce el `RMSE` de `9.34` a **`7.41 mg/m³`** (`-20.7%`, $R^2 = 0.622$). En `2014–2015`, el **Ensamble Híbrido Extrapolable** reduce el `RMSE` de `11.92–12.17` (`Set A`) a **`8.61 mg/m³`** (`-27.8%`, $R^2 = +0.337$).
2. **Regímenes físicos y no linealidad (`K-Means` + `ANOVA` + `Tukey HSD`):** `K-Means` identificó tres modos de operación en entrenamiento: *Carga Parcial* (`~112 MWh`, `NOX = 68.53 mg/m³`), *Carga Nominal* (`~134 MWh`, `NOX = 69.28 mg/m³`) y *Carga Plena DLN* (`~158 MWh`, **`NOX = 65.05 mg/m³`**). `ANOVA` ($F = 198.48, p < 10^{-85}$) y `Tukey HSD` ($p \le 0.001$) demuestran que a plena carga disminuyen las emisiones por operación óptima de premezcla pobre (*Dry Low NOx*), explicando el fracaso de MCO lineal simple.
3. **Deriva física en `2014–2015` y vigilancia con `Isolation Forest`:** A igual carga (`132–136 MWh`) y temperatura ambiente (`15–20 °C`), a partir de `2014` la planta operó con menor `TIT` y mayor `CO`, reduciendo el nivel real de `NOX` unos `8–9 mg/m³` (*trade-off* $\text{CO}$–$\text{NO}_x$). Los árboles y `SVR RBF` mantienen alta correlación dinámica ($r > 0.80$) pero no extrapolan fuera del rango histórico de `TIT`, mientras que el **Ensamble Híbrido Extrapolable** sí proyecta esa caída térmica. `Isolation Forest` detecta el incremento de condiciones fuera de dominio en `2015` (`11.08%` de alertas) donde el error es mayor.

---

## Notebooks disponibles

- **[`notebooks/Proyecto_Final_Turbina_Colab.ipynb`](notebooks/Proyecto_Final_Turbina_Colab.ipynb)** — **Notebook principal completo (compatible con Google Colab y entorno local):** incluye carga con verificación SHA-256 (o descarga automática desde UCI en Colab), exploración, `PCA`, `K-Means`, `ANOVA/Tukey/Kruskal-Wallis`, `VIF`, diagnóstico de residuos MCO, iteración de modelos en `2013`, evaluación final `2014–2015`, `Isolation Forest` y la clase integrada `SensorVirtualTurbinaNOx` con pruebas automatizadas.
- **[`notebooks/01_carga_y_variables.ipynb`](notebooks/01_carga_y_variables.ipynb)** — Avance exploratorio inicial conservado íntegramente.

---

## Instalación, ejecución y pruebas locales

```sh
uv sync --locked
uv run python -m scripts.verificar_setup
uv run python -m unittest discover -s tests -v
uv run jupyter lab
```

---

## Fuente e integridad de datos

- [UCI: Gas Turbine CO and NOx Emission Data Set](https://archive.ics.uci.edu/dataset/551/gas+turbine+co+and+nox+emission+data+set) · [DOI: 10.24432/C5WC95](https://doi.org/10.24432/C5WC95) · Licencia [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/).
- Artículo original: Kaya, H., Tüfekci, P., & Uzun, E. (2019), [DOI: 10.3906/elk-1807-87](https://doi.org/10.3906/elk-1807-87).
- Documentación de variables y advertencias sobre unidades (`CDP`, `TEY`): [`docs/VARIABLES.md`](docs/VARIABLES.md).
