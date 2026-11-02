#!/usr/bin/env python3
"""
Genera la documentación automática del modelo semántico a partir de los archivos TMDL/PBIR:
  docs/02_diccionario_datos.md   (parámetros, actualización incremental, relaciones, tablas y columnas)
  docs/03_catalogo_medidas.md    (todas las medidas DAX agrupadas por tema, con descripción y código)
  docs/09_inventario_visuales.md (páginas y visuales del reporte con los campos que usan)

Uso (desde la carpeta raíz del proyecto; solo requiere Python 3.8+, sin librerías extra):
    python tools/generar_docs_modelo.py
Ejecutar después de cada cambio al modelo y antes de hacer commit.
Para documentar una medida nueva: agregar un comentario /// encima de la medida en TMDL,
o un comentario // en la primera línea de su expresión, o una entrada en FIJAS (abajo).
"""
import glob, json, os, re, datetime

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROY = "2026_dashboard_exp1"
DEF = os.path.join(RAIZ, f"{PROY}.SemanticModel", "definition")
PAGS = os.path.join(RAIZ, f"{PROY}.Report", "definition", "pages")
DOCS = os.path.join(RAIZ, "docs")

def leer(p):
    with open(p, encoding="utf-8") as f:
        return f.read().replace("\r\n", "\n")

TOP = re.compile(r"^\t(measure|column|partition|annotation|hierarchy|refreshPolicy)\b", re.M)
PROP = re.compile(r"^\t\t(formatString|lineageTag|displayFolder|dataCategory|annotation|changedProperty|isHidden|formatStringDefinition)\b", re.M)

def expresiones():
    s = leer(os.path.join(DEF, "expressions.tmdl")); out = []
    for b in re.split(r"\n(?=(?:/// .*\n)*expression )", "\n" + s):
        m = re.match(r"((?:/// .*\n)*)expression (\w+) =\s*(.*?)(?:\n\tlineageTag|\Z)", b, re.S)
        if m:
            out.append((m.group(2), m.group(1).replace("///", "").strip(), m.group(3).strip()))
    return out

CULTIVO = {"Cana": "caña de azúcar", "Banano": "banano", "Aguacate": "aguacate", "Palma": "palma de aceite", "Maiz": "maíz"}
PLAGA = {"Roya": "roya", "Roya_Nocturna": "roya (mojadura total > 8 h)", "Carbon": "carbón", "Salivosa": "salivosa",
         "Barrenador": "barrenador", "Sigatoka": "sigatoka", "Phytophthora": "Phytophthora", "Frio_Aguacate": "frío en aguacate (Tmín < 12 °C)",
         "Mancha_Asfalto": "mancha de asfalto", "Moko": "moko", "Sequia_Granos": "sequía en granos", "PC_Palma": "pudrición del cogollo en palma",
         "Balance": "balance hídrico semanal", "Deficit": "estaciones en déficit crítico", "VPD": "VPD máximo diurno",
         "Temp_Nocturna": "temperatura nocturna media", "Estres_Termico": "horas de estrés térmico", "Viento": "viento máximo diurno"}
