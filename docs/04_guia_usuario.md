# Guía de usuario del tablero agroclimático

Esta guía explica cómo leer el tablero semanal. Está pensada para agrónomos y técnicos de campo.

## Cómo filtrar

| Filtro | Qué hace |
|---|---|
| **Año hidrológico** | El año agrícola-hidrológico inicia a inicios de noviembre. Ej.: el año 2026 va de fines de oct-2025 a fines de oct-2026. |
| **Semana** | Semana hidrológica (lunes a domingo). La etiqueta muestra número, año y fechas: `52 \| 2026 (19-oct - 25-oct)`. |
| **Estrato altitudinal** | Limita a las estaciones de un estrato. |
| **Mapa** | Clic en una estación para ver solo esa estación; Ctrl + clic para varias. |

**Con varias estaciones seleccionadas:**
- Las **cantidades** (lluvia, ETo, balance, horas de mojadura, horas de luz, grados día, radiación acumulada) muestran el **promedio por estación**. Ej.: 3 estaciones con 20, 30 y 40 mm → **30 mm**, no 90.
- Los **días de riesgo** son el promedio de días por estación (puede verse 2.3 días).
- Los **máximos y mínimos** (temperatura máxima, viento máximo, VPD máximo…) muestran **el valor más extremo** entre las estaciones: el peor caso del grupo.

## Semáforos

🔴 1 = alerta · 🟡 2 = precaución · 🟢 3 = normal

| Indicador | 🟡 Precaución | 🔴 Alerta | Base |
|---|---|---|---|
| Balance hídrico semanal | < 0 mm | < −20 mm | Lluvia − ETo de la semana |
| Estaciones en déficit | — | ≥ 1 estación con balance < −20 mm | |
| VPD máximo diurno | > 2.0 kPa | > 3.0 kPa | Estrés atmosférico |
| Temperatura nocturna media | > 22 °C | > 24 °C | Respiración nocturna, maduración |
| Estrés térmico (horas/semana) | > 14 h | > 28 h | Horas con T > 35 °C y radiación > 800 W/m² |
| Viento máximo diurno | > 40 km/h | > 60 km/h | Riesgo de volcamiento |
| Roya | ≥ 1 día | ≥ 3 días | ver tabla de condiciones |
| Carbón | ≥ 3 días | ≥ 5 días | |
| Salivosa | ≥ 2 días | ≥ 4 días | |
| Barrenador | ≥ 2 días | ≥ 4 días | |
| Sigatoka (banano) | ≥ 1 día | ≥ 3 días | |
| Frío en aguacate | ≥ 1 día | ≥ 3 días | Tmín < 12 °C |
| Mancha de asfalto | ≥ 2 días | ≥ 4 días | |
| Sequía en granos | ≥ 3 días secos | ≥ 5 días secos | Día seco = lluvia < 1 mm |
| Phytophthora | ≥ 1 día | ≥ 3 días y balance > 50 mm | |
| Pudrición del cogollo (palma) | lluvia > 100 mm y Tmed < 26 °C | lluvia > 150 mm y Tmed < 26 °C | |

> Los umbrales son **valores de referencia** de la literatura y la experiencia del ICC; están sujetos a validación con datos de campo.

## Condiciones de riesgo de plagas y enfermedades

**Diarias** (se cuentan los días de la semana que cumplen todas las condiciones):

| Plaga / enfermedad | Temperatura media | Humedad relativa media | Otras condiciones |
|---|---|---|---|
| Roya | 15–25 °C | > 80 % | > 6 h de mojadura diurna |
| Roya (nocturna) | 15–25 °C | > 80 % | > 8 h de mojadura total |
| Carbón | 25–30 °C | — | día seco |
| Salivosa | 22–28 °C | > 80 % | lluvia > 5 mm |
| Barrenador | > 24 °C | 60–80 % | día seco |
| Sigatoka | 25–28 °C | > 90 % | > 4 h de mojadura nocturna |
| Phytophthora | 20–30 °C | — | balance diario > 0 |
| Mancha de asfalto | 20–28 °C | > 80 % | — |

