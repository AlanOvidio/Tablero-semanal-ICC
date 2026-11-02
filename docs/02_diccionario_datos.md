# Diccionario de datos

> Generado automáticamente por `tools/generar_docs_modelo.py` el 2026-11-02. No editar a mano: los cambios se pierden al regenerar.

## Parámetros y funciones de Power Query

| Nombre | Descripción | Definición |
|---|---|---|
| `RangeEnd` | Fin del rango de carga en Desktop, exclusivo. Usar las 00:00 del día siguiente al último día que se quiere ver. | `#datetime(2026, 10, 26, 12, 0, 0)` |
| `fxLecturasEstacion_met` | Lecturas de 15 min de una estación (endpoint /ws/redmet/estaciones/lecturas). | Función (ver `expressions.tmdl`) |
| `RangeStart` | Inicio del rango de carga en Desktop (en el servicio lo fija la actualización incremental). Usar 00:00. | `#datetime(2024, 10, 28, 0, 0, 0)` |
| `InicioAnioHidrologico` | Fecha de referencia del inicio del año hidrológico (se usan su mes y día; la semana inicia el lunes). | `#date(2025, 11, 2)` |
| `fxLecturasEstacion_met_diario` | Resumen diario de una estación (endpoint /ws/getlecturasdia). | Función (ver `expressions.tmdl`) |

## Actualización incremental

| Tabla | Ventana de historia | Se refresca en cada actualización |
|---|---|---|
| `Fact_Diaria_met` | 18 años | últimos 7 días |
| `Fact_Horaria_riesgo` | 5 años | últimos 7 días |
| `Fact_Meteorologia` | 18 años | últimos 7 días |
| `Fact_Subdiaria_met_aux` | 5 años | últimos 7 días |

## Relaciones

| Desde (muchos) | Hacia (uno) | Activa | Filtro |
|---|---|---|---|
| `Fact_Diaria_met.Fecha` | `Calendario.Fecha` | Sí | una dirección |
| `Fact_Diaria_met.estacionid` | `Estaciones_met.estacionid` | Sí | una dirección |
| `Fact_Meteorologia.'Fecha 2'` | `Calendario.Fecha` | **No** (inactiva) | una dirección |
| `Fact_Meteorologia.estacionid` | `Estaciones_met.estacionid` | **No** (inactiva) | una dirección |
| `Fact_Subdiaria_met_aux.estacionid` | `Estaciones_met.estacionid` | Sí | una dirección |
| `Fact_Subdiaria_met_aux.Fecha` | `Calendario.Fecha` | Sí | una dirección |
| `Fact_Horaria_riesgo.Fecha` | `Calendario.Fecha` | Sí | una dirección |
| `Fact_Horaria_riesgo.estacionid` | `Estaciones_met.estacionid` | Sí | una dirección |
| `Fact_Horaria_riesgo.Hora` | `Horas_Dia.Hora` | Sí | una dirección |
| `Fact_Horaria_riesgo.Sector_Viento` | `Direcciones_Viento.Orden` | Sí | una dirección |

## Tablas

### `Calendario` — tabla de fechas marcada

| Columna | Tipo | Formato | Ordenar por | Notas |
|---|---|---|---|---|
| `Fecha` | dateTime | dd-mmm |  | clave |
| `Mes_Num` | int64 | 0 |  |  |
| `Dia_Semana` | string |  | `Dia_Semana_Num` |  |
| `Año_Hidrologico` | int64 | 0 |  |  |
| `Semana_Hidrologica` | int64 | 0 |  |  |
| `Semana_Etiqueta` | string |  | `Inicio_Semana` |  |
| `Anio` | int64 | 0 |  |  |
| `Mes_Nombre` | string |  | `Mes_Num` |  |
| `Dia_Semana_Num` | int64 | 0 |  |  |
| `Inicio_Semana` | dateTime | Long Date |  |  |
| `Fin_Semana` | dateTime | Long Date |  |  |
| `Semana_Anio_Etiqueta` | string |  | `Inicio_Semana` |  |
| `Semana_Anio_Num` | int64 | 0 |  |  |
| `Fecha_Corta` | string |  |  |  |

**Jerarquía `Jerarquía hidrológica`:** Año hidrológico (`Año_Hidrologico`) → Semana (`Semana_Hidrologica`) → Fecha (`Fecha`)

<details><summary>Consulta de Power Query (M)</summary>

```powerquery
let
    FechaInicio = #date(2008, 1, 1),
    FechaFin    = Date.From(DateTime.LocalNow()),

    MesInicioHidro = Date.Month(InicioAnioHidrologico),
    DiaInicioHidro = Date.Day(InicioAnioHidrologico),

    ListaFechas = List.Dates(
        FechaInicio,
        Duration.Days(FechaFin - FechaInicio) + 1,
        #duration(1, 0, 0, 0)
    ),

    Tabla = Table.FromList(
        ListaFechas,
        Splitter.SplitByNothing(),
        {"Fecha"}
    ),

    TipoFecha = Table.TransformColumnTypes(
        Tabla, {{"Fecha", type date}}
    ),

    AgregaAnio = Table.AddColumn(
        TipoFecha, "Anio",
        each Date.Year([Fecha]), Int64.Type
    ),

    AgregaMes = Table.AddColumn(
        AgregaAnio, "Mes_Num",
        each Date.Month([Fecha]), Int64.Type
    ),

    AgregaNombreMes = Table.AddColumn(
        AgregaMes, "Mes_Nombre",
        each Date.ToText([Fecha], "MMMM", "es-GT"), type text
    ),

    AgregaDiaSemanaNum = Table.AddColumn(
        AgregaNombreMes, "Dia_Semana_Num",
        each Date.DayOfWeek([Fecha], Day.Monday), Int64.Type
    ),

    AgregaDiaSemana = Table.AddColumn(
        AgregaDiaSemanaNum, "Dia_Semana",
        each Date.DayOfWeekName([Fecha], "es-GT"), type text
    ),

    // Lunes de la semana a la que pertenece esta fecha
    AgregaInicioSemana = Table.AddColumn(
        AgregaDiaSemana, "Inicio_Semana",
        each Date.AddDays([Fecha], -[Dia_Semana_Num]), type date
    ),

    // Domingo de esa misma semana
    AgregaFinSemana = Table.AddColumn(
        AgregaInicioSemana, "Fin_Semana",
        each Date.AddDays([Inicio_Semana], 6), type date
    ),

    // Año hidrológico basado en Inicio_Semana
    // Si Inicio_Semana >= lunes de la semana del inicio hidrológico
    // → pertenece al año hidrológico SIGUIENTE
    AgregaAñoHidro = Table.AddColumn(
        AgregaFinSemana, "Año_Hidrologico",
        each
            let
                AnioIni     = Date.Year([Inicio_Semana]),
                InicioHidro = #date(AnioIni, MesInicioHidro, DiaInicioHidro),
                DiaSeiNov   = Date.DayOfWeek(InicioHidro, Day.Monday),
                LunesInicio = Date.AddDays(InicioHidro, -DiaSeiNov)
            in
                if [Inicio_Semana] >= LunesInicio
                then AnioIni + 1  // ← CORRECCIÓN: suma 1
                else AnioIni,
        Int64.Type
    ),

    // Semana hidrológica basada en Inicio_Semana
    // El inicio del año hidrológico es AnioH - 1
    AgregaSemanaHidro = Table.AddColumn(
        AgregaAñoHidro, "Semana_Hidrologica",
        each
            let
                AnioH       = [Año_Hidrologico] - 1,  // ← CORRECCIÓN: resta 1
                InicioHidro = #date(AnioH, MesInicioHidro, DiaInicioHidro),
                DiaSeiNov   = Date.DayOfWeek(InicioHidro, Day.Monday),
                LunesInicio = Date.AddDays(InicioHidro, -DiaSeiNov),
                Dias        = Duration.Days([Inicio_Semana] - LunesInicio)
            in
                Number.IntegerDivide(Dias, 7) + 1,
        Int64.Type
    ),

    // Etiqueta semana hidrológica
    AgregaEtiquetaSemana = Table.AddColumn(
        AgregaSemanaHidro, "Semana_Etiqueta",
        each
            Text.PadStart(Text.From([Semana_Hidrologica]), 2, "0") &
            " | " &
            Text.From([Año_Hidrologico]) &
            " (" &
            Date.ToText([Inicio_Semana], "dd-MMM", "es-GT") &
            " - " &
            Date.ToText([Fin_Semana], "dd-MMM", "es-GT") &
            ")",
        type text
    ),

    // Etiqueta semana calendario estándar
    AgregaEtiquetaSemanaAnio = Table.AddColumn(
        AgregaEtiquetaSemana, "Semana_Anio_Etiqueta",
        each
            Text.From([Anio]) &
            " - S" &
            Text.PadStart(
                Text.From(Date.WeekOfYear([Inicio_Semana], Day.Monday)),
                2, "0"
            ) &
            " (" &
            Date.ToText([Inicio_Semana], "dd-MMM", "es-GT") &
            " - " &
            Date.ToText([Fin_Semana], "dd-MMM", "es-GT") &
            ")",
        type text
    ),

    // Número de semana del año
    AgregaNumSemanaAnio = Table.AddColumn(
        AgregaEtiquetaSemanaAnio, "Semana_Anio_Num",
        each Date.WeekOfYear([Inicio_Semana], Day.Monday), Int64.Type
    ),
    //Agregar fecha corta
    AgregaFechaCorta = Table.AddColumn(
    AgregaNumSemanaAnio, "Fecha_Corta",
    each Date.ToText([Fecha], "dd-MMM", "es-GT"), type text
),

    // Ordenamiento
    #"Filas ordenadas" = Table.Sort(
        AgregaFechaCorta, {{"Fecha", Order.Descending}}
    )

in
    #"Filas ordenadas"
```
</details>


