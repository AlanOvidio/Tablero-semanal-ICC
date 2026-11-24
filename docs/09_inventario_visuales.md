# Inventario de páginas y visuales

> Generado automáticamente por `tools/generar_docs_modelo.py` el 2026-11-24. No editar a mano.

## Agua y energía

Tamaño 1300×1624 · 24 visuales · carpeta `d18dbb7729765a1097a1`

| Visual | Título | Campos | ID |
|---|---|---|---|
| cardVisual |  | Datos_Al_Diaria | `6a3c85` |
| cardVisual |  | Titulo_Semana | `8dde3a` |
| slicer | Estrato altitudinal | estrato.nombre | `63d13e` |
| slicer | Estación | finca | `9d1ab0` |
| slicer | Año hidrológico | Año_Selector | `37e7d0` |
| slicer | Semana | Semana_Selector | `eb6fea` |
| azureMap | Balance hídrico de la semana por estación (tamaño = lluvia) | Precip_Semanal, finca), Balance_Semanal, ETO_Semanal, longitud, latitud | `320625` |
| cardVisual | Precipitación semanal | Precip_Semanal | `a602cf` |
| cardVisual | Evapotranspiración semanal | ETO_Semanal | `7c4f09` |
| cardVisual | Balance hídrico | Balance_Semanal | `c70aec` |
| tableEx | Resumen de la semana | Variable, Resumen_Actual, Resumen_Semana_Anterior, Resumen_Anio_Anterior, Unidad | `38eac1` |
| clusteredColumnChart | Balances anteriores | Semana_Eje, Balance_Por_Semana | `53badd` |
| cardVisual | Estaciones en déficit | Estaciones_Deficit_Critico | `951738` |
| areaChart | Balance hídrico diario | Jerarquía hidrológica.Fecha, Precip_Diaria, ETO_Diaria, Precip_Max_Evento | `407063` |
| tableEx | Listado estaciones en deficit | finca, Balance_Semanal | `baf85d` |
| cardVisual | Temperaturas semanales | Temp_Max, Temp_Media, Temp_Min | `ecfd5a` |
| lineChart | Temperaturas diarias | Jerarquía hidrológica.Fecha, Temp_Media, Temp_Min, Temp_Max, IC_Max_Diurno, IC_Media_Diurno | `0f0df0` |
| cardVisual | Sensación térmica semanal | IC_Media_Diurno, IC_Max_Diurno | `99776d` |
| slicer | Ventana de radiación y grados día | Ventana | `84c8f0` |
| lineChart |  | Semana_Eje, GDD_Texto_Actual, GDD_Texto_Anterior, GDD_Acum8_Media, GDD_Desv_Acum, GDD_Desv_Acum_Ant, Desv_Media_Linea | `0df326` |
| lineChart |  | Semana_Eje, Rad_Texto_Actual, Rad_Texto_Anterior, Rad_Acum8_Media, Rad_Desv_Acum, Rad_Desv_Acum_Ant, Desv_Media_Linea | `0352b1` |

## Estrés atmosférico y vegetal

Tamaño 1300×1755 · 21 visuales · carpeta `6d6c6ba3b87858a5a48f`

| Visual | Título | Campos | ID |
|---|---|---|---|
| cardVisual |  | Datos_Al_Diaria | `ddf457` |
| cardVisual |  | Titulo_Semana | `d3b855` |
| slicer | Estrato altitudinal | estrato.nombre | `8bf32c` |
| slicer | Año hidrológico | Año_Selector | `221923` |
| slicer | Semana | Semana_Selector | `0296bd` |
| slicer | Estación | finca | `7121f5` |
| scatterChart | Estrés de día frente a recuperación de noche por estación | finca, estrato.nombre, Mojadura_Horas_Nocturna_Semanal, VPD_Max_Diurna, Temp_Nocturna_Media | `45261e` |
| azureMap | DPV máximo diurno por estación (tamaño = horas de estrés térmico) | Horas_Estres_Termico_Semanal, finca), VPD_Max_Diurna, Temp_Nocturna_Media, longitud, latitud | `57ba35` |
| lineChart | Condiciones de estrés atmosférico (DPV y eje secundario a elegir) | Jerarquía hidrológica.Fecha, DN_DPV_MED_D, DN_DPV_MAX_D, DN_DPV_MED_N, DN_HR_MIN, DN_HR_MED, DN_T_NOC, DN_T_MIN_NOC | `72c2e0` |
| slicer | Periodo | Vista | `1faa8c` |
| slicer | Eje secundario | Opcion | `97eb68` |
| slicer | Series (desmarca para quitar) | Serie | `c5e0fb` |
| lineChart | Condiciones de estrés vegetal | Jerarquía hidrológica.Fecha, DN_MOJ_D, DN_MOJ_N, DN_LUZ_D, DN_ESTRES_D, DN_IRR_MAX, DN_IRR_LUZ | `f07ad3` |
| slicer | Periodo | Vista | `a2e798` |
| slicer | Series (desmarca para quitar) | Serie | `bf35ba` |
| slicer | Periodo | Vista | `6afee0` |
| lineChart | Comportamiento del viento | Fecha, DN_V_MAX_D, DN_V_MAX_N, DN_V_MED_D, DN_V_MED_N | `a55767` |
| slicer | Series (desmarca para quitar) | Serie | `2e996b` |

