# Notebooks del Proyecto

1. **`01_carga_y_variables.ipynb`** *(Avance inicial preservado)*: Carga y unión de los cinco CSV originales (`36,733 × 12`), diccionario de variables y exploración descriptiva sobre `2011–2012`.
2. **`Proyecto_Final_Turbina_Colab.ipynb`** *(Proyecto Final Completo — Compatible Local y Google Colab)*:
   - Carga reproducible con verificación SHA-256 (local desde `data/raw/` o descarga automática desde UCI al abrirse en Google Colab).
   - Descubrimiento de regímenes físicos de operación (`PCA` + `K-Means`) y contraste inferencial (`ANOVA`, `Tukey HSD` y `Kruskal-Wallis`) sobre entrenamiento (`2011–2012`).
   - Diagnóstico de multicolinealidad (`VIF`) y verificación de supuestos de residuos en Regresión Lineal MCO (Q-Q Plot, homocedasticidad y secuencia temporal).
   - Iteración y comparación en Validación (`2013`) entre **Set A** (`AT, AP, AH`) y **Set B** (9 sensores ambientales y operativos, sin `CO`), cubriendo Baseline, MCO, Ridge, Lasso, PCA+MCO, Polinomial Grado 2 + Ridge, Árboles CART, Random Forest, SVR (Kernel RBF) y Ensambles por Agregación.
   - Evaluación final única en Prueba (`2014–2015`), análisis físico de deriva interanual, monitoreo de condiciones fuera de dominio con `Isolation Forest` y sistema integrado `SensorVirtualTurbinaNOx` con batería de pruebas automatizadas.

Desde la raíz del repositorio: `uv run jupyter lab` (kernel **Python 3 (ipykernel)**), o abrir directamente `Proyecto_Final_Turbina_Colab.ipynb` en Google Colab y pulsar **Ejecutar todas**.
