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

### 2026-11-25 · Ajustes tras la primera publicación
- `Leyenda_Mapa_Riesgo`: la segunda etiqueta "Sin datos" se distinguía con un espacio final, que el servicio ignora al comparar textos; la actualización fallaba al ordenar `Rango` por `Orden`. Ahora usa un espacio de ancho cero.
- Mojadura de la hoja (mapa de calor y mapa geográfico): leyenda válida para una o varias estaciones: *Seca*, *Mojadura parcial (< 50 %)*, *Mojadura predominante (≥ 50 %)*; unidad "% de registros horarios con la hoja mojada".

### 2026-11-24 · Estaciones de El Salvador e informes por país
- `TablaEstaciones_met`: se agregan las 9 estaciones de El Salvador (38 Central Izalco, 39 COPAL, 40 Chaparrastique, 45 Agua Santa, 46 El Carmen, 47 San Clemente, 78 Miravalle, 79 El Cipitillo, 80 San Ildefonso).
- Un modelo semántico y tres informes: `Tablero-semanal-ICC` (trabajo, sin filtro de país), `Tablero-semanal-ICC-GT` y `Tablero-semanal-ICC-SV` (generados con `tools/generar_informes_pais.py`, filtro de país a nivel de informe, solo las cuatro páginas públicas, mapas con ajuste automático). Ver [05 · Operación](05_operacion.md).
- `Titulo_Semana`: antepone el país cuando hay uno solo, y "Todas las estaciones" se evalúa sobre las columnas de los segmentadores (estrato, finca, estación), no sobre toda la tabla, para que el filtro de país no lo cambie.

### 2026-11-24 · Nombre del proyecto
- El proyecto pasa de `2026_dashboard_exp1` a **`Tablero-semanal-ICC`** (`.pbip`, `.Report` y `.SemanticModel`). En el servicio se renombran el reporte y el modelo semántico al mismo nombre antes de publicar, para conservar el enlace de *Publicar en la web* y la programación.