FIJAS = {
 "Precip_Diaria": "Lluvia diaria (mm); por estación y promedio entre estaciones.",
 "Precip_Semanal": "Lluvia de la semana hidrológica en contexto (mm); suma por estación, promedio entre estaciones.",
 "ETO_Diaria": "ETo diaria (mm); promedio entre estaciones con dato de ETo.",
 "ETO_Semanal": "ETo de la semana (mm); suma por estación, promedio entre estaciones.",
 "Balance_Diario": "Balance hídrico diario P − ETo (mm), solo días con ambos datos; promedio entre estaciones.",
 "Balance_Acumulado_Anual": "Precipitación acumulada − ETo acumulada del año hidrológico (mm).",
 "Estaciones_Deficit_Critico": "Número de estaciones con balance semanal < −20 mm.",
 "Estaciones_Superavit": "Número de estaciones con balance semanal > 0 mm.",
 "Temp_Max": "Temperatura máxima (°C): extremo de las estaciones seleccionadas.",
 "Temp_Min": "Temperatura mínima (°C): extremo de las estaciones seleccionadas.",
 "Temp_Media": "Temperatura media diaria promedio (°C).",
 "Amplitud_Termica": "Temp_Max − Temp_Min (°C).",
 "HR_Media": "Humedad relativa media (%).", "HR_Min": "Humedad relativa mínima (%): extremo.", "HR_Max": "Humedad relativa máxima (%): extremo.",
 "IC_Max": "Índice de calor máximo diurno (°C): extremo.", "IC_Max_Diurno": "Índice de calor máximo diurno (°C): extremo.",
 "IC_Media": "Índice de calor medio diurno (°C).", "IC_Media_Diurno": "Índice de calor medio diurno (°C).",
 "Temp_Nocturna_Media": "Temperatura media nocturna (19–05 h) (°C).", "Temp_Min_Nocturna": "Temperatura mínima nocturna (°C): extremo.",
 "VPD_Media_Diurna": "Déficit de presión de vapor medio diurno (kPa).", "VPD_Max_Diurna": "VPD máximo diurno (kPa): extremo.",
 "VPD_Media_Nocturna": "VPD medio nocturno (kPa).", "VPD_Min_Nocturno": "VPD mínimo nocturno (kPa): extremo.",
 "Mojadura_Horas_Semanal": "Horas de mojadura diurna (sensor > 4); suma por estación, promedio entre estaciones.",
 "Mojadura_Horas_Nocturna_Semanal": "Horas de mojadura nocturna; suma por estación, promedio entre estaciones.",
 "Mojadura_Horas_Total_Semanal": "Horas de mojadura total; suma por estación, promedio entre estaciones.",
 "Horas_Estres_Termico_Semanal": "Horas con T > 35 °C y radiación > 800 W/m²; suma por estación, promedio entre estaciones.",
 "Duracion_Mojadura": "Hora fin − hora inicio de mojadura (h), promedio.",
 "Viento_Media": "Velocidad media diaria del viento (km/h).", "Viento_Max": "Racha/velocidad máxima (km/h): extremo.",
 "Viento_Max_Diurno": "Velocidad máxima diurna (km/h): extremo.", "Viento_Max_Nocturno": "Velocidad máxima nocturna (km/h): extremo.",
 "Viento_Media_Diurna": "Velocidad media diurna (km/h).", "Viento_Media_Nocturna": "Velocidad media nocturna (km/h).",
 "Riesgo_Volcamiento": "Semáforo de viento máximo (> 40 amarillo, > 60 rojo, km/h).",
 "_Viento_Horas_Validas": "Horas-estación con dato de viento válido en el período del día seleccionado.",
 "_Viento_Horas_Sector": "Horas-estación no calmas con viento desde el sector en contexto.",
 "Pct_Calmas_Viento": "% de horas con viento por debajo del umbral de calma.",
 "Viento_Media_Periodo": "Velocidad media en el período del día seleccionado (km/h).",
 "Viento_Media_Sector": "Velocidad media de las horas que soplan desde el sector (km/h).",
 "Dir_Predominante": "Sector(es) con mayor frecuencia de viento.",
 "Rad_Max_Diurna": "Irradiancia máxima diurna (W/m²): extremo.",
 "Rad_Media_Diurna": "Irradiancia media en ventana fija 06–18 h (W/m²). Sin uso en visuales; reemplazada por Rad_Media_Luz.",
 "Rad_Acumulada_Semanal": "Radiación de la semana (MJ/m²) desde Fact_Diaria_met; suma por estación, promedio entre estaciones.",
 "Rad_Acumulada_Anual": "Radiación acumulada del año hidrológico (MJ/m²).", "Rad_Acumulada_Anual_Anterior": "Ídem, año hidrológico anterior.",
 "Rad_Acumulada_Anual_Grafica": "Radiación acumulada por semana del eje (Semanas_Anio), año actual.",
 "Rad_Acumulada_Anual_Anterior_Grafica": "Radiación acumulada por semana del eje, año anterior.",
 "Delta_Rad_Acumulada_YoY": "Diferencia de radiación acumulada vs. año anterior (MJ/m²).",
 "Horas_Luz": "Horas del periodo de luz (primera a última lectura > 40 W/m²); suma por estación, promedio entre estaciones.",
 "Hora_Inicio_Luz": "Hora media de inicio del periodo de luz (h decimal).", "Hora_Fin_Luz": "Hora media de fin del periodo de luz (h decimal).",
 "Duracion_Luz_Media": "Duración media diaria del periodo de luz (h).",
 "_Semana_Hidro_Actual": "Semana hidrológica en contexto (máx.).", "_Anio_Hidro_Actual": "Año hidrológico en contexto (máx.).",
 "_Conteo_Filas_Diarias": "Validación: filas en Fact_Diaria_met.", "_Conteo_Estaciones_Met": "Validación: estaciones con datos diarios.",
 "N_Lecturas_Promedio": "Calidad: lecturas de 15 min promedio por día-estación (96 = completo).",
 "Dia_Completo_Pct": "Calidad: % de días-estación con ≥ 80 lecturas.",
 "GDD_Display_cana": "Texto con GDD acumulado de caña actual y del año anterior.",
 "Indice_Riesgo_Hora": "Suma promedio de banderas horarias (roya + salivosa + barrenador + carbón).",
 "Condicion_Plaga_Hora": "Fracción de horas-estación favorables a la plaga elegida en el segmentador Plagas.",
 "Frec_Dir_Periodo": "% de horas-estación con viento desde el sector en contexto.",
}
def auto_desc(n):
    if n in FIJAS: return FIJAS[n]
    m = re.match(r"Semaforo_(.+)", n)
    if m: return f"Semáforo de {PLAGA.get(m.group(1), m.group(1))}: 1 rojo, 2 amarillo, 3 verde."
    m = re.match(r"Dias_Riesgo_(.+)|Dias_(Sequia)_Critica_Granos", n)
    if m:
        k = m.group(1) or "Sequia_Granos"
        return f"Días (promedio por estación) con condiciones favorables a {PLAGA.get(k, k)}."
    m = re.match(r"Condicion_(\w+)_Hora", n)
    if m: return f"Fracción de horas-estación favorables a {m.group(1).lower()} (bandera horaria)."
    m = re.match(r"GDD_(\w+?)_ST_(Semanal|Acumulado)(_Anterior)?(_Grafica)?$", n)
    if m:
        c = CULTIVO.get(m.group(1), m.group(1)); t = "de la semana" if m.group(2) == "Semanal" else "acumulada del año hidrológico"
        return f"Suma térmica con temperatura óptima tope para {c} {t}" + (", año anterior" if m.group(3) else "") + (" (por semana del eje)" if m.group(4) else "") + "."
    m = re.match(r"GDD_Semanal_Base(\d+)", n)
    if m: return f"Grados día base {m.group(1)} °C de la semana."
    m = re.match(r"(Precip|ETO)_Acumulada_Anual(_Anterior)?", n)
    if m: return f"{'Lluvia' if m.group(1) == 'Precip' else 'ETo'} acumulada desde el inicio del año hidrológico (mm)" + (", año anterior." if m.group(2) else ".")
    m = re.match(r"(\w+?)_Historico(_Promedio|_Max|_Min)?$", n)
    if m: return f"{m.group(1).replace('_', ' ')}: {'promedio' if m.group(2) in (None, '_Promedio') else m.group(2)[1:].lower()} de la misma semana en años hidrológicos anteriores al seleccionado."
    m = re.match(r"Delta_(\w+)_YoY", n)
    if m: return f"Diferencia de {m.group(1).replace('_', ' ')} vs. la misma semana del año hidrológico anterior."
    m = re.match(r"Hora_(\w+)", n)
    if m: return f"Hora promedio de {m.group(1).replace('_', ' ').lower()}."
    m = re.match(r"ETO_(Max_Diurna|Acum_Diurna_Semanal|Acum_Nocturna_Semanal)", n)
    if m: return {"Max_Diurna": "ETo máxima de 15 min diurna (mm): extremo.", "Acum_Diurna_Semanal": "ETo acumulada diurna (mm); suma por estación, promedio.", "Acum_Nocturna_Semanal": "ETo acumulada nocturna (mm); suma por estación, promedio."}[m.group(1)]
    return None


