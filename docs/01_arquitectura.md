# Arquitectura del modelo

## Flujo de datos

```mermaid
flowchart LR
    subgraph API["API REDMET (redmet.icc.org.gt)"]
        A1["/ws/redmet/estaciones<br/>metadatos"]
        A2["/ws/redmet/estaciones/lecturas<br/>lecturas de 15 min"]
        A3["/ws/getlecturasdia<br/>resumen diario"]
    end
    subgraph PQ["Power Query (M)"]
        L["TablaEstaciones_met<br/>(lista de IDs)"]
        F1["fxLecturasEstacion_met"]
        F2["fxLecturasEstacion_met_diario"]
    end
    subgraph M["Modelo (estrella)"]
        E["Estaciones_met"]
        C["Calendario<br/>(año hidrológico)"]
        D["Fact_Diaria_met<br/>18 años"]
        S["Fact_Subdiaria_met_aux<br/>5 años"]
        H["Fact_Horaria_riesgo<br/>5 años"]
    end
    A1 --> E
    L --> F1 & F2
    A2 --> F1 --> S & H
    A2 -.-> R["Fact_Meteorologia<br/>(consulta sin carga)"]
    A3 --> F2 --> D
    E -.-> D & S & H
    C -.-> D & S & H
    D & S & H --> REP["Reporte<br/>Agua y energía · Estrés · Horario · Riesgos del cultivo"]
```

Cada tabla de hechos llama a la API **por estación** (una llamada por cada ID de `TablaEstaciones_met`) y filtra por `RangeStart`/`RangeEnd`. Esto permite la **actualización incremental**: en el servicio solo se vuelven a descargar los últimos 7 días.

## Tablas de hechos

| Tabla | Grano | Fuente | Historia | Uso |
|---|---|---|---|---|
| `Fact_Diaria_met` | estación × día | endpoint diario | 18 años | Lluvia, ETo, balance, temperaturas, HR, viento medio, radiación diaria (MJ), GDD por cultivo. Base de **históricos y acumulados**. |
| `Fact_Subdiaria_met_aux` | estación × día | agregación de lecturas de 15 min | 5 años | Variables diurnas/nocturnas: VPD, mojadura, índice de calor, viento diurno/nocturno, horas de extremos, periodo de luz y energía, calidad de datos (`N_Lecturas`, `Dia_Completo`). |
| `Fact_Horaria_riesgo` | estación × día × hora | agregación de lecturas de 15 min | 5 años | Condiciones horarias de riesgos y variables del mapa de calor (T, HR, mojadura, lluvia, viento, radiación, índice de calor) y viento horario vectorial (rosa de vientos). |

`Fact_Meteorologia` (lecturas crudas de 15 min) queda como consulta de Power Query **sin carga** al modelo desde 2026-11-24: ningún visual la usaba y era la tabla más pesada. Se reactiva con *Habilitar carga*; copia de su definición en `_respaldo/fact_meteorologia_2026-11-24/`.

## Dimensiones y tablas auxiliares

| Tabla | Rol |
|---|---|
| `Estaciones_met` | Estaciones de `TablaEstaciones_met` (finca, coordenadas, altitud, estrato altitudinal, país). Filtra a las tres tablas de hechos. |
| `Calendario` | Tabla de fechas marcada (2008 → hoy, hora de Guatemala). Año y semana **hidrológicos** con la jerarquía `Jerarquía hidrológica` (Año hidrológico → Semana → Fecha); selectores automáticos `Año_Selector` y `Semana_Selector`; `Semana_Eje` (número de semana para ejes). |
| `TablaEstaciones_met` | Lista fija de IDs de estaciones que se descargan. **Aquí se agregan o quitan estaciones.** |
| `Semanas_Grafica`, `Semanas_Anio` | Ejes desconectados para gráficas por semana (balances anteriores, radiación y grados día) que no deben filtrarse por el segmentador de semana. |
| `Horas_Dia`, `Periodos_Dia` | Eje de horas del mapa de calor y períodos del día de la rosa de vientos. |
| `Cultivos`, `Riesgos_Cultivo` | Cultivos (base y tope de grados día) y catálogo de riesgos con umbrales, generados desde `config/riesgos_cultivo.csv`. |
| `Vistas_Mapa_Calor`, `Leyenda_Mapa_Calor`, `Leyenda_Mapa_Riesgo` | Vistas, rangos y colores del mapa de calor y del mapa de riesgos. |
| `Resumen_Variables`, `Ventana_Semanas`, `Series_DiaNoche`, `Periodo_Vista`, `Eje_Secundario` | Tablas desconectadas para la tabla *Resumen de la semana*, la ventana de radiación y grados día y los botones día/noche. |
| `Direcciones_Viento` | 8 sectores de 45° (N … NO), relacionados con `Fact_Horaria_riesgo[Sector_Viento]`. |
| `_Medidas`, `_Riesgos` | Medidas DAX: generales y del motor de riesgos, mapas y gráficas (esta última generada por `tools/generar_riesgos_modelo.py`). |

## Calendario hidrológico

