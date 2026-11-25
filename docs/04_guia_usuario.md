# Guía de usuario del tablero agroclimático

Esta guía explica cómo leer el tablero semanal. Está pensada para agrónomos y técnicos de campo. Las condiciones, umbrales y fuentes de cada riesgo están en el [catálogo de riesgos](10_catalogo_riesgos.md).

## Encabezado de cada página

| Elemento | Qué hace |
|---|---|
| **Indicador de semana** | Estaciones o estrato seleccionados y fechas de la semana; si la semana va incompleta, cuántos días tienen datos. En *Riesgos del cultivo* incluye el cultivo. |
| **Datos al…** | Último día (o día y hora, en la página horaria) con datos en el modelo. |
| **Año hidrológico** | Inicia el lunes de la semana que contiene el 2 de noviembre. «Año hidrológico actual» avanza solo; los años anteriores se muestran como «2025-2026». |
| **Semana** | Semana hidrológica de lunes a domingo, p. ej. `02 \| 2026-2027 (09-nov - 15-nov)`. Por defecto **«Última semana completa»**; **«Semana en curso»** muestra la semana actual mientras avanza. |
| **Estrato altitudinal** | Botones; sin selección se muestran todos los estratos. |
| **Estación** | Lista desplegable; cada página tiene su propia selección. |

Año, semana y estrato se mantienen al cambiar de página; la estación no.

**Con varias estaciones seleccionadas:**
- Las **cantidades** (lluvia, ETo, balance, horas de mojadura, luz o estrés, grados día, radiación) muestran el **promedio por estación**. Ej.: 3 estaciones con 20, 30 y 40 mm → **30 mm**, no 90.
- Los **días de riesgo** son el promedio de días por estación (puede verse 2.3 días).
- Los **máximos y mínimos** (temperatura máxima, viento máximo, DPV máximo…) muestran **el valor más extremo** entre las estaciones.

## 1 · Agua y energía de la semana

| Visual | Qué muestra | Cómo interpretarlo |
|---|---|---|
| Mapa de estaciones | Color = balance hídrico de la semana (café = déficit, verde azulado = excedente); tamaño = lluvia | Localiza las fincas con déficit. |
| Tarjetas de lluvia, ETo y balance | Totales de la semana | Balance negativo = la planta consume más agua de la que llueve. |
| Resumen de la semana | Lluvia, ETo, balance, temperaturas, radiación, horas de luz y grados día: esta semana, semana anterior y hace un año | Si la semana va incompleta, las comparaciones usan los mismos días. |
| Balance hídrico diario | Lluvia, ETo y lluvia máxima en 15 min por día | Un máximo de 15 min cercano al total diario indica aguaceros intensos y escorrentía. |
| Balances anteriores | Balance de las 3 semanas previas (cruza el cambio de año) | Tendencia de déficits acumulados. |
| Estaciones en déficit / listado | Estaciones con balance < −20 mm | Priorizar riego en esas fincas. |
| Temperaturas | Máxima, media, mínima e índice de calor | El índice de calor combina temperatura y humedad. |
| Radiación y grados día | **Desviación acumulada** frente a la media de los mismos días de años anteriores, para el año actual y el anterior; la línea dorada es la media (0). Ventana: 4, 8 o 12 semanas o desde el inicio del año | Sobre 0: más radiación o calor que lo normal. El título y la información al pasar el cursor dan el acumulado con la desviación entre paréntesis. Grados día con base 10 °C y tope 30 °C. |

## 2 · Estrés atmosférico y vegetal

Cada gráfica tiene a su derecha botones **Día (06–18 h) / Noche (19–05 h) / Ambos** y una lista para quitar series. Las variables solo diurnas (irradiancia, horas de luz, estrés térmico) desaparecen con «Noche»; la HR mínima y media (24 h) se ven siempre.