def medidas(texto):
    out = []
    for m in re.finditer(r"^\tmeasure (.+?) =", texto, re.M):
        nombre = m.group(1).strip().strip("'")
        nx = TOP.search(texto, m.end())
        blk = texto[m.start(): nx.start() if nx else len(texto)]
        cab = blk.index("=") + 1
        pm = PROP.search(blk, cab)
        raw = blk[cab: pm.start() if pm else len(blk)]
        if "```" in raw:
            raw = raw.split("```")[1]
        lineas = [l[3:] if l.startswith("\t\t\t") else l.strip() for l in raw.split("\n")]
        expr = "\n".join(lineas).strip()
        g = lambda k: (re.search(rf"^\t\t{k}: (.+)$", blk, re.M) or [None, None])[1]
        previa = texto[:m.start()].rstrip("\n").split("\n")[-1].strip()
        desc = previa[3:].strip() if previa.startswith("///") else None
        if not desc:
            com = [l.strip()[2:].strip() for l in expr.split("\n") if l.strip().startswith("//")]
            desc = " ".join(com[:2]) if com else None
        if not desc:
            desc = auto_desc(nombre)
        out.append(dict(nombre=nombre, expr=expr, fmt=g("formatString"), cat=g("dataCategory"),
                        carpeta=g("displayFolder"), desc=desc))
    return out