### `Direcciones_Viento`

| Columna | Tipo | Formato | Ordenar por | Notas |
|---|---|---|---|---|
| `Direccion` | string |  |  |  |
| `Desde` | double |  |  |  |
| `Hasta` | double |  |  |  |
| `Orden` | int64 | 0 |  |  |

<details><summary>Consulta de Power Query (M)</summary>

```powerquery
let
    Tabla = Table.FromRows(
        {
            {1, "N",   337.5, 22.5},
            {2, "NE",  22.5,  67.5},
            {3, "E",   67.5,  112.5},
            {4, "SE",  112.5, 157.5},
            {5, "S",   157.5, 202.5},
            {6, "SO",  202.5, 247.5},
            {7, "O",   247.5, 292.5},
            {8, "NO",  292.5, 337.5}
        },
        {"Orden", "Direccion", "Desde", "Hasta"}
    ),
    Tipos = Table.TransformColumnTypes(
        Tabla,
        {
            {"Orden",     Int64.Type},
            {"Direccion", type text},
            {"Desde",     type number},
            {"Hasta",     type number}
        }
    )
in
    Tipos
```
</details>


### `Estaciones_met`

| Columna | Tipo | Formato | Ordenar por | Notas |
|---|---|---|---|---|
| `estacionid` | int64 | 0 |  |  |
| `estrato_id` | int64 | 0 |  |  |
| `codigo` | string |  |  |  |
| `finca` | string |  |  |  |
| `latitud` | double |  |  |  |
| `longitud` | double |  |  |  |
| `altitud` | int64 | 0 |  |  |
| `activa` | boolean | """TRUE"";""TRUE"";""FALSE""" |  |  |
| `redmet` | boolean | """TRUE"";""TRUE"";""FALSE""" |  |  |
| `pais_id` | int64 | 0 |  |  |
| `pais.id` | int64 | 0 |  |  |
| `pais.nombre` | string |  |  |  |
| `estrato.id` | int64 | 0 |  |  |
| `estrato.nombre` | string |  |  |  |

<details><summary>Consulta de Power Query (M)</summary>

```powerquery
let
    Origen = Json.Document(Web.Contents(
        "https://redmet.icc.org.gt/ws/redmet/estaciones", 
        [Headers=[Accept="Application/json"]]
    )),
    #"Convertida en tabla" = Table.FromRecords({Origen}),
    #"Expandir estaciones" = Table.ExpandListColumn(
        #"Convertida en tabla", "estaciones"
    ),
    #"Expandir campos" = Table.ExpandRecordColumn(
        #"Expandir estaciones", "estaciones",
        {
            "estacionid", "estrato_id", "codigo", "finca",
            "latitud", "longitud", "altitud", "activa", "redmet",
            "pais_id", "pais", "estrato"
        },
        {
            "estacionid", "estrato_id", "codigo", "finca",
            "latitud", "longitud", "altitud", "activa", "redmet",
            "pais_id", "pais", "estrato"
        }
    ),
    #"Expandir pais" = Table.ExpandRecordColumn(
        #"Expandir campos", "pais",
        {"id", "nombre"},
        {"pais.id", "pais.nombre"}
    ),
    #"Expandir estrato" = Table.ExpandRecordColumn(
        #"Expandir pais", "estrato",
        {"id", "nombre"},
        {"estrato.id", "estrato.nombre"}
    ),
    #"Tipos correctos" = Table.TransformColumnTypes(
        #"Expandir estrato",
        {
            // claves — todas Int64 para que relacionen con las Facts
            {"estacionid",  Int64.Type},
            {"estrato_id",  Int64.Type},
            {"pais_id",     Int64.Type},
            {"pais.id",     Int64.Type},
            {"estrato.id",  Int64.Type},
            // descriptivos
            {"codigo",          type text},
            {"finca",           type text},
            {"pais.nombre",     type text},
            {"estrato.nombre",  type text},
            // geográficos
            {"latitud",   type number},
            {"longitud",  type number},
            {"altitud",   Int64.Type},
            // flags
            {"activa",  type logical},
            {"redmet",  type logical}
        }
    )
in
    #"Tipos correctos"
```
</details>


### `Fact_Diaria_met` — actualización incremental