**Horarias** (mapa de calor *Condiciones meteorológicas favorables a plagas/enfermedades*): cada celda es la fracción de estaciones-hora que cumplen la condición en esa hora y día.

| Plaga | Condición horaria |
|---|---|
| Roya | T 15–25 °C, HR > 80 %, mojadura > 4 |
| Salivosa | T 22–28 °C, HR > 80 %, lluvia > 0 |
| Barrenador | T > 24 °C, HR 60–80 %, lluvia < 1 mm |
| Carbón | T 25–30 °C, lluvia < 1 mm |

## Página «Resumen Semanal»

| Sección | Qué muestra | Cómo interpretarlo |
|---|---|---|
| Mapa de estaciones | Lluvia, ETo, balance y temperatura máxima por estación | El tamaño/color identifica estaciones con déficit. Clic para filtrar. |
| Tarjetas de lluvia, ETo y balance | Totales de la semana | Balance negativo = la planta consume más agua de la que llueve. |
| Estaciones en déficit / listado | Estaciones con balance < −20 mm | Priorizar riego en esas fincas. |
| Balance hídrico diario | Lluvia diaria, ETo diaria y lluvia máxima en 15 min | Un máximo de 15 min cercano al total diario indica aguaceros intensos y escorrentía. |
| Balances anteriores | Balance de las 3 semanas previas | Tendencia: déficits acumulados. |
| Temperaturas diarias / semanales | Máx., media, mín. e índice de calor | El índice de calor combina temperatura y humedad (sensación térmica). |
| Estrés atmosférico | VPD diurno/nocturno y humedad relativa | VPD > 2 kPa: cierre estomático y menor crecimiento. |
| Estrés vegetal | Horas de mojadura, **horas de luz**, horas de estrés térmico, irradiancia media y máxima | La irradiancia media se calcula solo dentro del periodo de luz (radiación > 40 W/m²). |
| Radiación solar acumulada | Energía acumulada del año vs. año anterior (MJ/m²) | Menos radiación acumulada → menor potencial de fotosíntesis y acumulación de sacarosa. |
| VPD y temperatura nocturna | Noches cálidas y secas | Noches > 22–24 °C aumentan la respiración. |
| Suma térmica acumulada | Grados día de caña (base 10 °C, tope 34 °C) vs. año anterior | Adelanto o retraso del desarrollo del cultivo. |
| Comportamiento del viento | Velocidad media y máxima, diurna y nocturna (km/h) | Riesgo de volcamiento, deriva de aplicaciones. |
| Plagas por hora | Mapa de calor hora × día | Horas del día en que se concentran condiciones favorables. |
| Rosa de vientos | Frecuencia del viento por dirección (8 sectores) en el período del día elegido | El pétalo más largo es la dirección más frecuente (de dónde **viene** el viento); el color indica su velocidad media. Las calmas (< 1.8 km/h) se informan aparte. |

## Página «Resumen Semanal – Caña de azúcar»

Versión enfocada en caña: tarjetas de alerta de roya, carbón, salivosa, barrenador, estrés térmico y VPD; contexto productivo (balance, temperatura nocturna, grados día acumulados vs. año anterior, horas de luz, mojadura); mapa; tabla de estaciones con días de riesgo; y gráficas de VPD, balance y mojadura, radiación, viento y suma térmica.

## Preguntas frecuentes

**¿Por qué la semana actual aparece vacía?** El tablero se actualiza hasta el domingo de la última semana completa; la semana en curso no tiene datos.

**¿Por qué la lluvia del mapa no coincide con la tarjeta?** El mapa muestra cada estación; la tarjeta, el promedio de las estaciones seleccionadas.

**¿Por qué lluvia − ETo no da exactamente el balance?** Algunas estaciones no miden ETo todos los días; el balance solo usa días con ambos datos.