### 2026-11-20 · Fase 2b: reorganización en cuatro páginas
- El *Resumen Semanal* se redistribuye en: **Agua y energía de la semana**, **Estrés diurno y recuperación nocturna**, **Comportamiento horario** y **Riesgos del cultivo**. Ancho 1300 px con desplazamiento vertical y los visuales con su tamaño, colores y reglas originales (una primera versión de 1280 × 720 quedó demasiado pequeña; copia en `_respaldo/fase2b_v1/`). La página original queda en `_respaldo/fase2b_2026-11-20/`.
- Encabezado común: título con enlace a la documentación, indicador de semana (`Titulo_Semana`; `Titulo_Contexto` con el cultivo en la página 4), tarjeta «Datos al…» (`Datos_Al_Diaria` / `Datos_Al_Horaria`), logo, y segmentadores Año y Semana con selección automática (`Calendario[Año_Selector]`, `Calendario[Semana_Selector]`: «Año hidrológico actual», «Semana en curso»), Estrato y Estación sincronizados entre páginas; Cultivo solo en la página 4.
- `Estaciones_met` solo incluye las estaciones de `TablaEstaciones_met`.
- `Balance_Por_Semana` cuenta las 3 semanas previas por fecha de inicio (cruza el cambio de año hidrológico); eje `Semanas_Grafica[Semana_Corta]`.
- Página 1: el mapa de estaciones se colorea por balance hídrico (`Mapa_Balance_Color`, café → verde azulado, para no confundirse con el semáforo); tabla *Resumen de la semana* (esta semana / semana anterior / hace un año, con los mismos días si la semana va incompleta); radiación y grados día **semana a semana** (últimas 12 semanas vs. año anterior) con el acumulado del año en el título.
- Página 2: gráfica día / noche con botones de variable y de periodo (Día | Noche | Ambos) y lista de series para quitar líneas (`Series_DiaNoche`, `Periodo_Vista`, `DiaNoche_Valor`, nota de lectura `DiaNoche_Nota`); debajo, las cuatro gráficas de estrés originales.
- Páginas 3 y 4: mapa de calor con tabla de leyenda (`Leyenda_Mapa_Calor`, `Leyenda_Mostrar`); en la 3 solo variables meteorológicas, en la 4 solo riesgos con la paleta original.
- Ajustes tras la revisión (2026-11-20): segmentadores de estrato como en la versión de una página (sin selección = todos); ejes semanales solo con el número de semana (`Semana_Eje`); radiación y grados día como **desviación acumulada** frente a la media histórica de cada semana en las últimas 8 semanas (año actual, año anterior y línea de la media; `Rad_Desv_Acum`, `GDD_Desv_Acum`, `Desv_Media_Linea`).
- Página 2: botones Día | Noche | Ambos y lista de series aplicados a las gráficas día/noche (temperatura, estrés atmosférico, humedad relativa, estrés vegetal, irradiancia, viento, ETo; las variables solo diurnas no aparecen con «Noche»), con la nota de lectura en el subtítulo de cada gráfica; mapa por DPV máximo diurno (tamaño = horas de estrés térmico) y dispersión DPV diurno vs. T nocturna por estación.
- Página 3: nombres de variables corregidos (temperatura del aire, velocidad del viento, mojadura de la hoja, irradiancia, sensación térmica (índice de calor)), leyenda con unidades y mapa de estaciones con el promedio semanal de la variable elegida.
- Página 4: cultivo con botones y mapa de estaciones con el peor semáforo de los riesgos del cultivo (`Mapa_Riesgo_Color`).
- 2026-11-23: el segmentador de estación ya no se sincroniza entre páginas (año, semana y estrato sí).
- 2026-11-23: radiación y grados día vuelven a la **desviación acumulada** (año actual, año anterior y media en 0), ahora comparando **los mismos días** de años anteriores (`DATEADD`, hasta 18 años) en lugar del número de semana, para que la semana 53 tenga referencia; los acumulados de 8 semanas (actual, media y año anterior) van en el título y en la información sobre herramientas (`Rad_Acum8*`, `GDD_Acum8*`, `*_Titulo_Desv`).
- 2026-11-23: etiquetas de semana y de año con el año hidrológico como «2026-2027»; la opción del año en curso sigue siendo «Año hidrológico actual».
- 2026-11-23: la página 2 se llama **Estrés atmosférico y vegetal** y vuelve a las gráficas originales: estrés atmosférico fusionado con «VPD y temperatura nocturna» (eje secundario a elegir: humedad relativa o temperatura nocturna, tabla `Eje_Secundario`), estrés vegetal y viento; cada una con botones Día / Noche / Ambos y lista de series propias (medidas `DN_*`, tabla `Series_DiaNoche[Grafica]`).
- 2026-11-23: la semana elegida por defecto es la **«Última semana completa»** (la semana en curso suele no tener datos todavía); «Año hidrológico actual» es el año de esa semana.
- 2026-11-23: mapas con el nombre de la estación como etiqueta y coordenadas y valores a dos decimales; leyenda del mapa de calor con una denominación para cada rango de DPV y una explicación de la mojadura (% de estaciones con la hoja mojada en esa hora).
- 2026-11-24: **control de calidad** en Power Query con los rangos de `aplicar_qc` (scripts R): en las tablas de 15 min, fuera de rango = faltante (lluvia < 0 o > 90 mm; T < −5 o > 50 °C; HR < 20 o > 100 %; radiación < 0 o > 1500 W/m²; viento < 0 o > 270 km/h; mojadura < 0 o > 10; ETo < 0 o > 90; dirección 360 → 0 y fuera de 0–360 faltante). En `Fact_Diaria_met`, temperaturas y HR con los mismos límites y negativos de lluvia, ETo y radiación como faltantes.
- 2026-11-24: radiación y grados día con selector de ventana (`Ventana_Semanas`: 4, 8, 12 semanas o desde el inicio del año hidrológico); título e información sobre herramientas con el acumulado y la desviación entre paréntesis.
- 2026-11-24: página 2 con líneas de referencia (DPV 0.4 y 1.6 kPa, mojadura 6 h, viento 10 km/h); dispersión coloreada por estrato con referencias en DPV 1.6 kPa y T nocturna 24 °C.
- 2026-11-24: página 4: contexto productivo con mojadura total y nocturna (h/semana); mapa de riesgos por número de riesgos en alerta en escala de morados (`Mapa_Riesgo_Color`); con un riesgo elegido en el semáforo muestra su semáforo.
- 2026-11-24: mapa de riesgos en **azules** (contrastan con el mapa base gris y no se confunden con el semáforo); leyenda y título dinámicos (`Leyenda_Mapa_Riesgo`, `Leyenda_Riesgo_Mostrar`, `Leyenda_Riesgo_Titulo`): número de alertas sin riesgo elegido, semáforo con un riesgo elegido.
- 2026-11-24: `Fact_Diaria_met`: los grados día quedan vacíos (no error) cuando el control de calidad deja vacía la temperatura.
- 2026-11-24: **`Fact_Meteorologia` deja de cargarse** al modelo (no la usaba ningún visual y era la tabla más pesada; Desktop se cerraba al aplicar cambios). La consulta queda en Power Query como expresión sin carga; copia de la tabla en `_respaldo/fact_meteorologia_2026-11-24/`.

### 2026-11-03 · Preparación para el servicio
- `Calendario`: la fecha final usa la hora de Guatemala (UTC−6) en lugar de la hora local de la máquina; en el servicio la hora es UTC.
- Publicación: desde Desktop con el proyecto de este repositorio, reemplazando el modelo semántico `2026_dashboard_exp1` del área de trabajo. La carpeta de OneDrive queda solo como archivo.

### 2026-11-03 · Mapa de calor de variables y ejes por día
- El mapa de calor tiene un selector **Ver** (tabla `Vistas_Mapa_Calor`): *Riesgos* (como antes) o una variable horaria: temperatura, humedad relativa, déficit de presión de vapor (calculado con T y HR horarias), sensación térmica, mojadura (% de horas-estación mojadas), lluvia (mm/h), viento (km/h) y radiación (W/m²).
- Colores por rangos físicos fijos por variable (`Mapa_Calor_Color`, texto blanco en fondos oscuros); la leyenda va en el título (`Mapa_Calor_Titulo`). Formato dinámico de `Mapa_Calor_Valor` según la vista.
- `Fact_Horaria_riesgo` agrega `IC_Media` (índice de calor horario de la API).
- Al final del Resumen Semanal, enlace a la documentación en GitHub (github.com/AlanOvidio/Tablero-semanal-ICC).
- Gráficas diarias con eje categórico (una etiqueta por día): sin horas en semanas cortas y con los cortes alineados de lunes a domingo.
- Revisión del calendario: las semanas van de lunes a domingo; el año hidrológico empieza el lunes de la semana que contiene el 2 de noviembre (2026: 27-oct-2025, 53 semanas; 2027: 02-nov-2026).

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