- El año hidrológico inicia el **lunes de la semana que contiene la fecha** `InicioAnioHidrologico` (mes/día; actualmente 2 de noviembre).
- Una semana pertenece al año hidrológico **siguiente** si su lunes es igual o posterior a ese lunes. Ejemplo: la semana del 27-oct-2025 es la semana 1 del año hidrológico **2026**.
- `Semana_Etiqueta` = `"03 | 2025-2026 (10-nov - 16-nov)"`, ordenada cronológicamente por `Inicio_Semana`.
- `Semana_Selector` llama «Última semana completa» a la semana anterior a la actual y «Semana en curso» a la actual; `Año_Selector` llama «Año hidrológico actual» al año de la última semana completa. Los segmentadores guardan esas etiquetas y avanzan solos en cada actualización.

## Definiciones físicas

| Concepto | Definición en el modelo |
|---|---|
| Diurno / nocturno (temperatura, VPD, viento, mojadura, ETo, horas de extremos) | Ventana **fija**: diurno 06:00–18:59, nocturno 19:00–05:59. |
| Periodo de luz (radiación) | De la **primera a la última lectura con radiación > 40 W/m²** del día. Las lecturas faltantes no lo acortan. |
| Irradiancia media de luz (`Rad_Media_Luz`) | Promedio de las lecturas disponibles dentro del periodo de luz (incluye nubosidad). |
| Energía diurna (`Energia_Luz_MJ`) | `Rad_Media_Luz × duración de luz × 3600 / 10⁶` (MJ/m²). |
| Radiación diaria (`Rad_MJ`, Fact_Diaria) | Suma de lecturas de 15 min en W/m² (dato de la API) × 900 s / 10⁶. |
| VPD | `(1 − HR/100) × 0.6108 · exp(17.27·T/(T+237.3))` (kPa), por lectura de 15 min. |
| Mojadura | Lectura de 15 min con sensor > 4 cuenta 0.25 h. |
| Estrés térmico | Lectura con T > 35 °C y radiación > 800 W/m² cuenta 0.25 h. |
| Día seco | Lluvia diaria < 1 mm. |
| Balance hídrico | P − ETo por día; vacío si falta la ETo (no se rellena con 0). |
| Dirección del viento | Promedios **vectoriales** (ponderados por velocidad); nunca promedio aritmético de grados. |
| Calma | Velocidad horaria < 1.8 km/h (≈ 0.5 m/s). |
| GDD con tope (`GDD_*_ST`) | `min(max(Tmed − Tbase, 0), Tópt − Tbase)`: caña 10/34, banano 15/28, aguacate 10/24, palma 15/30, maíz 10/30 °C. |
| Día completo | ≥ 80 de 96 lecturas de 15 min. |

Unidades: viento en **km/h**, lluvia y ETo en mm, radiación en W/m² (irradiancia) o MJ/m² (energía), VPD en kPa.

## Control de calidad

En Power Query, antes del filtro incremental, las lecturas fuera de rango se convierten en faltantes (rangos de `aplicar_qc` de los scripts R):

| Variable (15 min) | Faltante si |
|---|---|
| Precipitación | < 0 o > 90 mm |
| Temperatura | < −5 o > 50 °C |
| Humedad relativa | < 20 o > 100 % |
| Radiación | < 0 o > 1500 W/m² |
| Velocidad del viento | < 0 o > 270 km/h |
| Mojadura | < 0 o > 10 |
| ETo | < 0 o > 90 |
| Dirección del viento | 360 → 0; fuera de 0–360, faltante |

En `Fact_Diaria_met` se aplican los mismos límites a temperaturas y HR, y se descartan los valores negativos de lluvia, ETo y radiación.

## Reglas de agregación entre estaciones

Cuando el filtro abarca varias estaciones (selección en el mapa, estrato altitudinal):

| Tipo de medida | Regla | Ejemplos |
|---|---|---|
| **Sumas** | Se suma **por estación** en el período y luego se **promedian las estaciones**. | Lluvia, ETo, balance, horas de mojadura/luz/estrés, GDD, radiación acumulada |
| **Conteos de días de riesgo** | Días por estación, promediados entre las estaciones **con datos**. Las condiciones (incl. mojadura) se evalúan dentro de la misma estación. | `Dias_Riesgo_*` |
| **Promedios** | Promedio de todos los días-estación. | Temperatura media, HR media, VPD medio |
| **Máximos y mínimos** | **Extremo** de las estaciones seleccionadas (peor caso). | Temp. máx./mín., viento máx., VPD máx., índice de calor máx. |
| **Máximo de lluvia en 15 min** | Máximo por estación, promediado (nunca supera la lluvia diaria promedio). | `Precip_Max_Evento` |

Cada variable se promedia sobre las estaciones que **la miden**. Por eso `Precip_Semanal − ETO_Semanal` puede diferir ligeramente de `Balance_Semanal` (este solo usa días con ambos datos).

## Históricos

La desviación acumulada de radiación y grados día compara con la media de **los mismos días** de hasta 18 años anteriores (`DATEADD`). Las medidas `*_Historico_*` comparan la **misma semana hidrológica** en los años **anteriores al año seleccionado**. En el servicio usan toda la historia de `Fact_Diaria_met` (desde 2008); en Desktop solo lo que cargue `RangeStart`.