| Visual | Qué muestra | Cómo interpretarlo |
|---|---|---|
| Mapa | Color = DPV máximo diurno (día más seco de la semana); tamaño = horas de estrés térmico | Dónde hubo días más secos y calurosos. |
| Dispersión por estación | DPV máximo diurno (X) frente a temperatura media nocturna (Y); tamaño = mojadura nocturna; color = estrato | Arriba a la derecha: días secos y noches cálidas (más estrés, menos recuperación). |
| Estrés atmosférico | DPV diurno y nocturno; eje secundario a elegir: HR o temperatura nocturna | DPV > 1.6 kPa: cierre de estomas y estrés hídrico; < 0.4 kPa: aire muy húmedo, riesgo de enfermedades. Un DPV nocturno < 0.3 kPa indica que la planta se rehidrata de noche. Noches > 24 °C aumentan la respiración. |
| Estrés vegetal | Horas de mojadura diurna y nocturna, horas de luz, horas de estrés térmico; irradiancia máxima y media de luz | Mojadura nocturna > 6 h con T 18–28 °C favorece enfermedades foliares. Estrés térmico = horas con T > 35 °C y radiación > 800 W/m². |
| Viento | Velocidad media y máxima, diurna y nocturna (km/h) | > 10 km/h de día: deriva de aplicaciones; noches en calma favorecen mojadura e inversión térmica. |

Las líneas punteadas horizontales marcan esos umbrales.

## 3 · Comportamiento horario

| Visual | Qué muestra | Cómo interpretarlo |
|---|---|---|
| Mapa de calor | Variable elegida (temperatura del aire, humedad relativa, DPV, sensación térmica, mojadura de la hoja, lluvia, velocidad del viento, irradiancia) por hora y día, promedio de las estaciones | Colores por rangos fijos (ver leyenda). En mojadura, el color indica el % de registros horarios con la hoja mojada: *Seca*, *Mojadura parcial* (< 50 %) o *Mojadura predominante* (≥ 50 %). En el mapa de calor cada casilla reúne las estaciones seleccionadas en esa hora (con una sola estación es seca o predominante); en el mapa geográfico, las horas de cada estación. |
| Mapa de estaciones | Promedio de la semana de la misma variable en cada estación | Diferencias entre fincas. |
| Rosa de vientos | Frecuencia del viento por dirección en el periodo del día elegido | El pétalo más largo es de dónde **viene** el viento con más frecuencia; el color indica su velocidad media. Las calmas (< 1.8 km/h) se informan aparte. |

## 4 · Riesgos del cultivo

Elegir el cultivo con los botones. Los umbrales son **valores de referencia** de la literatura, sujetos a validación con datos de campo (columna *Validado* del catálogo).

| Visual | Qué muestra | Cómo interpretarlo |
|---|---|---|
| Riesgos en alerta / precaución | Número de riesgos del cultivo en cada nivel | Resumen rápido de la semana. |
| Contexto productivo | Balance, temperatura nocturna, grados día acumulados, horas de luz, mojadura total y nocturna (h/semana) | Condiciones generales del cultivo. |
| Semáforo de riesgos | Valor de la semana de cada riesgo con su umbral de precaución y de alerta, condición evaluada, aplicación y confianza | 🟢 normal · 🟡 precaución · 🔴 alerta · gris sin datos. Clic en un riesgo para verlo en el mapa horario y en el mapa de estaciones. |
| Mapa de calor de riesgos | % de horas-estación favorables al riesgo o a la categoría elegidos; sin selección, todos los riesgos horarios del cultivo | Horas del día en que se concentran las condiciones favorables. |
| Mapa de estaciones | Número de riesgos en alerta (azules); con un riesgo elegido en el semáforo, su semáforo | Dónde se concentran las alertas. |
| Matriz por estrato y estación | Valor de cada riesgo por estación, coloreado con el semáforo | Expandir el estrato para ver las estaciones. |

## Preguntas frecuentes

**¿Por qué la semana en curso aparece vacía o incompleta?** Los datos se actualizan después del control de calidad; por eso la semana por defecto es la última completa.

**¿Por qué la lluvia del mapa no coincide con la tarjeta?** El mapa muestra cada estación; la tarjeta, el promedio de las estaciones seleccionadas.

**¿Por qué lluvia − ETo no da exactamente el balance?** Algunas estaciones no miden ETo todos los días; el balance solo usa días con ambos datos.

**¿Por qué faltan algunos valores?** Las lecturas fuera de rango (p. ej. T < −5 °C o > 50 °C, HR < 20 %, radiación > 1500 W/m²) se descartan como faltantes; ver [Arquitectura](01_arquitectura.md#control-de-calidad).