| Columna | Tipo | Formato | Ordenar por | Notas |
|---|---|---|---|---|
| `estacionid` | int64 | 0 |  |  |
| `Fecha` | dateTime | Long Date |  |  |
| `Temp_Max` | double |  |  |  |
| `Temp_Min` | double |  |  |  |
| `Temp_Media` | double |  |  |  |
| `HR_Media` | double |  |  |  |
| `HR_Min` | double |  |  |  |
| `Precip_Total` | double |  |  |  |
| `Viento_Media` | double |  |  |  |
| `ETO_Total` | double |  |  |  |
| `Balance_Hidrico` | double |  |  |  |
| `Rad_Total` | double |  |  |  |
| `HR_Max` | double |  |  |  |
| `Rad_MJ` | double |  |  |  |
| `Amplitud_Termica` | double |  |  |  |
| `Dia_Seco` | boolean | """TRUE"";""TRUE"";""FALSE""" |  |  |
| `GDD_Base10` | double |  |  |  |
| `GDD_Base15` | double |  |  |  |
| `GDD_Cana_ST` | double |  |  |  |
| `GDD_Banano_ST` | double |  |  |  |
| `GDD_Aguacate_ST` | double |  |  |  |
| `GDD_Palma_ST` | double |  |  |  |
| `GDD_Maiz_ST` | double |  |  |  |

<details><summary>Consulta de Power Query (M)</summary>

```powerquery
let
    Fuente = TablaEstaciones_met,

    EjecutarAPI = Table.AddColumn(
        Fuente,
        "Lecturas",
        each fxLecturasEstacion_met_diario([estacionid], RangeStart, RangeEnd)
    ),

    ExpandirLista = Table.ExpandListColumn(EjecutarAPI, "Lecturas"),

    ExpandirCampos = Table.ExpandRecordColumn(
        ExpandirLista,
        "Lecturas",
        {
            "dia", "tempavg", "tempmin", "tempmax",
            "radiaciontotal", "humedadavg", "humedadmin", "humedadmax",
            "vientoavg", "lluviasum", "etosum"
        },
        {
            "Fecha", "Temp_Media", "Temp_Min", "Temp_Max",
            "Rad_Total", "HR_Media", "HR_Min", "HR_Max",
            "Viento_Media", "Precip_Total", "ETO_Total"
        }
    ),

    // ETO llega como texto; vacíos quedan null (no 0)
    ConvertirTextos = Table.TransformColumnTypes(
        ExpandirCampos,
        {{"ETO_Total", type text}}
    ),

    ReemplazarNulos = Table.ReplaceValue(
        ConvertirTextos,
        null, null, Replacer.ReplaceValue,
        {"ETO_Total"}
    ),

    ReemplazarVacios = Table.ReplaceValue(
        ReemplazarNulos,
        "", null, Replacer.ReplaceValue,
        {"ETO_Total"}
    ),

    CambiarTipos = Table.TransformColumnTypes(
        ReemplazarVacios,
        {
            {"estacionid",  Int64.Type},
            {"Fecha",       type date},
            {"Temp_Media",  type number},
            {"Temp_Min",    type number},
            {"Temp_Max",    type number},
            {"Rad_Total",   type number},
            {"HR_Media",    type number},
            {"HR_Min",      type number},
            {"HR_Max",      type number},
            {"Viento_Media",type number},
            {"Precip_Total",type number},
            {"ETO_Total",   type number}
        }
    ),

    // ── FILTRO INCREMENTAL PRIMERO ────────────────────────────────────
    FiltrarIncremental = Table.SelectRows(
        CambiarTipos,
        each
            [Fecha] >= Date.From(List.Max({RangeStart, #datetime(2008, 1, 1, 0, 0, 0)})) and
            [Fecha] < Date.From(RangeEnd)
    ),

    // Radiación en MJ/m²/día: Σ lecturas 15 min (W/m²) × 900 s / 1e6
    AgregarRad_MJ = Table.AddColumn(
        FiltrarIncremental, "Rad_MJ",
        each [Rad_Total] * 900 / 1000000, type number
    ),

    // Amplitud térmica
    AgregarAmplitud = Table.AddColumn(
        AgregarRad_MJ, "Amplitud_Termica",
        each [Temp_Max] - [Temp_Min], type number
    ),

    // Balance hídrico diario
    AgregarBalance = Table.AddColumn(
        AgregarAmplitud, "Balance_Hidrico",
        each [Precip_Total] - [ETO_Total], type number
    ),

    // Día seco
    AgregarDiaSeco = Table.AddColumn(
        AgregarBalance, "Dia_Seco",
        each [Precip_Total] < 1, type logical
    ),

    // GDD base 10°C
    AgregarGDD_Base10 = Table.AddColumn(
        AgregarDiaSeco, "GDD_Base10",
        each
            let gdd = [Temp_Media] - 10
            in if gdd > 0 then gdd else 0,
        type number
    ),

    // GDD base 15°C
    AgregarGDD_Base15 = Table.AddColumn(
        AgregarGDD_Base10, "GDD_Base15",
        each
            let gdd = [Temp_Media] - 15
            in if gdd > 0 then gdd else 0,
        type number
    ),

    // Suma térmica caña (base 10, óptima 34)
    AgregarGDD_Cana_ST = Table.AddColumn(
        AgregarGDD_Base15, "GDD_Cana_ST",
        each
            if [Temp_Media] <= 10 then 0
            else if [Temp_Media] >= 34 then 34 - 10
            else [Temp_Media] - 10,
        type number
    ),

    // Suma térmica banano (base 15, óptima 28)
    AgregarGDD_Banano_ST = Table.AddColumn(
        AgregarGDD_Cana_ST, "GDD_Banano_ST",
        each
            if [Temp_Media] <= 15 then 0
            else if [Temp_Media] >= 28 then 28 - 15
            else [Temp_Media] - 15,
        type number
    ),

    // Suma térmica aguacate (base 10, óptima 24)
    AgregarGDD_Aguacate_ST = Table.AddColumn(
        AgregarGDD_Banano_ST, "GDD_Aguacate_ST",
        each
            if [Temp_Media] <= 10 then 0
            else if [Temp_Media] >= 24 then 24 - 10
            else [Temp_Media] - 10,
        type number
    ),

    // Suma térmica palma (base 15, óptima 30)
    AgregarGDD_Palma_ST = Table.AddColumn(
        AgregarGDD_Aguacate_ST, "GDD_Palma_ST",
        each
            if [Temp_Media] <= 15 then 0
            else if [Temp_Media] >= 30 then 30 - 15
            else [Temp_Media] - 15,
        type number
    ),

    // Suma térmica maíz (base 10, óptima 30)
    AgregarGDD_Maiz_ST = Table.AddColumn(
        AgregarGDD_Palma_ST, "GDD_Maiz_ST",
        each
            if [Temp_Media] <= 10 then 0
            else if [Temp_Media] >= 30 then 30 - 10
            else [Temp_Media] - 10,
        type number
    )

in
    AgregarGDD_Maiz_ST
```
</details>


### `Fact_Horaria_riesgo` — actualización incremental

| Columna | Tipo | Formato | Ordenar por | Notas |
|---|---|---|---|---|
| `estacionid` | int64 | 0 |  |  |
| `Fecha` | dateTime | Long Date |  |  |
| `Hora` | int64 | 0 |  |  |
| `Temp_Media` | double |  |  |  |
| `HR_Media` | double |  |  |  |
| `Mojadura_Max` | double |  |  |  |
| `Precip_Total` | double |  |  |  |
| `Flag_Roya` | int64 | 0 |  |  |
| `Flag_Salivosa` | int64 | 0 |  |  |
| `Flag_Barrenador` | int64 | 0 |  |  |
| `Flag_Carbon` | int64 | 0 |  |  |
| `Indice_Riesgo` | int64 | 0 |  |  |
| `Viento_Media` | double | 0.0 |  |  |
| `Dir_Viento` | double | 0 |  |  |
| `Sector_Viento` | int64 | 0 |  |  |