def tablas():
    res = {}
    for f in sorted(glob.glob(os.path.join(DEF, "tables", "*.tmdl"))):
        s = leer(f)
        nombre = re.search(r"^table (.+)$", s, re.M).group(1).strip().strip("'")
        t = dict(columnas=[], medidas=medidas(s) if "\tmeasure " in s else [], politica=None, jerarquias=[],
                 fecha="\tdataCategory: Time" in s.split("\n\tcolumn", 1)[0], fuente="")
        for c in re.finditer(r"^\tcolumn (.+?)\n((?:\t\t.*\n|\n(?=\t\t))*)", s, re.M):
            b = c.group(2); g = lambda k: (re.search(rf"^\t\t{k}: (.+)$", b, re.M) or [None, None])[1]
            t["columnas"].append(dict(nombre=c.group(1).strip().strip("'"), tipo=g("dataType"), fmt=g("formatString"),
                                      orden=g("sortByColumn"), clave="\t\tisKey" in b, oculta="\t\tisHidden" in b))
        rp = re.search(r"^\trefreshPolicy\n((?:\t\t\w+: .+\n)+)", s, re.M)
        if rp: t["politica"] = dict(re.findall(r"\t\t(\w+): (.+)", rp.group(1)))
        for h in re.finditer(r"^\thierarchy (.+)\n((?:\t\t.*\n|\n)*)", s, re.M):
            niv = re.findall(r"\t\tlevel (.+)\n(?:\t\t\t.*\n)*?\t\t\tcolumn: (.+)", h.group(2))
            t["jerarquias"].append((h.group(1).strip("'"), [(a.strip("'"), b) for a, b in niv]))
        src = re.search(r"^\tpartition .+?\n.*?source =\s*\n?(.*?)(?=\n\tannotation|\n\t\w|\Z)", s, re.S | re.M)
        if src: t["fuente"] = re.sub(r"^\t{2,4}", "", src.group(1).strip("`\n"), flags=re.M).strip("`\n ")
        res[nombre] = t
    return res

def relaciones():
    s = leer(os.path.join(DEF, "relationships.tmdl")); out = []
    for r in re.split(r"(?=^relationship )", s, flags=re.M):
        if not r.strip(): continue
        out.append(dict(desde=re.search(r"fromColumn: (.+)", r).group(1), hacia=re.search(r"toColumn: (.+)", r).group(1),
                        activa="isActive: false" not in r,
                        filtro=(re.search(r"crossFilteringBehavior: (.+)", r) or [None, "oneDirection"])[1]))
    return out

GRUPOS = [
    ("Viento", lambda n, c: c == "Viento" or "Viento" in n or n.startswith(("Direccion", "Rosa", "Frec_Dir", "Dir_", "Riesgo_Volcamiento", "Pct_Calmas"))),
    ("Radiación y luz", lambda n, c: c == "Radiación" or "Rad_" in n or n == "Horas_Luz"),
    ("Semáforos", lambda n, c: n.startswith("Semaforo")),
    ("Días y condiciones de riesgo (plagas, enfermedades, clima)", lambda n, c: n.startswith(("Dias_", "Condicion_", "Indice_Riesgo"))),
    ("Grados día / suma térmica (GDD)", lambda n, c: n.startswith("GDD")),
    ("Históricos y comparaciones interanuales", lambda n, c: "Historico" in n or n.startswith("Delta_") or "Anterior" in n),
    ("Precipitación, ETo y balance hídrico", lambda n, c: n.startswith(("Precip", "ETO", "Balance", "Estaciones_"))),
    ("Temperatura y sensación térmica", lambda n, c: n.startswith(("Temp", "Amplitud", "IC_", "Hora_Temp", "Hora_IC"))),
    ("Humedad, VPD, mojadura y estrés", lambda n, c: n.startswith(("HR_", "VPD", "Mojadura", "Horas_Estres", "Hora_", "Duracion_Mojadura"))),
    ("Auxiliares, calidad de datos y validación", lambda n, c: True),
]

