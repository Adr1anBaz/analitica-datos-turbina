# Publicar avance exploratorio y dataset

**Objetivo:** documentar el avance real y publicar el notebook actualizado junto con los cinco CSV originales completos en el repositorio privado.

**Alcance:** solicitud del usuario de actualizar README, publicar el trabajo reciente y alojar todo el dataset en GitHub. Esta solicitud sustituye la exclusión anterior de los originales del control de versiones.

## Tareas

- [ ] Revisar íntegramente el notebook modificado localmente; conservar el trabajo del usuario e identificar qué partes de la conversación faltan.
- [ ] Incorporar únicamente la exploración ya realizada y sus explicaciones claras: faltantes, tipos, boxplots, histogramas, comparación anual, correlación y dispersión AT/NOX. Mantener el estilo de los ejemplos del profesor.
- [ ] Actualizar README con la pregunta del proyecto, el papel de los años y una lista de avances y pendientes. No afirmar que existen modelos, escalado o evaluación final.
- [ ] Ajustar `.gitignore` para versionar sólo los cinco CSV originales de `data/raw/`; conservar exclusiones de entorno, secretos, cachés y datos derivados. Actualizar documentación contradictoria sobre la distribución de datos e incluir atribución y licencia publicada por UCI.
- [ ] Verificar hashes de los cinco CSV, ejecutar pruebas y notebook, revisar diff y confirmar que no se incluye contenido ajeno al proyecto.
- [ ] Crear commit y publicar en `main`; verificar sincronización remota y presencia de los cinco originales completos.

## Comprobaciones

Los originales deben sumar 36,733 filas y conservar once columnas. El DataFrame unido debe tener doce columnas incluyendo `anio`. La exploración debe usar exclusivamente 2011–2012. No entrenar modelos ni añadir análisis nuevos en esta entrega.

## Ejecución

Plan aprobado por el usuario. Implementación directa en esta sesión, sin delegación. La comprobación final debe confirmar nueve pruebas, seis figuras regeneradas, cinco CSV completos con hashes originales y sincronización de `main` con GitHub.