<details><summary>Consulta de Power Query (M)</summary>

```powerquery
let
    // Lecturas de 15 min directo de la API (misma función que Fact_Subdiaria_met_aux)
    Fuente = TablaEstaciones_met,

    EjecutarAPI = Table.AddColumn(
        Fuente,
        "Lecturas",
        each fxLecturasEstacion_met([estacionid], RangeStart, RangeEnd)
    ),

    ExpandirLista = Table.ExpandListColumn(EjecutarAPI, "Lecturas"),

    ExpandirCampos = Table.ExpandRecordColumn(
        ExpandirLista,
        "Lecturas",
        {
            "fecha", "temperatura", "humedad_relativa",
            "mojadura", "precipitacion",
            "velocidad_viento", "direccion_viento"
        }
    ),

    CambiarTipos = Table.TransformColumnTypes(
        ExpandirCampos,
        {
            {"estacionid",       Int64.Type},
            {"fecha",            type datetime},
            {"temperatura",      type number},
            {"humedad_relativa", type number},
            {"mojadura",         type number},
            {"precipitacion",    type number},
            {"velocidad_viento", type number},
            {"direccion_viento", type number}
        }
    ),

    // ── FILTRO INCREMENTAL ────────────────────────────────────────────
    FiltrarIncremental = Table.SelectRows(
        CambiarTipos,
        each
            [fecha] >= List.Max({RangeStart, #datetime(2008, 1, 1, 0, 0, 0)}) and
            [fecha] < RangeEnd
    ),

    SeleccionarColumnas = Table.AddColumn(
        FiltrarIncremental, "Fecha",
        each Date.From([fecha]), type date
    ),

    // Extraer hora
    AgregarHora = Table.AddColumn(
        SeleccionarColumnas, "Hora",
        each Time.Hour(DateTime.Time([fecha])), Int64.Type
    ),

    // Componentes vectoriales del viento ponderadas por velocidad
    // (direccion_viento = de donde sopla, grados desde el N en sentido horario)
    AgregarU = Table.AddColumn(
        AgregarHora, "Viento_U",
        each if [velocidad_viento] <> null and [direccion_viento] <> null
             then [velocidad_viento] * Number.Sin([direccion_viento] * Number.PI / 180)
             else null,
        type number
    ),
    AgregarV = Table.AddColumn(
        AgregarU, "Viento_V",
        each if [velocidad_viento] <> null and [direccion_viento] <> null
             then [velocidad_viento] * Number.Cos([direccion_viento] * Number.PI / 180)
             else null,
        type number
    ),

    // Agrupar por estacion + fecha + hora
    Agrupado = Table.Group(
        AgregarV,
        {"estacionid", "Fecha", "Hora"},
        {
            {"Temp_Media",    each List.Average([temperatura]),      type number},
            {"HR_Media",      each List.Average([humedad_relativa]), type number},
            {"Mojadura_Max",  each List.Max([mojadura]),             type number},
            {"Precip_Total",  each List.Sum([precipitacion]),        type number},
            {"Viento_Media",  each List.Average([velocidad_viento]),  type number},
            {"Viento_U",      each List.Sum([Viento_U]),               type number},
            {"Viento_V",      each List.Sum([Viento_V]),               type number}
        }
    ),


    // Dirección resultante horaria (0-360°) y sector de 45° (1=N ... 8=NO)
    AgregarDir = Table.AddColumn(
        Agrupado, "Dir_Viento",
        each if [Viento_U] = null or [Viento_V] = null or ([Viento_U] = 0 and [Viento_V] = 0)
             then null
             else Number.Mod(Number.Atan2([Viento_U], [Viento_V]) * 180 / Number.PI + 360, 360),
        type number
    ),
    AgregarSector = Table.AddColumn(
        AgregarDir, "Sector_Viento",
        each if [Dir_Viento] = null then null
             else Number.Mod(Number.RoundDown(([Dir_Viento] + 22.5) / 45), 8) + 1,
        Int64.Type
    ),
    QuitarUV = Table.RemoveColumns(AgregarSector, {"Viento_U", "Viento_V"}),

    // Flags de condición por hora
    AgregarRoya = Table.AddColumn(
        QuitarUV, "Flag_Roya",
        each if [Temp_Media] <> null and [HR_Media] <> null and [Mojadura_Max] <> null
             and [Temp_Media] >= 15 and [Temp_Media] <= 25
             and [HR_Media] > 80
             and [Mojadura_Max] > 4
             then 1 else 0,
        Int64.Type
    ),

    AgregarSalivosa = Table.AddColumn(
        AgregarRoya, "Flag_Salivosa",
        each if [Temp_Media] <> null and [HR_Media] <> null and [Precip_Total] <> null
             and [Temp_Media] >= 22 and [Temp_Media] <= 28
             and [HR_Media] > 80
             and [Precip_Total] > 0
             then 1 else 0,
        Int64.Type
    ),

    AgregarBarrenador = Table.AddColumn(
        AgregarSalivosa, "Flag_Barrenador",
        each if [Temp_Media] <> null and [HR_Media] <> null and [Precip_Total] <> null
             and [Temp_Media] > 24
             and [HR_Media] >= 60 and [HR_Media] <= 80
             and [Precip_Total] < 1
             then 1 else 0,
        Int64.Type
    ),

    AgregarCarbon = Table.AddColumn(
        AgregarBarrenador, "Flag_Carbon",
        each if [Temp_Media] <> null and [Precip_Total] <> null
             and [Temp_Media] >= 25 and [Temp_Media] <= 30
             and [Precip_Total] < 1
             then 1 else 0,
        Int64.Type
    ),

    AgregarIndice = Table.AddColumn(
        AgregarCarbon, "Indice_Riesgo",
        each [Flag_Roya] + [Flag_Salivosa] + [Flag_Barrenador] + [Flag_Carbon],
        Int64.Type
    ),

    TiposFinales = Table.TransformColumnTypes(
        AgregarIndice,
        {
            {"estacionid", Int64.Type},
            {"Fecha",      type date},
            {"Hora",       Int64.Type}
        }
    )

in
    TiposFinales
```
</details>


### `Fact_Meteorologia` — actualización incremental

| Columna | Tipo | Formato | Ordenar por | Notas |
|---|---|---|---|---|
| `estacionid` | int64 | 0 |  |  |
| `fecha` | dateTime | General Date |  |  |
| `temperatura` | double |  |  |  |
| `radiacion` | double |  |  |  |
| `humedad_relativa` | double | 0 |  |  |
| `precipitacion` | double |  |  |  |
| `velocidad_viento` | double |  |  |  |
| `presion_atmosferica` | double |  |  |  |
| `mojadura` | double | 0 |  |  |
| `direccion_viento` | double |  |  |  |
| `eto` | double |  |  |  |
| `indice_calor` | double |  |  |  |
| `updated_at` | dateTime | General Date |  |  |
| `created_at` | dateTime | General Date |  |  |
| `Fecha 2` | dateTime | Long Date |  |  |

