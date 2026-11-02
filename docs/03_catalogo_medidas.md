# Catálogo de medidas DAX

> Generado automáticamente por `tools/generar_docs_modelo.py` el 2026-11-02 (150 medidas). No editar a mano.

Convenciones: las medidas con prefijo `_` son auxiliares; `Semaforo_*` devuelve 1 = rojo, 2 = amarillo, 3 = verde. Las medidas de suma (lluvia, ETo, balance, horas, GDD, radiación acumulada) **suman por estación y promedian entre estaciones**; los máximos y mínimos devuelven **el extremo** de las estaciones seleccionadas. Ver `04_guia_usuario.md` y `06_decisiones_y_cambios.md`.

## Índice

- [Viento](#viento) (19)
- [Radiación y luz](#radiación-y-luz) (16)
- [Semáforos](#semáforos) (16)
- [Días y condiciones de riesgo (plagas, enfermedades, clima)](#días-y-condiciones-de-riesgo-plagas-enfermedades-clima) (17)
- [Grados día / suma térmica (GDD)](#grados-día--suma-térmica-gdd) (17)
- [Históricos y comparaciones interanuales](#históricos-y-comparaciones-interanuales) (14)
- [Precipitación, ETo y balance hídrico](#precipitación-eto-y-balance-hídrico) (16)
- [Temperatura y sensación térmica](#temperatura-y-sensación-térmica) (13)
- [Humedad, VPD, mojadura y estrés](#humedad-vpd-mojadura-y-estrés) (16)
- [Auxiliares, calidad de datos y validación](#auxiliares-calidad-de-datos-y-validación) (6)

## Viento

| Medida | Formato | Descripción |
|---|---|---|
| `Viento_Media` |  | Velocidad media diaria del viento (km/h). |
| `Viento_Max` |  | Racha/velocidad máxima (km/h): extremo. |
| `Riesgo_Volcamiento` |  | Semáforo de viento máximo (> 40 amarillo, > 60 rojo, km/h). |
| `Viento_Max_Diurno` |  | Velocidad máxima diurna (km/h): extremo. |
| `Viento_Media_Diurna` |  | Velocidad media diurna (km/h). |
| `Viento_Max_Nocturno` |  | Velocidad máxima nocturna (km/h): extremo. |
| `Viento_Media_Nocturna` |  | Velocidad media nocturna (km/h). |
| `Semaforo_Viento` |  | Semáforo de viento máximo diurno: 1 rojo, 2 amarillo, 3 verde. |
| `Direccion_Viento_Max` |  | Media circular (vectorial) de la dirección: evita que 350° y 10° den 180° |
| `Direccion_Predominante_Diurna` |  | Media circular (vectorial) de la dirección: evita que 350° y 10° den 180° |
| `Frec_Dir_Periodo` | 0.0% | % de horas-estación en que el viento sopla desde el sector en contexto (usar con Direcciones_Viento[Direccion] en el eje) |
| `_Viento_Umbral_Calma` | 0.0 | Umbral de calma (km/h). 1.8 km/h ≈ 0.5 m/s (criterio OMM). Si la API entrega m/s, cambiar a 0.5 |
| `_Viento_Horas_Validas` | #,0 | Horas-estación con dato de viento válido en el período del día seleccionado. |
| `_Viento_Horas_Sector` | #,0 | Horas-estación no calmas con viento desde el sector en contexto. |
| `Pct_Calmas_Viento` | 0.0% | % de horas con viento por debajo del umbral de calma. |
| `Viento_Media_Periodo` | 0.0 | Velocidad media en el período del día seleccionado (km/h). |
| `Viento_Media_Sector` | 0.0 | Velocidad media de las horas que soplan desde el sector (km/h). |
| `Dir_Predominante` |  | Sector(es) con mayor frecuencia de viento. |
| `Rosa_Vientos_SVG` |  · URL de imagen | Rosa de vientos como imagen SVG (categoría de datos: URL de imagen). Pétalos = % de horas-estación por sector; color = velocidad media del sector. |

<details><summary><code>Viento_Media</code></summary>

```dax
AVERAGE(Fact_Diaria_met[Viento_Media])
```
</details>

<details><summary><code>Viento_Max</code></summary>

```dax
MAX(Fact_Subdiaria_met_aux[Viento_Max])
```
</details>

<details><summary><code>Riesgo_Volcamiento</code></summary>

```dax
VAR viento = [Viento_Max]
RETURN
    SWITCH(
        TRUE(),
        viento > 60, 1,
        viento > 40, 2,
        3
    )
```
</details>

<details><summary><code>Viento_Max_Diurno</code></summary>

```dax
MAX(Fact_Subdiaria_met_aux[Viento_Max_Diurno])
```
</details>

<details><summary><code>Viento_Media_Diurna</code></summary>

```dax
AVERAGE(Fact_Subdiaria_met_aux[Viento_Media_Diurna])
```
</details>

<details><summary><code>Viento_Max_Nocturno</code></summary>

```dax
MAX(Fact_Subdiaria_met_aux[Viento_Max_Nocturno])
```
</details>

<details><summary><code>Viento_Media_Nocturna</code></summary>

```dax
AVERAGE(Fact_Subdiaria_met_aux[Viento_Media_Nocturna])
```
</details>

<details><summary><code>Semaforo_Viento</code></summary>

```dax
VAR viento = [Viento_Max_Diurno]
RETURN
    SWITCH(
        TRUE(),
        viento > 60, 1,
        viento > 40, 2,
        3
    )
```
</details>

<details><summary><code>Direccion_Viento_Max</code></summary>

```dax
// Media circular (vectorial) de la dirección: evita que 350° y 10° den 180°
VAR T = FILTER(Fact_Subdiaria_met_aux, NOT ISBLANK(Fact_Subdiaria_met_aux[Direccion_Viento_Max]))
VAR sn = AVERAGEX(T, SIN(RADIANS(Fact_Subdiaria_met_aux[Direccion_Viento_Max])))
VAR cs = AVERAGEX(T, COS(RADIANS(Fact_Subdiaria_met_aux[Direccion_Viento_Max])))
VAR ang =
    SWITCH(
        TRUE(),
        ISBLANK(sn) || ISBLANK(cs), BLANK(),
        cs > 0, DEGREES(ATAN(sn / cs)),
        cs < 0, DEGREES(ATAN(sn / cs)) + 180,
        sn > 0, 90,
        sn < 0, 270,
        BLANK()
    )
RETURN
IF(NOT ISBLANK(ang), MOD(ang + 360, 360))
```
</details>

<details><summary><code>Direccion_Predominante_Diurna</code></summary>

```dax
// Media circular (vectorial) de la dirección: evita que 350° y 10° den 180°
VAR T = FILTER(Fact_Subdiaria_met_aux, NOT ISBLANK(Fact_Subdiaria_met_aux[Direccion_Predominante_Diurna]))
VAR sn = AVERAGEX(T, SIN(RADIANS(Fact_Subdiaria_met_aux[Direccion_Predominante_Diurna])))
VAR cs = AVERAGEX(T, COS(RADIANS(Fact_Subdiaria_met_aux[Direccion_Predominante_Diurna])))
VAR ang =
    SWITCH(
        TRUE(),
        ISBLANK(sn) || ISBLANK(cs), BLANK(),
        cs > 0, DEGREES(ATAN(sn / cs)),
        cs < 0, DEGREES(ATAN(sn / cs)) + 180,
        sn > 0, 90,
        sn < 0, 270,
        BLANK()
    )
RETURN
IF(NOT ISBLANK(ang), MOD(ang + 360, 360))
```
</details>

<details><summary><code>Frec_Dir_Periodo</code></summary>

```dax
// % de horas-estación en que el viento sopla desde el sector en contexto
// (usar con Direcciones_Viento[Direccion] en el eje)
DIVIDE([_Viento_Horas_Sector], [_Viento_Horas_Validas])
```
</details>

<details><summary><code>_Viento_Umbral_Calma</code></summary>

```dax
// Umbral de calma (km/h). 1.8 km/h ≈ 0.5 m/s (criterio OMM).
// Si la API entrega m/s, cambiar a 0.5
1.8
```
</details>

<details><summary><code>_Viento_Horas_Validas</code></summary>

```dax
VAR HoraDesde = SELECTEDVALUE(Periodos_Dia[HoraDesde], 0)
VAR HoraHasta = SELECTEDVALUE(Periodos_Dia[HoraHasta], 23)
VAR U = [_Viento_Umbral_Calma]
RETURN
CALCULATE(
    COUNTROWS(Fact_Horaria_riesgo),
    Fact_Horaria_riesgo[Hora] >= HoraDesde,
    Fact_Horaria_riesgo[Hora] <= HoraHasta,
    FILTER(
        ALL(Fact_Horaria_riesgo[Viento_Media], Fact_Horaria_riesgo[Sector_Viento]),
        NOT ISBLANK(Fact_Horaria_riesgo[Viento_Media])
            && (Fact_Horaria_riesgo[Viento_Media] < U
                || NOT ISBLANK(Fact_Horaria_riesgo[Sector_Viento]))
    ),
    ALL(Direcciones_Viento)
)
```
</details>

<details><summary><code>_Viento_Horas_Sector</code></summary>

```dax
VAR HoraDesde = SELECTEDVALUE(Periodos_Dia[HoraDesde], 0)
VAR HoraHasta = SELECTEDVALUE(Periodos_Dia[HoraHasta], 23)
VAR U = [_Viento_Umbral_Calma]
RETURN
CALCULATE(
    COUNTROWS(Fact_Horaria_riesgo),
    Fact_Horaria_riesgo[Hora] >= HoraDesde,
    Fact_Horaria_riesgo[Hora] <= HoraHasta,
    Fact_Horaria_riesgo[Viento_Media] >= U,
    NOT ISBLANK(Fact_Horaria_riesgo[Sector_Viento])
)
```
</details>

<details><summary><code>Pct_Calmas_Viento</code></summary>

```dax
VAR Validas = [_Viento_Horas_Validas]
RETURN
IF(
    Validas > 0,
    1 - DIVIDE(CALCULATE([_Viento_Horas_Sector], ALL(Direcciones_Viento)), Validas)
)
```
</details>

<details><summary><code>Viento_Media_Periodo</code></summary>

```dax
VAR HoraDesde = SELECTEDVALUE(Periodos_Dia[HoraDesde], 0)
VAR HoraHasta = SELECTEDVALUE(Periodos_Dia[HoraHasta], 23)
RETURN
CALCULATE(
    AVERAGE(Fact_Horaria_riesgo[Viento_Media]),
    Fact_Horaria_riesgo[Hora] >= HoraDesde,
    Fact_Horaria_riesgo[Hora] <= HoraHasta,
    ALL(Direcciones_Viento)
)
```
</details>

<details><summary><code>Viento_Media_Sector</code></summary>

```dax
VAR HoraDesde = SELECTEDVALUE(Periodos_Dia[HoraDesde], 0)
VAR HoraHasta = SELECTEDVALUE(Periodos_Dia[HoraHasta], 23)
VAR U = [_Viento_Umbral_Calma]
RETURN
CALCULATE(
    AVERAGE(Fact_Horaria_riesgo[Viento_Media]),
    Fact_Horaria_riesgo[Hora] >= HoraDesde,
    Fact_Horaria_riesgo[Hora] <= HoraHasta,
    Fact_Horaria_riesgo[Viento_Media] >= U,
    NOT ISBLANK(Fact_Horaria_riesgo[Sector_Viento])
)
```
</details>

<details><summary><code>Dir_Predominante</code></summary>

```dax
VAR T =
    ADDCOLUMNS(
        ALL(Direcciones_Viento[Orden], Direcciones_Viento[Direccion]),
        "@n", [_Viento_Horas_Sector]
    )
VAR Mx = MAXX(T, [@n])
RETURN
IF(Mx > 0, CONCATENATEX(FILTER(T, [@n] = Mx), Direcciones_Viento[Direccion], "/"))
```
</details>

<details><summary><code>Rosa_Vientos_SVG</code></summary>

```dax
// Rosa de vientos como imagen SVG (categoría de datos: URL de imagen).
// Pétalos = % de horas-estación por sector; color = velocidad media del sector.
VAR U        = [_Viento_Umbral_Calma]
VAR Unidad   = "km/h"
VAR cx       = 150
VAR cy       = 150
VAR R0       = 130
VAR px       = 350
VAR Periodo  = SELECTEDVALUE(Periodos_Dia[Periodo], "Todas las horas")
VAR Total    = [_Viento_Horas_Validas]
VAR Sectores =
    ADDCOLUMNS(
        ALL(Direcciones_Viento[Orden], Direcciones_Viento[Direccion]),
        "@Pct", DIVIDE([_Viento_Horas_Sector], Total) * 100,
        "@Vel", [Viento_Media_Sector]
    )
VAR MaxPct   = MAXX(Sectores, [@Pct])
VAR Paso     = SWITCH(TRUE(), MaxPct <= 4, 1, MaxPct <= 10, 2, MaxPct <= 25, 5, MaxPct <= 50, 10, 20)
VAR Escala   = MAX(CEILING(MaxPct / Paso, 1) * Paso, Paso)
VAR Dominante = CONCATENATEX(FILTER(Sectores, [@Pct] = MaxPct && MaxPct > 0), Direcciones_Viento[Direccion], "/")
VAR Calmas   = 100 - SUMX(Sectores, [@Pct])
VAR VelMedia = [Viento_Media_Periodo]
VAR C1 = "rgb(198,219,239)"
VAR C2 = "rgb(107,174,214)"
VAR C3 = "rgb(33,113,181)"
VAR C4 = "rgb(8,48,107)"
VAR Anillos =
    CONCATENATEX(
        GENERATESERIES(1, Escala / Paso, 1),
        VAR rr = [Value] * Paso / Escala * R0
        RETURN
            "<circle cx='" & cx & "' cy='" & cy & "' r='" & FORMAT(rr, "0.0", "en-US")
            & "' fill='none' stroke='rgb(205,205,205)' stroke-width='0.8'/>"
            & "<text x='" & FORMAT(cx + rr * SIN(RADIANS(67.5)) + 2, "0.0", "en-US")
            & "' y='" & FORMAT(cy - rr * COS(RADIANS(67.5)) - 2, "0.0", "en-US")
            & "' font-size='9' fill='rgb(110,110,110)' stroke='white' stroke-width='2.5' paint-order='stroke'>" & FORMAT([Value] * Paso, "0") & "%</text>",
        ""
    )
VAR Ejes =
    "<line x1='" & cx - R0 & "' y1='" & cy & "' x2='" & cx + R0 & "' y2='" & cy & "' stroke='rgb(225,225,225)'/>"
    & "<line x1='" & cx & "' y1='" & cy - R0 & "' x2='" & cx & "' y2='" & cy + R0 & "' stroke='rgb(225,225,225)'/>"
    & "<text x='" & cx & "' y='" & cy - R0 - 8 & "' text-anchor='middle' font-size='13' font-weight='bold' fill='rgb(60,60,60)'>N</text>"
    & "<text x='" & cx + R0 + 8 & "' y='" & cy + 5 & "' text-anchor='start' font-size='13' font-weight='bold' fill='rgb(60,60,60)'>E</text>"
    & "<text x='" & cx & "' y='" & cy + R0 + 20 & "' text-anchor='middle' font-size='13' font-weight='bold' fill='rgb(60,60,60)'>S</text>"
    & "<text x='" & cx - R0 - 8 & "' y='" & cy + 5 & "' text-anchor='end' font-size='13' font-weight='bold' fill='rgb(60,60,60)'>O</text>"
VAR Petalos =
    CONCATENATEX(
        FILTER(Sectores, [@Pct] > 0),
        VAR c   = (Direcciones_Viento[Orden] - 1) * 45
        VAR r   = [@Pct] / Escala * R0
        VAR a1  = RADIANS(c - 20)
        VAR a2  = RADIANS(c + 20)
        VAR v   = [@Vel]
        VAR col = SWITCH(TRUE(), v < 5, C1, v < 10, C2, v < 20, C3, C4)
        RETURN
            "<path d='M" & cx & "," & cy
            & " L" & FORMAT(cx + r * SIN(a1), "0.0", "en-US") & "," & FORMAT(cy - r * COS(a1), "0.0", "en-US")
            & " A" & FORMAT(r, "0.0", "en-US") & "," & FORMAT(r, "0.0", "en-US") & " 0 0,1 "
            & FORMAT(cx + r * SIN(a2), "0.0", "en-US") & "," & FORMAT(cy - r * COS(a2), "0.0", "en-US")
            & " Z' fill='" & col & "' stroke='white' stroke-width='1'/>",
        ""
    )
VAR Panel =
    "<text x='" & px & "' y='30' font-size='15' font-weight='bold' fill='rgb(40,40,40)'>Rosa de vientos · " & Periodo & "</text>"
    & "<text x='" & px & "' y='58' font-size='13' fill='rgb(60,60,60)'>Dirección predominante: <tspan font-weight='bold'>"
        & Dominante & "</tspan> (" & FORMAT(MaxPct, "0.0", "en-US") & "%)</text>"
    & "<text x='" & px & "' y='78' font-size='13' fill='rgb(60,60,60)'>Velocidad media: <tspan font-weight='bold'>"
        & FORMAT(VelMedia, "0.0", "en-US") & " " & Unidad & "</tspan></text>"
    & "<text x='" & px & "' y='98' font-size='13' fill='rgb(60,60,60)'>Calmas (menos de " & FORMAT(U, "0.0", "en-US") & " " & Unidad
        & "): <tspan font-weight='bold'>" & FORMAT(Calmas, "0.0", "en-US") & "%</tspan></text>"
    & "<text x='" & px & "' y='118' font-size='13' fill='rgb(60,60,60)'>Horas-estación analizadas: "
        & FORMAT(Total, "#,0", "en-US") & "</text>"
    & "<text x='" & px & "' y='150' font-size='12' font-weight='bold' fill='rgb(90,90,90)'>Frecuencia por sector (% · vel. media)</text>"
    & CONCATENATEX(
        Sectores,
        VAR i = Direcciones_Viento[Orden] - 1
        VAR x = px + INT(i / 4) * 140
        VAR y = 170 + MOD(i, 4) * 18
        RETURN
            "<text x='" & x & "' y='" & y & "' font-size='11' fill='rgb(60,60,60)'><tspan font-weight='bold'>"
            & Direcciones_Viento[Direccion] & "</tspan><tspan x='" & x + 28 & "'>"
            & FORMAT(COALESCE([@Pct], 0), "0.0", "en-US") & "% · "
            & IF(ISBLANK([@Vel]), "-", FORMAT([@Vel], "0.0", "en-US")) & "</tspan></text>",
        "",
        Direcciones_Viento[Orden], ASC
    )
    & "<text x='" & px & "' y='255' font-size='12' fill='rgb(90,90,90)'>Color: velocidad media del sector (" & Unidad & ")</text>"
    & "<rect x='" & px & "' y='263' width='14' height='10' fill='" & C1 & "'/><text x='" & px + 18 & "' y='272' font-size='10' fill='rgb(60,60,60)'>0-5</text>"
    & "<rect x='" & px + 70 & "' y='263' width='14' height='10' fill='" & C2 & "'/><text x='" & px + 88 & "' y='272' font-size='10' fill='rgb(60,60,60)'>5-10</text>"
    & "<rect x='" & px + 140 & "' y='263' width='14' height='10' fill='" & C3 & "'/><text x='" & px + 158 & "' y='272' font-size='10' fill='rgb(60,60,60)'>10-20</text>"
    & "<rect x='" & px + 210 & "' y='263' width='14' height='10' fill='" & C4 & "'/><text x='" & px + 228 & "' y='272' font-size='10' fill='rgb(60,60,60)'>20+</text>"
VAR Contenido =
    IF(
        COALESCE(Total, 0) = 0,
        "<text x='310' y='150' text-anchor='middle' font-size='14' fill='rgb(120,120,120)'>Sin datos de viento para la selección</text>",
        Anillos & Ejes & Petalos & Panel
    )
VAR Svg =
    "<svg xmlns='http://www.w3.org/2000/svg' width='620' height='310' viewBox='0 0 620 300' font-family='Segoe UI, Arial, sans-serif'>"
    & "<rect width='620' height='300' fill='white'/>" & Contenido & "</svg>"
VAR Cod1 = SUBSTITUTE(SUBSTITUTE(Svg, "%", "%25"), "#", "%23")
VAR Cod2 = SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(Cod1, "·", "%C2%B7"), "ñ", "%C3%B1"), "ó", "%C3%B3")
VAR Cod3 = SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(Cod2, "á", "%C3%A1"), "é", "%C3%A9"), "í", "%C3%AD"), "ú", "%C3%BA")
RETURN
    "data:image/svg+xml;utf8," & Cod3
```
</details>

## Radiación y luz

| Medida | Formato | Descripción |
|---|---|---|
| `Rad_Media_Diurna` |  | Irradiancia media en ventana fija 06–18 h (W/m²). Sin uso en visuales; reemplazada por Rad_Media_Luz. |
| `Rad_Max_Diurna` |  | Irradiancia máxima diurna (W/m²): extremo. |
| `Horas_Luz` |  | Horas con radiación > 40 W/m² (duración del día con luz, no heliofanía) |
| `Rad_Acumulada_Semanal` |  | Radiación de la semana (MJ/m²) desde Fact_Diaria_met; suma por estación, promedio entre estaciones. |
| `Rad_Historico_Promedio` |  | Rad: promedio de la misma semana en años hidrológicos anteriores al seleccionado. |
| `Delta_Rad_YoY` |  | Diferencia de Rad vs. la misma semana del año hidrológico anterior. |
| `Rad_Acumulada_Anual_Grafica` |  | Radiación acumulada por semana del eje (Semanas_Anio), año actual. |
| `Rad_Acumulada_Anual_Anterior_Grafica` |  | Radiación acumulada por semana del eje, año anterior. |
| `Rad_Acumulada_Anual` |  | Radiación acumulada del año hidrológico (MJ/m²). |
| `Rad_Acumulada_Anual_Anterior` |  | Ídem, año hidrológico anterior. |
| `Delta_Rad_Acumulada_YoY` |  | Diferencia de radiación acumulada vs. año anterior (MJ/m²). |
| `Rad_Media_Luz` | 0.0 | Irradiancia media del periodo de luz (W/m²) |
| `Energia_Luz_MJ` | 0.00 | Energía diurna diaria promedio (MJ/m²/día) = irradiancia media de luz × duración de luz |
| `Duracion_Luz_Media` | 0.0 | Duración media del periodo de luz por día (h) |
| `Hora_Inicio_Luz` | 0.00 | Hora media de inicio del periodo de luz (h decimal). |
| `Hora_Fin_Luz` | 0.00 | Hora media de fin del periodo de luz (h decimal). |

<details><summary><code>Rad_Media_Diurna</code></summary>

```dax
AVERAGE(Fact_Subdiaria_met_aux[Rad_Media_Diurna])
```
</details>

<details><summary><code>Rad_Max_Diurna</code></summary>

```dax
MAX(Fact_Subdiaria_met_aux[Rad_Max_Diurna])
```
</details>

<details><summary><code>Horas_Luz</code></summary>

```dax
// Horas del periodo de luz (primera a última lectura > 40 W/m²), sumadas por estación
// en el periodo y promediadas entre estaciones
AVERAGEX(
    VALUES(Estaciones_met[estacionid]),
    CALCULATE(SUM(Fact_Subdiaria_met_aux[Duracion_Luz_h]))
)
```
</details>

<details><summary><code>Rad_Acumulada_Semanal</code></summary>

```dax
CALCULATE(
    AVERAGEX(VALUES(Estaciones_met[estacionid]), CALCULATE(SUM(Fact_Diaria_met[Rad_MJ]))),
    FILTER(
        Calendario,
        Calendario[Semana_Hidrologica] = MAX(Calendario[Semana_Hidrologica]) &&
        Calendario[Año_Hidrologico]    = MAX(Calendario[Año_Hidrologico])
    )
)
```
</details>

<details><summary><code>Rad_Historico_Promedio</code></summary>

```dax
VAR AnioActual   = MAX(Calendario[Año_Hidrologico])
VAR SemanaActual = MAX(Calendario[Semana_Hidrologica])
RETURN
CALCULATE(
    AVERAGEX(
        VALUES(Calendario[Año_Hidrologico]),
        CALCULATE(AVERAGEX(VALUES(Estaciones_met[estacionid]), CALCULATE(SUM(Fact_Diaria_met[Rad_MJ]))))
    ),
    ALL(Calendario),
    Calendario[Semana_Hidrologica] = SemanaActual,
    Calendario[Año_Hidrologico]    < AnioActual
)
```
</details>

<details><summary><code>Delta_Rad_YoY</code></summary>

```dax
VAR AnioActual   = MAX(Calendario[Año_Hidrologico])
VAR SemanaActual = MAX(Calendario[Semana_Hidrologica])
VAR actual =
    CALCULATE(
        AVERAGEX(VALUES(Estaciones_met[estacionid]), CALCULATE(SUM(Fact_Diaria_met[Rad_MJ]))),
        FILTER(
            Calendario,
            Calendario[Semana_Hidrologica] = SemanaActual &&
            Calendario[Año_Hidrologico]    = AnioActual
        )
    )
VAR anterior =
    CALCULATE(
        AVERAGEX(VALUES(Estaciones_met[estacionid]), CALCULATE(SUM(Fact_Diaria_met[Rad_MJ]))),
        FILTER(
            ALL(Calendario),
            Calendario[Semana_Hidrologica] = SemanaActual &&
            Calendario[Año_Hidrologico]    = AnioActual - 1
        )
    )
RETURN
    IF(NOT ISBLANK(anterior), actual - anterior, BLANK())
```
</details>

<details><summary><code>Rad_Acumulada_Anual_Grafica</code></summary>

```dax
VAR AnioActual = CALCULATE(
    MAX(Calendario[Año_Hidrologico]),
    ALLSELECTED(Calendario)
)
VAR SemanaEje = MAX(Semanas_Anio[Semana_Num])
RETURN
IF(
    SemanaEje <= CALCULATE(
        MAX(Calendario[Semana_Hidrologica]),
        ALLSELECTED(Calendario)
    ),
    CALCULATE(
        AVERAGEX(VALUES(Estaciones_met[estacionid]), CALCULATE(SUM(Fact_Diaria_met[Rad_MJ]))),
        ALL(Calendario),
        Calendario[Año_Hidrologico]    = AnioActual,
        Calendario[Semana_Hidrologica] <= SemanaEje
    ),
    BLANK()
)
```
</details>

<details><summary><code>Rad_Acumulada_Anual_Anterior_Grafica</code></summary>

```dax
VAR AnioActual = CALCULATE(
    MAX(Calendario[Año_Hidrologico]),
    ALLSELECTED(Calendario)
)
VAR SemanaEje = MAX(Semanas_Anio[Semana_Num])
RETURN
CALCULATE(
    AVERAGEX(VALUES(Estaciones_met[estacionid]), CALCULATE(SUM(Fact_Diaria_met[Rad_MJ]))),
    ALL(Calendario),
    Calendario[Año_Hidrologico]    = AnioActual - 1,
    Calendario[Semana_Hidrologica] <= SemanaEje
)
```
</details>

<details><summary><code>Rad_Acumulada_Anual</code></summary>

```dax
CALCULATE(
    AVERAGEX(VALUES(Estaciones_met[estacionid]), CALCULATE(SUM(Fact_Diaria_met[Rad_MJ]))),
    FILTER(
        ALL(Calendario),
        Calendario[Año_Hidrologico]    = MAX(Calendario[Año_Hidrologico]) &&
        Calendario[Semana_Hidrologica] <= MAX(Calendario[Semana_Hidrologica])
    )
)
```
</details>

<details><summary><code>Rad_Acumulada_Anual_Anterior</code></summary>

```dax
CALCULATE(
    AVERAGEX(VALUES(Estaciones_met[estacionid]), CALCULATE(SUM(Fact_Diaria_met[Rad_MJ]))),
    FILTER(
        ALL(Calendario),
        Calendario[Año_Hidrologico]    = MAX(Calendario[Año_Hidrologico]) - 1 &&
        Calendario[Semana_Hidrologica] <= MAX(Calendario[Semana_Hidrologica])
    )
)
```
</details>

<details><summary><code>Delta_Rad_Acumulada_YoY</code></summary>

```dax
VAR actual   = [Rad_Acumulada_Anual]
VAR anterior = [Rad_Acumulada_Anual_Anterior]
RETURN
    IF(NOT ISBLANK(anterior), actual - anterior, BLANK())
```
</details>

<details><summary><code>Rad_Media_Luz</code></summary>

```dax
// Irradiancia media del periodo de luz (W/m²)
AVERAGE(Fact_Subdiaria_met_aux[Rad_Media_Luz])
```
</details>

<details><summary><code>Energia_Luz_MJ</code></summary>

```dax
// Energía diurna diaria promedio (MJ/m²/día) = irradiancia media de luz × duración de luz
AVERAGE(Fact_Subdiaria_met_aux[Energia_Luz_MJ])
```
</details>

<details><summary><code>Duracion_Luz_Media</code></summary>

```dax
// Duración media del periodo de luz por día (h)
AVERAGE(Fact_Subdiaria_met_aux[Duracion_Luz_h])
```
</details>

<details><summary><code>Hora_Inicio_Luz</code></summary>

```dax
AVERAGE(Fact_Subdiaria_met_aux[Hora_Inicio_Luz])
```
</details>

<details><summary><code>Hora_Fin_Luz</code></summary>

```dax
AVERAGE(Fact_Subdiaria_met_aux[Hora_Fin_Luz])
```
</details>

## Semáforos

| Medida | Formato | Descripción |
|---|---|---|
| `Semaforo_Balance` | 0 | Semáforo de balance hídrico semanal: 1 rojo, 2 amarillo, 3 verde. |
| `Semaforo_Deficit` | 0 | Semáforo de estaciones en déficit crítico: 1 rojo, 2 amarillo, 3 verde. |
| `Semaforo_VPD` |  | Semáforo de VPD máximo diurno: 1 rojo, 2 amarillo, 3 verde. |
| `Semaforo_Temp_Nocturna` |  | Semáforo de temperatura nocturna media: 1 rojo, 2 amarillo, 3 verde. |
| `Semaforo_Estres_Termico` |  | Semáforo de horas de estrés térmico: 1 rojo, 2 amarillo, 3 verde. |
| `Semaforo_Roya` |  | Semáforo de roya: 1 rojo, 2 amarillo, 3 verde. |
| `Semaforo_Carbon` |  | Semáforo de carbón: 1 rojo, 2 amarillo, 3 verde. |
| `Semaforo_Salivosa` |  | Semáforo de salivosa: 1 rojo, 2 amarillo, 3 verde. |
| `Semaforo_Barrenador` |  | Semáforo de barrenador: 1 rojo, 2 amarillo, 3 verde. |
| `Semaforo_Sigatoka` |  | Semáforo de sigatoka: 1 rojo, 2 amarillo, 3 verde. |
| `Semaforo_Phytophthora` |  | Semáforo de Phytophthora: 1 rojo, 2 amarillo, 3 verde. |
| `Semaforo_Frio_Aguacate` |  | Semáforo de frío en aguacate (Tmín < 12 °C): 1 rojo, 2 amarillo, 3 verde. |
| `Semaforo_PC_Palma` |  | Semáforo de pudrición del cogollo en palma: 1 rojo, 2 amarillo, 3 verde. |
| `Semaforo_Mancha_Asfalto` |  | Semáforo de mancha de asfalto: 1 rojo, 2 amarillo, 3 verde. |
| `Semaforo_Sequia_Granos` |  | Semáforo de sequía en granos: 1 rojo, 2 amarillo, 3 verde. |
| `Semaforo_Roya_Nocturna` |  | Semáforo de roya (mojadura total > 8 h): 1 rojo, 2 amarillo, 3 verde. |

<details><summary><code>Semaforo_Balance</code></summary>

```dax
VAR balance = [Balance_Semanal]
RETURN
    SWITCH(
        TRUE(),
        balance < -20, 1,
        balance < 0,   2,
        3
    )
```
</details>

<details><summary><code>Semaforo_Deficit</code></summary>

```dax
IF([Estaciones_Deficit_Critico] > 0, 1, 3)
```
</details>

<details><summary><code>Semaforo_VPD</code></summary>

```dax
VAR vpd = [VPD_Max_Diurna]
RETURN
    SWITCH(
        TRUE(),
        vpd > 3.0, 1,
        vpd > 2.0, 2,
        3
    )
```
</details>

<details><summary><code>Semaforo_Temp_Nocturna</code></summary>

```dax
VAR tn = [Temp_Nocturna_Media]
RETURN
    SWITCH(
        TRUE(),
        tn > 24, 1,
        tn > 22, 2,
        3
    )
```
</details>

<details><summary><code>Semaforo_Estres_Termico</code></summary>

```dax
VAR horas = [Horas_Estres_Termico_Semanal]
RETURN
    SWITCH(
        TRUE(),
        horas > 28, 1,
        horas > 14, 2,
        3
    )
```
</details>

<details><summary><code>Semaforo_Roya</code></summary>

```dax
VAR dias = [Dias_Riesgo_Roya]
RETURN
    SWITCH(
        TRUE(),
        dias >= 3, 1,
        dias >= 1, 2,
        3
    )
```
</details>

<details><summary><code>Semaforo_Carbon</code></summary>

```dax
VAR dias = [Dias_Riesgo_Carbon]
RETURN
    SWITCH(
        TRUE(),
        dias >= 5, 1,
        dias >= 3, 2,
        3
    )
```
</details>

<details><summary><code>Semaforo_Salivosa</code></summary>

```dax
VAR dias = [Dias_Riesgo_Salivosa]
RETURN
    SWITCH(
        TRUE(),
        dias >= 4, 1,
        dias >= 2, 2,
        3
    )
```
</details>

<details><summary><code>Semaforo_Barrenador</code></summary>

```dax
VAR dias = [Dias_Riesgo_Barrenador]
RETURN
    SWITCH(
        TRUE(),
        dias >= 4, 1,
        dias >= 2, 2,
        3
    )
```
</details>

<details><summary><code>Semaforo_Sigatoka</code></summary>

```dax
VAR dias = [Dias_Riesgo_Sigatoka]
RETURN
    SWITCH(
        TRUE(),
        dias >= 3, 1,
        dias >= 1, 2,
        3
    )
```
</details>

<details><summary><code>Semaforo_Phytophthora</code></summary>

```dax
VAR dias = [Dias_Riesgo_Phytophthora]
VAR balance = [Balance_Semanal]
RETURN
    SWITCH(
        TRUE(),
        dias >= 3 && balance > 50, 1,
        dias >= 1, 2,
        3
    )
```
</details>

<details><summary><code>Semaforo_Frio_Aguacate</code></summary>

```dax
VAR dias = [Dias_Riesgo_Frio_Aguacate]
RETURN
    SWITCH(
        TRUE(),
        dias >= 3, 1,
        dias >= 1, 2,
        3
    )
```
</details>

<details><summary><code>Semaforo_PC_Palma</code></summary>

```dax
VAR PrecipSemanal = [Precip_Semanal]
VAR TempMedia = [Temp_Media]
RETURN
    SWITCH(
        TRUE(),
        PrecipSemanal > 150 && TempMedia < 26, 1,
        PrecipSemanal > 100 && TempMedia < 26, 2,
        3
    )
```
</details>

<details><summary><code>Semaforo_Mancha_Asfalto</code></summary>

```dax
VAR dias = [Dias_Riesgo_Mancha_Asfalto]
RETURN
    SWITCH(
        TRUE(),
        dias >= 4, 1,
        dias >= 2, 2,
        3
    )
```
</details>

<details><summary><code>Semaforo_Sequia_Granos</code></summary>

```dax
VAR dias = [Dias_Sequia_Critica_Granos]
RETURN
    SWITCH(
        TRUE(),
        dias >= 5, 1,
        dias >= 3, 2,
        3
    )
```
</details>

<details><summary><code>Semaforo_Roya_Nocturna</code></summary>

```dax
VAR dias = [Dias_Riesgo_Roya_Nocturna]
RETURN
    SWITCH(
        TRUE(),
        dias >= 3, 1,
        dias >= 1, 2,
        3
    )
```
</details>

## Días y condiciones de riesgo (plagas, enfermedades, clima)

| Medida | Formato | Descripción |
|---|---|---|
| `Dias_Riesgo_Roya` |  | Promedio de días por estación (solo estaciones con datos en el periodo) |
| `Dias_Riesgo_Carbon` |  | Promedio de días por estación (solo estaciones con datos en el periodo) |
| `Dias_Riesgo_Salivosa` |  | Promedio de días por estación (solo estaciones con datos en el periodo) |
| `Dias_Riesgo_Barrenador` |  | Promedio de días por estación (solo estaciones con datos en el periodo) |
| `Dias_Riesgo_Sigatoka` |  | Promedio de días por estación (solo estaciones con datos en el periodo) |
| `Dias_Riesgo_Moko` |  | Días (promedio por estación) con condiciones favorables a moko. |
| `Dias_Riesgo_Phytophthora` |  | Promedio de días por estación (solo estaciones con datos en el periodo) |
| `Dias_Riesgo_Frio_Aguacate` |  | Promedio de días por estación (solo estaciones con datos en el periodo) |
| `Dias_Riesgo_Mancha_Asfalto` |  | Promedio de días por estación (solo estaciones con datos en el periodo) |
| `Dias_Sequia_Critica_Granos` |  | Promedio de días por estación (solo estaciones con datos en el periodo) |
| `Dias_Riesgo_Roya_Nocturna` |  | Promedio de días por estación (solo estaciones con datos en el periodo) |
| `Indice_Riesgo_Hora` |  | Suma promedio de banderas horarias (roya + salivosa + barrenador + carbón). |
| `Condicion_Roya_Hora` |  | Fracción de horas-estación favorables a roya (bandera horaria). |
| `Condicion_Barrenador_Hora` |  | Fracción de horas-estación favorables a barrenador (bandera horaria). |
| `Condicion_Salivosa_Hora` |  | Fracción de horas-estación favorables a salivosa (bandera horaria). |
| `Condicion_Carbon_Hora` |  | Fracción de horas-estación favorables a carbon (bandera horaria). |
| `Condicion_Plaga_Hora` |  | Fracción de horas-estación favorables a la plaga elegida en el segmentador Plagas. |

<details><summary><code>Dias_Riesgo_Roya</code></summary>

```dax
VAR AnioActual   = MAX(Calendario[Año_Hidrologico])
VAR SemanaActual = MAX(Calendario[Semana_Hidrologica])
VAR Periodo =
    FILTER(
        ALL(Calendario),
        Calendario[Año_Hidrologico]    = AnioActual &&
        Calendario[Semana_Hidrologica] = SemanaActual
    )
// Promedio de días por estación (solo estaciones con datos en el periodo)
VAR Estaciones =
    FILTER(
        VALUES(Estaciones_met[estacionid]),
        NOT ISEMPTY(CALCULATETABLE(Fact_Diaria_met, Periodo))
    )
RETURN
AVERAGEX(
    Estaciones,
    CALCULATE(
        COUNTROWS(Fact_Diaria_met),
        Periodo,
        Fact_Diaria_met[Temp_Media] >= 15,
        Fact_Diaria_met[Temp_Media] <= 25,
        Fact_Diaria_met[HR_Media]   > 80,
        FILTER(
            CALCULATETABLE(VALUES(Calendario[Fecha]), Periodo),
            CALCULATE(MAX(Fact_Subdiaria_met_aux[Mojadura_Horas_Diurna])) > 6
        )
    ) + 0
)
```
</details>

<details><summary><code>Dias_Riesgo_Carbon</code></summary>

```dax
// Promedio de días por estación (solo estaciones con datos en el periodo)
VAR Estaciones =
    FILTER(
        VALUES(Estaciones_met[estacionid]),
        NOT ISEMPTY(CALCULATETABLE(Fact_Diaria_met))
    )
RETURN
AVERAGEX(
    Estaciones,
    CALCULATE(
        COUNTROWS(Fact_Diaria_met),
        Fact_Diaria_met[Temp_Media] >= 25,
        Fact_Diaria_met[Temp_Media] <= 30,
        Fact_Diaria_met[Dia_Seco]   = TRUE()
    ) + 0
)
```
</details>

<details><summary><code>Dias_Riesgo_Salivosa</code></summary>

```dax
// Promedio de días por estación (solo estaciones con datos en el periodo)
VAR Estaciones =
    FILTER(
        VALUES(Estaciones_met[estacionid]),
        NOT ISEMPTY(CALCULATETABLE(Fact_Diaria_met))
    )
RETURN
AVERAGEX(
    Estaciones,
    CALCULATE(
        COUNTROWS(Fact_Diaria_met),
        Fact_Diaria_met[Temp_Media] >= 22,
        Fact_Diaria_met[Temp_Media] <= 28,
        Fact_Diaria_met[HR_Media]   > 80,
        Fact_Diaria_met[Precip_Total] > 5
    ) + 0
)
```
</details>

<details><summary><code>Dias_Riesgo_Barrenador</code></summary>

```dax
// Promedio de días por estación (solo estaciones con datos en el periodo)
VAR Estaciones =
    FILTER(
        VALUES(Estaciones_met[estacionid]),
        NOT ISEMPTY(CALCULATETABLE(Fact_Diaria_met))
    )
RETURN
AVERAGEX(
    Estaciones,
    CALCULATE(
        COUNTROWS(Fact_Diaria_met),
        Fact_Diaria_met[Temp_Media] > 24,
        Fact_Diaria_met[HR_Media]   >= 60,
        Fact_Diaria_met[HR_Media]   <= 80,
        Fact_Diaria_met[Dia_Seco]   = TRUE()
    ) + 0
)
```
</details>

<details><summary><code>Dias_Riesgo_Sigatoka</code></summary>

```dax
VAR AnioActual   = MAX(Calendario[Año_Hidrologico])
VAR SemanaActual = MAX(Calendario[Semana_Hidrologica])
VAR Periodo =
    FILTER(
        ALL(Calendario),
        Calendario[Año_Hidrologico]    = AnioActual &&
        Calendario[Semana_Hidrologica] = SemanaActual
    )
// Promedio de días por estación (solo estaciones con datos en el periodo)
VAR Estaciones =
    FILTER(
        VALUES(Estaciones_met[estacionid]),
        NOT ISEMPTY(CALCULATETABLE(Fact_Diaria_met, Periodo))
    )
RETURN
AVERAGEX(
    Estaciones,
    CALCULATE(
        COUNTROWS(Fact_Diaria_met),
        Periodo,
        Fact_Diaria_met[Temp_Media] >= 25,
        Fact_Diaria_met[Temp_Media] <= 28,
        Fact_Diaria_met[HR_Media]   > 90,
        FILTER(
            CALCULATETABLE(VALUES(Calendario[Fecha]), Periodo),
            CALCULATE(MAX(Fact_Subdiaria_met_aux[Mojadura_Horas_Nocturna])) > 4
        )
    ) + 0
)
```
</details>

<details><summary><code>Dias_Riesgo_Moko</code></summary>

```dax
VAR PrecipSemanal = [Precip_Semanal]
VAR BalanceSemanal = [Balance_Semanal]
RETURN
    IF(
        PrecipSemanal > 100 && BalanceSemanal > 0,
        1, 3
    )
```
</details>

<details><summary><code>Dias_Riesgo_Phytophthora</code></summary>

```dax
// Promedio de días por estación (solo estaciones con datos en el periodo)
VAR Estaciones =
    FILTER(
        VALUES(Estaciones_met[estacionid]),
        NOT ISEMPTY(CALCULATETABLE(Fact_Diaria_met))
    )
RETURN
AVERAGEX(
    Estaciones,
    CALCULATE(
        COUNTROWS(Fact_Diaria_met),
        Fact_Diaria_met[Balance_Hidrico] > 0,
        Fact_Diaria_met[Temp_Media] >= 20,
        Fact_Diaria_met[Temp_Media] <= 30
    ) + 0
)
```
</details>

<details><summary><code>Dias_Riesgo_Frio_Aguacate</code></summary>

```dax
// Promedio de días por estación (solo estaciones con datos en el periodo)
VAR Estaciones =
    FILTER(
        VALUES(Estaciones_met[estacionid]),
        NOT ISEMPTY(CALCULATETABLE(Fact_Diaria_met))
    )
RETURN
AVERAGEX(
    Estaciones,
    CALCULATE(
        COUNTROWS(Fact_Diaria_met),
        Fact_Diaria_met[Temp_Min] < 12
    ) + 0
)
```
</details>

<details><summary><code>Dias_Riesgo_Mancha_Asfalto</code></summary>

```dax
// Promedio de días por estación (solo estaciones con datos en el periodo)
VAR Estaciones =
    FILTER(
        VALUES(Estaciones_met[estacionid]),
        NOT ISEMPTY(CALCULATETABLE(Fact_Diaria_met))
    )
RETURN
AVERAGEX(
    Estaciones,
    CALCULATE(
        COUNTROWS(Fact_Diaria_met),
        Fact_Diaria_met[Temp_Media] >= 20,
        Fact_Diaria_met[Temp_Media] <= 28,
        Fact_Diaria_met[HR_Media]   > 80
    ) + 0
)
```
</details>

<details><summary><code>Dias_Sequia_Critica_Granos</code></summary>

```dax
// Promedio de días por estación (solo estaciones con datos en el periodo)
VAR Estaciones =
    FILTER(
        VALUES(Estaciones_met[estacionid]),
        NOT ISEMPTY(CALCULATETABLE(Fact_Diaria_met))
    )
RETURN
AVERAGEX(
    Estaciones,
    CALCULATE(
        COUNTROWS(Fact_Diaria_met),
        Fact_Diaria_met[Dia_Seco] = TRUE()
    ) + 0
)
```
</details>

<details><summary><code>Dias_Riesgo_Roya_Nocturna</code></summary>

```dax
VAR AnioActual   = MAX(Calendario[Año_Hidrologico])
VAR SemanaActual = MAX(Calendario[Semana_Hidrologica])
VAR Periodo =
    FILTER(
        ALL(Calendario),
        Calendario[Año_Hidrologico]    = AnioActual &&
        Calendario[Semana_Hidrologica] = SemanaActual
    )
// Promedio de días por estación (solo estaciones con datos en el periodo)
VAR Estaciones =
    FILTER(
        VALUES(Estaciones_met[estacionid]),
        NOT ISEMPTY(CALCULATETABLE(Fact_Diaria_met, Periodo))
    )
RETURN
AVERAGEX(
    Estaciones,
    CALCULATE(
        COUNTROWS(Fact_Diaria_met),
        Periodo,
        Fact_Diaria_met[Temp_Media] >= 15,
        Fact_Diaria_met[Temp_Media] <= 25,
        Fact_Diaria_met[HR_Media]   > 80,
        FILTER(
            CALCULATETABLE(VALUES(Calendario[Fecha]), Periodo),
            CALCULATE(MAX(Fact_Subdiaria_met_aux[Mojadura_Horas_Total])) > 8
        )
    ) + 0
)
```
</details>

<details><summary><code>Indice_Riesgo_Hora</code></summary>

```dax
AVERAGE(Fact_Horaria_riesgo[Indice_Riesgo])
```
</details>

<details><summary><code>Condicion_Roya_Hora</code></summary>

```dax
AVERAGE(Fact_Horaria_riesgo[Flag_Roya])
```
</details>

<details><summary><code>Condicion_Barrenador_Hora</code></summary>

```dax
AVERAGE(Fact_Horaria_riesgo[Flag_Barrenador])
```
</details>

<details><summary><code>Condicion_Salivosa_Hora</code></summary>

```dax
AVERAGE(Fact_Horaria_riesgo[Flag_Salivosa])
```
</details>

<details><summary><code>Condicion_Carbon_Hora</code></summary>

```dax
AVERAGE(Fact_Horaria_riesgo[Flag_Carbon])
```
</details>

<details><summary><code>Condicion_Plaga_Hora</code></summary>

```dax
VAR EsRoya      = CALCULATE(HASONEVALUE(Plagas[id]), Plagas[id] = 1)
VAR EsCarbon    = CALCULATE(HASONEVALUE(Plagas[id]), Plagas[id] = 2)
VAR EsSalivosa  = CALCULATE(HASONEVALUE(Plagas[id]), Plagas[id] = 3)
VAR EsBarrenador = CALCULATE(HASONEVALUE(Plagas[id]), Plagas[id] = 4)
RETURN
SWITCH(
    TRUE(),
    EsRoya,       [Condicion_Roya_Hora],
    EsCarbon,     [Condicion_Carbon_Hora],
    EsSalivosa,   [Condicion_Salivosa_Hora],
    EsBarrenador, [Condicion_Barrenador_Hora],
    [Indice_Riesgo_Hora]
)
```
</details>

## Grados día / suma térmica (GDD)

| Medida | Formato | Descripción |
|---|---|---|
| `GDD_Semanal_Base10` |  | Grados día base 10 °C de la semana. |
| `GDD_Semanal_Base15` |  | Grados día base 15 °C de la semana. |
| `GDD_Cana_ST_Semanal` |  | Suma térmica con temperatura óptima tope para caña de azúcar de la semana. |
| `GDD_Banano_ST_Semanal` |  | Suma térmica con temperatura óptima tope para banano de la semana. |
| `GDD_Aguacate_ST_Semanal` |  | Suma térmica con temperatura óptima tope para aguacate de la semana. |
| `GDD_Palma_ST_Semanal` |  | Suma térmica con temperatura óptima tope para palma de aceite de la semana. |
| `GDD_Maiz_ST_Semanal` |  | Suma térmica con temperatura óptima tope para maíz de la semana. |
| `GDD_Cana_ST_Acumulado` |  | Suma térmica con temperatura óptima tope para caña de azúcar acumulada del año hidrológico. |
| `GDD_Cana_ST_Acumulado_Anterior` |  | Suma térmica con temperatura óptima tope para caña de azúcar acumulada del año hidrológico, año anterior. |
| `GDD_Banano_ST_Acumulado` |  | Suma térmica con temperatura óptima tope para banano acumulada del año hidrológico. |
| `GDD_Banano_ST_Acumulado_Anterior` |  | Suma térmica con temperatura óptima tope para banano acumulada del año hidrológico, año anterior. |
| `GDD_Aguacate_ST_Acumulado` |  | Suma térmica con temperatura óptima tope para aguacate acumulada del año hidrológico. |
| `GDD_Palma_ST_Acumulado` |  | Suma térmica con temperatura óptima tope para palma de aceite acumulada del año hidrológico. |
| `GDD_Maiz_ST_Acumulado` |  | Suma térmica con temperatura óptima tope para maíz acumulada del año hidrológico. |
| `GDD_Display_cana` |  | Texto con GDD acumulado de caña actual y del año anterior. |
| `GDD_Cana_ST_Acumulado_Grafica` |  | Suma térmica con temperatura óptima tope para caña de azúcar acumulada del año hidrológico (por semana del eje). |
| `GDD_Cana_ST_Acumulado_Anterior_Grafica` |  | Suma térmica con temperatura óptima tope para caña de azúcar acumulada del año hidrológico, año anterior (por semana del eje). |

<details><summary><code>GDD_Semanal_Base10</code></summary>

```dax
AVERAGEX(VALUES(Estaciones_met[estacionid]), CALCULATE(SUM(Fact_Diaria_met[GDD_Base10])))
```
</details>

<details><summary><code>GDD_Semanal_Base15</code></summary>

```dax
AVERAGEX(VALUES(Estaciones_met[estacionid]), CALCULATE(SUM(Fact_Diaria_met[GDD_Base15])))
```
</details>

<details><summary><code>GDD_Cana_ST_Semanal</code></summary>

```dax
AVERAGEX(VALUES(Estaciones_met[estacionid]), CALCULATE(SUM(Fact_Diaria_met[GDD_Cana_ST])))
```
</details>

<details><summary><code>GDD_Banano_ST_Semanal</code></summary>

```dax
AVERAGEX(VALUES(Estaciones_met[estacionid]), CALCULATE(SUM(Fact_Diaria_met[GDD_Banano_ST])))
```
</details>

<details><summary><code>GDD_Aguacate_ST_Semanal</code></summary>

```dax
AVERAGEX(VALUES(Estaciones_met[estacionid]), CALCULATE(SUM(Fact_Diaria_met[GDD_Aguacate_ST])))
```
</details>

<details><summary><code>GDD_Palma_ST_Semanal</code></summary>

```dax
AVERAGEX(VALUES(Estaciones_met[estacionid]), CALCULATE(SUM(Fact_Diaria_met[GDD_Palma_ST])))
```
</details>

<details><summary><code>GDD_Maiz_ST_Semanal</code></summary>

```dax
AVERAGEX(VALUES(Estaciones_met[estacionid]), CALCULATE(SUM(Fact_Diaria_met[GDD_Maiz_ST])))
```
</details>

<details><summary><code>GDD_Cana_ST_Acumulado</code></summary>

```dax
CALCULATE(
    AVERAGEX(VALUES(Estaciones_met[estacionid]), CALCULATE(SUM(Fact_Diaria_met[GDD_Cana_ST]))),
    FILTER(
        ALL(Calendario),
        Calendario[Año_Hidrologico]    = MAX(Calendario[Año_Hidrologico]) &&
        Calendario[Semana_Hidrologica] <= MAX(Calendario[Semana_Hidrologica])
    )
)
```
</details>

<details><summary><code>GDD_Cana_ST_Acumulado_Anterior</code></summary>

```dax
CALCULATE(
    AVERAGEX(VALUES(Estaciones_met[estacionid]), CALCULATE(SUM(Fact_Diaria_met[GDD_Cana_ST]))),
    FILTER(
        ALL(Calendario),
        Calendario[Año_Hidrologico]    = MAX(Calendario[Año_Hidrologico]) - 1 &&
        Calendario[Semana_Hidrologica] <= MAX(Calendario[Semana_Hidrologica])
    )
)
```
</details>

<details><summary><code>GDD_Banano_ST_Acumulado</code></summary>

```dax
CALCULATE(
    AVERAGEX(VALUES(Estaciones_met[estacionid]), CALCULATE(SUM(Fact_Diaria_met[GDD_Banano_ST]))),
    FILTER(
        ALL(Calendario),
        Calendario[Año_Hidrologico]    = MAX(Calendario[Año_Hidrologico]) &&
        Calendario[Semana_Hidrologica] <= MAX(Calendario[Semana_Hidrologica])
    )
)
```
</details>

<details><summary><code>GDD_Banano_ST_Acumulado_Anterior</code></summary>

```dax
CALCULATE(
    AVERAGEX(VALUES(Estaciones_met[estacionid]), CALCULATE(SUM(Fact_Diaria_met[GDD_Banano_ST]))),
    FILTER(
        ALL(Calendario),
        Calendario[Año_Hidrologico]    = MAX(Calendario[Año_Hidrologico]) - 1 &&
        Calendario[Semana_Hidrologica] <= MAX(Calendario[Semana_Hidrologica])
    )
)
```
</details>

<details><summary><code>GDD_Aguacate_ST_Acumulado</code></summary>

```dax
CALCULATE(
    AVERAGEX(VALUES(Estaciones_met[estacionid]), CALCULATE(SUM(Fact_Diaria_met[GDD_Aguacate_ST]))),
    FILTER(
        ALL(Calendario),
        Calendario[Año_Hidrologico]    = MAX(Calendario[Año_Hidrologico]) &&
        Calendario[Semana_Hidrologica] <= MAX(Calendario[Semana_Hidrologica])
    )
)
```
</details>

<details><summary><code>GDD_Palma_ST_Acumulado</code></summary>

```dax
CALCULATE(
    AVERAGEX(VALUES(Estaciones_met[estacionid]), CALCULATE(SUM(Fact_Diaria_met[GDD_Palma_ST]))),
    FILTER(
        ALL(Calendario),
        Calendario[Año_Hidrologico]    = MAX(Calendario[Año_Hidrologico]) &&
        Calendario[Semana_Hidrologica] <= MAX(Calendario[Semana_Hidrologica])
    )
)
```
</details>

<details><summary><code>GDD_Maiz_ST_Acumulado</code></summary>

```dax
CALCULATE(
    AVERAGEX(VALUES(Estaciones_met[estacionid]), CALCULATE(SUM(Fact_Diaria_met[GDD_Maiz_ST]))),
    FILTER(
        ALL(Calendario),
        Calendario[Año_Hidrologico]    = MAX(Calendario[Año_Hidrologico]) &&
        Calendario[Semana_Hidrologica] <= MAX(Calendario[Semana_Hidrologica])
    )
)
```
</details>

<details><summary><code>GDD_Display_cana</code></summary>

```dax
"Acumulado: " & FORMAT([GDD_Cana_ST_Acumulado], "0.0") & 
" | Año ant.: " & FORMAT([GDD_Cana_ST_Acumulado_Anterior], "0.0")
```
</details>

<details><summary><code>GDD_Cana_ST_Acumulado_Grafica</code></summary>

```dax
VAR AnioActual = CALCULATE(
    MAX(Calendario[Año_Hidrologico]),
    ALLSELECTED(Calendario)
)
VAR SemanaMax = CALCULATE(
    MAX(Calendario[Semana_Hidrologica]),
    ALLSELECTED(Calendario)
)
VAR SemanaEje = MAX('Semanas_Anio'[Semana_Num])
RETURN
IF(
    SemanaEje <= SemanaMax,
    CALCULATE(
        AVERAGEX(VALUES(Estaciones_met[estacionid]), CALCULATE(SUM(Fact_Diaria_met[GDD_Cana_ST]))),
        ALL(Calendario),
        Calendario[Año_Hidrologico]    = AnioActual,
        Calendario[Semana_Hidrologica] <= SemanaEje
    ),
    BLANK()
)
```
</details>

<details><summary><code>GDD_Cana_ST_Acumulado_Anterior_Grafica</code></summary>

```dax
VAR AnioActual = CALCULATE(
    MAX(Calendario[Año_Hidrologico]),
    ALLSELECTED(Calendario)
)
VAR SemanaEje = MAX('Semanas_Anio'[Semana_Num])
RETURN
CALCULATE(
    AVERAGEX(VALUES(Estaciones_met[estacionid]), CALCULATE(SUM(Fact_Diaria_met[GDD_Cana_ST]))),
    ALL(Calendario),
    Calendario[Año_Hidrologico]    = AnioActual - 1,
    Calendario[Semana_Hidrologica] <= SemanaEje
)
```
</details>

## Históricos y comparaciones interanuales

| Medida | Formato | Descripción |
|---|---|---|
| `Precip_Historico_Promedio` |  | Precip: promedio de la misma semana en años hidrológicos anteriores al seleccionado. |
| `Precip_Historico_Max` |  | Precip: max de la misma semana en años hidrológicos anteriores al seleccionado. |
| `Precip_Historico_Min` |  | Precip: min de la misma semana en años hidrológicos anteriores al seleccionado. |
| `Temp_Max_Historico` |  | Temp Max: promedio de la misma semana en años hidrológicos anteriores al seleccionado. |
| `Temp_Min_Historico` |  | Temp Min: promedio de la misma semana en años hidrológicos anteriores al seleccionado. |
| `Temp_Media_Historico` |  | Temp Media: promedio de la misma semana en años hidrológicos anteriores al seleccionado. |
| `Precip_Acumulada_Anual_Anterior` |  | Lluvia acumulada desde el inicio del año hidrológico (mm), año anterior. |
| `Delta_Precip_YoY` |  | Diferencia de Precip vs. la misma semana del año hidrológico anterior. |
| `Delta_Temp_Media_YoY` |  | Diferencia de Temp Media vs. la misma semana del año hidrológico anterior. |
| `Delta_Balance_YoY` |  | Diferencia de Balance vs. la misma semana del año hidrológico anterior. |
| `Amplitud_Termica_Historico` |  | Amplitud Termica: promedio de la misma semana en años hidrológicos anteriores al seleccionado. |
| `ETO_Historico_Promedio` |  | ETO: promedio de la misma semana en años hidrológicos anteriores al seleccionado. |
| `Balance_Historico_Promedio` |  | Balance: promedio de la misma semana en años hidrológicos anteriores al seleccionado. |
| `Delta_ETO_YoY` |  | Diferencia de ETO vs. la misma semana del año hidrológico anterior. |

<details><summary><code>Precip_Historico_Promedio</code></summary>

```dax
VAR AnioActual   = MAX(Calendario[Año_Hidrologico])
VAR SemanaActual = MAX(Calendario[Semana_Hidrologica])
RETURN
CALCULATE(
    AVERAGEX(
        VALUES(Calendario[Año_Hidrologico]),
        CALCULATE(AVERAGEX(VALUES(Estaciones_met[estacionid]), CALCULATE(SUM(Fact_Diaria_met[Precip_Total]))))
    ),
    ALL(Calendario),
    Calendario[Semana_Hidrologica] = SemanaActual,
    Calendario[Año_Hidrologico]    < AnioActual
)
```
</details>

<details><summary><code>Precip_Historico_Max</code></summary>

```dax
VAR AnioActual   = MAX(Calendario[Año_Hidrologico])
VAR SemanaActual = MAX(Calendario[Semana_Hidrologica])
RETURN
CALCULATE(
    MAXX(
        VALUES(Calendario[Año_Hidrologico]),
        CALCULATE(AVERAGEX(VALUES(Estaciones_met[estacionid]), CALCULATE(SUM(Fact_Diaria_met[Precip_Total]))))
    ),
    ALL(Calendario),
    Calendario[Semana_Hidrologica] = SemanaActual,
    Calendario[Año_Hidrologico]    < AnioActual
)
```
</details>

<details><summary><code>Precip_Historico_Min</code></summary>

```dax
VAR AnioActual   = MAX(Calendario[Año_Hidrologico])
VAR SemanaActual = MAX(Calendario[Semana_Hidrologica])
RETURN
CALCULATE(
    MINX(
        VALUES(Calendario[Año_Hidrologico]),
        CALCULATE(AVERAGEX(VALUES(Estaciones_met[estacionid]), CALCULATE(SUM(Fact_Diaria_met[Precip_Total]))))
    ),
    ALL(Calendario),
    Calendario[Semana_Hidrologica] = SemanaActual,
    Calendario[Año_Hidrologico]    < AnioActual
)
```
</details>

<details><summary><code>Temp_Max_Historico</code></summary>

```dax
VAR AnioActual   = MAX(Calendario[Año_Hidrologico])
VAR SemanaActual = MAX(Calendario[Semana_Hidrologica])
RETURN
CALCULATE(
    MAX(Fact_Diaria_met[Temp_Max]),
    ALL(Calendario),
    Calendario[Semana_Hidrologica] = SemanaActual,
    Calendario[Año_Hidrologico]    < AnioActual
)
```
</details>

<details><summary><code>Temp_Min_Historico</code></summary>

```dax
VAR AnioActual   = MAX(Calendario[Año_Hidrologico])
VAR SemanaActual = MAX(Calendario[Semana_Hidrologica])
RETURN
CALCULATE(
    MIN(Fact_Diaria_met[Temp_Min]),
    ALL(Calendario),
    Calendario[Semana_Hidrologica] = SemanaActual,
    Calendario[Año_Hidrologico]    < AnioActual
)
```
</details>

<details><summary><code>Temp_Media_Historico</code></summary>

```dax
VAR AnioActual   = MAX(Calendario[Año_Hidrologico])
VAR SemanaActual = MAX(Calendario[Semana_Hidrologica])
RETURN
CALCULATE(
    AVERAGEX(
        VALUES(Calendario[Año_Hidrologico]),
        CALCULATE(AVERAGE(Fact_Diaria_met[Temp_Media]))
    ),
    ALL(Calendario),
    Calendario[Semana_Hidrologica] = SemanaActual,
    Calendario[Año_Hidrologico]    < AnioActual
)
```
</details>

<details><summary><code>Precip_Acumulada_Anual_Anterior</code></summary>

```dax
CALCULATE(
    AVERAGEX(VALUES(Estaciones_met[estacionid]), CALCULATE(SUM(Fact_Diaria_met[Precip_Total]))),
    FILTER(
        ALL(Calendario),
        Calendario[Año_Hidrologico]    = MAX(Calendario[Año_Hidrologico]) - 1 &&
        Calendario[Semana_Hidrologica] <= MAX(Calendario[Semana_Hidrologica])
    )
)
```
</details>

<details><summary><code>Delta_Precip_YoY</code></summary>

```dax
VAR AnioActual   = MAX(Calendario[Año_Hidrologico])
VAR SemanaActual = MAX(Calendario[Semana_Hidrologica])
VAR actual = [Precip_Semanal]
VAR anterior = 
    CALCULATE(
        [Precip_Semanal],
        FILTER(
            ALL(Calendario),
            Calendario[Semana_Hidrologica] = SemanaActual &&
            Calendario[Año_Hidrologico]    = AnioActual - 1
        )
    )
RETURN
    IF(
        NOT ISBLANK(anterior) && anterior <> 0,
        actual - anterior,
        BLANK()
    )
```
</details>

<details><summary><code>Delta_Temp_Media_YoY</code></summary>

```dax
VAR AnioActual   = MAX(Calendario[Año_Hidrologico])
VAR SemanaActual = MAX(Calendario[Semana_Hidrologica])
VAR actual = [Temp_Media]
VAR anterior = 
    CALCULATE(
        [Temp_Media],
        FILTER(
            ALL(Calendario),
            Calendario[Semana_Hidrologica] = SemanaActual &&
            Calendario[Año_Hidrologico]    = AnioActual - 1
        )
    )
RETURN
    IF(NOT ISBLANK(anterior), actual - anterior, BLANK())
```
</details>

<details><summary><code>Delta_Balance_YoY</code></summary>

```dax
VAR AnioActual   = MAX(Calendario[Año_Hidrologico])
VAR SemanaActual = MAX(Calendario[Semana_Hidrologica])
VAR actual = [Balance_Semanal]
VAR anterior = 
    CALCULATE(
        [Balance_Semanal],
        FILTER(
            ALL(Calendario),
            Calendario[Semana_Hidrologica] = SemanaActual &&
            Calendario[Año_Hidrologico]    = AnioActual - 1
        )
    )
RETURN
    IF(NOT ISBLANK(anterior), actual - anterior, BLANK())
```
</details>

<details><summary><code>Amplitud_Termica_Historico</code></summary>

```dax
VAR AnioActual   = MAX(Calendario[Año_Hidrologico])
VAR SemanaActual = MAX(Calendario[Semana_Hidrologica])
RETURN
CALCULATE(
    AVERAGEX(
        VALUES(Calendario[Año_Hidrologico]),
        CALCULATE(AVERAGE(Fact_Diaria_met[Amplitud_Termica]))
    ),
    ALL(Calendario),
    Calendario[Semana_Hidrologica] = SemanaActual,
    Calendario[Año_Hidrologico]    < AnioActual
)
```
</details>

<details><summary><code>ETO_Historico_Promedio</code></summary>

```dax
VAR AnioActual   = MAX(Calendario[Año_Hidrologico])
VAR SemanaActual = MAX(Calendario[Semana_Hidrologica])
RETURN
CALCULATE(
    AVERAGEX(
        VALUES(Calendario[Año_Hidrologico]),
        CALCULATE(AVERAGEX(VALUES(Estaciones_met[estacionid]), CALCULATE(SUM(Fact_Diaria_met[ETO_Total]))))
    ),
    ALL(Calendario),
    Calendario[Semana_Hidrologica] = SemanaActual,
    Calendario[Año_Hidrologico]    < AnioActual
)
```
</details>

<details><summary><code>Balance_Historico_Promedio</code></summary>

```dax
VAR AnioActual   = MAX(Calendario[Año_Hidrologico])
VAR SemanaActual = MAX(Calendario[Semana_Hidrologica])
RETURN
CALCULATE(
    AVERAGEX(
        VALUES(Calendario[Año_Hidrologico]),
        CALCULATE(AVERAGEX(VALUES(Estaciones_met[estacionid]), CALCULATE(SUM(Fact_Diaria_met[Balance_Hidrico]))))
    ),
    ALL(Calendario),
    Calendario[Semana_Hidrologica] = SemanaActual,
    Calendario[Año_Hidrologico]    < AnioActual
)
```
</details>

<details><summary><code>Delta_ETO_YoY</code></summary>

```dax
VAR AnioActual   = MAX(Calendario[Año_Hidrologico])
VAR SemanaActual = MAX(Calendario[Semana_Hidrologica])
VAR actual = [ETO_Semanal]
VAR anterior =
    CALCULATE(
        [ETO_Semanal],
        FILTER(
            ALL(Calendario),
            Calendario[Semana_Hidrologica] = SemanaActual &&
            Calendario[Año_Hidrologico]    = AnioActual - 1
        )
    )
RETURN
    IF(NOT ISBLANK(anterior), actual - anterior, BLANK())
```
</details>

## Precipitación, ETo y balance hídrico

| Medida | Formato | Descripción |
|---|---|---|
| `Precip_Semanal` |  | Lluvia de la semana hidrológica en contexto (mm); suma por estación, promedio entre estaciones. |
| `Precip_Diaria` |  | Lluvia diaria (mm); por estación y promedio entre estaciones. |
| `Precip_Max_Evento` |  | Máximo de 15 min por estación, promediado entre estaciones (consistente con Precip_Diaria: nunca supera el promedio diario) |
| `ETO_Semanal` |  | ETo de la semana (mm); suma por estación, promedio entre estaciones. |
| `ETO_Diaria` |  | ETo diaria (mm); promedio entre estaciones con dato de ETo. |
| `Balance_Semanal` |  | Σ balance diario (P − ETo, días con ambos datos) por estación, promediado entre estaciones |
| `Balance_Diario` |  | Balance hídrico diario P − ETo (mm), solo días con ambos datos; promedio entre estaciones. |
| `Precip_Acumulada_Anual` |  | Lluvia acumulada desde el inicio del año hidrológico (mm). |
| `ETO_Acumulada_Anual` |  | ETo acumulada desde el inicio del año hidrológico (mm). |
| `Balance_Acumulado_Anual` |  | Precipitación acumulada − ETo acumulada del año hidrológico (mm). |
| `Estaciones_Deficit_Critico` | 0 | Número de estaciones con balance semanal < −20 mm. |
| `Estaciones_Superavit` | 0 | Número de estaciones con balance semanal > 0 mm. |
| `Balance_Por_Semana` |  | Balance de las 3 semanas previas a la seleccionada: Σ balance diario por estación, promediado entre estaciones (igual que Balance_Semanal) |
| `ETO_Max_Diurna` |  | ETo máxima de 15 min diurna (mm): extremo. |
| `ETO_Acum_Diurna_Semanal` |  | ETo acumulada diurna (mm); suma por estación, promedio. |
| `ETO_Acum_Nocturna_Semanal` |  | ETo acumulada nocturna (mm); suma por estación, promedio. |

<details><summary><code>Precip_Semanal</code></summary>

```dax
CALCULATE(
    AVERAGEX(VALUES(Estaciones_met[estacionid]), CALCULATE(SUM(Fact_Diaria_met[Precip_Total]))),
    FILTER(
        Calendario,
        Calendario[Semana_Hidrologica] = MAX(Calendario[Semana_Hidrologica]) &&
        Calendario[Año_Hidrologico]    = MAX(Calendario[Año_Hidrologico])
    )
)
```
</details>

<details><summary><code>Precip_Diaria</code></summary>

```dax
AVERAGEX(VALUES(Estaciones_met[estacionid]), CALCULATE(SUM(Fact_Diaria_met[Precip_Total])))
```
</details>

<details><summary><code>Precip_Max_Evento</code></summary>

```dax
// Máximo de 15 min por estación, promediado entre estaciones
// (consistente con Precip_Diaria: nunca supera el promedio diario)
AVERAGEX(
    VALUES(Estaciones_met[estacionid]),
    CALCULATE(MAX(Fact_Subdiaria_met_aux[Precip_Max15min]))
)
```
</details>

<details><summary><code>ETO_Semanal</code></summary>

```dax
ROUND(CALCULATE(
    AVERAGEX(VALUES(Estaciones_met[estacionid]), CALCULATE(SUM(Fact_Diaria_met[ETO_Total]))),
    FILTER(
        Calendario,
        Calendario[Semana_Hidrologica] = MAX(Calendario[Semana_Hidrologica]) &&
        Calendario[Año_Hidrologico]    = MAX(Calendario[Año_Hidrologico])
    )
), 2)
```
</details>

<details><summary><code>ETO_Diaria</code></summary>

```dax
AVERAGEX(VALUES(Estaciones_met[estacionid]), CALCULATE(SUM(Fact_Diaria_met[ETO_Total])))
```
</details>

<details><summary><code>Balance_Semanal</code></summary>

```dax
// Σ balance diario (P − ETo, días con ambos datos) por estación, promediado entre estaciones
ROUND(
    CALCULATE(
        AVERAGEX(
            VALUES(Estaciones_met[estacionid]),
            CALCULATE(SUM(Fact_Diaria_met[Balance_Hidrico]))
        ),
        FILTER(
            Calendario,
            Calendario[Semana_Hidrologica] = MAX(Calendario[Semana_Hidrologica]) &&
            Calendario[Año_Hidrologico]    = MAX(Calendario[Año_Hidrologico])
        )
    ),
    2
)
```
</details>

<details><summary><code>Balance_Diario</code></summary>

```dax
AVERAGEX(VALUES(Estaciones_met[estacionid]), CALCULATE(SUM(Fact_Diaria_met[Balance_Hidrico])))
```
</details>

<details><summary><code>Precip_Acumulada_Anual</code></summary>

```dax
CALCULATE(
    AVERAGEX(VALUES(Estaciones_met[estacionid]), CALCULATE(SUM(Fact_Diaria_met[Precip_Total]))),
    FILTER(
        ALL(Calendario),
        Calendario[Año_Hidrologico]    = MAX(Calendario[Año_Hidrologico]) &&
        Calendario[Semana_Hidrologica] <= MAX(Calendario[Semana_Hidrologica])
    )
)
```
</details>

<details><summary><code>ETO_Acumulada_Anual</code></summary>

```dax
CALCULATE(
    AVERAGEX(VALUES(Estaciones_met[estacionid]), CALCULATE(SUM(Fact_Diaria_met[ETO_Total]))),
    FILTER(
        ALL(Calendario),
        Calendario[Año_Hidrologico]    = MAX(Calendario[Año_Hidrologico]) &&
        Calendario[Semana_Hidrologica] <= MAX(Calendario[Semana_Hidrologica])
    )
)
```
</details>

<details><summary><code>Balance_Acumulado_Anual</code></summary>

```dax
[Precip_Acumulada_Anual] - [ETO_Acumulada_Anual]
```
</details>

<details><summary><code>Estaciones_Deficit_Critico</code></summary>

```dax
CALCULATE(
    DISTINCTCOUNT(Fact_Diaria_met[estacionid]),
    FILTER(
        VALUES(Fact_Diaria_met[estacionid]),
        CALCULATE(SUM(Fact_Diaria_met[Balance_Hidrico])) < -20
    )
)
```
</details>

<details><summary><code>Estaciones_Superavit</code></summary>

```dax
CALCULATE(
    DISTINCTCOUNT(Fact_Diaria_met[estacionid]),
    FILTER(
        VALUES(Fact_Diaria_met[estacionid]),
        CALCULATE(SUM(Fact_Diaria_met[Balance_Hidrico])) > 0
    )
)
```
</details>

<details><summary><code>Balance_Por_Semana</code></summary>

```dax
// Balance de las 3 semanas previas a la seleccionada:
// Σ balance diario por estación, promediado entre estaciones (igual que Balance_Semanal)
VAR SemanaActual = CALCULATE(MAX(Calendario[Semana_Hidrologica]), ALLSELECTED(Calendario))
VAR AnioActual   = CALCULATE(MAX(Calendario[Año_Hidrologico]),    ALLSELECTED(Calendario))
VAR SemanaEje    = MAX(Semanas_Grafica[Semana_Hidrologica])
VAR AnioEje      = MAX(Semanas_Grafica[Año_Hidrologico])
RETURN
IF(
    AnioEje = AnioActual &&
    SemanaEje >= SemanaActual - 3 &&
    SemanaEje <= SemanaActual - 1,
    CALCULATE(
        AVERAGEX(
            VALUES(Estaciones_met[estacionid]),
            CALCULATE(SUM(Fact_Diaria_met[Balance_Hidrico]))
        ),
        ALL(Calendario),
        TREATAS({SemanaEje}, Calendario[Semana_Hidrologica]),
        TREATAS({AnioEje},   Calendario[Año_Hidrologico])
    )
)
```
</details>

<details><summary><code>ETO_Max_Diurna</code></summary>

```dax
MAX(Fact_Subdiaria_met_aux[ETO_Max_Diurna])
```
</details>

<details><summary><code>ETO_Acum_Diurna_Semanal</code></summary>

```dax
AVERAGEX(VALUES(Estaciones_met[estacionid]), CALCULATE(SUM(Fact_Subdiaria_met_aux[ETO_Acum_Diurna])))
```
</details>

<details><summary><code>ETO_Acum_Nocturna_Semanal</code></summary>

```dax
AVERAGEX(VALUES(Estaciones_met[estacionid]), CALCULATE(SUM(Fact_Subdiaria_met_aux[ETO_Acum_Nocturna])))
```
</details>

## Temperatura y sensación térmica

| Medida | Formato | Descripción |
|---|---|---|
| `Temp_Max` |  | Temperatura máxima (°C): extremo de las estaciones seleccionadas. |
| `Temp_Min` |  | Temperatura mínima (°C): extremo de las estaciones seleccionadas. |
| `Temp_Media` |  | Temperatura media diaria promedio (°C). |
| `Amplitud_Termica` |  | Temp_Max − Temp_Min (°C). |
| `IC_Max` |  | Índice de calor máximo diurno (°C): extremo. |
| `IC_Media` |  | Índice de calor medio diurno (°C). |
| `IC_Media_Diurno` |  | Índice de calor medio diurno (°C). |
| `IC_Max_Diurno` |  | Índice de calor máximo diurno (°C): extremo. |
| `Temp_Nocturna_Media` |  | Temperatura media nocturna (19–05 h) (°C). |
| `Hora_Temp_Max_Diurna` |  | Hora promedio de temp max diurna. |
| `Hora_IC_Max_Diurno` |  | Hora promedio de ic max diurno. |
| `Hora_Temp_Min_Nocturna` |  | Hora promedio de temp min nocturna. |
| `Temp_Min_Nocturna` |  | Temperatura mínima nocturna (°C): extremo. |

<details><summary><code>Temp_Max</code></summary>

```dax
MAX(Fact_Diaria_met[Temp_Max])
```
</details>

<details><summary><code>Temp_Min</code></summary>

```dax
MIN(Fact_Diaria_met[Temp_Min])
```
</details>

<details><summary><code>Temp_Media</code></summary>

```dax
AVERAGE(Fact_Diaria_met[Temp_Media])
```
</details>

<details><summary><code>Amplitud_Termica</code></summary>

```dax
[Temp_Max] - [Temp_Min]
```
</details>

<details><summary><code>IC_Max</code></summary>

```dax
MAX(Fact_Subdiaria_met_aux[IC_Max_Diurno])
```
</details>

<details><summary><code>IC_Media</code></summary>

```dax
AVERAGE(Fact_Subdiaria_met_aux[IC_Media_Diurno])
```
</details>

<details><summary><code>IC_Media_Diurno</code></summary>

```dax
AVERAGE(Fact_Subdiaria_met_aux[IC_Media_Diurno])
```
</details>

<details><summary><code>IC_Max_Diurno</code></summary>

```dax
MAX(Fact_Subdiaria_met_aux[IC_Max_Diurno])
```
</details>

<details><summary><code>Temp_Nocturna_Media</code></summary>

```dax
AVERAGE(Fact_Subdiaria_met_aux[Temp_Nocturna_Media])
```
</details>

<details><summary><code>Hora_Temp_Max_Diurna</code></summary>

```dax
AVERAGE(Fact_Subdiaria_met_aux[Hora_Temp_Max_Diurna])
```
</details>

<details><summary><code>Hora_IC_Max_Diurno</code></summary>

```dax
AVERAGE(Fact_Subdiaria_met_aux[Hora_IC_Max_Diurno])
```
</details>

<details><summary><code>Hora_Temp_Min_Nocturna</code></summary>

```dax
AVERAGE(Fact_Subdiaria_met_aux[Hora_Temp_Min_Nocturna])
```
</details>

<details><summary><code>Temp_Min_Nocturna</code></summary>

```dax
MIN(Fact_Subdiaria_met_aux[Temp_Min_Nocturna])
```
</details>

## Humedad, VPD, mojadura y estrés

| Medida | Formato | Descripción |
|---|---|---|
| `HR_Media` |  | Humedad relativa media (%). |
| `HR_Min` |  | Humedad relativa mínima (%): extremo. |
| `VPD_Media_Diurna` |  | Déficit de presión de vapor medio diurno (kPa). |
| `VPD_Max_Diurna` |  | VPD máximo diurno (kPa): extremo. |
| `Mojadura_Horas_Semanal` |  | Horas de mojadura diurna (sensor > 4); suma por estación, promedio entre estaciones. |
| `Horas_Estres_Termico_Semanal` |  | Horas con T > 35 °C y radiación > 800 W/m²; suma por estación, promedio entre estaciones. |
| `VPD_Media_Nocturna` |  | VPD medio nocturno (kPa). |
| `Mojadura_Horas_Nocturna_Semanal` |  | Horas de mojadura nocturna; suma por estación, promedio entre estaciones. |
| `Mojadura_Horas_Total_Semanal` |  | Horas de mojadura total; suma por estación, promedio entre estaciones. |
| `HR_Max` |  | Humedad relativa máxima (%): extremo. |
| `Hora_VPD_Max_Diurna` |  | Hora promedio de vpd max diurna. |
| `Hora_ETO_Max_Diurna` |  | Hora promedio de eto max diurna. |
| `Hora_Inicio_Mojadura` |  | Hora promedio de inicio mojadura. |
| `Hora_Fin_Mojadura` |  | Hora promedio de fin mojadura. |
| `VPD_Min_Nocturno` |  | VPD mínimo nocturno (kPa): extremo. |
| `Duracion_Mojadura` |  | Hora fin − hora inicio de mojadura (h), promedio. |

<details><summary><code>HR_Media</code></summary>

```dax
AVERAGE(Fact_Diaria_met[HR_Media])
```
</details>

<details><summary><code>HR_Min</code></summary>

```dax
MIN(Fact_Diaria_met[HR_Min])
```
</details>

<details><summary><code>VPD_Media_Diurna</code></summary>

```dax
AVERAGE(Fact_Subdiaria_met_aux[VPD_Media_Diurna])
```
</details>

<details><summary><code>VPD_Max_Diurna</code></summary>

```dax
MAX(Fact_Subdiaria_met_aux[VPD_Max_Diurna])
```
</details>

<details><summary><code>Mojadura_Horas_Semanal</code></summary>

```dax
AVERAGEX(VALUES(Estaciones_met[estacionid]), CALCULATE(SUM(Fact_Subdiaria_met_aux[Mojadura_Horas_Diurna])))
```
</details>

<details><summary><code>Horas_Estres_Termico_Semanal</code></summary>

```dax
AVERAGEX(VALUES(Estaciones_met[estacionid]), CALCULATE(SUM(Fact_Subdiaria_met_aux[Horas_Estres_Termico])))
```
</details>

<details><summary><code>VPD_Media_Nocturna</code></summary>

```dax
AVERAGE(Fact_Subdiaria_met_aux[VPD_Media_Nocturna])
```
</details>

<details><summary><code>Mojadura_Horas_Nocturna_Semanal</code></summary>

```dax
AVERAGEX(VALUES(Estaciones_met[estacionid]), CALCULATE(SUM(Fact_Subdiaria_met_aux[Mojadura_Horas_Nocturna])))
```
</details>

<details><summary><code>Mojadura_Horas_Total_Semanal</code></summary>

```dax
AVERAGEX(VALUES(Estaciones_met[estacionid]), CALCULATE(SUM(Fact_Subdiaria_met_aux[Mojadura_Horas_Total])))
```
</details>

<details><summary><code>HR_Max</code></summary>

```dax
MAX(Fact_Diaria_met[HR_Max])
```
</details>

<details><summary><code>Hora_VPD_Max_Diurna</code></summary>

```dax
AVERAGE(Fact_Subdiaria_met_aux[Hora_VPD_Max_Diurna])
```
</details>

<details><summary><code>Hora_ETO_Max_Diurna</code></summary>

```dax
AVERAGE(Fact_Subdiaria_met_aux[Hora_ETO_Max_Diurna])
```
</details>

<details><summary><code>Hora_Inicio_Mojadura</code></summary>

```dax
AVERAGE(Fact_Subdiaria_met_aux[Hora_Inicio_Mojadura])
```
</details>

<details><summary><code>Hora_Fin_Mojadura</code></summary>

```dax
AVERAGE(Fact_Subdiaria_met_aux[Hora_Fin_Mojadura])
```
</details>

<details><summary><code>VPD_Min_Nocturno</code></summary>

```dax
MIN(Fact_Subdiaria_met_aux[VPD_Min_Nocturno])
```
</details>

<details><summary><code>Duracion_Mojadura</code></summary>

```dax
IF(
    NOT ISBLANK([Hora_Fin_Mojadura]) && NOT ISBLANK([Hora_Inicio_Mojadura]),
    [Hora_Fin_Mojadura] - [Hora_Inicio_Mojadura],
    BLANK()
)
```
</details>

## Auxiliares, calidad de datos y validación

| Medida | Formato | Descripción |
|---|---|---|
| `_Semana_Hidro_Actual` | 0 | Semana hidrológica en contexto (máx.). |
| `_Anio_Hidro_Actual` | 0 | Año hidrológico en contexto (máx.). |
| `_Conteo_Filas_Diarias` | 0 | Validación: filas en Fact_Diaria_met. |
| `_Conteo_Estaciones_Met` | 0 | Validación: estaciones con datos diarios. |
| `N_Lecturas_Promedio` |  | Calidad: lecturas de 15 min promedio por día-estación (96 = completo). |
| `Dia_Completo_Pct` |  | Calidad: % de días-estación con ≥ 80 lecturas. |

<details><summary><code>_Semana_Hidro_Actual</code></summary>

```dax
MAX(Calendario[Semana_Hidrologica])
```
</details>

<details><summary><code>_Anio_Hidro_Actual</code></summary>

```dax
MAX(Calendario[Año_Hidrologico])
```
</details>

<details><summary><code>_Conteo_Filas_Diarias</code></summary>

```dax
COUNTROWS(Fact_Diaria_met)
```
</details>

<details><summary><code>_Conteo_Estaciones_Met</code></summary>

```dax
DISTINCTCOUNT(Fact_Diaria_met[estacionid])
```
</details>

<details><summary><code>N_Lecturas_Promedio</code></summary>

```dax
AVERAGE(Fact_Subdiaria_met_aux[N_Lecturas])
```
</details>

<details><summary><code>Dia_Completo_Pct</code></summary>

```dax
DIVIDE(
    CALCULATE(
        COUNTROWS(Fact_Subdiaria_met_aux),
        Fact_Subdiaria_met_aux[Dia_Completo] = TRUE()
    ),
    COUNTROWS(Fact_Subdiaria_met_aux),
    0
) * 100
```
</details>