def grupo(m):
    for g, f in GRUPOS:
        if f(m["nombre"], m["carpeta"]): return g

def esc(x): return (x or "").replace("|", "\\|").replace("\n", " ")

def ancla(g): return re.sub(r"[^a-z0-9áéíóúñü -]", "", g.lower()).replace(" ", "-")

PARAM_DESC = {
    "RangeStart": "Inicio del rango de carga en Desktop (en el servicio lo fija la actualización incremental). Usar 00:00.",
    "RangeEnd": "Fin del rango de carga en Desktop, exclusivo. Usar las 00:00 del día siguiente al último día que se quiere ver.",
    "InicioAnioHidrologico": "Fecha de referencia del inicio del año hidrológico (se usan su mes y día; la semana inicia el lunes).",
    "fxLecturasEstacion_met": "Lecturas de 15 min de una estación (endpoint /ws/redmet/estaciones/lecturas).",
    "fxLecturasEstacion_met_diario": "Resumen diario de una estación (endpoint /ws/getlecturasdia).",
}

def gen_diccionario(T, R, E, fecha):
    L = ["# Diccionario de datos\n", f"> Generado automáticamente por `tools/generar_docs_modelo.py` el {fecha}. No editar a mano: los cambios se pierden al regenerar.\n",
         "## Parámetros y funciones de Power Query\n", "| Nombre | Descripción | Definición |", "|---|---|---|"]
    for n, d, e in E:
        if e.lstrip().startswith("(") or "=>" in e.split("\n")[0]:
            L.append(f"| `{n}` | {PARAM_DESC.get(n) or esc(d)} | Función (ver `expressions.tmdl`) |")
        else:
            L.append(f"| `{n}` | {PARAM_DESC.get(n) or esc(d)} | `{esc(e.split(' meta ')[0])}` |")
    L += ["\n## Actualización incremental\n", "| Tabla | Ventana de historia | Se refresca en cada actualización |", "|---|---|---|"]
    for n, t in T.items():
        p = t["politica"]
        if p:
            L.append(f"| `{n}` | {p.get('rollingWindowPeriods')} {'años' if p.get('rollingWindowGranularity') == 'year' else p.get('rollingWindowGranularity')} | "
                     f"últimos {p.get('incrementalPeriods')} {'días' if p.get('incrementalGranularity') == 'day' else p.get('incrementalGranularity')} |")
    L += ["\n## Relaciones\n", "| Desde (muchos) | Hacia (uno) | Activa | Filtro |", "|---|---|---|---|"]
    for r in R:
        L.append(f"| `{r['desde']}` | `{r['hacia']}` | {'Sí' if r['activa'] else '**No** (inactiva)'} | {'ambas direcciones' if r['filtro'] == 'bothDirections' else 'una dirección'} |")
    L.append("\n## Tablas\n")
    for n, t in T.items():
        if n == "_Medidas": continue
        etiq = [x for x in ["tabla de fechas marcada" if t["fecha"] else "", "actualización incremental" if t["politica"] else ""] if x]
        L.append(f"### `{n}`" + (f" — {', '.join(etiq)}" if etiq else "") + "\n")
        L += ["| Columna | Tipo | Formato | Ordenar por | Notas |", "|---|---|---|---|---|"]
        for c in t["columnas"]:
            notas = ", ".join(x for x in ["clave" if c["clave"] else "", "oculta" if c["oculta"] else ""] if x)
            L.append(f"| `{c['nombre']}` | {c['tipo']} | {esc(c['fmt'])} | {('`' + c['orden'] + '`') if c['orden'] else ''} | {notas} |")
        for h, niv in t["jerarquias"]:
            L.append(f"\n**Jerarquía `{h}`:** " + " → ".join(f"{a} (`{b}`)" for a, b in niv))
        if t["fuente"]:
            L += ["\n<details><summary>Consulta de Power Query (M)</summary>\n", "```powerquery", t["fuente"], "```", "</details>\n"]
        L.append("")
    return "\n".join(L)