<details><summary>Consulta de Power Query (M)</summary>

```powerquery
let
    Fuente = TablaEstaciones_met,

    EjecutarAPI = Table.AddColumn(
        Fuente,
        "Lecturas",
        each fxLecturasEstacion_met([estacionid], RangeStart, RangeEnd)
    ),

    ExpandirLista = Table.ExpandListColumn(EjecutarAPI, "Lecturas"),

    ExpandirCampos = Table.ExpandRecordColumn(
        ExpandirLista,
        "Lecturas",
        {
            "fecha", "temperatura", "radiacion",
            "humedad_relativa", "precipitacion", "velocidad_viento",
            "presion_atmosferica", "mojadura", "direccion_viento",
            "eto", "indice_calor", "updated_at", "created_at"
        }
    ),

    CambiarTipos = Table.TransformColumnTypes(
        ExpandirCampos,
        {
            {"estacionid",          Int64.Type},
            {"fecha",               type datetime},
            {"temperatura",         type number},
            {"radiacion",           type number},
            {"humedad_relativa",    type number},
            {"precipitacion",       type number},
            {"velocidad_viento",    type number},
            {"presion_atmosferica", type number},
            {"mojadura",            type number},
            {"direccion_viento",    type number},
            {"eto",                 type number},
            {"indice_calor",        type number},
            {"updated_at",          type datetime},
            {"created_at",          type datetime}
        }
    ),

    // ── FILTRO INCREMENTAL PRIMERO ────────────────────────────────────
    FiltrarIncremental = Table.SelectRows(
        CambiarTipos,
        each
            [fecha] >= List.Max({RangeStart, #datetime(2008, 1, 1, 0, 0, 0)}) and
            [fecha] < RangeEnd
    ),

    // Columna Fecha tipo date para relacionar con Calendario
    AgregarFecha = Table.AddColumn(
        FiltrarIncremental, "Fecha",
        each Date.From([fecha]), type date
    )

in
    AgregarFecha
```
</details>


### `Fact_Subdiaria_met_aux` — actualización incremental

| Columna | Tipo | Formato | Ordenar por | Notas |
|---|---|---|---|---|
| `estacionid` | int64 | 0 |  |  |
| `Fecha` | dateTime | Long Date |  |  |
| `N_Lecturas` | int64 | 0 |  |  |
| `Precip_Max15min` | double |  |  |  |
| `Dia_Completo` | boolean | """TRUE"";""TRUE"";""FALSE""" |  |  |
| `Viento_Max` | double |  |  |  |
| `Temp_Nocturna_Media` | double |  |  |  |
| `Rad_Media_Diurna` | double |  |  |  |
| `Rad_Max_Diurna` | double |  |  |  |
| `IC_Max_Diurno` | double |  |  |  |
| `IC_Media_Diurno` | double |  |  |  |
| `Mojadura_Horas_Diurna` | double |  |  |  |
| `Brillo_Solar_Horas` | double |  |  |  |
| `Horas_Estres_Termico` | double |  |  |  |
| `VPD_Media_Diurna` | double |  |  |  |
| `VPD_Max_Diurna` | double |  |  |  |
| `Mojadura_Horas_Total` | double |  |  |  |
| `Mojadura_Horas_Nocturna` | double |  |  |  |
| `VPD_Media_Nocturna` | double |  |  |  |
| `Hora_Viento_Max` | int64 | 0 |  |  |
| `Direccion_Viento_Max` | double |  |  |  |
| `Viento_Max_Diurno` | double |  |  |  |
| `Viento_Media_Diurna` | double |  |  |  |
| `Direccion_Predominante_Diurna` | double |  |  |  |
| `Viento_Max_Nocturno` | double |  |  |  |
| `Viento_Media_Nocturna` | double |  |  |  |
| `Temp_Min_Nocturna` | double |  |  |  |
| `Hora_Temp_Max_Diurna` | int64 | 0 |  |  |
| `Hora_VPD_Max_Diurna` | int64 | 0 |  |  |
| `Hora_IC_Max_Diurno` | int64 | 0 |  |  |
| `Hora_Temp_Min_Nocturna` | int64 | 0 |  |  |
| `Hora_ETO_Max_Diurna` | int64 | 0 |  |  |
| `Hora_Inicio_Mojadura` | int64 | 0 |  |  |
| `Hora_Fin_Mojadura` | int64 | 0 |  |  |
| `ETO_Max_Diurna` | double |  |  |  |
| `ETO_Acum_Diurna` | double |  |  |  |
| `ETO_Acum_Nocturna` | double |  |  |  |
| `VPD_Min_Nocturno` | double |  |  |  |
| `Hora_Inicio_Luz` | double | 0.00 |  |  |
| `Hora_Fin_Luz` | double | 0.00 |  |  |
| `Duracion_Luz_h` | double | 0.00 |  |  |
| `Rad_Media_Luz` | double | 0.0 |  |  |
| `Energia_Luz_MJ` | double | 0.00 |  |  |

<details><summary>Consulta de Power Query (M)</summary>

