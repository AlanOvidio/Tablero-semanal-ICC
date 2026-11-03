# Decisiones de diseño y bitácora de cambios

Registrar aquí cada cambio relevante al modelo o al reporte: **qué** cambió, **por qué**, y su efecto en los números.

## Decisiones vigentes

| # | Decisión | Motivo | Fecha |
|---|---|---|---|
| D1 | `Fact_Diaria_met` se carga del endpoint diario (`getlecturasdia`), no agregando los datos de 15 min. | El endpoint ya trae ETo, temperatura, HR, viento y radiación; es mucho más liviano para 18 años. | 2026-09 |
| D2 | Ventanas de actualización incremental: diaria 18 años; subdiaria y horaria 5 años; últimos 7 días en cada refresco. | Climatología desde 2008 con la tabla liviana; las de 15 min solo para el boletín y comparación interanual, dentro del límite de 2 h de Pro. | 2026-10-28 |
| D3 | `Fact_Horaria_riesgo` consulta la API directamente (no referencia a `Fact_Meteorologia`). | Una consulta que referencia otra la vuelve a ejecutar completa y no hereda su actualización incremental. | 2026-10-28 |
| D4 | `Fact_Meteorologia` se conserva cargada aunque no se use. | Decisión del proyecto (disponibilidad del dato crudo). | 2026-10-29 |
| D5 | Sumas: por estación y luego promedio entre estaciones. Máximos/mínimos: extremo de las estaciones. | Un estrato con 10 estaciones no debe mostrar 10 veces la lluvia; los extremos sirven como alerta del peor caso. | 2026-10-28 / 29 |
| D6 | Días de riesgo: promedio de días por estación, evaluando todas las condiciones dentro de la misma estación. | Antes se mezclaba la mojadura de una estación con la temperatura y la HR de otra. | 2026-10-28 |
| D7 | ETo faltante = vacía (no 0). Balance diario vacío si falta la ETo. | Rellenar con 0 inflaba el balance (balance = lluvia). | 2026-10-28 |
| D8 | Históricos: misma semana hidrológica en años **anteriores al seleccionado**, con `ALL(Calendario)`. | `ALLEXCEPT` perdía el filtro de semana cuando el visual usaba `Semana_Etiqueta`; comparar contra el año en curso incluía el propio año seleccionado. | 2026-10-28 |
| D9 | Sin fecha/hora automática; `Calendario` marcado como tabla de fechas con `Jerarquía hidrológica`. | Una sola fuente de fechas, jerarquía alineada al calendario del boletín, menos tablas ocultas. | 2026-10-28 |
| D10 | Ventana diurna/nocturna fija (06–18 / 19–05) para temperatura, VPD, viento, mojadura y ETo. | Decisión del proyecto: consistencia entre estaciones y semanas. | 2026-10-28 |
| D11 | Para la radiación, la **luz define el periodo diurno**: primera a última lectura > 40 W/m²; media sobre lecturas disponibles; energía = media × duración. | Robusto a lecturas faltantes (nocturnas no afectan; diurnas se promedian), sin suponer horas fijas. | 2026-11-01 |
| D12 | `Horas_Luz` (antes `Brillo_Solar_Horas`) es la duración del periodo con luz (umbral 40 W/m²), **no** heliofanía OMM (120 W/m²). | El umbral de 40 define el día con luz. | 2026-10-28 / 11-01 |
| D13 | `Rad_MJ` = Σ W/m² (dato API) × 900 s / 10⁶. | El endpoint entrega la suma de lecturas de 15 min (96 por día), no MJ. Antes se usaba /97. | 2026-10-29 |
| D14 | Direcciones de viento: promedio vectorial; rosa de vientos con 8 sectores, calma < 1.8 km/h, frecuencias sobre horas-estación. | El promedio aritmético de grados es incorrecto (350° y 10° → 180°). | 2026-10-28 |
| D15 | La rosa de vientos se dibuja como imagen SVG generada por una medida (`Rosa_Vientos_SVG`) en una tabla nativa. | No requiere visuales personalizados; funciona en el servicio, en móvil y al exportar. | 2026-10-28 |