def gen_catalogo(T, fecha):
    ms = T["_Medidas"]["medidas"]; por = {}
    for m in ms: por.setdefault(grupo(m), []).append(m)
    L = ["# Catálogo de medidas DAX\n", f"> Generado automáticamente por `tools/generar_docs_modelo.py` el {fecha} ({len(ms)} medidas). No editar a mano.\n",
         "Convenciones: las medidas con prefijo `_` son auxiliares; `Semaforo_*` devuelve 1 = rojo, 2 = amarillo, 3 = verde. "
         "Las medidas de suma (lluvia, ETo, balance, horas, GDD, radiación acumulada) **suman por estación y promedian entre estaciones**; "
         "los máximos y mínimos devuelven **el extremo** de las estaciones seleccionadas. Ver `04_guia_usuario.md` y `06_decisiones_y_cambios.md`.\n",
         "## Índice\n"]
    orden = [g for g, _ in GRUPOS if g in por]
    for g in orden: L.append(f"- [{g}](#{ancla(g)}) ({len(por[g])})")
    for g in orden:
        L += [f"\n## {g}\n", "| Medida | Formato | Descripción |", "|---|---|---|"]
        for m in por[g]:
            fmt = esc(m["fmt"]) + (" · URL de imagen" if m["cat"] == "ImageUrl" else "")
            L.append(f"| `{m['nombre']}` | {fmt} | {esc(m['desc'])} |")
        for m in por[g]:
            L += [f"\n<details><summary><code>{m['nombre']}</code></summary>\n", "```dax", m["expr"], "```", "</details>"]
    return "\n".join(L)

def gen_visuales(fecha):
    orden = json.load(open(os.path.join(PAGS, "pages.json"), encoding="utf-8"))["pageOrder"]
    L = ["# Inventario de páginas y visuales\n", f"> Generado automáticamente por `tools/generar_docs_modelo.py` el {fecha}. No editar a mano.\n"]
    for pid in orden:
        pj = json.load(open(os.path.join(PAGS, pid, "page.json"), encoding="utf-8"))
        vis = []
        for vf in glob.glob(os.path.join(PAGS, pid, "visuals", "*", "visual.json")):
            d = json.load(open(vf, encoding="utf-8")); v = d.get("visual", {})
            tit = None
            for a, b in (("visualContainerObjects", "title"), ("objects", "header")):
                try: tit = v[a][b][0]["properties"]["text"]["expr"]["Literal"]["Value"].strip("'")
                except Exception: pass
                if tit: break
            campos = [p["queryRef"].split(".", 1)[-1] for w in v.get("query", {}).get("queryState", {}).values() for p in w["projections"]]
            pos = d.get("position", {})
            vis.append((round(pos.get("y", 0)), pos.get("x", 0), v.get("visualType"), tit, d["name"], campos))
        vis.sort()
        L += [f"## {pj['displayName'].strip()}\n", f"Tamaño {pj.get('width')}×{pj.get('height')} · {len(vis)} visuales · carpeta `{pid}`\n",
              "| Visual | Título | Campos | ID |", "|---|---|---|---|"]
        for y, x, tipo, tit, vid, campos in vis:
            if not campos: continue
            L.append(f"| {tipo} | {esc(tit)} | {esc(', '.join(campos))} | `{vid[:6]}` |")
        L.append("")
    return "\n".join(L)

if __name__ == "__main__":
    fecha = datetime.date.today().isoformat()
    T, R, E = tablas(), relaciones(), expresiones()
    os.makedirs(DOCS, exist_ok=True)
    for nombre, contenido in [("02_diccionario_datos.md", gen_diccionario(T, R, E, fecha)),
                              ("03_catalogo_medidas.md", gen_catalogo(T, fecha)),
                              ("09_inventario_visuales.md", gen_visuales(fecha))]:
        with open(os.path.join(DOCS, nombre), "w", encoding="utf-8", newline="\n") as f:
            f.write(contenido + "\n")
        print("OK", nombre)