```powerquery
let
    Fuente = TablaEstaciones_met,

    EjecutarAPI = Table.AddColumn(
        Fuente,
        "Lecturas",
        each fxLecturasEstacion_met([estacionid], RangeStart, RangeEnd)
    ),

    ExpandirLista = Table.ExpandListColumn(EjecutarAPI, "Lecturas"),

    ExpandirCampos = Table.ExpandRecordColumn(
        ExpandirLista,
        "Lecturas",
        {
            "fecha", "precipitacion", "velocidad_viento",
            "temperatura", "radiacion", "humedad_relativa",
            "mojadura", "indice_calor", "direccion_viento", "eto"
        },
        {
            "fecha", "precipitacion", "velocidad_viento",
            "temperatura", "radiacion", "humedad_relativa",
            "mojadura", "indice_calor", "direccion_viento", "eto"
        }
    ),

    CambiarTipos = Table.TransformColumnTypes(
        ExpandirCampos,
        {
            {"estacionid",       Int64.Type},
            {"fecha",            type datetime},
            {"precipitacion",    type number},
            {"velocidad_viento", type number},
            {"temperatura",      type number},
            {"radiacion",        type number},
            {"humedad_relativa", type number},
            {"mojadura",         type number},
            {"indice_calor",     type number},
            {"direccion_viento", type number},
            {"eto",              type number}
        }
    ),

    FiltrarIncremental = Table.SelectRows(
        CambiarTipos,
        each
            [fecha] >= List.Max({RangeStart, #datetime(2008, 1, 1, 0, 0, 0)}) and
            [fecha] < RangeEnd
    ),

    AgregarFecha = Table.AddColumn(
        FiltrarIncremental, "Fecha",
        each Date.From([fecha]), type date
    ),

    AgregarHora = Table.AddColumn(
        AgregarFecha, "Hora",
        each Time.Hour(DateTime.Time([fecha])), Int64.Type
    ),

    AgregarEsDiurno = Table.AddColumn(
        AgregarHora, "Es_Diurno",
        each [Hora] >= 6 and [Hora] <= 18, type logical
    ),

    AgregarEsNocturno = Table.AddColumn(
        AgregarEsDiurno, "Es_Nocturno",
        each [Hora] >= 19 or [Hora] < 6, type logical
    ),

    AgregarVPD = Table.AddColumn(
        AgregarEsNocturno, "VPD",
        each
            let
                T  = [temperatura],
                HR = [humedad_relativa],
                es = 0.6108 * Number.Exp(17.27 * T / (T + 237.3))
            in
                (1 - HR / 100) * es,
        type number
    ),

    AgregarMojadura_Flag = Table.AddColumn(
        AgregarVPD, "Mojadura_Flag",
        each if [mojadura] <> null and [mojadura] > 4 then 0.25 else 0,
        type number
    ),

    AgregarBrillo_Flag = Table.AddColumn(
        AgregarMojadura_Flag, "Brillo_Flag",
        each if [radiacion] <> null and [radiacion] > 40 then 0.25 else 0,
        type number
    ),

    AgregarEstres_Flag = Table.AddColumn(
        AgregarBrillo_Flag, "Estres_Flag",
        each if [temperatura] <> null and [radiacion] <> null and [temperatura] > 35 and [radiacion] > 800 then 0.25 else 0,
        type number
    ),

    Agrupado = Table.Group(
        AgregarEstres_Flag,
        {"estacionid", "Fecha"},
        {
            // ── Control de calidad ────────────────────────────────────
            {"N_Lecturas",
                each Table.RowCount(_),
                Int64.Type},

            // ── Variables generales ───────────────────────────────────
            {"Precip_Max15min",
                each List.Max([precipitacion]),
                type number},

            // ── Viento general ────────────────────────────────────────
            {"Viento_Max",
                each List.Max([velocidad_viento]),
                type number},

            {"Hora_Viento_Max",
                each
                    let
                        maxV  = List.Max([velocidad_viento]),
                        pares = List.Select(
                            List.Zip({[velocidad_viento], [Hora]}),
                            each _{0} = maxV
                        )
                    in
                        if List.IsEmpty(pares) then null
                        else List.First(pares){1},
                Int64.Type},

            {"Direccion_Viento_Max",
                each
                    let
                        maxV  = List.Max([velocidad_viento]),
                        pares = List.Select(
                            List.Zip({[velocidad_viento], [direccion_viento]}),
                            each _{0} = maxV
                        )
                    in
                        if List.IsEmpty(pares) then null
                        else List.First(pares){1},
                type number},

            // ── Viento diurno ─────────────────────────────────────────
            {"Viento_Max_Diurno",
                each
                    let
                        pares = List.Select(
                            List.Zip({[velocidad_viento], [Es_Diurno]}),
                            each _{1} = true
                        )
                    in
                        if List.IsEmpty(pares) then null
                        else List.Max(List.Transform(pares, each _{0})),
                type number},

            {"Viento_Media_Diurna",
                each
                    let
                        pares = List.Select(
                            List.Zip({[velocidad_viento], [Es_Diurno]}),
                            each _{1} = true
                        )
                    in
                        if List.IsEmpty(pares) then null
                        else List.Average(List.Transform(pares, each _{0})),
                type number},

            {"Direccion_Predominante_Diurna",
                each
                    let
                        // promedio vectorial ponderado por velocidad (no aritmético)
                        pares = List.Select(
                            List.Zip({[velocidad_viento], [direccion_viento], [Es_Diurno]}),
                            each _{2} = true and _{0} <> null and _{1} <> null
                        ),
                        u = List.Sum(List.Transform(pares, each _{0} * Number.Sin(_{1} * Number.PI / 180))),
                        v = List.Sum(List.Transform(pares, each _{0} * Number.Cos(_{1} * Number.PI / 180)))
                    in
                        if List.IsEmpty(pares) or (u = 0 and v = 0) then null
                        else Number.Mod(Number.Atan2(u, v) * 180 / Number.PI + 360, 360),
                type number},

            // ── Viento nocturno ───────────────────────────────────────
            {"Viento_Max_Nocturno",
                each
                    let
                        pares = List.Select(
                            List.Zip({[velocidad_viento], [Es_Nocturno]}),
                            each _{1} = true
                        )
                    in
                        if List.IsEmpty(pares) then null
                        else List.Max(List.Transform(pares, each _{0})),
                type number},

            {"Viento_Media_Nocturna",
                each
                    let
                        pares = List.Select(
                            List.Zip({[velocidad_viento], [Es_Nocturno]}),
                            each _{1} = true
                        )
                    in
                        if List.IsEmpty(pares) then null
                        else List.Average(List.Transform(pares, each _{0})),
                type number},

            // ── Temperatura nocturna ──────────────────────────────────
            {"Temp_Nocturna_Media",
                each
                    let
                        pares = List.Select(
                            List.Zip({[temperatura], [Es_Nocturno]}),
                            each _{1} = true
                        )
                    in
                        if List.IsEmpty(pares) then null
                        else List.Average(List.Transform(pares, each _{0})),
                type number},

            {"Temp_Min_Nocturna",
                each
                    let
                        pares = List.Select(
                            List.Zip({[temperatura], [Es_Nocturno]}),
                            each _{1} = true
                        )
                    in
                        if List.IsEmpty(pares) then null
                        else List.Min(List.Transform(pares, each _{0})),
                type number},

            // ── Horas de extremos ─────────────────────────────────────
            {"Hora_Temp_Max_Diurna",
                each
                    let
                        pares   = List.Select(
                            List.Zip({[temperatura], [Hora], [Es_Diurno]}),
                            each _{2} = true
                        ),
                        maxT    = if List.IsEmpty(pares) then null
                                  else List.Max(List.Transform(pares, each _{0})),
                        horaMax = List.Select(pares, each _{0} = maxT)
                    in
                        if List.IsEmpty(horaMax) then null
                        else List.First(horaMax){1},
                Int64.Type},

            {"Hora_VPD_Max_Diurna",
                each
                    let
                        pares   = List.Select(
                            List.Zip({[VPD], [Hora], [Es_Diurno]}),
                            each _{2} = true
                        ),
                        maxV    = if List.IsEmpty(pares) then null
                                  else List.Max(List.Transform(pares, each _{0})),
                        horaMax = List.Select(pares, each _{0} = maxV)
                    in
                        if List.IsEmpty(horaMax) then null
                        else List.First(horaMax){1},
                Int64.Type},

            {"Hora_IC_Max_Diurno",
                each
                    let
                        pares   = List.Select(
                            List.Zip({[indice_calor], [Hora], [Es_Diurno]}),
                            each _{2} = true
                        ),
                        maxIC   = if List.IsEmpty(pares) then null
                                  else List.Max(List.Transform(pares, each _{0})),
                        horaMax = List.Select(pares, each _{0} = maxIC)
                    in
                        if List.IsEmpty(horaMax) then null
                        else List.First(horaMax){1},
                Int64.Type},

            {"Hora_Temp_Min_Nocturna",
                each
                    let
                        pares   = List.Select(
                            List.Zip({[temperatura], [Hora], [Es_Nocturno]}),
                            each _{2} = true
                        ),
                        minT    = if List.IsEmpty(pares) then null
                                  else List.Min(List.Transform(pares, each _{0})),
                        horaMin = List.Select(pares, each _{0} = minT)
                    in
                        if List.IsEmpty(horaMin) then null
                        else List.First(horaMin){1},
                Int64.Type},

            {"Hora_ETO_Max_Diurna",
                each
                    let
                        pares   = List.Select(
                            List.Zip({[eto], [Hora], [Es_Diurno]}),
                            each _{2} = true
                        ),
                        maxETO  = if List.IsEmpty(pares) then null
                                  else List.Max(List.Transform(pares, each _{0})),
                        horaMax = List.Select(pares, each _{0} = maxETO)
                    in
                        if List.IsEmpty(horaMax) then null
                        else List.First(horaMax){1},
                Int64.Type},

            // ── Mojadura ──────────────────────────────────────────────
            {"Mojadura_Horas_Total",
                each List.Sum([Mojadura_Flag]),
                type number},

            {"Mojadura_Horas_Diurna",
                each
                    let
                        pares = List.Select(
                            List.Zip({[Mojadura_Flag], [Es_Diurno]}),
                            each _{1} = true
                        )
                    in
                        List.Sum(List.Transform(pares, each _{0})),
                type number},

            {"Mojadura_Horas_Nocturna",
                each
                    let
                        pares = List.Select(
                            List.Zip({[Mojadura_Flag], [Es_Nocturno]}),
                            each _{1} = true
                        )
                    in
                        List.Sum(List.Transform(pares, each _{0})),
                type number},

            {"Hora_Inicio_Mojadura",
                each
                    let
                        pares = List.Select(
                            List.Zip({[Mojadura_Flag], [Hora]}),
                            each _{0} > 0
                        )
                    in
                        if List.IsEmpty(pares) then null
                        else List.Min(List.Transform(pares, each _{1})),
                Int64.Type},

            {"Hora_Fin_Mojadura",
                each
                    let
                        pares = List.Select(
                            List.Zip({[Mojadura_Flag], [Hora]}),
                            each _{0} > 0
                        )
                    in
                        if List.IsEmpty(pares) then null
                        else List.Max(List.Transform(pares, each _{1})),
                Int64.Type},

            // ── Radiación diurna ──────────────────────────────────────
            {"Rad_Media_Diurna",
                each
                    let
                        pares = List.Select(
                            List.Zip({[radiacion], [Es_Diurno]}),
                            each _{1} = true
                        )
                    in
                        if List.IsEmpty(pares) then null
                        else List.Average(List.Transform(pares, each _{0})),
                type number},

            {"Rad_Max_Diurna",
                each
                    let
                        pares = List.Select(
                            List.Zip({[radiacion], [Es_Diurno]}),
                            each _{1} = true
                        )
                    in
                        if List.IsEmpty(pares) then null
                        else List.Max(List.Transform(pares, each _{0})),
                type number},

            // ── Periodo de luz (radiación > 40 W/m²) ─────────────────
            // La luz define el periodo diurno: de la primera a la última lectura > 40 W/m².
            {"Hora_Inicio_Luz",
                each
                    let
                        t = List.Transform(
                                List.Select(List.Zip({[radiacion], [fecha]}), each _{0} <> null and _{0} > 40),
                                each Time.Hour(DateTime.Time(_{1})) + Time.Minute(DateTime.Time(_{1})) / 60)
                    in
                        if List.IsEmpty(t) then null else List.Min(t),
                type number},
            {"Hora_Fin_Luz",
                each
                    let
                        t = List.Transform(
                                List.Select(List.Zip({[radiacion], [fecha]}), each _{0} <> null and _{0} > 40),
                                each Time.Hour(DateTime.Time(_{1})) + Time.Minute(DateTime.Time(_{1})) / 60)
                    in
                        if List.IsEmpty(t) then null else List.Max(t),
                type number},
            // Irradiancia media de las lecturas disponibles DENTRO del periodo de luz
            // (incluye bajones por nubosidad; los faltantes no cuentan como cero)
            {"Rad_Media_Luz",
                each
                    let
                        hora   = (d) => Time.Hour(DateTime.Time(d)) + Time.Minute(DateTime.Time(d)) / 60,
                        pares  = List.Select(List.Zip({[radiacion], [fecha]}), each _{0} <> null),
                        luz    = List.Transform(List.Select(pares, each _{0} > 40), each hora(_{1})),
                        ini    = if List.IsEmpty(luz) then null else List.Min(luz),
                        fin    = if List.IsEmpty(luz) then null else List.Max(luz),
                        dentro = if ini = null then {} else
                                 List.Select(pares, each hora(_{1}) >= ini and hora(_{1}) <= fin)
                    in
                        if List.IsEmpty(dentro) then null
                        else List.Average(List.Transform(dentro, each _{0})),
                type number},

            // ── Índice de calor diurno ────────────────────────────────
            {"IC_Max_Diurno",
                each
                    let
                        pares = List.Select(
                            List.Zip({[indice_calor], [Es_Diurno]}),
                            each _{1} = true
                        )
                    in
                        if List.IsEmpty(pares) then null
                        else List.Max(List.Transform(pares, each _{0})),
                type number},

            {"IC_Media_Diurno",
                each
                    let
                        pares = List.Select(
                            List.Zip({[indice_calor], [Es_Diurno]}),
                            each _{1} = true
                        )
                    in
                        if List.IsEmpty(pares) then null
                        else List.Average(List.Transform(pares, each _{0})),
                type number},

            // ── Brillo solar y estrés térmico ─────────────────────────
            {"Brillo_Solar_Horas",
                each List.Sum([Brillo_Flag]),
                type number},

            {"Horas_Estres_Termico",
                each List.Sum([Estres_Flag]),
                type number},

            // ── ETO subdiaria ─────────────────────────────────────────
            {"ETO_Max_Diurna",
                each
                    let
                        pares = List.Select(
                            List.Zip({[eto], [Es_Diurno]}),
                            each _{1} = true
                        )
                    in
                        if List.IsEmpty(pares) then null
                        else List.Max(List.Transform(pares, each _{0})),
                type number},

            {"ETO_Acum_Diurna",
                each
                    let
                        pares = List.Select(
                            List.Zip({[eto], [Es_Diurno]}),
                            each _{1} = true
                        )
                    in
                        if List.IsEmpty(pares) then null
                        else List.Sum(List.Transform(pares, each _{0})),
                type number},

            {"ETO_Acum_Nocturna",
                each
                    let
                        pares = List.Select(
                            List.Zip({[eto], [Es_Nocturno]}),
                            each _{1} = true
                        )
                    in
                        if List.IsEmpty(pares) then null
                        else List.Sum(List.Transform(pares, each _{0})),
                type number},

            // ── VPD diurno ────────────────────────────────────────────
            {"VPD_Media_Diurna",
                each
                    let
                        pares = List.Select(
                            List.Zip({[VPD], [Es_Diurno]}),
                            each _{1} = true
                        )
                    in
                        if List.IsEmpty(pares) then null
                        else List.Average(List.Transform(pares, each _{0})),
                type number},

            {"VPD_Max_Diurna",
                each
                    let
                        pares = List.Select(
                            List.Zip({[VPD], [Es_Diurno]}),
                            each _{1} = true
                        )
                    in
                        if List.IsEmpty(pares) then null
                        else List.Max(List.Transform(pares, each _{0})),
                type number},

            // ── VPD nocturno ──────────────────────────────────────────
            {"VPD_Media_Nocturna",
                each
                    let
                        pares = List.Select(
                            List.Zip({[VPD], [Es_Nocturno]}),
                            each _{1} = true
                        )
                    in
                        if List.IsEmpty(pares) then null
                        else List.Average(List.Transform(pares, each _{0})),
                type number},

            {"VPD_Min_Nocturno",
                each
                    let
                        pares = List.Select(
                            List.Zip({[VPD], [Es_Nocturno]}),
                            each _{1} = true
                        )
                    in
                        if List.IsEmpty(pares) then null
                        else List.Min(List.Transform(pares, each _{0})),
                type number}
        }
    ),

    // Duración del periodo de luz (h) y energía diurna (MJ/m²)
    AgregarDuracionLuz = Table.AddColumn(
        Agrupado, "Duracion_Luz_h",
        each if [Hora_Inicio_Luz] = null then null
             else [Hora_Fin_Luz] - [Hora_Inicio_Luz] + 0.25,
        type number
    ),
    AgregarEnergiaLuz = Table.AddColumn(
        AgregarDuracionLuz, "Energia_Luz_MJ",
        each if [Rad_Media_Luz] = null or [Duracion_Luz_h] = null then null
             else [Rad_Media_Luz] * [Duracion_Luz_h] * 3600 / 1000000,
        type number
    ),
    AgregarDiaCompleto = Table.AddColumn(
        AgregarEnergiaLuz, "Dia_Completo",
        each [N_Lecturas] >= 80, type logical
    ),

    TiposFinales = Table.TransformColumnTypes(
        AgregarDiaCompleto,
        {
            {"estacionid", Int64.Type},
            {"Fecha",      type date}
        }
    )

in
    TiposFinales
```
</details>