## Bitácora de cambios

### 2026-11-03 · Mapa de calor por categoría
- `Riesgos_Cultivo` agrega `Categoria` (Enfermedades, Plagas, Clima (abióticos), Manejo y producción), derivada de `tipo`.
- El segmentador del mapa de calor es jerárquico (categoría → riesgo) y admite varias selecciones. Con un riesgo, el mapa muestra el % de horas-estación favorables; con una categoría o varios riesgos, el % de horas-estación con al menos uno favorable; sin selección, todos los riesgos horarios del cultivo excepto los indicadores favorables (ventana de aplicación).
- Tooltip `Riesgo_Hora_N`: número promedio de riesgos favorables por hora-estación. El título (`Riesgo_Hora_Titulo`) indica qué se muestra.
- Un clic en una fila del semáforo también filtra el mapa de calor a ese riesgo (si tiene condición horaria).
- Condiciones horarias (mapa de calor y riesgos por hora): una hora sin dato en alguna variable usada ya no cuenta como favorable.

### 2026-11-03 · Fase 2: Resumen Semanal multicultivo
- Segunda fila de segmentadores: **Cultivo** (selección única, Caña de azúcar por defecto) y **Estación** (desplegable, varias); tarjeta con título dinámico (`Titulo_Contexto`). El contenido existente bajó 80 px.
- Bloque *Riesgos del cultivo* al final: conteo de riesgos en alerta/precaución, contexto productivo con `GDD_Cultivo_Acumulado`, matriz semáforo (riesgo, situación, umbrales, condición, aplicación, confianza) y matriz estrato/estación × riesgo coloreada con `Riesgo_Color`.
- Mapa de calor horario con `Riesgo_Hora`; su segmentador usa `Riesgos_Cultivo[Riesgo]` (solo riesgos con condición horaria) y solo filtra el mapa. Si no hay riesgo elegido válido para el cultivo, se muestra el primero con condición horaria; el título (`Riesgo_Hora_Titulo`) indica cuál.
- Gráfica de suma térmica con `GDD_Cultivo_Grafica` / `GDD_Cultivo_Anterior_Grafica` (base y tope del cultivo elegido).
- Reporte: filtrado cruzado por defecto en lugar de resaltado.
- Ajustes tras la primera prueba: el mapa de calor muestra 0 % (todas las horas con datos); `_Riesgo_En_Cultivo` garantiza que el semáforo, la matriz por estación y los conteos solo muestren riesgos del cultivo elegido; la rosa de vientos indica «Calma» cuando no hay viento ≥ 1.8 km/h.
- Barrenador (caña) y pudrición del cogollo (palma) con versión horaria aproximada para el mapa de calor; coludo evaluado de noviembre a abril (fin de lluvias y transición).
- La página *Resumen Semanal* deja de estar marcada como tooltip (estaba activada por error).
- Descartado el relleno de días faltantes en acumulados: el tablero se actualiza después del control de calidad de datos.
- Retirados: página *Resumen Semanal – Caña Azúcar*, tabla `Plagas` y medida `Condicion_Plaga_Hora` (copias en `_respaldo/fase2_2026-11-03/`). Las medidas `Dias_Riesgo_*` se conservan porque las usa *Validaciones 4*.

