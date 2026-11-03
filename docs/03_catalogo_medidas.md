# Catálogo de medidas DAX

> Generado automáticamente por `tools/generar_docs_modelo.py` el 2026-11-03 (209 medidas). No editar a mano.

Convenciones: las medidas con prefijo `_` son auxiliares; `Semaforo_*` devuelve 1 = rojo, 2 = amarillo, 3 = verde. Las medidas de suma (lluvia, ETo, balance, horas, GDD, radiación acumulada) **suman por estación y promedian entre estaciones**; los máximos y mínimos devuelven **el extremo** de las estaciones seleccionadas. Ver `04_guia_usuario.md` y `06_decisiones_y_cambios.md`.

## Índice

- [Motor de riesgos por cultivo (generado desde config/riesgos_cultivo.csv)](#motor-de-riesgos-por-cultivo-generado-desde-configriesgos_cultivocsv) (60)
- [Viento](#viento) (19)
- [Radiación y luz](#radiación-y-luz) (16)
- [Semáforos](#semáforos) (16)
- [Días y condiciones de riesgo (plagas, enfermedades, clima)](#días-y-condiciones-de-riesgo-plagas-enfermedades-clima) (16)
- [Grados día / suma térmica (GDD)](#grados-día--suma-térmica-gdd) (17)
- [Históricos y comparaciones interanuales](#históricos-y-comparaciones-interanuales) (14)
- [Precipitación, ETo y balance hídrico](#precipitación-eto-y-balance-hídrico) (16)
- [Temperatura y sensación térmica](#temperatura-y-sensación-térmica) (13)
- [Humedad, VPD, mojadura y estrés](#humedad-vpd-mojadura-y-estrés) (16)
- [Auxiliares, calidad de datos y validación](#auxiliares-calidad-de-datos-y-validación) (6)

## Motor de riesgos por cultivo (generado desde config/riesgos_cultivo.csv)

| Medida | Formato | Descripción |
|---|---|---|
| `R_CAN_ROYA_CAFE` | 0.# | Roya café (Caña de azúcar). Unidad: días/semana. Las esporas requieren una película de agua ≥ 6 h para germinar; temperatura óptima de germinación 21 °C. Día favorable: Tmed 15–25 °C, HR media > 80 % y ≥ 6 h de mojadura. Hora favorable: T 15–25 °C, HR > 80 %, mojadura > 4. |
| `R_CAN_ROYA_NARANJA` | 0.# | Roya naranja (Caña de azúcar). Unidad: días/semana. Día favorable: Tmed 20–25 °C (cualquier mojadura) o Tmed > 25 °C con mojadura > 8 h. Desfavorable: Tmed < 20 °C, o > 25 °C con mojadura < 8 h. Germinación óptima con HR > 98 % y 21 °C. Esporula hasta la madurez y aun en época seca. |
| `R_CAN_ESCALDADURA` | 0.# | Escaldadura foliar (Caña de azúcar). Unidad: días/semana. Importante en Guatemala: la alternancia de periodos lluviosos severos y secos severos favorece su expresión; se dispersa con la combinación de lluvia y viento fuertes. Día de dispersión: lluvia > 20 mm y viento máx > 30 km/h. |
| `R_CAN_SALIVOSA` | 0.# | Salivosa (Aeneolamia) (Caña de azúcar). Unidad: días/semana. Aparece en abril con las primeras lluvias: 50–100 mm de lluvia inicial acumulan humedad suficiente para la eclosión de la mayoría de los huevos. La población se relaciona con la lluvia de 4 semanas antes; presenta 3–4 picos en la época lluviosa y desaparece en noviembre por el fotoperiodo, aunque siga lloviendo. Día favorable: lluvia > 5 |
| `R_CAN_BARRENADOR` | 0.# | Barrenador (Diatraea) (Caña de azúcar). Unidad: días/semana. La infestación aumenta con el establecimiento de la época seca y en la maduración. Día favorable: Tmed > 24 °C, HR media 60–80 %, día seco. 4–5 generaciones/año en El Salvador (oct–jun). Hora favorable (aproximación para el mapa de calor): T > 24 °C, HR 60–80 % y sin lluvia. |
| `R_CAN_CHINCHE_ENCAJE` | 0.# | Chinche de encaje (Caña de azúcar). Unidad: días secos/semana. Plaga en aumento en la zona cañera. Las lluvias intensas de julio a septiembre la reducen (derriban las colonias de ninfas); el estrés por exceso de humedad o por sequía la favorece. Semana favorable: sin días con lluvia > 20 mm y ≥ 4 días secos. |
| `R_CAN_COLUDO` | 0.# | Coludo (saltahojas antillano) (Caña de azúcar). Unidad: días/semana. Plaga exótica favorecida por la época seca (noviembre–abril, incluida la transición): baja precipitación, alta evapotranspiración y baja humedad relativa. Día favorable: día seco y HR media < 70 %. |
| `R_CAN_ESTRES` | 0.# | Estrés térmico (Caña de azúcar). Unidad: horas/semana. Hora con T > 36 °C (umbral máximo de estrés para caña de azúcar; rango óptimo 20–33 °C) y radiación > 800 W/m². |
| `R_CAN_SUELO_SATURADO` | 0.# | Suelo saturado: limitación de cosecha y tránsito (Caña de azúcar). Unidad: días/semana. Día con lluvia > 10 mm durante la zafra: anegamiento del suelo que limita el corte, el alce y el tránsito de maquinaria. |
| `R_CAN_APLICACION` | 0.# | Ventana para aplicación aérea (Caña de azúcar). Unidad: horas aptas/día. Hora apta para aplicar (madurantes y otros productos): T < 30 °C, HR > 60 % y viento < 10 km/h, de día. Evitar la inversión térmica (diciembre–febrero, noches despejadas y sin viento). Indicador positivo: horas aptas por día. |
| `R_CAN_QUEMA` | 0.# | Riesgo de quema / incendio (Caña de azúcar). Unidad: días/semana. Día con HR mínima < 40 %, viento máximo > 20 km/h y ≥ 3 días secos consecutivos. |
| `R_CAN_MADURACION` | 0.# | Condiciones de maduración (Caña de azúcar). Unidad: días/semana. Condiciones favorables a la acumulación de sacarosa, de 4 a 6 semanas antes del corte: oscilación térmica día-noche ≈ 15 °C, lluvia de 30–100 mm/mes y 11.5–12.5 h de luz. El exceso de humedad en suelo y planta (inicio de zafra) la frena. Día favorable: amplitud térmica ≥ 15 °C; mes favorable: lluvia 30–100 mm. Semáforo invertido. |
| `R_BAN_SIG_NEGRA` | 0.# | Sigatoka negra (Banano). Unidad: días/semana. Óptimo 26–28 °C; la infección cae bajo ~20 °C (requiere ~21.5–28 °C). HR > 80 % favorable y > 90 % fuertemente asociada; lluvia frecuente y mojadura persistente. Radiación alta la reduce. Día favorable: Tmed 21.5–28 °C, HR media > 90 % y > 4 h de mojadura nocturna. Índice acumulado: días favorables en 14 días. |
| `R_BAN_MOKO` | 0.# | Moko (dispersión) (Banano). Unidad: semana. Semana con lluvia > 100 mm y balance positivo (dispersión por agua). |
| `R_BAN_VOLCAMIENTO` | 0.# | Volcamiento por viento (Banano). Unidad: km/h. Viento máximo diurno > 40 km/h (precaución) / > 60 km/h (alerta). |
| `R_BAN_ESTRES` | 0.# | Estrés térmico (Banano). Unidad: horas/semana. Hora con T > 38 °C (umbral máximo de estrés para banano; rango óptimo 20–30 °C) y radiación > 800 W/m². |
| `R_AGU_PHYTO` | 0.# | Phytophthora (pudrición de raíz) (Aguacate). Unidad: días/semana. Humedad alta, temperaturas altas y exceso de agua (mal drenaje). Día favorable: Tmed 20–30 °C y balance diario > 0. |
| `R_AGU_ANTRACNOSIS` | 0.# | Antracnosis (Aguacate). Unidad: días/semana. Favorecida por temperaturas altas y humedad; la lluvia la dispersa. Día favorable: Tmed 20–30 °C, HR media > 80 % y lluvia > 1 mm o > 6 h de mojadura. |
| `R_AGU_FRIO` | 0.# | Frío (Aguacate). Unidad: días/semana. Tmín < 12 °C (umbral mínimo de estrés para aguacate). |
| `R_AGU_CALOR` | 0.# | Golpe de calor / quemadura de fruto (Aguacate). Unidad: horas/semana. Hora con T > 36 °C (umbral máximo de estrés para aguacate; rango óptimo 15–30 °C) y radiación > 800 W/m². |
| `R_AGU_VIENTO` | 0.# | Caída de flor y fruto por viento (Aguacate). Unidad: km/h. Vientos fuertes causan caída de flor y fruto. Viento máximo diurno > 30 / 45 km/h. |
| `R_PAL_PC` | 0.# | Pudrición del cogollo (P. palmivora) (Palma de aceite). Unidad: días/semana. Severidad mayor con HR alta, lluvias frecuentes y encharcamiento; los periodos secos la reducen; el patógeno tolera 11–35 °C. Día favorable: lluvia > 5 mm y HR media > 90 %. Índice: días favorables en 14 días. Hora favorable (aproximación para el mapa de calor): T 11–35 °C, HR > 90 % y lluvia > 0. |
| `R_PAL_ESTRES` | 0.# | Estrés térmico (Palma de aceite). Unidad: horas/semana. Hora con T > 34 °C (umbral máximo de estrés para palma de aceite; rango óptimo 22–32 °C) y radiación > 800 W/m². |
| `R_MAI_ASFALTO` | 0.# | Maíz – Mancha de asfalto (Granos básicos). Unidad: días/semana. Favorecida por temperaturas frescas (16–22 °C) y HR alta: HR media > 75 % y 7 h de mojadura nocturna. Aparece unas 2 semanas antes de la floración y alcanza su máximo ~6 semanas después. Presente en el altiplano de Guatemala. |
| `R_MAI_ROYA` | 0.# | Maíz – Roya común (Granos básicos). Unidad: días/semana. Noches de 18–21 °C, temperatura diurna moderada, HR alta y ≥ 6 h de mojadura. |
| `R_MAI_TIZON` | 0.# | Maíz – Tizón foliar (Exserohilum) (Granos básicos). Unidad: días/semana. 18–28 °C con mojadura prolongada (lluvia o rocío). |
| `R_MAI_MANCHA_GRIS` | 0.# | Maíz – Mancha gris (Cercospora) (Granos básicos). Unidad: días/semana. Cálido (~27–32 °C) con HR > 90 % durante > 12 h. |
| `R_MAI_COGOLLERO` | 0.# | Maíz – Gusano cogollero (generaciones) (Granos básicos). Unidad: días/semana (severidad). Generaciones por grados día: temperatura base 10.9 °C y 559 grados día por generación (indicador acumulado). Severidad: daño mayor con T > 30 °C y poca lluvia; día favorable: Tmáx > 30 °C y día seco. |
| `R_MAI_CALOR_FLOR` | 0.# | Maíz – Estrés térmico en floración (Granos básicos). Unidad: días/semana. Tmáx > 38 °C (umbral máximo de estrés para maíz; rango óptimo 10–35 °C). |
| `R_FRI_MUSTIA` | 0.# | Frijol – Mustia hilachosa (Granos básicos). Unidad: días/semana. 25–32 °C con lluvia frecuente (salpique). Día favorable: Tmed 25–32 °C y lluvia > 5 mm. |
| `R_FRI_ROYA` | 0.# | Frijol – Roya (Granos básicos). Unidad: días/semana. 17–27 °C con lluvia frecuente o noches frescas con rocío prolongado (prefloración y floración). Día favorable: Tmed 17–27 °C y (lluvia > 1 mm o > 8 h de mojadura nocturna). |
| `R_FRI_ANTRACNOSIS` | 0.# | Frijol – Antracnosis (Granos básicos). Unidad: días/semana. HR alta (~92 %), lluvias frecuentes y 13–26 °C (óptimo 17 °C); zonas > 1000 msnm. |
| `R_FRI_MANCHA_ANGULAR` | 0.# | Frijol – Mancha angular (Granos básicos). Unidad: días/semana. 18–28 °C con alternancia de periodos lluviosos y días secos. Semana favorable: ≥ 2 días con lluvia y ≥ 2 días secos con Tmed 18–28 °C. |
| `R_FRI_BACTERIOSIS` | 0.# | Frijol – Bacteriosis común (Granos básicos). Unidad: días/semana. 20–32 °C con lluvia frecuente (salpique); zonas < 1200 msnm. |
| `R_FRI_MOSAICO` | 0.# | Frijol – Mosaico dorado (mosca blanca) (Granos básicos). Unidad: días/semana. 25–30 °C, zonas < 1200 msnm; poblaciones de mosca blanca aumentan en periodos secos. Día favorable: Tmed 25–30 °C y día seco. |
| `R_FRI_CALOR_FLOR` | 0.# | Frijol – Estrés por calor en floración (Granos básicos). Unidad: días/semana. Tmáx > 34 °C (umbral máximo de estrés para frijol; rango óptimo 15–27 °C). Noches > 20 °C también reducen el cuajado. |
| `R_GRA_SEQUIA` | 0.# | Sequía (Granos básicos). Unidad: días/semana. Días secos (lluvia < 1 mm). |
| `R_CAN_FLORACION` | 0.# | Condiciones de inducción floral (Caña de azúcar). Unidad: días en la ventana (16 días). Ventana de inducción en Guatemala: segunda quincena de agosto (fotoperiodo de 12 h 30 min hacia el 23–25 ago). Noche inductiva: Tmín 21–24 °C, con Tmáx ≤ 32 °C y suelo húmedo (sin déficit). Tmín < 18 °C reduce la floración; Tmáx > 32 °C la inhibe; más horas de brillo solar en agosto la reducen. |
| `R_CAN_ACAME` | 0.# | Acame (volcamiento) (Caña de azúcar). Unidad: días/semana. Viento máximo fuerte combinado con lluvia (suelo húmedo y tallos pesados). Día con viento máx > 40 km/h y lluvia > 10 mm. |
| `R_AGU_ACAROS` | 0.# | Ácaros (arañita) (Aguacate). Unidad: días/semana. Más comunes en época seca y favorecidos por el viento. Día favorable: día seco, HR media < 65 % y viento máx > 20 km/h. |
| `R_MAI_ACHAPARRAMIENTO` | 0.# | Maíz – Chicharrita y achaparramiento (Granos básicos). Unidad: días/semana. El vector (Dalbulus maidis) se favorece con escasez de lluvia, altas temperaturas y baja humedad relativa; mayor incidencia cuando la siembra coincide con lluvias irregulares. Día favorable: día seco, Tmed > 26 °C y HR media < 70 %. |
| `R_MAI_PUDRICION_MAZORCA` | 0.# | Maíz – Pudrición de mazorca (Granos básicos). Unidad: días con lluvia/semana. Los años más lluviosos producen epifitias (Stenocarpella y Fusarium). Semana favorable: ≥ 4 días con lluvia > 1 mm. |
| `Riesgo_Valor` | 0.# | Valor del riesgo seleccionado (días, horas o km/h según la unidad), promediado entre estaciones. |
| `Riesgo_Semaforo` | 0 | 1 = alerta, 2 = precaución, 3 = normal. En indicadores favorables (invertidos) menos valor es peor. |
| `Riesgo_Color` |  | Color hexadecimal del semáforo para formato condicional. |
| `Riesgo_Etiqueta` |  | Valor con su unidad para tarjetas. |
| `Riesgos_En_Alerta` | 0 | Número de riesgos del cultivo en alerta (rojo). |
| `Riesgos_En_Precaucion` | 0 | Número de riesgos del cultivo en precaución (amarillo). |
| `Riesgo_Hora` | 0% | Mapa de calor: fracción de horas-estación favorables al riesgo seleccionado (solo riesgos con condición horaria). |
| `GDD_Cultivo` | 0 | Grados día con tope del cultivo seleccionado en el periodo (por estación, promedio entre estaciones). |
| `GDD_Cultivo_Acumulado` | 0 | Grados día acumulados del año hidrológico hasta la semana en contexto. |
| `GDD_Cultivo_Acumulado_Anterior` | 0 | Ídem, año hidrológico anterior. |
| `GDD_Cultivo_Grafica` | 0 | Para la gráfica de acumulados por semana (eje Semanas_Anio), año actual. |
| `GDD_Cultivo_Anterior_Grafica` | 0 | Para la gráfica de acumulados por semana, año anterior. |
| `Cogollero_Generaciones` | 0.0 | Generaciones potenciales de gusano cogollero en el año hidrológico (base 10.9 °C, 559 grados día por generación). |
| `Salivosa_Lluvia_Temporada` | 0 | Lluvia acumulada desde el 1 de abril (inicio de la temporada de salivosa). |
| `Salivosa_Alerta_Emergencia` | 0 | 1 cuando la lluvia acumulada de la temporada alcanza 50 mm (eclosión de la mayoría de los huevos). |
| `Riesgo_Hora_Titulo` |  | Título del mapa de calor horario con el riesgo que se está mostrando. |
| `Titulo_Contexto` |  | Título dinámico del Resumen Semanal: cultivo, estaciones o estrato y fechas del periodo. |
| `_Riesgo_En_Cultivo` |  | TRUE si el riesgo en contexto pertenece al cultivo seleccionado (garantiza que no se muestren riesgos de otros cultivos). |

<details><summary><code>R_CAN_ROYA_CAFE</code></summary>

```dax
VAR _Est =
    FILTER(
        VALUES(Estaciones_met[estacionid]),
        NOT ISEMPTY(CALCULATETABLE(Fact_Diaria_met))
    )
RETURN
AVERAGEX(
    _Est,
    SUMX(
        VALUES(Calendario[Fecha]),
            VAR tmed = CALCULATE(AVERAGE(Fact_Diaria_met[Temp_Media]))
            VAR hr = CALCULATE(AVERAGE(Fact_Diaria_met[HR_Media]))
            VAR mojt = CALCULATE(MAX(Fact_Subdiaria_met_aux[Mojadura_Horas_Total]))
            RETURN IF(NOT ISBLANK(tmed) && NOT ISBLANK(hr) && NOT ISBLANK(mojt) && ( tmed >= 15 && tmed <= 25 && hr > 80 && mojt >= 6 ), 1, 0)
    )
)
```
</details>

<details><summary><code>R_CAN_ROYA_NARANJA</code></summary>

```dax
VAR _Est =
    FILTER(
        VALUES(Estaciones_met[estacionid]),
        NOT ISEMPTY(CALCULATETABLE(Fact_Diaria_met))
    )
RETURN
AVERAGEX(
    _Est,
    SUMX(
        VALUES(Calendario[Fecha]),
            VAR tmed = CALCULATE(AVERAGE(Fact_Diaria_met[Temp_Media]))
            VAR mojt = CALCULATE(MAX(Fact_Subdiaria_met_aux[Mojadura_Horas_Total]))
            RETURN IF(NOT ISBLANK(tmed) && NOT ISBLANK(mojt) && ( ( tmed >= 20 && tmed <= 25 ) || ( tmed > 25 && mojt > 8 ) ), 1, 0)
    )
)
```
</details>

<details><summary><code>R_CAN_ESCALDADURA</code></summary>

```dax
VAR _Est =
    FILTER(
        VALUES(Estaciones_met[estacionid]),
        NOT ISEMPTY(CALCULATETABLE(Fact_Diaria_met))
    )
RETURN
AVERAGEX(
    _Est,
    SUMX(
        VALUES(Calendario[Fecha]),
            VAR p = CALCULATE(SUM(Fact_Diaria_met[Precip_Total]))
            VAR vmax = CALCULATE(MAX(Fact_Subdiaria_met_aux[Viento_Max]))
            RETURN IF(NOT ISBLANK(p) && NOT ISBLANK(vmax) && ( p > 20 && vmax > 30 ), 1, 0)
    )
)
```
</details>

<details><summary><code>R_CAN_SALIVOSA</code></summary>

```dax
VAR _Est =
    FILTER(
        VALUES(Estaciones_met[estacionid]),
        NOT ISEMPTY(CALCULATETABLE(Fact_Diaria_met))
    )
RETURN
AVERAGEX(
    _Est,
    SUMX(
        FILTER(VALUES(Calendario[Fecha]), MONTH(Calendario[Fecha]) IN { 4, 5, 6, 7, 8, 9, 10, 11 }),
            VAR tmed = CALCULATE(AVERAGE(Fact_Diaria_met[Temp_Media]))
            VAR hr = CALCULATE(AVERAGE(Fact_Diaria_met[HR_Media]))
            VAR p = CALCULATE(SUM(Fact_Diaria_met[Precip_Total]))
            RETURN IF(NOT ISBLANK(tmed) && NOT ISBLANK(hr) && NOT ISBLANK(p) && ( p > 5 && hr > 80 && tmed >= 22 && tmed <= 30 ), 1, 0)
    )
)
```
</details>

<details><summary><code>R_CAN_BARRENADOR</code></summary>

```dax
VAR _Est =
    FILTER(
        VALUES(Estaciones_met[estacionid]),
        NOT ISEMPTY(CALCULATETABLE(Fact_Diaria_met))
    )
RETURN
AVERAGEX(
    _Est,
    SUMX(
        VALUES(Calendario[Fecha]),
            VAR tmed = CALCULATE(AVERAGE(Fact_Diaria_met[Temp_Media]))
            VAR hr = CALCULATE(AVERAGE(Fact_Diaria_met[HR_Media]))
            VAR p = CALCULATE(SUM(Fact_Diaria_met[Precip_Total]))
            RETURN IF(NOT ISBLANK(tmed) && NOT ISBLANK(hr) && NOT ISBLANK(p) && ( tmed > 24 && hr >= 60 && hr <= 80 && p < 1 ), 1, 0)
    )
)
```
</details>

<details><summary><code>R_CAN_CHINCHE_ENCAJE</code></summary>

```dax
VAR _Est =
    FILTER(
        VALUES(Estaciones_met[estacionid]),
        NOT ISEMPTY(CALCULATETABLE(Fact_Diaria_met))
    )
RETURN
AVERAGEX(
    _Est,
    CALCULATE(
        VAR _fuerte = CALCULATE(COUNTROWS(FILTER(Fact_Diaria_met, Fact_Diaria_met[Precip_Total] > 20)))
        VAR _secos = CALCULATE(COUNTROWS(FILTER(Fact_Diaria_met, Fact_Diaria_met[Precip_Total] < 1)))
        RETURN IF(COALESCE(_fuerte, 0) > 0, 0, COALESCE(_secos, 0))
    )
)
```
</details>

<details><summary><code>R_CAN_COLUDO</code></summary>

```dax
VAR _Est =
    FILTER(
        VALUES(Estaciones_met[estacionid]),
        NOT ISEMPTY(CALCULATETABLE(Fact_Diaria_met))
    )
RETURN
AVERAGEX(
    _Est,
    SUMX(
        FILTER(VALUES(Calendario[Fecha]), MONTH(Calendario[Fecha]) IN { 11, 12, 1, 2, 3, 4 }),
            VAR hr = CALCULATE(AVERAGE(Fact_Diaria_met[HR_Media]))
            VAR p = CALCULATE(SUM(Fact_Diaria_met[Precip_Total]))
            RETURN IF(NOT ISBLANK(hr) && NOT ISBLANK(p) && ( p < 1 && hr < 70 ), 1, 0)
    )
)
```
</details>

<details><summary><code>R_CAN_ESTRES</code></summary>

```dax
VAR _Est =
    FILTER(
        VALUES(Estaciones_met[estacionid]),
        NOT ISEMPTY(CALCULATETABLE(Fact_Horaria_riesgo))
    )
RETURN
AVERAGEX(_Est, COALESCE(CALCULATE(COUNTROWS(FILTER(Fact_Horaria_riesgo, Fact_Horaria_riesgo[Temp_Media] > 36 && Fact_Horaria_riesgo[Rad_Media] > 800))), 0))
```
</details>

<details><summary><code>R_CAN_SUELO_SATURADO</code></summary>

```dax
VAR _Est =
    FILTER(
        VALUES(Estaciones_met[estacionid]),
        NOT ISEMPTY(CALCULATETABLE(Fact_Diaria_met))
    )
RETURN
AVERAGEX(
    _Est,
    SUMX(
        FILTER(VALUES(Calendario[Fecha]), MONTH(Calendario[Fecha]) IN { 11, 12, 1, 2, 3, 4, 5 }),
            VAR p = CALCULATE(SUM(Fact_Diaria_met[Precip_Total]))
            RETURN IF(NOT ISBLANK(p) && ( p > 10 ), 1, 0)
    )
)
```
</details>

<details><summary><code>R_CAN_APLICACION</code></summary>

```dax
VAR _Est =
    FILTER(
        VALUES(Estaciones_met[estacionid]),
        NOT ISEMPTY(CALCULATETABLE(Fact_Horaria_riesgo))
    )
RETURN
AVERAGEX(_Est, DIVIDE(COALESCE(CALCULATE(COUNTROWS(FILTER(Fact_Horaria_riesgo, Fact_Horaria_riesgo[Temp_Media] < 30 && Fact_Horaria_riesgo[HR_Media] > 60 && Fact_Horaria_riesgo[Viento_Media] < 10 && Fact_Horaria_riesgo[Rad_Media] > 40))), 0), CALCULATE(DISTINCTCOUNT(Fact_Horaria_riesgo[Fecha]))))
```
</details>

<details><summary><code>R_CAN_QUEMA</code></summary>

```dax
VAR _Est =
    FILTER(
        VALUES(Estaciones_met[estacionid]),
        NOT ISEMPTY(CALCULATETABLE(Fact_Diaria_met))
    )
RETURN
AVERAGEX(
    _Est,
    SUMX(
        VALUES(Calendario[Fecha]),
            VAR _d = Calendario[Fecha]
            VAR hrmin = CALCULATE(MIN(Fact_Diaria_met[HR_Min]))
            VAR vmax = CALCULATE(MAX(Fact_Subdiaria_met_aux[Viento_Max]))
            VAR seco3 = CALCULATE(COUNTROWS(FILTER(Fact_Diaria_met, Fact_Diaria_met[Precip_Total] < 1)), DATESBETWEEN(Calendario[Fecha], _d - 2, _d))
            RETURN IF(NOT ISBLANK(hrmin) && NOT ISBLANK(vmax) && ( hrmin < 40 && vmax > 20 && seco3 = 3 ), 1, 0)
    )
)
```
</details>

<details><summary><code>R_CAN_MADURACION</code></summary>

```dax
VAR _Est =
    FILTER(
        VALUES(Estaciones_met[estacionid]),
        NOT ISEMPTY(CALCULATETABLE(Fact_Diaria_met))
    )
RETURN
AVERAGEX(
    _Est,
    SUMX(
        FILTER(VALUES(Calendario[Fecha]), MONTH(Calendario[Fecha]) IN { 11, 12, 1, 2, 3, 4 }),
            VAR _d = Calendario[Fecha]
            VAR tmin = CALCULATE(MIN(Fact_Diaria_met[Temp_Min]))
            VAR tmax = CALCULATE(MAX(Fact_Diaria_met[Temp_Max]))
            VAR p30 = CALCULATE(SUM(Fact_Diaria_met[Precip_Total]), DATESBETWEEN(Calendario[Fecha], _d - 29, _d))
            RETURN IF(NOT ISBLANK(tmin) && NOT ISBLANK(tmax) && ( (tmax - tmin) >= 15 && p30 >= 30 && p30 <= 100 ), 1, 0)
    )
)
```
</details>

<details><summary><code>R_BAN_SIG_NEGRA</code></summary>

```dax
VAR _Est =
    FILTER(
        VALUES(Estaciones_met[estacionid]),
        NOT ISEMPTY(CALCULATETABLE(Fact_Diaria_met))
    )
RETURN
AVERAGEX(
    _Est,
    SUMX(
        VALUES(Calendario[Fecha]),
            VAR tmed = CALCULATE(AVERAGE(Fact_Diaria_met[Temp_Media]))
            VAR hr = CALCULATE(AVERAGE(Fact_Diaria_met[HR_Media]))
            VAR mojn = CALCULATE(MAX(Fact_Subdiaria_met_aux[Mojadura_Horas_Nocturna]))
            RETURN IF(NOT ISBLANK(tmed) && NOT ISBLANK(hr) && NOT ISBLANK(mojn) && ( tmed >= 21.5 && tmed <= 28 && hr > 90 && mojn > 4 ), 1, 0)
    )
)
```
</details>

<details><summary><code>R_BAN_MOKO</code></summary>

```dax
VAR _Est =
    FILTER(
        VALUES(Estaciones_met[estacionid]),
        NOT ISEMPTY(CALCULATETABLE(Fact_Diaria_met))
    )
RETURN
AVERAGEX(
    _Est,
    CALCULATE(
        VAR _p = CALCULATE(SUM(Fact_Diaria_met[Precip_Total]))
        VAR _b = CALCULATE(SUM(Fact_Diaria_met[Balance_Hidrico]))
        RETURN IF(_p > 100 && _b > 0, 1, 0)
    )
)
```
</details>

<details><summary><code>R_BAN_VOLCAMIENTO</code></summary>

```dax
CALCULATE(MAX(Fact_Subdiaria_met_aux[Viento_Max_Diurno]))
```
</details>

<details><summary><code>R_BAN_ESTRES</code></summary>

```dax
VAR _Est =
    FILTER(
        VALUES(Estaciones_met[estacionid]),
        NOT ISEMPTY(CALCULATETABLE(Fact_Horaria_riesgo))
    )
RETURN
AVERAGEX(_Est, COALESCE(CALCULATE(COUNTROWS(FILTER(Fact_Horaria_riesgo, Fact_Horaria_riesgo[Temp_Media] > 38 && Fact_Horaria_riesgo[Rad_Media] > 800))), 0))
```
</details>

<details><summary><code>R_AGU_PHYTO</code></summary>

```dax
VAR _Est =
    FILTER(
        VALUES(Estaciones_met[estacionid]),
        NOT ISEMPTY(CALCULATETABLE(Fact_Diaria_met))
    )
RETURN
AVERAGEX(
    _Est,
    SUMX(
        VALUES(Calendario[Fecha]),
            VAR tmed = CALCULATE(AVERAGE(Fact_Diaria_met[Temp_Media]))
            VAR bal = CALCULATE(SUM(Fact_Diaria_met[Balance_Hidrico]))
            RETURN IF(NOT ISBLANK(tmed) && NOT ISBLANK(bal) && ( tmed >= 20 && tmed <= 30 && bal > 0 ), 1, 0)
    )
)
```
</details>

<details><summary><code>R_AGU_ANTRACNOSIS</code></summary>

```dax
VAR _Est =
    FILTER(
        VALUES(Estaciones_met[estacionid]),
        NOT ISEMPTY(CALCULATETABLE(Fact_Diaria_met))
    )
RETURN
AVERAGEX(
    _Est,
    SUMX(
        VALUES(Calendario[Fecha]),
            VAR tmed = CALCULATE(AVERAGE(Fact_Diaria_met[Temp_Media]))
            VAR hr = CALCULATE(AVERAGE(Fact_Diaria_met[HR_Media]))
            VAR p = CALCULATE(SUM(Fact_Diaria_met[Precip_Total]))
            VAR mojt = CALCULATE(MAX(Fact_Subdiaria_met_aux[Mojadura_Horas_Total]))
            RETURN IF(NOT ISBLANK(tmed) && NOT ISBLANK(hr) && NOT ISBLANK(p) && NOT ISBLANK(mojt) && ( tmed >= 20 && tmed <= 30 && hr > 80 && ( p > 1 || mojt > 6 ) ), 1, 0)
    )
)
```
</details>

<details><summary><code>R_AGU_FRIO</code></summary>

```dax
VAR _Est =
    FILTER(
        VALUES(Estaciones_met[estacionid]),
        NOT ISEMPTY(CALCULATETABLE(Fact_Diaria_met))
    )
RETURN
AVERAGEX(
    _Est,
    SUMX(
        VALUES(Calendario[Fecha]),
            VAR tmin = CALCULATE(MIN(Fact_Diaria_met[Temp_Min]))
            RETURN IF(NOT ISBLANK(tmin) && ( tmin < 12 ), 1, 0)
    )
)
```
</details>

<details><summary><code>R_AGU_CALOR</code></summary>

```dax
VAR _Est =
    FILTER(
        VALUES(Estaciones_met[estacionid]),
        NOT ISEMPTY(CALCULATETABLE(Fact_Horaria_riesgo))
    )
RETURN
AVERAGEX(_Est, COALESCE(CALCULATE(COUNTROWS(FILTER(Fact_Horaria_riesgo, Fact_Horaria_riesgo[Temp_Media] > 36 && Fact_Horaria_riesgo[Rad_Media] > 800))), 0))
```
</details>

<details><summary><code>R_AGU_VIENTO</code></summary>

```dax
CALCULATE(MAX(Fact_Subdiaria_met_aux[Viento_Max_Diurno]))
```
</details>

<details><summary><code>R_PAL_PC</code></summary>

```dax
VAR _Est =
    FILTER(
        VALUES(Estaciones_met[estacionid]),
        NOT ISEMPTY(CALCULATETABLE(Fact_Diaria_met))
    )
RETURN
AVERAGEX(
    _Est,
    SUMX(
        VALUES(Calendario[Fecha]),
            VAR tmed = CALCULATE(AVERAGE(Fact_Diaria_met[Temp_Media]))
            VAR hr = CALCULATE(AVERAGE(Fact_Diaria_met[HR_Media]))
            VAR p = CALCULATE(SUM(Fact_Diaria_met[Precip_Total]))
            RETURN IF(NOT ISBLANK(tmed) && NOT ISBLANK(hr) && NOT ISBLANK(p) && ( tmed >= 11 && tmed <= 35 && hr > 90 && p > 5 ), 1, 0)
    )
)
```
</details>

<details><summary><code>R_PAL_ESTRES</code></summary>

```dax
VAR _Est =
    FILTER(
        VALUES(Estaciones_met[estacionid]),
        NOT ISEMPTY(CALCULATETABLE(Fact_Horaria_riesgo))
    )
RETURN
AVERAGEX(_Est, COALESCE(CALCULATE(COUNTROWS(FILTER(Fact_Horaria_riesgo, Fact_Horaria_riesgo[Temp_Media] > 34 && Fact_Horaria_riesgo[Rad_Media] > 800))), 0))
```
</details>

<details><summary><code>R_MAI_ASFALTO</code></summary>

```dax
VAR _Est =
    FILTER(
        VALUES(Estaciones_met[estacionid]),
        NOT ISEMPTY(CALCULATETABLE(Fact_Diaria_met))
    )
RETURN
AVERAGEX(
    _Est,
    SUMX(
        VALUES(Calendario[Fecha]),
            VAR tmed = CALCULATE(AVERAGE(Fact_Diaria_met[Temp_Media]))
            VAR hr = CALCULATE(AVERAGE(Fact_Diaria_met[HR_Media]))
            VAR mojn = CALCULATE(MAX(Fact_Subdiaria_met_aux[Mojadura_Horas_Nocturna]))
            RETURN IF(NOT ISBLANK(tmed) && NOT ISBLANK(hr) && NOT ISBLANK(mojn) && ( tmed >= 16 && tmed <= 22 && hr > 75 && mojn >= 7 ), 1, 0)
    )
)
```
</details>

<details><summary><code>R_MAI_ROYA</code></summary>

```dax
VAR _Est =
    FILTER(
        VALUES(Estaciones_met[estacionid]),
        NOT ISEMPTY(CALCULATETABLE(Fact_Diaria_met))
    )
RETURN
AVERAGEX(
    _Est,
    SUMX(
        VALUES(Calendario[Fecha]),
            VAR tmin = CALCULATE(MIN(Fact_Diaria_met[Temp_Min]))
            VAR mojt = CALCULATE(MAX(Fact_Subdiaria_met_aux[Mojadura_Horas_Total]))
            RETURN IF(NOT ISBLANK(tmin) && NOT ISBLANK(mojt) && ( tmin >= 18 && tmin <= 21 && mojt >= 6 ), 1, 0)
    )
)
```
</details>

<details><summary><code>R_MAI_TIZON</code></summary>

```dax
VAR _Est =
    FILTER(
        VALUES(Estaciones_met[estacionid]),
        NOT ISEMPTY(CALCULATETABLE(Fact_Diaria_met))
    )
RETURN
AVERAGEX(
    _Est,
    SUMX(
        VALUES(Calendario[Fecha]),
            VAR tmed = CALCULATE(AVERAGE(Fact_Diaria_met[Temp_Media]))
            VAR mojt = CALCULATE(MAX(Fact_Subdiaria_met_aux[Mojadura_Horas_Total]))
            RETURN IF(NOT ISBLANK(tmed) && NOT ISBLANK(mojt) && ( tmed >= 18 && tmed <= 28 && mojt >= 6 ), 1, 0)
    )
)
```
</details>

<details><summary><code>R_MAI_MANCHA_GRIS</code></summary>

```dax
VAR _Est =
    FILTER(
        VALUES(Estaciones_met[estacionid]),
        NOT ISEMPTY(CALCULATETABLE(Fact_Diaria_met))
    )
RETURN
AVERAGEX(
    _Est,
    SUMX(
        VALUES(Calendario[Fecha]),
            VAR tmed = CALCULATE(AVERAGE(Fact_Diaria_met[Temp_Media]))
            VAR h90 = CALCULATE(COUNTROWS(FILTER(Fact_Horaria_riesgo, Fact_Horaria_riesgo[HR_Media] > 90)))
            RETURN IF(NOT ISBLANK(tmed) && ( tmed >= 27 && tmed <= 32 && h90 >= 12 ), 1, 0)
    )
)
```
</details>

<details><summary><code>R_MAI_COGOLLERO</code></summary>

```dax
VAR _Est =
    FILTER(
        VALUES(Estaciones_met[estacionid]),
        NOT ISEMPTY(CALCULATETABLE(Fact_Diaria_met))
    )
RETURN
AVERAGEX(
    _Est,
    SUMX(
        VALUES(Calendario[Fecha]),
            VAR tmax = CALCULATE(MAX(Fact_Diaria_met[Temp_Max]))
            VAR p = CALCULATE(SUM(Fact_Diaria_met[Precip_Total]))
            RETURN IF(NOT ISBLANK(tmax) && NOT ISBLANK(p) && ( tmax > 30 && p < 1 ), 1, 0)
    )
)
```
</details>

<details><summary><code>R_MAI_CALOR_FLOR</code></summary>

```dax
VAR _Est =
    FILTER(
        VALUES(Estaciones_met[estacionid]),
        NOT ISEMPTY(CALCULATETABLE(Fact_Diaria_met))
    )
RETURN
AVERAGEX(
    _Est,
    SUMX(
        VALUES(Calendario[Fecha]),
            VAR tmax = CALCULATE(MAX(Fact_Diaria_met[Temp_Max]))
            RETURN IF(NOT ISBLANK(tmax) && ( tmax > 38 ), 1, 0)
    )
)
```
</details>

<details><summary><code>R_FRI_MUSTIA</code></summary>

```dax
VAR _Est =
    FILTER(
        VALUES(Estaciones_met[estacionid]),
        NOT ISEMPTY(CALCULATETABLE(Fact_Diaria_met))
    )
RETURN
AVERAGEX(
    _Est,
    SUMX(
        VALUES(Calendario[Fecha]),
            VAR tmed = CALCULATE(AVERAGE(Fact_Diaria_met[Temp_Media]))
            VAR p = CALCULATE(SUM(Fact_Diaria_met[Precip_Total]))
            RETURN IF(NOT ISBLANK(tmed) && NOT ISBLANK(p) && ( tmed >= 25 && tmed <= 32 && p > 5 ), 1, 0)
    )
)
```
</details>

<details><summary><code>R_FRI_ROYA</code></summary>

```dax
VAR _Est =
    FILTER(
        VALUES(Estaciones_met[estacionid]),
        NOT ISEMPTY(CALCULATETABLE(Fact_Diaria_met))
    )
RETURN
AVERAGEX(
    _Est,
    SUMX(
        VALUES(Calendario[Fecha]),
            VAR tmed = CALCULATE(AVERAGE(Fact_Diaria_met[Temp_Media]))
            VAR p = CALCULATE(SUM(Fact_Diaria_met[Precip_Total]))
            VAR mojn = CALCULATE(MAX(Fact_Subdiaria_met_aux[Mojadura_Horas_Nocturna]))
            RETURN IF(NOT ISBLANK(tmed) && NOT ISBLANK(p) && NOT ISBLANK(mojn) && ( tmed >= 17 && tmed <= 27 && ( p > 1 || mojn >= 8 ) ), 1, 0)
    )
)
```
</details>

<details><summary><code>R_FRI_ANTRACNOSIS</code></summary>

```dax
VAR _Est =
    FILTER(
        VALUES(Estaciones_met[estacionid]),
        NOT ISEMPTY(CALCULATETABLE(Fact_Diaria_met))
            && CALCULATE(MAX(Estaciones_met[altitud])) >= 1000
    )
RETURN
AVERAGEX(
    _Est,
    SUMX(
        VALUES(Calendario[Fecha]),
            VAR tmed = CALCULATE(AVERAGE(Fact_Diaria_met[Temp_Media]))
            VAR hr = CALCULATE(AVERAGE(Fact_Diaria_met[HR_Media]))
            VAR p = CALCULATE(SUM(Fact_Diaria_met[Precip_Total]))
            RETURN IF(NOT ISBLANK(tmed) && NOT ISBLANK(hr) && NOT ISBLANK(p) && ( tmed >= 13 && tmed <= 26 && hr > 90 && p >= 1 ), 1, 0)
    )
)
```
</details>

<details><summary><code>R_FRI_MANCHA_ANGULAR</code></summary>

```dax
VAR _Est =
    FILTER(
        VALUES(Estaciones_met[estacionid]),
        NOT ISEMPTY(CALCULATETABLE(Fact_Diaria_met))
    )
RETURN
AVERAGEX(
    _Est,
    CALCULATE(
        VAR _lluv = CALCULATE(COUNTROWS(FILTER(Fact_Diaria_met, Fact_Diaria_met[Precip_Total] >= 1)))
        VAR _sec = CALCULATE(COUNTROWS(FILTER(Fact_Diaria_met, Fact_Diaria_met[Precip_Total] < 1)))
        VAR _t = CALCULATE(COUNTROWS(FILTER(Fact_Diaria_met, Fact_Diaria_met[Temp_Media] >= 18 && Fact_Diaria_met[Temp_Media] <= 28)))
        RETURN IF(COALESCE(_lluv, 0) >= 2 && COALESCE(_sec, 0) >= 2, COALESCE(_t, 0), 0)
    )
)
```
</details>

<details><summary><code>R_FRI_BACTERIOSIS</code></summary>

```dax
VAR _Est =
    FILTER(
        VALUES(Estaciones_met[estacionid]),
        NOT ISEMPTY(CALCULATETABLE(Fact_Diaria_met))
            && CALCULATE(MAX(Estaciones_met[altitud])) < 1200
    )
RETURN
AVERAGEX(
    _Est,
    SUMX(
        VALUES(Calendario[Fecha]),
            VAR tmed = CALCULATE(AVERAGE(Fact_Diaria_met[Temp_Media]))
            VAR p = CALCULATE(SUM(Fact_Diaria_met[Precip_Total]))
            RETURN IF(NOT ISBLANK(tmed) && NOT ISBLANK(p) && ( tmed >= 20 && tmed <= 32 && p > 5 ), 1, 0)
    )
)
```
</details>

<details><summary><code>R_FRI_MOSAICO</code></summary>

```dax
VAR _Est =
    FILTER(
        VALUES(Estaciones_met[estacionid]),
        NOT ISEMPTY(CALCULATETABLE(Fact_Diaria_met))
            && CALCULATE(MAX(Estaciones_met[altitud])) < 1200
    )
RETURN
AVERAGEX(
    _Est,
    SUMX(
        VALUES(Calendario[Fecha]),
            VAR tmed = CALCULATE(AVERAGE(Fact_Diaria_met[Temp_Media]))
            VAR p = CALCULATE(SUM(Fact_Diaria_met[Precip_Total]))
            RETURN IF(NOT ISBLANK(tmed) && NOT ISBLANK(p) && ( tmed >= 25 && tmed <= 30 && p < 1 ), 1, 0)
    )
)
```
</details>

<details><summary><code>R_FRI_CALOR_FLOR</code></summary>

```dax
VAR _Est =
    FILTER(
        VALUES(Estaciones_met[estacionid]),
        NOT ISEMPTY(CALCULATETABLE(Fact_Diaria_met))
    )
RETURN
AVERAGEX(
    _Est,
    SUMX(
        VALUES(Calendario[Fecha]),
            VAR tmax = CALCULATE(MAX(Fact_Diaria_met[Temp_Max]))
            RETURN IF(NOT ISBLANK(tmax) && ( tmax > 34 ), 1, 0)
    )
)
```
</details>

<details><summary><code>R_GRA_SEQUIA</code></summary>

```dax
VAR _Est =
    FILTER(
        VALUES(Estaciones_met[estacionid]),
        NOT ISEMPTY(CALCULATETABLE(Fact_Diaria_met))
    )
RETURN
AVERAGEX(
    _Est,
    SUMX(
        VALUES(Calendario[Fecha]),
            VAR p = CALCULATE(SUM(Fact_Diaria_met[Precip_Total]))
            RETURN IF(NOT ISBLANK(p) && ( p < 1 ), 1, 0)
    )
)
```
</details>

<details><summary><code>R_CAN_FLORACION</code></summary>

```dax
VAR _Est =
    FILTER(
        VALUES(Estaciones_met[estacionid]),
        NOT ISEMPTY(CALCULATETABLE(Fact_Diaria_met))
    )
RETURN
AVERAGEX(
    _Est,
    SUMX(
        FILTER(VALUES(Calendario[Fecha]), MONTH(Calendario[Fecha]) = 8 && DAY(Calendario[Fecha]) >= 16),
            VAR tmin = CALCULATE(MIN(Fact_Diaria_met[Temp_Min]))
            VAR tmax = CALCULATE(MAX(Fact_Diaria_met[Temp_Max]))
            RETURN IF(NOT ISBLANK(tmin) && NOT ISBLANK(tmax) && ( tmin >= 21 && tmin <= 24 && tmax <= 32 ), 1, 0)
    )
)
```
</details>

<details><summary><code>R_CAN_ACAME</code></summary>

```dax
VAR _Est =
    FILTER(
        VALUES(Estaciones_met[estacionid]),
        NOT ISEMPTY(CALCULATETABLE(Fact_Diaria_met))
    )
RETURN
AVERAGEX(
    _Est,
    SUMX(
        VALUES(Calendario[Fecha]),
            VAR p = CALCULATE(SUM(Fact_Diaria_met[Precip_Total]))
            VAR vmax = CALCULATE(MAX(Fact_Subdiaria_met_aux[Viento_Max]))
            RETURN IF(NOT ISBLANK(p) && NOT ISBLANK(vmax) && ( vmax > 40 && p > 10 ), 1, 0)
    )
)
```
</details>

<details><summary><code>R_AGU_ACAROS</code></summary>

```dax
VAR _Est =
    FILTER(
        VALUES(Estaciones_met[estacionid]),
        NOT ISEMPTY(CALCULATETABLE(Fact_Diaria_met))
    )
RETURN
AVERAGEX(
    _Est,
    SUMX(
        VALUES(Calendario[Fecha]),
            VAR hr = CALCULATE(AVERAGE(Fact_Diaria_met[HR_Media]))
            VAR p = CALCULATE(SUM(Fact_Diaria_met[Precip_Total]))
            VAR vmax = CALCULATE(MAX(Fact_Subdiaria_met_aux[Viento_Max]))
            RETURN IF(NOT ISBLANK(hr) && NOT ISBLANK(p) && NOT ISBLANK(vmax) && ( p < 1 && hr < 65 && vmax > 20 ), 1, 0)
    )
)
```
</details>

<details><summary><code>R_MAI_ACHAPARRAMIENTO</code></summary>

```dax
VAR _Est =
    FILTER(
        VALUES(Estaciones_met[estacionid]),
        NOT ISEMPTY(CALCULATETABLE(Fact_Diaria_met))
    )
RETURN
AVERAGEX(
    _Est,
    SUMX(
        VALUES(Calendario[Fecha]),
            VAR tmed = CALCULATE(AVERAGE(Fact_Diaria_met[Temp_Media]))
            VAR hr = CALCULATE(AVERAGE(Fact_Diaria_met[HR_Media]))
            VAR p = CALCULATE(SUM(Fact_Diaria_met[Precip_Total]))
            RETURN IF(NOT ISBLANK(tmed) && NOT ISBLANK(hr) && NOT ISBLANK(p) && ( p < 1 && tmed > 26 && hr < 70 ), 1, 0)
    )
)
```
</details>

<details><summary><code>R_MAI_PUDRICION_MAZORCA</code></summary>

```dax
VAR _Est =
    FILTER(
        VALUES(Estaciones_met[estacionid]),
        NOT ISEMPTY(CALCULATETABLE(Fact_Diaria_met))
    )
RETURN
AVERAGEX(
    _Est,
    SUMX(
        VALUES(Calendario[Fecha]),
            VAR p = CALCULATE(SUM(Fact_Diaria_met[Precip_Total]))
            RETURN IF(NOT ISBLANK(p) && ( p > 1 ), 1, 0)
    )
)
```
</details>

<details><summary><code>Riesgo_Valor</code></summary>

```dax
VAR _id = SELECTEDVALUE(Riesgos_Cultivo[ID])
RETURN
IF(
    [_Riesgo_En_Cultivo],
SWITCH(
    _id,
    "CAN_ROYA_CAFE", [R_CAN_ROYA_CAFE],
    "CAN_ROYA_NARANJA", [R_CAN_ROYA_NARANJA],
    "CAN_ESCALDADURA", [R_CAN_ESCALDADURA],
    "CAN_SALIVOSA", [R_CAN_SALIVOSA],
    "CAN_BARRENADOR", [R_CAN_BARRENADOR],
    "CAN_CHINCHE_ENCAJE", [R_CAN_CHINCHE_ENCAJE],
    "CAN_COLUDO", [R_CAN_COLUDO],
    "CAN_ESTRES", [R_CAN_ESTRES],
    "CAN_SUELO_SATURADO", [R_CAN_SUELO_SATURADO],
    "CAN_APLICACION", [R_CAN_APLICACION],
    "CAN_QUEMA", [R_CAN_QUEMA],
    "CAN_MADURACION", [R_CAN_MADURACION],
    "BAN_SIG_NEGRA", [R_BAN_SIG_NEGRA],
    "BAN_MOKO", [R_BAN_MOKO],
    "BAN_VOLCAMIENTO", [R_BAN_VOLCAMIENTO],
    "BAN_ESTRES", [R_BAN_ESTRES],
    "AGU_PHYTO", [R_AGU_PHYTO],
    "AGU_ANTRACNOSIS", [R_AGU_ANTRACNOSIS],
    "AGU_FRIO", [R_AGU_FRIO],
    "AGU_CALOR", [R_AGU_CALOR],
    "AGU_VIENTO", [R_AGU_VIENTO],
    "PAL_PC", [R_PAL_PC],
    "PAL_ESTRES", [R_PAL_ESTRES],
    "MAI_ASFALTO", [R_MAI_ASFALTO],
    "MAI_ROYA", [R_MAI_ROYA],
    "MAI_TIZON", [R_MAI_TIZON],
    "MAI_MANCHA_GRIS", [R_MAI_MANCHA_GRIS],
    "MAI_COGOLLERO", [R_MAI_COGOLLERO],
    "MAI_CALOR_FLOR", [R_MAI_CALOR_FLOR],
    "FRI_MUSTIA", [R_FRI_MUSTIA],
    "FRI_ROYA", [R_FRI_ROYA],
    "FRI_ANTRACNOSIS", [R_FRI_ANTRACNOSIS],
    "FRI_MANCHA_ANGULAR", [R_FRI_MANCHA_ANGULAR],
    "FRI_BACTERIOSIS", [R_FRI_BACTERIOSIS],
    "FRI_MOSAICO", [R_FRI_MOSAICO],
    "FRI_CALOR_FLOR", [R_FRI_CALOR_FLOR],
    "GRA_SEQUIA", [R_GRA_SEQUIA],
    "CAN_FLORACION", [R_CAN_FLORACION],
    "CAN_ACAME", [R_CAN_ACAME],
    "AGU_ACAROS", [R_AGU_ACAROS],
    "MAI_ACHAPARRAMIENTO", [R_MAI_ACHAPARRAMIENTO],
    "MAI_PUDRICION_MAZORCA", [R_MAI_PUDRICION_MAZORCA],
    BLANK()
)
)
```
</details>

<details><summary><code>Riesgo_Semaforo</code></summary>

```dax
VAR _v = [Riesgo_Valor]
VAR _am = SELECTEDVALUE(Riesgos_Cultivo[Umbral_Amarillo])
VAR _ro = SELECTEDVALUE(Riesgos_Cultivo[Umbral_Rojo])
VAR _inv = SELECTEDVALUE(Riesgos_Cultivo[Invertido])
RETURN
IF(
    ISBLANK(_v) || ISBLANK(_am), BLANK(),
    IF(_inv,
        SWITCH(TRUE(), _v <= _ro, 1, _v <= _am, 2, 3),
        SWITCH(TRUE(), _v >= _ro, 1, _v >= _am, 2, 3)
    )
)
```
</details>

<details><summary><code>Riesgo_Color</code></summary>

```dax
SWITCH([Riesgo_Semaforo], 1, "#D64550", 2, "#F2B134", 3, "#3BA272", "#B0B0B0")
```
</details>

<details><summary><code>Riesgo_Etiqueta</code></summary>

```dax
VAR _v = [Riesgo_Valor]
RETURN IF(NOT [_Riesgo_En_Cultivo], BLANK(), IF(ISBLANK(_v), "Sin datos", FORMAT(_v, "0.#") & " " & SELECTEDVALUE(Riesgos_Cultivo[Unidad])))
```
</details>

<details><summary><code>Riesgos_En_Alerta</code></summary>

```dax
COUNTROWS(FILTER(VALUES(Riesgos_Cultivo[ID]), [Riesgo_Semaforo] = 1))
```
</details>

<details><summary><code>Riesgos_En_Precaucion</code></summary>

```dax
COUNTROWS(FILTER(VALUES(Riesgos_Cultivo[ID]), [Riesgo_Semaforo] = 2))
```
</details>

<details><summary><code>Riesgo_Hora</code></summary>

```dax
VAR _sel = IF([_Riesgo_En_Cultivo], SELECTEDVALUE(Riesgos_Cultivo[ID]))
VAR _def =
    MAXX(
        TOPN(
            1,
            CALCULATETABLE(
                FILTER(Riesgos_Cultivo, Riesgos_Cultivo[Tiene_Horaria]),
                REMOVEFILTERS(Riesgos_Cultivo[Riesgo], Riesgos_Cultivo[ID], Riesgos_Cultivo[Orden_Nombre]),
                TREATAS(VALUES(Cultivos[Cultivo]), Riesgos_Cultivo[Cultivo])
            ),
            Riesgos_Cultivo[Orden], ASC
        ),
        Riesgos_Cultivo[ID]
    )
VAR _id = COALESCE(_sel, _def)
VAR _n = COUNTROWS(Fact_Horaria_riesgo)
RETURN
DIVIDE(
    SWITCH(
        _id,
        "CAN_ROYA_CAFE", COUNTROWS(FILTER(Fact_Horaria_riesgo, Fact_Horaria_riesgo[Temp_Media] >= 15 && Fact_Horaria_riesgo[Temp_Media] <= 25 && Fact_Horaria_riesgo[HR_Media] > 80 && Fact_Horaria_riesgo[Mojadura_Max] > 4)) + 0,
        "CAN_ROYA_NARANJA", COUNTROWS(FILTER(Fact_Horaria_riesgo, Fact_Horaria_riesgo[Temp_Media] >= 18 && Fact_Horaria_riesgo[Temp_Media] <= 28 && ( Fact_Horaria_riesgo[HR_Media] >= 98 || Fact_Horaria_riesgo[Mojadura_Max] > 4 ))) + 0,
        "CAN_SALIVOSA", COUNTROWS(FILTER(Fact_Horaria_riesgo, Fact_Horaria_riesgo[Temp_Media] >= 22 && Fact_Horaria_riesgo[Temp_Media] <= 30 && Fact_Horaria_riesgo[HR_Media] > 80 && Fact_Horaria_riesgo[Precip_Total] > 0)) + 0,
        "CAN_BARRENADOR", COUNTROWS(FILTER(Fact_Horaria_riesgo, Fact_Horaria_riesgo[Temp_Media] > 24 && Fact_Horaria_riesgo[HR_Media] >= 60 && Fact_Horaria_riesgo[HR_Media] <= 80 && Fact_Horaria_riesgo[Precip_Total] = 0)) + 0,
        "CAN_ESTRES", COUNTROWS(FILTER(Fact_Horaria_riesgo, Fact_Horaria_riesgo[Temp_Media] > 36 && Fact_Horaria_riesgo[Rad_Media] > 800)) + 0,
        "CAN_APLICACION", COUNTROWS(FILTER(Fact_Horaria_riesgo, Fact_Horaria_riesgo[Temp_Media] < 30 && Fact_Horaria_riesgo[HR_Media] > 60 && Fact_Horaria_riesgo[Viento_Media] < 10 && Fact_Horaria_riesgo[Rad_Media] > 40)) + 0,
        "BAN_SIG_NEGRA", COUNTROWS(FILTER(Fact_Horaria_riesgo, Fact_Horaria_riesgo[Temp_Media] >= 21.5 && Fact_Horaria_riesgo[Temp_Media] <= 28 && ( Fact_Horaria_riesgo[HR_Media] > 90 || Fact_Horaria_riesgo[Mojadura_Max] > 4 ))) + 0,
        "BAN_ESTRES", COUNTROWS(FILTER(Fact_Horaria_riesgo, Fact_Horaria_riesgo[Temp_Media] > 38 && Fact_Horaria_riesgo[Rad_Media] > 800)) + 0,
        "AGU_ANTRACNOSIS", COUNTROWS(FILTER(Fact_Horaria_riesgo, Fact_Horaria_riesgo[Temp_Media] >= 20 && Fact_Horaria_riesgo[Temp_Media] <= 30 && Fact_Horaria_riesgo[HR_Media] > 80 && ( Fact_Horaria_riesgo[Mojadura_Max] > 4 || Fact_Horaria_riesgo[Precip_Total] > 0 ))) + 0,
        "AGU_CALOR", COUNTROWS(FILTER(Fact_Horaria_riesgo, Fact_Horaria_riesgo[Temp_Media] > 36 && Fact_Horaria_riesgo[Rad_Media] > 800)) + 0,
        "PAL_PC", COUNTROWS(FILTER(Fact_Horaria_riesgo, Fact_Horaria_riesgo[Temp_Media] >= 11 && Fact_Horaria_riesgo[Temp_Media] <= 35 && Fact_Horaria_riesgo[HR_Media] > 90 && Fact_Horaria_riesgo[Precip_Total] > 0)) + 0,
        "PAL_ESTRES", COUNTROWS(FILTER(Fact_Horaria_riesgo, Fact_Horaria_riesgo[Temp_Media] > 34 && Fact_Horaria_riesgo[Rad_Media] > 800)) + 0,
        "MAI_ASFALTO", COUNTROWS(FILTER(Fact_Horaria_riesgo, Fact_Horaria_riesgo[Temp_Media] >= 16 && Fact_Horaria_riesgo[Temp_Media] <= 22 && Fact_Horaria_riesgo[HR_Media] > 75 && Fact_Horaria_riesgo[Mojadura_Max] > 4)) + 0,
        "MAI_ROYA", COUNTROWS(FILTER(Fact_Horaria_riesgo, Fact_Horaria_riesgo[Temp_Media] >= 16 && Fact_Horaria_riesgo[Temp_Media] <= 23 && Fact_Horaria_riesgo[Mojadura_Max] > 4)) + 0,
        "MAI_TIZON", COUNTROWS(FILTER(Fact_Horaria_riesgo, Fact_Horaria_riesgo[Temp_Media] >= 18 && Fact_Horaria_riesgo[Temp_Media] <= 28 && Fact_Horaria_riesgo[Mojadura_Max] > 4)) + 0,
        "MAI_MANCHA_GRIS", COUNTROWS(FILTER(Fact_Horaria_riesgo, Fact_Horaria_riesgo[Temp_Media] >= 27 && Fact_Horaria_riesgo[Temp_Media] <= 32 && Fact_Horaria_riesgo[HR_Media] > 90)) + 0,
        "FRI_ROYA", COUNTROWS(FILTER(Fact_Horaria_riesgo, Fact_Horaria_riesgo[Temp_Media] >= 17 && Fact_Horaria_riesgo[Temp_Media] <= 27 && ( Fact_Horaria_riesgo[HR_Media] > 95 || Fact_Horaria_riesgo[Mojadura_Max] > 4 ))) + 0,
        BLANK()
    ),
    _n
)
```
</details>

<details><summary><code>GDD_Cultivo</code></summary>

```dax
VAR _b = SELECTEDVALUE(Cultivos[GDD_Base], 10)
VAR _t = SELECTEDVALUE(Cultivos[GDD_Tope], 30)
RETURN
AVERAGEX(
    VALUES(Estaciones_met[estacionid]),
    CALCULATE(
        SUMX(
            Fact_Diaria_met,
            VAR _x = Fact_Diaria_met[Temp_Media]
            RETURN IF(ISBLANK(_x), BLANK(), MIN(MAX(_x - _b, 0), _t - _b))
        )
    )
)
```
</details>

<details><summary><code>GDD_Cultivo_Acumulado</code></summary>

```dax
CALCULATE(
    [GDD_Cultivo],
    FILTER(
        ALL(Calendario),
        Calendario[Año_Hidrologico] = MAX(Calendario[Año_Hidrologico]) &&
        Calendario[Semana_Hidrologica] <= MAX(Calendario[Semana_Hidrologica])
    )
)
```
</details>

<details><summary><code>GDD_Cultivo_Acumulado_Anterior</code></summary>

```dax
CALCULATE(
    [GDD_Cultivo],
    FILTER(
        ALL(Calendario),
        Calendario[Año_Hidrologico] = MAX(Calendario[Año_Hidrologico]) - 1 &&
        Calendario[Semana_Hidrologica] <= MAX(Calendario[Semana_Hidrologica])
    )
)
```
</details>

<details><summary><code>GDD_Cultivo_Grafica</code></summary>

```dax
VAR _Anio = CALCULATE(MAX(Calendario[Año_Hidrologico]), ALLSELECTED(Calendario))
VAR _SemMax = CALCULATE(MAX(Calendario[Semana_Hidrologica]), ALLSELECTED(Calendario))
VAR _SemEje = MAX(Semanas_Anio[Semana_Num])
RETURN
IF(_SemEje <= _SemMax, CALCULATE([GDD_Cultivo], ALL(Calendario), Calendario[Año_Hidrologico] = _Anio, Calendario[Semana_Hidrologica] <= _SemEje))
```
</details>

<details><summary><code>GDD_Cultivo_Anterior_Grafica</code></summary>

```dax
VAR _Anio = CALCULATE(MAX(Calendario[Año_Hidrologico]), ALLSELECTED(Calendario))
VAR _SemMax = CALCULATE(MAX(Calendario[Semana_Hidrologica]), ALLSELECTED(Calendario))
VAR _SemEje = MAX(Semanas_Anio[Semana_Num])
RETURN
CALCULATE([GDD_Cultivo], ALL(Calendario), Calendario[Año_Hidrologico] = _Anio - 1, Calendario[Semana_Hidrologica] <= _SemEje)
```
</details>

<details><summary><code>Cogollero_Generaciones</code></summary>

```dax
CALCULATE(
    AVERAGEX(
        VALUES(Estaciones_met[estacionid]),
        CALCULATE(SUMX(Fact_Diaria_met, MAX(Fact_Diaria_met[Temp_Media] - 10.9, 0)))
    ),
    FILTER(ALL(Calendario), Calendario[Año_Hidrologico] = MAX(Calendario[Año_Hidrologico]) && Calendario[Semana_Hidrologica] <= MAX(Calendario[Semana_Hidrologica]))
) / 559
```
</details>

<details><summary><code>Salivosa_Lluvia_Temporada</code></summary>

```dax
VAR _fin = MAX(Calendario[Fecha])
VAR _ini = DATE(YEAR(_fin), 4, 1)
RETURN
IF(_fin >= _ini,
    CALCULATE(
        AVERAGEX(VALUES(Estaciones_met[estacionid]), CALCULATE(SUM(Fact_Diaria_met[Precip_Total]))),
        DATESBETWEEN(Calendario[Fecha], _ini, _fin)
    )
)
```
</details>

<details><summary><code>Salivosa_Alerta_Emergencia</code></summary>

```dax
IF([Salivosa_Lluvia_Temporada] >= 50, 1, 0)
```
</details>

<details><summary><code>Riesgo_Hora_Titulo</code></summary>

```dax
VAR _sel = IF([_Riesgo_En_Cultivo], SELECTEDVALUE(Riesgos_Cultivo[ID]))
VAR _def =
    MAXX(
        TOPN(
            1,
            CALCULATETABLE(
                FILTER(Riesgos_Cultivo, Riesgos_Cultivo[Tiene_Horaria]),
                REMOVEFILTERS(Riesgos_Cultivo[Riesgo], Riesgos_Cultivo[ID], Riesgos_Cultivo[Orden_Nombre]),
                TREATAS(VALUES(Cultivos[Cultivo]), Riesgos_Cultivo[Cultivo])
            ),
            Riesgos_Cultivo[Orden], ASC
        ),
        Riesgos_Cultivo[ID]
    )
VAR _id = COALESCE(_sel, _def)
VAR _nom = CALCULATE(SELECTEDVALUE(Riesgos_Cultivo[Riesgo]), REMOVEFILTERS(Riesgos_Cultivo), Riesgos_Cultivo[ID] = _id)
RETURN IF(ISBLANK(_nom), "Sin riesgo horario para este cultivo", "Horas favorables a " & LOWER(_nom) & " (% de horas-estación)")
```
</details>

<details><summary><code>Titulo_Contexto</code></summary>

```dax
VAR _ini = MIN(Calendario[Fecha])
VAR _fin = MAX(Calendario[Fecha])
VAR _est = FILTER(VALUES(Estaciones_met[estacionid]), NOT ISEMPTY(CALCULATETABLE(Fact_Diaria_met)))
VAR _n = COUNTROWS(_est)
VAR _txtEst =
    SWITCH(
        TRUE(),
        NOT ISFILTERED(Estaciones_met), "Todas las estaciones (" & _n & ")",
        _n = 1, "Estación " & CALCULATE(SELECTEDVALUE(Estaciones_met[finca]), _est),
        ISFILTERED(Estaciones_met[estrato.nombre]) && NOT ISFILTERED(Estaciones_met[finca]) && NOT ISFILTERED(Estaciones_met[estacionid]),
            "Estrato " & CONCATENATEX(VALUES(Estaciones_met[estrato.nombre]), Estaciones_met[estrato.nombre], ", ") & " (" & _n & " estaciones)",
        _n & " estaciones seleccionadas"
    )
RETURN
SELECTEDVALUE(Cultivos[Cultivo], "Sin cultivo") & "  ·  " & _txtEst & "  ·  " & FORMAT(_ini, "dd-mmm") & " al " & FORMAT(_fin, "dd-mmm-yyyy")
```
</details>

<details><summary><code>_Riesgo_En_Cultivo</code></summary>

```dax
NOT ISEMPTY(
    CALCULATETABLE(
        VALUES(Riesgos_Cultivo[ID]),
        TREATAS(VALUES(Cultivos[Cultivo]), Riesgos_Cultivo[Cultivo])
    )
)
```
</details>

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
        & IF(Dominante = "", "calma", Dominante) & "</tspan> (" & FORMAT(COALESCE(MaxPct, 0), "0.0", "en-US") & "%)</text>"
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
        Anillos & Ejes & Petalos
            & IF(COALESCE(MaxPct, 0) = 0,
                "<circle cx='" & cx & "' cy='" & cy & "' r='34' fill='white' stroke='rgb(150,150,150)'/>"
                & "<text x='" & cx & "' y='" & cy + 6 & "' text-anchor='middle' font-size='17' font-weight='bold' fill='rgb(90,90,90)'>Calma</text>")
            & Panel
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