### `Horas_Dia`

| Columna | Tipo | Formato | Ordenar por | Notas |
|---|---|---|---|---|
| `Hora` | int64 | 0 |  |  |
| `Hora_Etiqueta` | string |  |  |  |
| `Periodo` | string |  |  |  |

<details><summary>Consulta de Power Query (M)</summary>

```powerquery
let
    Lista = List.Numbers(0, 24, 1),
    Tabla = Table.FromList(
        Lista,
        Splitter.SplitByNothing(),
        {"Hora"}
    ),
    // Etiqueta legible
    AgregarEtiqueta = Table.AddColumn(
        Tabla, "Hora_Etiqueta",
        each Text.PadStart(Text.From([Hora]), 2, "0") & ":00",
        type text
    ),
    // Período del día
    AgregarPeriodo = Table.AddColumn(
        AgregarEtiqueta, "Periodo",
        each
            if [Hora] >= 6 and [Hora] <= 18 then "Diurno"
            else if [Hora] >= 19 and [Hora] <= 23 then "Nocturno tarde"
            else "Nocturno madrugada",
        type text
    ),
    Tipo = Table.TransformColumnTypes(
        AgregarPeriodo,
        {{"Hora", Int64.Type}}
    )
in
    Tipo
```
</details>


### `Periodos_Dia`

