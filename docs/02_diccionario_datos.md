# Diccionario de datos

> Generado automáticamente por `tools/generar_docs_modelo.py` el 2026-11-03. No editar a mano: los cambios se pierden al regenerar.

## Parámetros y funciones de Power Query

| Nombre | Descripción | Definición |
|---|---|---|
| `RangeEnd` | Fin del rango de carga en Desktop, exclusivo. Usar las 00:00 del día siguiente al último día que se quiere ver. | `#datetime(2026, 11, 2, 0, 0, 0)` |
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
| `Riesgos_Cultivo.Cultivo` | `Cultivos.Cultivo` | Sí | una dirección |

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


### `Cultivos`

| Columna | Tipo | Formato | Ordenar por | Notas |
|---|---|---|---|---|
| `Cultivo` | string |  | `Orden` |  |
| `Orden` | int64 | 0 |  | oculta |
| `GDD_Base` | double | 0.0 |  |  |
| `GDD_Tope` | double | 0.0 |  |  |

<details><summary>Consulta de Power Query (M)</summary>

```powerquery
let
    // Generado por tools/generar_riesgos_modelo.py desde config/riesgos_cultivo.csv. No editar a mano.
    Tabla = #table(type table [Cultivo = text, Orden = Int64.Type, GDD_Base = number, GDD_Tope = number], {
	{"Caña de azúcar", 1, 10, 34},
	{"Banano", 2, 15, 28},
	{"Aguacate", 3, 10, 24},
	{"Palma de aceite", 4, 15, 30},
	{"Granos básicos", 5, 10, 30}
    })
in
    Tabla
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
| `Rad_Media` | double | 0 |  |  |

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
            "velocidad_viento", "direccion_viento", "radiacion"
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
            {"direccion_viento", type number},
            {"radiacion",        type number}
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
            {"Rad_Media",     each List.Average([radiacion]),          type number},
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


### `Riesgos_Cultivo`

| Columna | Tipo | Formato | Ordenar por | Notas |
|---|---|---|---|---|
| `ID` | string |  |  |  |
| `Cultivo` | string |  |  |  |
| `Riesgo` | string |  | `Orden_Nombre` |  |
| `Tipo` | string |  |  |  |
| `Escala` | string |  |  |  |
| `Unidad` | string |  |  |  |
| `Umbral_Amarillo` | double | 0.## |  |  |
| `Umbral_Rojo` | double | 0.## |  |  |
| `Invertido` | boolean |  |  |  |
| `Tiene_Horaria` | boolean |  |  |  |
| `Condicion` | string |  |  |  |
| `Aplicacion` | string |  |  |  |
| `Fuente` | string |  |  |  |
| `Confianza` | string |  |  |  |
| `Validado` | boolean |  |  |  |
| `Orden` | int64 | 0 |  | oculta |
| `Orden_Nombre` | int64 | 0 |  | oculta |
| `Categoria` | string |  | `Orden_Categoria` |  |
| `Orden_Categoria` | int64 | 0 |  | oculta |

<details><summary>Consulta de Power Query (M)</summary>

```powerquery
let
    // Generado por tools/generar_riesgos_modelo.py desde config/riesgos_cultivo.csv. No editar a mano.
    Tabla = #table(type table [ID = text, Cultivo = text, Riesgo = text, Tipo = text, Escala = text, Unidad = text, Umbral_Amarillo = number, Umbral_Rojo = number, Invertido = logical, Tiene_Horaria = logical, Condicion = text, Aplicacion = text, Fuente = text, Confianza = text, Validado = logical, Orden = Int64.Type, Orden_Nombre = Int64.Type, Categoria = text, Orden_Categoria = Int64.Type], {
	{"CAN_ROYA_CAFE", "Caña de azúcar", "Roya café", "Enfermedad", "H/D", "días/semana", 1, 3, false, true, "Las esporas requieren una película de agua ≥ 6 h para germinar; temperatura óptima de germinación 21 °C. Día favorable: Tmed 15–25 °C, HR media > 80 % y ≥ 6 h de mojadura. Hora favorable: T 15–25 °C, HR > 80 %, mojadura > 4.", "Etapa sensible: plantas jóvenes (hasta 5–6 meses); interpretar según fecha de corte o siembra.", "CENGICANA2012_ENF; MODELO", "A", false, 101, 101, "Enfermedades", 1},
	{"CAN_ROYA_NARANJA", "Caña de azúcar", "Roya naranja", "Enfermedad", "H/D", "días/semana", 2, 4, false, true, "Día favorable: Tmed 20–25 °C (cualquier mojadura) o Tmed > 25 °C con mojadura > 8 h. Desfavorable: Tmed < 20 °C, o > 25 °C con mojadura < 8 h. Germinación óptima con HR > 98 % y 21 °C. Esporula hasta la madurez y aun en época seca.", "Todas las estaciones, todo el año.", "ANGELOTTI2022; CENGICANA2012_ENF", "A/B", false, 102, 102, "Enfermedades", 1},
	{"CAN_ESCALDADURA", "Caña de azúcar", "Escaldadura foliar", "Enfermedad (bacteriana)", "D", "días/semana", 1, 2, false, false, "Importante en Guatemala: la alternancia de periodos lluviosos severos y secos severos favorece su expresión; se dispersa con la combinación de lluvia y viento fuertes. Día de dispersión: lluvia > 20 mm y viento máx > 30 km/h.", "Todas las estaciones, todo el año.", "CENGICANA2012_ENF", "B", false, 103, 103, "Enfermedades", 1},
	{"CAN_SALIVOSA", "Caña de azúcar", "Salivosa (Aeneolamia)", "Plaga", "H/D", "días/semana", 2, 4, false, true, "Aparece en abril con las primeras lluvias: 50–100 mm de lluvia inicial acumulan humedad suficiente para la eclosión de la mayoría de los huevos. La población se relaciona con la lluvia de 4 semanas antes; presenta 3–4 picos en la época lluviosa y desaparece en noviembre por el fotoperiodo, aunque siga lloviendo. Día favorable: lluvia > 5 mm, HR media > 80 %, Tmed 22–30 °C. Alerta de emergencia: lluvia acumulada desde el inicio de la temporada ≥ 50 mm.", "Solo abril–noviembre (época lluviosa; crítico julio–agosto).", "CENGICANA_ET1997; UVG2017; UVG2016; IMN2019", "A", false, 104, 104, "Plagas", 2},
	{"CAN_BARRENADOR", "Caña de azúcar", "Barrenador (Diatraea)", "Plaga", "D", "días/semana", 2, 4, false, true, "La infestación aumenta con el establecimiento de la época seca y en la maduración. Día favorable: Tmed > 24 °C, HR media 60–80 %, día seco. 4–5 generaciones/año en El Salvador (oct–jun). Hora favorable (aproximación para el mapa de calor): T > 24 °C, HR 60–80 % y sin lluvia.", "Todas las estaciones. D. crambidoides predomina en estratos bajo y litoral; otras especies sobre 300 msnm.", "CENGICANA2012_MIP; UES2011; MODELO", "B", false, 105, 105, "Plagas", 2},
	{"CAN_CHINCHE_ENCAJE", "Caña de azúcar", "Chinche de encaje", "Plaga", "D/A", "días secos/semana", 4, 6, false, false, "Plaga en aumento en la zona cañera. Las lluvias intensas de julio a septiembre la reducen (derriban las colonias de ninfas); el estrés por exceso de humedad o por sequía la favorece. Semana favorable: sin días con lluvia > 20 mm y ≥ 4 días secos.", "Todas las estaciones; el efecto supresor de la lluvia es mayor en julio–septiembre.", "CENGICANA2012_MIP", "B", false, 106, 106, "Plagas", 2},
	{"CAN_COLUDO", "Caña de azúcar", "Coludo (saltahojas antillano)", "Plaga", "D", "días/semana", 3, 5, false, false, "Plaga exótica favorecida por la época seca (noviembre–abril, incluida la transición): baja precipitación, alta evapotranspiración y baja humedad relativa. Día favorable: día seco y HR media < 70 %.", "Solo noviembre–abril (fin de lluvias, transición y época seca).", "CENGICANA_ET2011", "B", false, 107, 107, "Plagas", 2},
	{"CAN_ESTRES", "Caña de azúcar", "Estrés térmico", "Abiótico", "H", "horas/semana", 14, 28, false, true, "Hora con T > 36 °C (umbral máximo de estrés para caña de azúcar; rango óptimo 20–33 °C) y radiación > 800 W/m².", "Todas las estaciones, todo el año.", "CHAVES2017", "A/B", false, 108, 108, "Clima (abióticos)", 3},
	{"CAN_SUELO_SATURADO", "Caña de azúcar", "Suelo saturado: limitación de cosecha y tránsito", "Operativo", "D", "días/semana", 1, 3, false, false, "Día con lluvia > 10 mm durante la zafra: anegamiento del suelo que limita el corte, el alce y el tránsito de maquinaria.", "Solo noviembre–mayo (zafra).", "OPER", "C", true, 109, 109, "Manejo y producción", 4},
	{"CAN_APLICACION", "Caña de azúcar", "Ventana para aplicación aérea", "Operativo (favorable)", "H", "horas aptas/día", 4, 2, true, true, "Hora apta para aplicar (madurantes y otros productos): T < 30 °C, HR > 60 % y viento < 10 km/h, de día. Evitar la inversión térmica (diciembre–febrero, noches despejadas y sin viento). Indicador positivo: horas aptas por día.", "Todo el año (madurantes: zafra, noviembre–abril). Riesgo de inversión térmica en diciembre–febrero.", "CENGICANA2012_MAD", "A", false, 110, 110, "Manejo y producción", 4},
	{"CAN_QUEMA", "Caña de azúcar", "Riesgo de quema / incendio", "Operativo", "D", "días/semana", 1, 3, false, false, "Día con HR mínima < 40 %, viento máximo > 20 km/h y ≥ 3 días secos consecutivos.", "Todas las estaciones, todo el año.", "OPER", "C", true, 111, 111, "Manejo y producción", 4},
	{"CAN_MADURACION", "Caña de azúcar", "Condiciones de maduración", "Productivo (favorable)", "D", "días/semana", 3, 1, true, false, "Condiciones favorables a la acumulación de sacarosa, de 4 a 6 semanas antes del corte: oscilación térmica día-noche ≈ 15 °C, lluvia de 30–100 mm/mes y 11.5–12.5 h de luz. El exceso de humedad en suelo y planta (inicio de zafra) la frena. Día favorable: amplitud térmica ≥ 15 °C; mes favorable: lluvia 30–100 mm. Semáforo invertido.", "Solo noviembre–abril (zafra).", "CENGICANA2012_MAD", "A", false, 112, 112, "Manejo y producción", 4},
	{"BAN_SIG_NEGRA", "Banano", "Sigatoka negra", "Enfermedad", "H/D/A", "días/semana", 1, 3, false, true, "Óptimo 26–28 °C; la infección cae bajo ~20 °C (requiere ~21.5–28 °C). HR > 80 % favorable y > 90 % fuertemente asociada; lluvia frecuente y mojadura persistente. Radiación alta la reduce. Día favorable: Tmed 21.5–28 °C, HR media > 90 % y > 4 h de mojadura nocturna. Índice acumulado: días favorables en 14 días.", "Todas las estaciones, todo el año.", "TEC2022", "A", false, 213, 213, "Enfermedades", 1},
	{"BAN_MOKO", "Banano", "Moko (dispersión)", "Enfermedad", "D", "semana", 1, 1, false, false, "Semana con lluvia > 100 mm y balance positivo (dispersión por agua).", "Todas las estaciones, todo el año.", "MODELO", "C", false, 214, 214, "Enfermedades", 1},
	{"BAN_VOLCAMIENTO", "Banano", "Volcamiento por viento", "Abiótico", "D", "km/h", 40, 60, false, false, "Viento máximo diurno > 40 km/h (precaución) / > 60 km/h (alerta).", "Todas las estaciones, todo el año.", "MODELO", "C", false, 215, 215, "Clima (abióticos)", 3},
	{"BAN_ESTRES", "Banano", "Estrés térmico", "Abiótico", "H", "horas/semana", 6, 14, false, true, "Hora con T > 38 °C (umbral máximo de estrés para banano; rango óptimo 20–30 °C) y radiación > 800 W/m².", "Todas las estaciones, todo el año.", "CHAVES2017", "A/B", false, 216, 108, "Clima (abióticos)", 3},
	{"AGU_PHYTO", "Aguacate", "Phytophthora (pudrición de raíz)", "Enfermedad", "D", "días/semana", 1, 3, false, false, "Humedad alta, temperaturas altas y exceso de agua (mal drenaje). Día favorable: Tmed 20–30 °C y balance diario > 0.", "Todas las estaciones, todo el año.", "INTACR2022", "B", false, 317, 317, "Enfermedades", 1},
	{"AGU_ANTRACNOSIS", "Aguacate", "Antracnosis", "Enfermedad", "H/D", "días/semana", 2, 4, false, true, "Favorecida por temperaturas altas y humedad; la lluvia la dispersa. Día favorable: Tmed 20–30 °C, HR media > 80 % y lluvia > 1 mm o > 6 h de mojadura.", "Todas las estaciones, todo el año.", "INTACR2022", "B", false, 318, 318, "Enfermedades", 1},
	{"AGU_FRIO", "Aguacate", "Frío", "Abiótico", "D", "días/semana", 1, 3, false, false, "Tmín < 12 °C (umbral mínimo de estrés para aguacate).", "Más relevante en estaciones altas.", "CHAVES2017; MODELO", "A/B", false, 319, 319, "Clima (abióticos)", 3},
	{"AGU_CALOR", "Aguacate", "Golpe de calor / quemadura de fruto", "Abiótico", "H", "horas/semana", 6, 14, false, true, "Hora con T > 36 °C (umbral máximo de estrés para aguacate; rango óptimo 15–30 °C) y radiación > 800 W/m².", "Todas las estaciones, todo el año.", "CHAVES2017; INTACR2022", "A/B", false, 320, 320, "Clima (abióticos)", 3},
	{"AGU_VIENTO", "Aguacate", "Caída de flor y fruto por viento", "Abiótico", "D", "km/h", 30, 45, false, false, "Vientos fuertes causan caída de flor y fruto. Viento máximo diurno > 30 / 45 km/h.", "Etapa sensible: floración y fruto pequeño.", "INTACR2022", "B", false, 321, 321, "Clima (abióticos)", 3},
	{"PAL_PC", "Palma de aceite", "Pudrición del cogollo (P. palmivora)", "Enfermedad", "D/A", "días/semana", 2, 4, false, true, "Severidad mayor con HR alta, lluvias frecuentes y encharcamiento; los periodos secos la reducen; el patógeno tolera 11–35 °C. Día favorable: lluvia > 5 mm y HR media > 90 %. Índice: días favorables en 14 días. Hora favorable (aproximación para el mapa de calor): T 11–35 °C, HR > 90 % y lluvia > 0.", "Todas las estaciones, todo el año.", "FEDEPALMA", "B", false, 422, 422, "Enfermedades", 1},
	{"PAL_ESTRES", "Palma de aceite", "Estrés térmico", "Abiótico", "H", "horas/semana", 14, 28, false, true, "Hora con T > 34 °C (umbral máximo de estrés para palma de aceite; rango óptimo 22–32 °C) y radiación > 800 W/m².", "Todas las estaciones, todo el año.", "CHAVES2017", "A/B", false, 423, 108, "Clima (abióticos)", 3},
	{"MAI_ASFALTO", "Granos básicos", "Maíz – Mancha de asfalto", "Enfermedad", "H/D", "días/semana", 2, 4, false, true, "Favorecida por temperaturas frescas (16–22 °C) y HR alta: HR media > 75 % y 7 h de mojadura nocturna. Aparece unas 2 semanas antes de la floración y alcanza su máximo ~6 semanas después. Presente en el altiplano de Guatemala.", "Etapa sensible: desde 2 semanas antes de la floración (interpretar según calendario de siembra).", "SENASICA2020; USFQ2024", "A/B", false, 524, 524, "Enfermedades", 1},
	{"MAI_ROYA", "Granos básicos", "Maíz – Roya común", "Enfermedad", "H/D", "días/semana", 2, 4, false, true, "Noches de 18–21 °C, temperatura diurna moderada, HR alta y ≥ 6 h de mojadura.", "Más relevante en estaciones altas (noches frescas).", "ISU", "B", false, 525, 525, "Enfermedades", 1},
	{"MAI_TIZON", "Granos básicos", "Maíz – Tizón foliar (Exserohilum)", "Enfermedad", "H/D", "días/semana", 2, 4, false, true, "18–28 °C con mojadura prolongada (lluvia o rocío).", "Todas las estaciones, todo el año.", "ISU", "B", false, 526, 526, "Enfermedades", 1},
	{"MAI_MANCHA_GRIS", "Granos básicos", "Maíz – Mancha gris (Cercospora)", "Enfermedad", "H/D", "días/semana", 2, 4, false, true, "Cálido (~27–32 °C) con HR > 90 % durante > 12 h.", "Todas las estaciones, todo el año.", "ISU", "B", false, 527, 527, "Enfermedades", 1},
	{"MAI_COGOLLERO", "Granos básicos", "Maíz – Gusano cogollero (generaciones)", "Plaga", "A/D", "días/semana (severidad)", 3, 5, false, false, "Generaciones por grados día: temperatura base 10.9 °C y 559 grados día por generación (indicador acumulado). Severidad: daño mayor con T > 30 °C y poca lluvia; día favorable: Tmáx > 30 °C y día seco.", "Todas las estaciones, todo el año.", "SENASICA2021; RAMIREZ2021; BHAT2026", "B", false, 528, 528, "Plagas", 2},
	{"MAI_CALOR_FLOR", "Granos básicos", "Maíz – Estrés térmico en floración", "Abiótico", "D", "días/semana", 1, 3, false, false, "Tmáx > 38 °C (umbral máximo de estrés para maíz; rango óptimo 10–35 °C).", "Etapa sensible: floración (interpretar según calendario de siembra).", "CHAVES2017", "A/B", false, 529, 529, "Clima (abióticos)", 3},
	{"FRI_MUSTIA", "Granos básicos", "Frijol – Mustia hilachosa", "Enfermedad", "D", "días/semana", 2, 4, false, false, "25–32 °C con lluvia frecuente (salpique). Día favorable: Tmed 25–32 °C y lluvia > 5 mm.", "Todas las estaciones, todo el año.", "IICA2008", "A", false, 530, 530, "Enfermedades", 1},
	{"FRI_ROYA", "Granos básicos", "Frijol – Roya", "Enfermedad", "H/D", "días/semana", 2, 4, false, true, "17–27 °C con lluvia frecuente o noches frescas con rocío prolongado (prefloración y floración). Día favorable: Tmed 17–27 °C y (lluvia > 1 mm o > 8 h de mojadura nocturna).", "Etapa sensible: prefloración y floración (el modelo no conoce la etapa; interpretar según calendario de siembra).", "ICTA2024; IICA2008", "A", false, 531, 531, "Enfermedades", 1},
	{"FRI_ANTRACNOSIS", "Granos básicos", "Frijol – Antracnosis", "Enfermedad", "D", "días/semana", 2, 4, false, false, "HR alta (~92 %), lluvias frecuentes y 13–26 °C (óptimo 17 °C); zonas > 1000 msnm.", "Solo estaciones ≥ 1000 msnm.", "ICTA2024; IICA2008", "A", false, 532, 532, "Enfermedades", 1},
	{"FRI_MANCHA_ANGULAR", "Granos básicos", "Frijol – Mancha angular", "Enfermedad", "D/A", "días/semana", 2, 4, false, false, "18–28 °C con alternancia de periodos lluviosos y días secos. Semana favorable: ≥ 2 días con lluvia y ≥ 2 días secos con Tmed 18–28 °C.", "Todas las estaciones, todo el año.", "IICA2008", "A", false, 533, 533, "Enfermedades", 1},
	{"FRI_BACTERIOSIS", "Granos básicos", "Frijol – Bacteriosis común", "Enfermedad", "D", "días/semana", 2, 4, false, false, "20–32 °C con lluvia frecuente (salpique); zonas < 1200 msnm.", "Solo estaciones < 1200 msnm.", "IICA2008", "A", false, 534, 534, "Enfermedades", 1},
	{"FRI_MOSAICO", "Granos básicos", "Frijol – Mosaico dorado (mosca blanca)", "Plaga / virus", "D", "días/semana", 3, 5, false, false, "25–30 °C, zonas < 1200 msnm; poblaciones de mosca blanca aumentan en periodos secos. Día favorable: Tmed 25–30 °C y día seco.", "Solo estaciones < 1200 msnm.", "IICA2008; CORRALES2017", "A", false, 535, 535, "Plagas", 2},
	{"FRI_CALOR_FLOR", "Granos básicos", "Frijol – Estrés por calor en floración", "Abiótico", "D", "días/semana", 2, 4, false, false, "Tmáx > 34 °C (umbral máximo de estrés para frijol; rango óptimo 15–27 °C). Noches > 20 °C también reducen el cuajado.", "Etapa sensible: floración (interpretar según calendario de siembra).", "CHAVES2017", "A/B", false, 536, 536, "Clima (abióticos)", 3},
	{"GRA_SEQUIA", "Granos básicos", "Sequía", "Abiótico", "D", "días/semana", 3, 5, false, false, "Días secos (lluvia < 1 mm).", "Todas las estaciones, todo el año.", "MODELO", "C", false, 537, 537, "Clima (abióticos)", 3},
	{"CAN_FLORACION", "Caña de azúcar", "Condiciones de inducción floral", "Productivo (no deseado)", "D", "días en la ventana (16 días)", 5, 10, false, false, "Ventana de inducción en Guatemala: segunda quincena de agosto (fotoperiodo de 12 h 30 min hacia el 23–25 ago). Noche inductiva: Tmín 21–24 °C, con Tmáx ≤ 32 °C y suelo húmedo (sin déficit). Tmín < 18 °C reduce la floración; Tmáx > 32 °C la inhibe; más horas de brillo solar en agosto la reducen.", "Solo 16–31 de agosto. Mayor intensidad en estratos medio y alto (menos brillo solar). Estratos CENGICAÑA: litoral < 40, bajo 40–100, medio 100–300, alto > 300 msnm.", "CENGICANA2012_FLOR; ARALDI2010", "A", false, 138, 138, "Manejo y producción", 4},
	{"CAN_ACAME", "Caña de azúcar", "Acame (volcamiento)", "Abiótico", "D", "días/semana", 1, 2, false, false, "Viento máximo fuerte combinado con lluvia (suelo húmedo y tallos pesados). Día con viento máx > 40 km/h y lluvia > 10 mm.", "Todas las estaciones, todo el año.", "OPER", "C", false, 139, 139, "Clima (abióticos)", 3},
	{"AGU_ACAROS", "Aguacate", "Ácaros (arañita)", "Plaga", "D", "días/semana", 3, 5, false, false, "Más comunes en época seca y favorecidos por el viento. Día favorable: día seco, HR media < 65 % y viento máx > 20 km/h.", "Todas las estaciones, todo el año.", "INTACR2022", "B", false, 340, 340, "Plagas", 2},
	{"MAI_ACHAPARRAMIENTO", "Granos básicos", "Maíz – Chicharrita y achaparramiento", "Plaga / vector", "D", "días/semana", 3, 5, false, false, "El vector (Dalbulus maidis) se favorece con escasez de lluvia, altas temperaturas y baja humedad relativa; mayor incidencia cuando la siembra coincide con lluvias irregulares. Día favorable: día seco, Tmed > 26 °C y HR media < 70 %.", "Todas las estaciones, todo el año.", "CASTANON2000", "B", false, 541, 541, "Plagas", 2},
	{"MAI_PUDRICION_MAZORCA", "Granos básicos", "Maíz – Pudrición de mazorca", "Enfermedad", "D", "días con lluvia/semana", 4, 6, false, false, "Los años más lluviosos producen epifitias (Stenocarpella y Fusarium). Semana favorable: ≥ 4 días con lluvia > 1 mm.", "Etapa sensible: llenado de grano y madurez.", "URBINA1993", "B", false, 542, 542, "Enfermedades", 1}
    })
in
    Tabla
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


### `_Riesgos`

| Columna | Tipo | Formato | Ordenar por | Notas |
|---|---|---|---|---|
| `Column` | None | 0 |  | oculta |

<details><summary>Consulta de Power Query (M)</summary>

```powerquery
Row("Column", BLANK())
```
</details>


