# Inventario de páginas y visuales

> Generado automáticamente por `tools/generar_docs_modelo.py` el 2026-11-03. No editar a mano.

## Validaciones1

Tamaño 1280×720 · 5 visuales · carpeta `54e371566cdde3e6b398`

| Visual | Título | Campos | ID |
|---|---|---|---|
| tableEx |  | finca, estrato.nombre, Semana_Etiqueta, Precip_Semanal, ETO_Semanal, Temp_Min, Temp_Max, Balance_Semanal | `b2a36f` |
| tableEx |  | Semana_Etiqueta | `9e3d74` |
| cardVisual |  | _Conteo_Estaciones_Met | `9f6b15` |
| cardVisual |  | _Conteo_Filas_Diarias | `81c35c` |

## Validaciones 2

Tamaño 1280×720 · 2 visuales · carpeta `3434c5d1010ec2da2aa3`

| Visual | Título | Campos | ID |
|---|---|---|---|
| tableEx |  | Anio, Mes_Nombre, Fecha, Año_Hidrologico), Semana_Hidrologica), Semana_Etiqueta, Inicio_Semana, Fin_Semana | `164c89` |
| tableEx |  | Anio, Mes_Nombre, Fecha, Año_Hidrologico), Semana_Hidrologica), Semana_Etiqueta, Inicio_Semana, Fin_Semana | `886e1e` |

## Validaciones 3

Tamaño 1280×720 · 1 visuales · carpeta `4f0784fbde51533914fe`

| Visual | Título | Campos | ID |
|---|---|---|---|
| tableEx |  | Año_Hidrologico), Semana_Hidrologica), Precip_Historico_Promedio, Precip_Historico_Max, Precip_Historico_Min | `7daf67` |

## Validaciones 4

Tamaño 1280×720 · 2 visuales · carpeta `2b3a32e95e82cae45213`

| Visual | Título | Campos | ID |
|---|---|---|---|
| tableEx |  | finca, Dias_Riesgo_Carbon, Dias_Riesgo_Barrenador, Dias_Riesgo_Roya, Dias_Riesgo_Salivosa | `2b9962` |

## Resumen Semanal

Tamaño 1300×4143 · 34 visuales · carpeta `ff3ee83505f7aab7cef2`

| Visual | Título | Campos | ID |
|---|---|---|---|
| slicer | Semana | Semana_Etiqueta | `e58943` |
| slicer | Año Hidrológico | Año_Hidrologico | `988805` |
| slicer | Estrato Altitudinal | estrato.nombre | `4b856a` |
| slicer | Cultivo | Cultivo | `6bf244` |
| slicer | Estación | finca | `191943` |
| cardVisual | Contexto | Titulo_Contexto | `10cd6c` |
| azureMap | Estaciones Meteorologicas | longitud, latitud, estacionid, estrato.nombre, Precip_Semanal, ETO_Semanal, Balance_Semanal, finca), Temp_Max | `5b2aaf` |
| cardVisual | Estaciones en déficit crítico | Estaciones_Deficit_Critico | `aec676` |
| tableEx | Listado estaciones en deficit | finca, Balance_Semanal | `36102a` |
| cardVisual | Evapotranspiración semanal | ETO_Semanal | `4214ec` |
| cardVisual | Precipitación semanal | Precip_Semanal | `09430e` |
| cardVisual | Balance hídrico | Balance_Semanal | `75a61a` |
| areaChart | Balance hídrico diario | Jerarquía hidrológica.Fecha, Precip_Diaria, ETO_Diaria, Precip_Max_Evento | `ec79ba` |
| clusteredColumnChart | Balances anteriores | Semana_Hidrologica, Balance_Por_Semana | `5856a3` |
| lineChart | Temperaturas diarias | Jerarquía hidrológica.Fecha, Temp_Media, Temp_Min, Temp_Max, IC_Max_Diurno, IC_Media_Diurno | `651e74` |
| cardVisual | Temperaturas semanales | Temp_Max, Temp_Media, Temp_Min | `c2a7a9` |
| cardVisual | Sensación térmica semanal | IC_Media_Diurno, IC_Max_Diurno | `4ec2c7` |
| lineChart | Condiciones de estrés atmosférico | Jerarquía hidrológica.Fecha, VPD_Media_Diurna, VPD_Max_Diurna, VPD_Media_Nocturna, HR_Min, HR_Media | `9c537a` |
| lineChart | Condiciones de estrés vegetal | Jerarquía hidrológica.Fecha, Mojadura_Horas_Semanal, Mojadura_Horas_Nocturna_Semanal, Horas_Luz, Horas_Estres_Termico_Semanal, Rad_Max_Diurna, Rad_Media_Luz | `0b6a1f` |
| lineChart | VPD y Temperatura Nocturna | Jerarquía hidrológica.Fecha, VPD_Max_Diurna, VPD_Media_Nocturna, VPD_Media_Diurna, Temp_Nocturna_Media, Temp_Min_Nocturna | `2c0af4` |
| lineChart | Radiación Solar Acumulada | Semana_Num, Rad_Acumulada_Anual_Anterior_Grafica, Rad_Acumulada_Anual_Grafica | `687d3b` |
| lineChart | Grados día acumulados del cultivo (año actual vs. anterior) | Semana_Num, GDD_Cultivo_Anterior_Grafica, GDD_Cultivo_Grafica | `5bd82a` |
| lineChart | Comportamiento del viento | Fecha, Viento_Max_Diurno, Viento_Max_Nocturno, Viento_Media_Diurna, Viento_Media_Nocturna | `9189ab` |
| slicer | Mapa de calor: categoría o riesgo (sin selección = todos) | Categoria, Riesgo | `781803` |
| pivotTable |  | Fecha_Corta, Hora_Etiqueta, Riesgo_Hora_N, Riesgo_Hora | `3afd62` |
| slicer | Período del día (rosa de vientos) | Periodo | `b16e5e` |
| tableEx |  | Rosa_Vientos_SVG | `411b72` |
| cardVisual | Riesgos del cultivo en la semana | Riesgos_En_Alerta, Riesgos_En_Precaucion | `cfd277` |
| cardVisual | Contexto Productivo | Balance_Semanal, Temp_Nocturna_Media, GDD_Cultivo_Acumulado, Horas_Luz, Mojadura_Horas_Total_Semanal, Mojadura_Horas_Semanal, GDD_Cultivo_Acumulado_Anterior | `179b16` |
| tableEx | Semáforo de riesgos (verde normal · amarillo precaución · rojo alerta · gris sin datos) | Riesgo, Riesgo_Etiqueta, Umbral_Amarillo, Umbral_Rojo, Condicion, Aplicacion, Confianza | `aa96ae` |
| pivotTable | Riesgos por estrato y estación (expandir el estrato para ver las estaciones) | Riesgo, estrato.nombre, finca, Riesgo_Valor | `034109` |

## Pronostico Semanal

Tamaño 1280×720 · 0 visuales · carpeta `762f91035868e502547c`

| Visual | Título | Campos | ID |
|---|---|---|---|

