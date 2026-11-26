# Diccionario de variables de la turbina de gas

Fuentes: [UCI](https://archive.ics.uci.edu/dataset/551/gas+turbine+co+and+nox+emission+data+set) y [Kaya, Tüfekci y Uzun (2019)](https://journals.tubitak.gov.tr/elektrik/vol27/iss6/53), DOI [10.3906/elk-1807-87](https://doi.org/10.3906/elk-1807-87). El artículo incluye un esquema de sensores y parámetros (figura 2).

Los cinco originales tienen las mismas once columnas. Son registros horarios de operación de una instalación, entre 2011 y 2015, en un rango de carga publicado de aproximadamente 75–100%. No son observaciones independientes de miles de turbinas.

| Columna | Significado | Unidad publicada | Sentido de ingeniería / precaución |
|---|---|---|---|
| AT | Temperatura ambiente | °C | Condiciones térmicas del aire de admisión; no temperatura de llama. |
| AP | Presión atmosférica | mbar | Condiciones ambientales de admisión. |
| AH | Humedad ambiente | % | Humedad del aire que ingresa al proceso. |
| AFDP | Diferencia de presión en el filtro de aire | mbar | Caída de presión a través del filtro; no basta para diagnosticar suciedad por sí sola. |
| GTEP | Presión de escape de la turbina de gas | mbar | Condiciones de escape; no asumir referencia absoluta o manométrica sin confirmación. |
| TIT | Temperatura de entrada a la turbina | °C | Estado térmico antes de la expansión; no equivale directamente a temperatura de llama. |
| TAT | Temperatura después de la turbina | °C | Estado térmico tras la expansión. |
| TEY | Producción energética de la turbina | MWh, escrita MWH en la fuente | No es eficiencia. Confirmar definición del agregado horario antes de interpretarla como potencia. |
| CDP | Presión de descarga del compresor | Inconsistente: mbar en tabla; bar en esquema | Conservar los valores. La unidad física necesita aclaración; no convertir por intuición. |
| CO | Concentración de monóxido de carbono en escape | mg/m³ | Una de las dos respuestas del estudio original; no confundir con CO₂. |
| NOX | Concentración de óxidos de nitrógeno, descritos como NO + NO₂ | mg/m³ | Candidata a respuesta principal de un futuro proyecto de regresión. |
| anio | Año del archivo de origen, añadido al unir | Año calendario | Procedencia, no medición física ni predictor elegido. |

## Dudas documentales y política de trabajo

**CDP:** la tabla 1 y UCI publican mbar para valores aproximadamente 9.85–15.16, mientras la figura 2 del artículo muestra `CDP: 13.1 bar`. Esto documenta una contradicción, no confirma una corrección. No alteramos números ni declaramos resuelta la unidad. Si se confirma bar, corregir la etiqueta no requiere cambiar esos números; una conversión a mbar sería una operación adicional explícita.

**TEY:** conservar la denominación de energía y unidad publicadas. Sólo si se confirma energía acumulada durante exactamente una hora se puede obtener potencia media dividiendo por ese intervalo. No renombrar como MW ni llamar eficiencia sin fundamento.

**Presiones y emisiones:** no asumir presión absoluta/manométrica ni condiciones normalizadas de volumen, oxígeno o humedad para las concentraciones si no están acreditadas. Las columnas no bastan para certificar cumplimiento regulatorio.

**Tiempo:** los archivos están ordenados cronológicamente según UCI, pero no incluyen timestamp por fila. `anio` identifica el archivo; no inventar un calendario continuo ni asumir que no hay huecos.

## Qué se podría investigar después

Como ruta candidata: estimar NOX con AT, AP y AH y comparar con un modelo que incorpore las seis variables operativas. Excluir CO y NOX de las entradas en esa formulación. Estimar la misma hora no es pronosticar una hora futura, y asociación no demuestra causalidad.

La separación de referencia del artículo es entrenamiento 2011–2012, validación 2013 y prueba 2014–2015. Aquí sólo se construye `df`, conservando el año para poder respetar esa separación después.