## Comportamiento horario

Tamaño 1300×1000 · 14 visuales · carpeta `657bfe7bc23e54a4a8f6`

| Visual | Título | Campos | ID |
|---|---|---|---|
| cardVisual |  | Titulo_Semana | `a8d1da` |
| cardVisual |  | Datos_Al_Horaria | `2d39c9` |
| slicer | Año hidrológico | Año_Selector | `4d1061` |
| slicer | Semana | Semana_Selector | `d3ca32` |
| slicer | Estrato altitudinal | estrato.nombre | `2176f3` |
| slicer | Estación | finca | `f7402a` |
| slicer | Variable del mapa de calor y del mapa de estaciones | Vista | `fb7bc0` |
| azureMap | Promedio de la semana por estación (variable del mapa de calor) | finca), Mapa_Calor_Valor, longitud, latitud | `9b9039` |
| pivotTable |  | Fecha_Corta, Hora_Etiqueta, Mapa_Calor_Valor | `98f782` |
| tableEx | Leyenda | Rango | `3ab19b` |
| slicer | Periodo del día (rosa de vientos) | Periodo | `1126be` |
| tableEx |  | Rosa_Vientos_SVG | `6a45b4` |

## Riesgos del cultivo

Tamaño 1300×2369.808917197452 · 18 visuales · carpeta `7d63878b01ae574c8b68`

| Visual | Título | Campos | ID |
|---|---|---|---|
| cardVisual |  | Titulo_Contexto | `3860fb` |
| cardVisual |  | Datos_Al_Diaria | `94935b` |
| slicer | Año hidrológico | Año_Selector | `5ca9e8` |
| slicer | Semana | Semana_Selector | `2dd43c` |
| slicer | Estrato altitudinal | estrato.nombre | `bc4ed0` |
| slicer | Estación | finca | `97646e` |
| slicer | Cultivo | Cultivo | `51dd08` |
| cardVisual | Contexto Productivo | Balance_Semanal, Temp_Nocturna_Media, GDD_Cultivo_Acumulado, Horas_Luz, Mojadura_Horas_Total_Semanal, Mojadura_Horas_Nocturna_Semanal, GDD_Cultivo_Acumulado_Anterior | `c35fd4` |
| cardVisual | Riesgos del cultivo en la semana | Riesgos_En_Alerta, Riesgos_En_Precaucion | `f409f8` |
| tableEx | Semáforo de riesgos (verde normal · amarillo precaución · rojo alerta · gris sin datos) | Riesgo, Riesgo_Etiqueta, Umbral_Amarillo, Umbral_Rojo, Condicion, Aplicacion, Confianza | `e9bcd0` |
| slicer | Riesgos del mapa horario (sin selección = todos) | Categoria, Riesgo | `15a15e` |
| tableEx | Leyenda | Rango | `6b6864` |
| pivotTable |  | Fecha_Corta, Hora_Etiqueta, Mapa_Calor_N, Mapa_Calor_Valor | `7379ed` |
| azureMap |  | Riesgos_En_Alerta, Riesgos_En_Precaucion, longitud, latitud | `7ac141` |
| tableEx |  | Rango | `fb7e92` |
| pivotTable | Riesgos por estrato y estación (expandir el estrato para ver las estaciones) | Riesgo, estrato.nombre, finca, Riesgo_Valor | `eb968e` |

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

## Pronostico Semanal

Tamaño 1280×720 · 0 visuales · carpeta `762f91035868e502547c`

| Visual | Título | Campos | ID |
|---|---|---|---|