| Columna | Tipo | Formato | Ordenar por | Notas |
|---|---|---|---|---|
| `id` | int64 | 0 |  |  |
| `Periodo` | string |  | `id` |  |
| `HoraDesde` | int64 | 0 |  |  |
| `HoraHasta` | int64 | 0 |  |  |

<details><summary>Consulta de Power Query (M)</summary>

```powerquery
let
    Tabla = Table.FromRows(
        {
            {0, "Todas las horas",  0,  23},
            {1, "Madrugada (00:00-05:59)",        0,   5},
            {2, "Mañana (06:00-11:59)",           6,  11},
            {3, "Tarde (12:00-17:59)",           12,  17},
            {4, "Noche (18:00-23:59)",           18,  23}
        },
        {"id", "Periodo", "HoraDesde", "HoraHasta"}
    ),
    Tipos = Table.TransformColumnTypes(
        Tabla,
        {
            {"id",        Int64.Type},
            {"Periodo",   type text},
            {"HoraDesde", Int64.Type},
            {"HoraHasta", Int64.Type}
        }
    )
in
    Tipos
```
</details>


### `Plagas`

| Columna | Tipo | Formato | Ordenar por | Notas |
|---|---|---|---|---|
| `id` | int64 | 0 |  |  |
| `Plaga` | string |  |  |  |

<details><summary>Consulta de Power Query (M)</summary>

```powerquery
let
    Tabla = Table.FromRows(
        {
            {1, "Roya Naranja"},
            {2, "Carbón"},
            {3, "Salivosa"},
            {4, "Barrenador"}
        },
        {"id", "Plaga"}
    ),
    #"Tipo cambiado" = Table.TransformColumnTypes(Tabla,{{"id", Int64.Type}})
in
    #"Tipo cambiado"
```
</details>


### `Semanas_Anio`

| Columna | Tipo | Formato | Ordenar por | Notas |
|---|---|---|---|---|
| `Semana_Num` | int64 | 0 |  |  |

<details><summary>Consulta de Power Query (M)</summary>

```powerquery
let
    // Genera semanas 1 a 53
    Lista = List.Numbers(1, 53, 1),
    Tabla = Table.FromList(
        Lista,
        Splitter.SplitByNothing(),
        {"Semana_Num"}
    ),
    Tipo = Table.TransformColumnTypes(
        Tabla, {{"Semana_Num", Int64.Type}}
    )
in
    Tipo
```
</details>


### `Semanas_Grafica`

| Columna | Tipo | Formato | Ordenar por | Notas |
|---|---|---|---|---|
| `Semana_Etiqueta` | string |  | `Inicio_Semana` |  |
| `Semana_Hidrologica` | int64 | 0 |  |  |
| `Año_Hidrologico` | int64 | 0 |  |  |
| `Inicio_Semana` | dateTime | Long Date |  |  |

<details><summary>Consulta de Power Query (M)</summary>

```powerquery
let
    Fuente = Calendario,
    Seleccion = Table.SelectColumns(
        Fuente,
        {
            "Semana_Etiqueta",
            "Semana_Hidrologica",
            "Año_Hidrologico",
            "Inicio_Semana"
        }
    ),
    SinDuplicados = Table.Distinct(Seleccion),
    Ordenado = Table.Sort(
        SinDuplicados,
        {{"Inicio_Semana", Order.Ascending}}
    )
in
    Ordenado
```
</details>


### `TablaEstaciones_met`

| Columna | Tipo | Formato | Ordenar por | Notas |
|---|---|---|---|---|
| `estacionid` | string |  |  |  |

<details><summary>Consulta de Power Query (M)</summary>

```powerquery
let
      Estaciones = {
       1,3,4,5,6,8,9,10,11,13,14,15,17,19,20,21,22,23,24,25,26,
        27,28,29,30,31,33,34,36,37,67,73,74,75,94
     },

    //    Estaciones = {
    //   1,3,8,34,36,38,75,38,40
    //},

    
    Tabla = Table.FromList(Estaciones, Splitter.SplitByNothing(), {"estacionid"})
in
    Tabla
```
</details>


