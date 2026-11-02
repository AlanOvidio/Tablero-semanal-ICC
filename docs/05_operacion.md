# Operación y mantenimiento

## Requisitos

- Power BI Desktop (versión de octubre 2026 o posterior) con formato PBIP/TMDL habilitado.
- Licencia Power BI **Pro** para publicar.
- Acceso de red a `https://redmet.icc.org.gt`.
- Python 3.8+ (solo para regenerar la documentación automática).

## Parámetros de Power Query

| Parámetro | Valor recomendado | Notas |
|---|---|---|
| `RangeStart` | `28-oct-2024 00:00` | Inicio del año hidrológico 2025: carga dos años hidrológicos completos en Desktop, suficiente para probar comparaciones con el año anterior. |
| `RangeEnd` | **00:00 del día siguiente** al último día del boletín | Es **exclusivo**. Con una hora distinta de 00:00 las tablas diaria y subdiaria cortan en días distintos (ver *Solución de problemas*). |
| `InicioAnioHidrologico` | `2-nov` | Solo se usan mes y día. |

En el **servicio** estos parámetros no se usan: cada tabla con actualización incremental fija su propio rango.

## Actualizar en Desktop (boletín semanal)

1. Cerrar Power BI en cualquier otro equipo y esperar a que OneDrive termine de sincronizar.
2. Abrir el `.pbip`.
3. Power Query → Administrar parámetros → `RangeEnd` = lunes 00:00 posterior a la semana del boletín.
4. **Inicio → Actualizar** (actualiza también `Calendario`, `Semanas_Grafica` y `Periodos_Dia`).
5. Revisar en la página *Validaciones1* que el número de estaciones con datos sea el esperado.

## Publicar y actualizar en el servicio

| Tabla | Ventana | Refresca |
|---|---|---|
| `Fact_Diaria_met`, `Fact_Meteorologia` | 18 años | últimos 7 días |
| `Fact_Subdiaria_met_aux`, `Fact_Horaria_riesgo` | 5 años | últimos 7 días |

- **Primera publicación o cambio de política/columnas:** el servicio hace una carga completa. Las tablas de 15 min con muchos años pueden tardar; si se excede el límite de 2 h de Pro o la API responde con *timeout*, reintentar o publicar primero con menos años y ampliar después.
- **Actualizaciones programadas:** solo se descargan los últimos 7 días de cada tabla.
- Las funciones de la API tienen un *timeout* de 5 min por estación. La API es sensible a consultas grandes; por eso se consulta estación por estación.

## Tareas frecuentes

### Agregar o quitar una estación
Editar la lista en la consulta `TablaEstaciones_met` (Power Query). Tras publicar, hacer una actualización completa para que se descargue su historia.

### Cambiar un umbral de semáforo o de riesgo
Editar la medida `Semaforo_*` o `Dias_Riesgo_*` en `_Medidas`. Actualizar la tabla de umbrales en [04 · Guía de usuario](04_guia_usuario.md) y registrar el cambio en [06](06_decisiones_y_cambios.md).

### Cambiar el umbral de calma del viento
Medida `_Viento_Umbral_Calma` (km/h).

### Regenerar la documentación automática
```
python tools/generar_docs_modelo.py
```
Actualiza `02_diccionario_datos.md`, `03_catalogo_medidas.md` y `09_inventario_visuales.md`.

## Solución de problemas

| Síntoma | Causa | Solución |
|---|---|---|
| Error al abrir: *TMDL objects cannot be merged… `expressions-NOMBREEQUIPO`* | Copias de conflicto de OneDrive (se guardó desde dos equipos o sin terminar de sincronizar). | Comparar cada archivo `*-NOMBREEQUIPO.*` con el original, conservar la versión correcta y mover/eliminar la copia. Con Git este problema desaparece (ver [07](07_repositorio_git.md)). |
| Error al abrir: *TMDL Format Error… Unsupported property* | Sintaxis TMDL inválida tras una edición manual. | Ir a la línea indicada. Ej.: las descripciones se escriben como `/// texto` encima del objeto, no como `description:`. |
| El segmentador de semana no llega a la semana actual | `Calendario` no se ha actualizado (genera fechas hasta el día de la actualización). | Actualizar `Calendario` y `Semanas_Grafica`. |
| El último día muestra datos de 15 min (VPD, índice de calor) pero no diarios (temperatura, HR, lluvia diaria) | `RangeEnd` no está a las 00:00: la tabla diaria filtra por fecha y la subdiaria por fecha y hora. | Poner `RangeEnd` a las 00:00 del día siguiente. |
| Faltan datos recientes de todas las tablas | `RangeEnd` desactualizado (solo afecta a Desktop). | Actualizar `RangeEnd`. |
| La lluvia máxima de 15 min supera la diaria con varias estaciones | (Corregido el 2026-10-29.) | — |
| Un visual muestra error de campo | Una medida o columna fue renombrada o eliminada. | Revisar [09 · Inventario de visuales](09_inventario_visuales.md) y reasignar el campo. |
| Valores de radiación o duración de luz anómalos en una estación | Sensor con valores nocturnos > 40 W/m² o huecos al amanecer/atardecer. | Revisar `N_Lecturas_Promedio`, `Dia_Completo_Pct`, `Hora_Inicio_Luz` y `Hora_Fin_Luz` de la estación. |

## Calidad de datos

- `Fact_Subdiaria_met_aux[N_Lecturas]` y `[Dia_Completo]` (≥ 80 de 96 lecturas) permiten evaluar la completitud por estación y día.
- Medidas: `N_Lecturas_Promedio`, `Dia_Completo_Pct`.
- La ETo y la radiación faltantes quedan **vacías**, no en cero: no sesgan los promedios.
- Los acumulados de `Fact_Diaria_met` (lluvia, ETo, radiación) no pueden detectar días con lecturas parciales, porque la API diaria entrega sumas sin el número de lecturas.