### 2026-11-03 · Fase 1b: motor de riesgos multicultivo
- Nuevo generador `tools/generar_riesgos_modelo.py`: crea desde `config/riesgos_cultivo.csv` las tablas `Cultivos` (5 cultivos con base y tope de grados día) y `Riesgos_Cultivo` (42 riesgos a incluir con umbrales, unidad, aplicación, fuente y validación), y la tabla de medidas `_Riesgos`.
- `_Riesgos`: una medida por riesgo (`R_<ID>`) y medidas genéricas para los visuales: `Riesgo_Valor`, `Riesgo_Semaforo` (umbrales desde la tabla; admite indicadores favorables invertidos), `Riesgo_Color`, `Riesgo_Etiqueta`, `Riesgos_En_Alerta`, `Riesgos_En_Precaucion`, `Riesgo_Hora` (mapa de calor horario), `GDD_Cultivo*` (grados día del cultivo seleccionado), `Cogollero_Generaciones`, `Salivosa_Lluvia_Temporada` y `Salivosa_Alerta_Emergencia`.
- Reglas: días favorables por estación promediados entre estaciones con datos; filtros automáticos por meses y altitud según el CSV; los riesgos horarios cuentan horas en `Fact_Horaria_riesgo`.
- `Fact_Horaria_riesgo`: nueva columna `Rad_Media` (radiación horaria) para estrés térmico y ventana de aplicación.
- Relación `Riesgos_Cultivo[Cultivo]` → `Cultivos[Cultivo]`. Las medidas anteriores de riesgo (`Dias_Riesgo_*`, `Semaforo_*`) se mantienen hasta que la Fase 2 cambie los visuales.

### 2026-11-02
- Documentación inicial (`README.md`, `docs/`), generador `tools/generar_docs_modelo.py` y `.gitignore` para el repositorio.
- Se quitaron de la documentación las referencias a organizaciones externas y a la experiencia institucional como fuente de umbrales.

### 2026-11-01
- Radiación basada en el periodo de luz (D11): nuevas columnas en `Fact_Subdiaria_met_aux` (`Hora_Inicio_Luz`, `Hora_Fin_Luz`, `Duracion_Luz_h`, `Rad_Media_Luz`, `Energia_Luz_MJ`) y sus medidas. Se eliminó `Rad_Media_Diurna_MJ`.
- `Horas_Luz` pasa a sumar `Duracion_Luz_h`. El gráfico de estrés vegetal usa `Rad_Media_Luz` como irradiancia media.
- Etiquetas de `Periodos_Dia` con rango horario (p. ej., "Mañana (06:00-11:59)").

### 2026-10-29
- `Precip_Max_Evento`: máximo de 15 min por estación, promediado (antes: máximo de todas las estaciones, podía superar la lluvia diaria promedio).
- `Balance_Semanal` y `Balance_Por_Semana`: Σ (P − ETo) por estación y promedio, consistente con `Balance_Diario`.
- `Rad_MJ` con 96 lecturas (D13). `Rad_Media_Diurna_MJ` integrada (luego reemplazada el 11-01).
- Se eliminaron copias de conflicto de OneDrive (`*-NOMBREEQUIPO.*`) que impedían abrir el proyecto.

### 2026-10-28
- Rosa de vientos: viento horario vectorial en `Fact_Horaria_riesgo` (`Viento_Media`, `Dir_Viento`, `Sector_Viento`), relación con `Direcciones_Viento`, medidas de frecuencia/calmas y visual SVG con segmentador de período.
- `Fact_Horaria_riesgo` directo de la API con actualización incremental (D3). `Fact_Subdiaria_met_aux` a 5 años (D2).
- Agregación multiestación (D5, D6) en 43 medidas de suma y 10 de días de riesgo.
- Históricos corregidos (D8). Medida `_Conteo_Estaciones_Hidro` (inexistente) retirada de su tarjeta.
- Calendario (D9): sin tablas automáticas, tabla de fechas marcada, jerarquía hidrológica en 7 gráficos diarios, etiquetas ordenadas cronológicamente, formato de fecha `dd-mmm`.
- Calidad de datos en M: ETo vacía (D7), banderas a prueba de nulos, dirección predominante vectorial.
- Limpieza: medidas duplicadas eliminadas (GDD sin tope, `_Año_Hidro_Actual`, `Rad_Media`, `_Test_*`). `Brillo_Solar_Horas` → `Horas_Luz`.

## Pendientes / ideas

- Validar los umbrales de riesgo con datos de campo.
- `Rad_Media_Diurna` (ventana fija) ya no se usa en visuales: evaluar su eliminación.
- Página *Pronóstico Semanal* sin contenido.
