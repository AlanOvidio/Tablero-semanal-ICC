#!/usr/bin/env python3
"""
Genera en el modelo semántico los objetos del motor de riesgos a partir de config/riesgos_cultivo.csv:

  tables/Cultivos.tmdl         cultivos, grados día (base y tope) y orden
  tables/Riesgos_Cultivo.tmdl  riesgos con estado 'incluir' (umbrales, unidad, escala, aplicación, fuente)
  tables/_Riesgos.tmdl         medidas: una por riesgo (R_<ID>), medidas genéricas para visuales
                               (valor, semáforo, color, etiqueta, mapa de calor horario) y grados día por cultivo
  relationships.tmdl / model.tmdl   relación Riesgos_Cultivo -> Cultivos y referencias de tablas

Uso (con Power BI Desktop CERRADO):
    python tools/generar_riesgos_modelo.py
Estos archivos se regeneran completos: no editarlos a mano. La lógica de cada riesgo está en PLANTILLAS (abajo);
los valores numéricos se toman del CSV. Un riesgo nuevo en el CSV necesita su plantilla aquí.
"""
import csv, os, uuid

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEF = os.path.join(RAIZ, "2026_dashboard_exp1.SemanticModel", "definition")
NS = uuid.UUID("6f1c2f2e-4a51-4e7e-9a0e-1c0ffee0c0de")
tag = lambda *p: str(uuid.uuid5(NS, "/".join(p)))
CRLF = "\r\n"

CULTIVOS = [  # cultivo, orden, base, tope   (GDD con tope: min(max(Tmed-base,0), tope-base))
    ("Caña de azúcar", 1, 10, 34), ("Banano", 2, 15, 28), ("Aguacate", 3, 10, 24),
    ("Palma de aceite", 4, 15, 30), ("Granos básicos", 5, 10, 30)]

def num(x, d=None):
    try: return float(str(x).replace(",", "."))
    except Exception: return d
def f(x):  # número DAX
    v = num(x); return ("%g" % v) if v is not None else "BLANK()"

# ───────────────────────── variables por estación-día (en contexto de una estación y una fecha) ─────────────
V = {
 "tmed": "CALCULATE(AVERAGE(Fact_Diaria_met[Temp_Media]))",
 "tmin": "CALCULATE(MIN(Fact_Diaria_met[Temp_Min]))",
 "tmax": "CALCULATE(MAX(Fact_Diaria_met[Temp_Max]))",
 "hr":   "CALCULATE(AVERAGE(Fact_Diaria_met[HR_Media]))",
 "hrmin":"CALCULATE(MIN(Fact_Diaria_met[HR_Min]))",
 "p":    "CALCULATE(SUM(Fact_Diaria_met[Precip_Total]))",
 "bal":  "CALCULATE(SUM(Fact_Diaria_met[Balance_Hidrico]))",
 "mojd": "CALCULATE(MAX(Fact_Subdiaria_met_aux[Mojadura_Horas_Diurna]))",
 "mojn": "CALCULATE(MAX(Fact_Subdiaria_met_aux[Mojadura_Horas_Nocturna]))",
 "mojt": "CALCULATE(MAX(Fact_Subdiaria_met_aux[Mojadura_Horas_Total]))",
 "vmax": "CALCULATE(MAX(Fact_Subdiaria_met_aux[Viento_Max]))",
 "h90":  "CALCULATE(COUNTROWS(FILTER(Fact_Horaria_riesgo, Fact_Horaria_riesgo[HR_Media] > 90)))",
 "p30":  "CALCULATE(SUM(Fact_Diaria_met[Precip_Total]), DATESBETWEEN(Calendario[Fecha], _d - 29, _d))",
 "seco3":"CALCULATE(COUNTROWS(FILTER(Fact_Diaria_met, Fact_Diaria_met[Precip_Total] < 1)), DATESBETWEEN(Calendario[Fecha], _d - 2, _d))",
}
NOBLANK = {"tmed", "tmin", "tmax", "hr", "hrmin", "p", "bal", "mojd", "mojn", "mojt", "vmax"}  # exigir dato

# ───────────────────────── plantillas por riesgo ─────────────────────────
# tipo 'dia'   : cuenta días favorables por estación y promedia estaciones    -> cond(r) usa variables V
# tipo 'hora'  : cuenta horas favorables (Fact_Horaria_riesgo) por estación     -> hcond(r) en columnas horarias
# tipo 'horas_dia': horas favorables por día (promedio)                       -> hcond
# tipo 'semana': evaluación sobre todo el periodo en contexto por estación     -> expr(r) completa por estación
# tipo 'max'   : valor extremo (máximo) del periodo                            -> expr
# 'horaria'    : condición horaria para el mapa de calor (opcional)
H = lambda c: f"Fact_Horaria_riesgo[{c}]"
T, HR, MJ, PP, RD, VT = H("Temp_Media"), H("HR_Media"), H("Mojadura_Max"), H("Precip_Total"), H("Rad_Media"), H("Viento_Media")
rng = lambda v, a, b: f"{v} >= {f(a)} && {v} <= {f(b)}"
PL = {
 "CAN_ROYA_CAFE": dict(tipo="dia", cond=lambda r: f"{rng('tmed', r['t_min'], r['t_max'])} && hr > {f(r['hr_min'])} && mojt >= {f(r['mojadura_min_h'])}",
                       horaria=lambda r: f"{rng(T, r['t_min'], r['t_max'])} && {HR} > {f(r['hr_min'])} && {MJ} > 4"),
 "CAN_ROYA_NARANJA": dict(tipo="dia", cond=lambda r: f"( {rng('tmed', r['t_min'], r['t_max'])} ) || ( tmed > {f(r['t_max'])} && mojt > {f(r['mojadura_min_h'])} )",
                       horaria=lambda r: f"{rng(T, 18, 28)} && ( {HR} >= 98 || {MJ} > 4 )"),
 "CAN_ESCALDADURA": dict(tipo="dia", cond=lambda r: f"p > {f(r['lluvia_min_mm'])} && vmax > 30"),
 "CAN_SALIVOSA": dict(tipo="dia", cond=lambda r: f"p > {f(r['lluvia_min_mm'])} && hr > {f(r['hr_min'])} && {rng('tmed', r['t_min'], r['t_max'])}",
                       horaria=lambda r: f"{rng(T, r['t_min'], r['t_max'])} && {HR} > {f(r['hr_min'])} && {PP} > 0"),
 "CAN_BARRENADOR": dict(tipo="dia", cond=lambda r: f"tmed > {f(r['t_min'])} && hr >= {f(r['hr_min'])} && hr <= {f(r['hr_max'])} && p < {f(r['lluvia_max_mm'])}",
                        horaria=lambda r: f"{T} > {f(r['t_min'])} && {HR} >= {f(r['hr_min'])} && {HR} <= {f(r['hr_max'])} && {PP} = 0"),
 "CAN_CHINCHE_ENCAJE": dict(tipo="semana", expr=lambda r:
     "VAR _fuerte = CALCULATE(COUNTROWS(FILTER(Fact_Diaria_met, Fact_Diaria_met[Precip_Total] > 20)))" + CRLF +
     f"VAR _secos = CALCULATE(COUNTROWS(FILTER(Fact_Diaria_met, Fact_Diaria_met[Precip_Total] < {f(r['lluvia_max_mm'])})))" + CRLF +
     "RETURN IF(COALESCE(_fuerte, 0) > 0, 0, COALESCE(_secos, 0))"),
 "CAN_COLUDO": dict(tipo="dia", cond=lambda r: f"p < {f(r['lluvia_max_mm'])} && hr < {f(r['hr_max'])}"),
 "CAN_ESTRES": dict(tipo="hora", hcond=lambda r: f"{T} > {f(r['t_min'])} && {RD} > 800", horaria=lambda r: f"{T} > {f(r['t_min'])} && {RD} > 800"),
 "CAN_SUELO_SATURADO": dict(tipo="dia", cond=lambda r: f"p > {f(r['lluvia_min_mm'])}"),
 "CAN_APLICACION": dict(tipo="horas_dia", hcond=lambda r: f"{T} < {f(r['t_max'])} && {HR} > {f(r['hr_min'])} && {VT} < 10 && {RD} > 40",
                        horaria=lambda r: f"{T} < {f(r['t_max'])} && {HR} > {f(r['hr_min'])} && {VT} < 10 && {RD} > 40"),
 "CAN_QUEMA": dict(tipo="dia", cond=lambda r: f"hrmin < {f(r['hr_max'])} && vmax > 20 && seco3 = 3"),
 "CAN_MADURACION": dict(tipo="dia", cond=lambda r: f"(tmax - tmin) >= {f(r['t_min'])} && p30 >= {f(r['lluvia_min_mm'])} && p30 <= {f(r['lluvia_max_mm'])}"),
 "CAN_FLORACION": dict(tipo="dia", fechas="MONTH(Calendario[Fecha]) = 8 && DAY(Calendario[Fecha]) >= 16",
                       cond=lambda r: f"{rng('tmin', r['t_min'], r['t_max'])} && tmax <= 32"),
 "CAN_ACAME": dict(tipo="dia", cond=lambda r: f"vmax > 40 && p > {f(r['lluvia_min_mm'])}"),
 "BAN_SIG_NEGRA": dict(tipo="dia", cond=lambda r: f"{rng('tmed', r['t_min'], r['t_max'])} && hr > {f(r['hr_min'])} && mojn > {f(r['mojadura_min_h'])}",
                       horaria=lambda r: f"{rng(T, r['t_min'], r['t_max'])} && ( {HR} > {f(r['hr_min'])} || {MJ} > 4 )"),
 "BAN_MOKO": dict(tipo="semana", expr=lambda r:
     "VAR _p = CALCULATE(SUM(Fact_Diaria_met[Precip_Total]))" + CRLF + "VAR _b = CALCULATE(SUM(Fact_Diaria_met[Balance_Hidrico]))" + CRLF +
     f"RETURN IF(_p > {f(r['lluvia_min_mm'])} && _b > 0, 1, 0)"),
 "BAN_VOLCAMIENTO": dict(tipo="max", expr=lambda r: "CALCULATE(MAX(Fact_Subdiaria_met_aux[Viento_Max_Diurno]))"),
 "BAN_ESTRES": dict(tipo="hora", hcond=lambda r: f"{T} > {f(r['t_min'])} && {RD} > 800", horaria=lambda r: f"{T} > {f(r['t_min'])} && {RD} > 800"),
 "AGU_PHYTO": dict(tipo="dia", cond=lambda r: f"{rng('tmed', r['t_min'], r['t_max'])} && bal > 0"),
 "AGU_ANTRACNOSIS": dict(tipo="dia", cond=lambda r: f"{rng('tmed', r['t_min'], r['t_max'])} && hr > {f(r['hr_min'])} && ( p > {f(r['lluvia_min_mm'])} || mojt > {f(r['mojadura_min_h'])} )",
                         horaria=lambda r: f"{rng(T, r['t_min'], r['t_max'])} && {HR} > {f(r['hr_min'])} && ( {MJ} > 4 || {PP} > 0 )"),
 "AGU_FRIO": dict(tipo="dia", cond=lambda r: f"tmin < {f(r['t_max'])}"),
 "AGU_CALOR": dict(tipo="hora", hcond=lambda r: f"{T} > {f(r['t_min'])} && {RD} > 800", horaria=lambda r: f"{T} > {f(r['t_min'])} && {RD} > 800"),
 "AGU_VIENTO": dict(tipo="max", expr=lambda r: "CALCULATE(MAX(Fact_Subdiaria_met_aux[Viento_Max_Diurno]))"),
 "AGU_ACAROS": dict(tipo="dia", cond=lambda r: f"p < {f(r['lluvia_max_mm'])} && hr < {f(r['hr_max'])} && vmax > 20"),
 "PAL_PC": dict(tipo="dia", cond=lambda r: f"{rng('tmed', r['t_min'], r['t_max'])} && hr > {f(r['hr_min'])} && p > {f(r['lluvia_min_mm'])}",
                horaria=lambda r: f"{rng(T, r['t_min'], r['t_max'])} && {HR} > {f(r['hr_min'])} && {PP} > 0"),
 "PAL_ESTRES": dict(tipo="hora", hcond=lambda r: f"{T} > {f(r['t_min'])} && {RD} > 800", horaria=lambda r: f"{T} > {f(r['t_min'])} && {RD} > 800"),
 "MAI_ASFALTO": dict(tipo="dia", cond=lambda r: f"{rng('tmed', r['t_min'], r['t_max'])} && hr > {f(r['hr_min'])} && mojn >= {f(r['mojadura_min_h'])}",
                     horaria=lambda r: f"{rng(T, r['t_min'], r['t_max'])} && {HR} > {f(r['hr_min'])} && {MJ} > 4"),
 "MAI_ROYA": dict(tipo="dia", cond=lambda r: f"{rng('tmin', r['t_min'], r['t_max'])} && mojt >= {f(r['mojadura_min_h'])}",
                  horaria=lambda r: f"{rng(T, 16, 23)} && {MJ} > 4"),
 "MAI_TIZON": dict(tipo="dia", cond=lambda r: f"{rng('tmed', r['t_min'], r['t_max'])} && mojt >= {f(r['mojadura_min_h'])}",
                   horaria=lambda r: f"{rng(T, r['t_min'], r['t_max'])} && {MJ} > 4"),
 "MAI_MANCHA_GRIS": dict(tipo="dia", cond=lambda r: f"{rng('tmed', r['t_min'], r['t_max'])} && h90 >= {f(r['horas_min_dia'])}",
                         horaria=lambda r: f"{rng(T, r['t_min'], r['t_max'])} && {HR} > {f(r['hr_min'])}"),
 "MAI_COGOLLERO": dict(tipo="dia", cond=lambda r: f"tmax > {f(r['t_min'])} && p < {f(r['lluvia_max_mm'])}"),
 "MAI_ACHAPARRAMIENTO": dict(tipo="dia", cond=lambda r: f"p < {f(r['lluvia_max_mm'])} && tmed > {f(r['t_min'])} && hr < {f(r['hr_max'])}"),
 "MAI_PUDRICION_MAZORCA": dict(tipo="dia", cond=lambda r: f"p > {f(r['lluvia_min_mm'])}"),
 "MAI_CALOR_FLOR": dict(tipo="dia", cond=lambda r: f"tmax > {f(r['t_min'])}"),
 "FRI_MUSTIA": dict(tipo="dia", cond=lambda r: f"{rng('tmed', r['t_min'], r['t_max'])} && p > {f(r['lluvia_min_mm'])}"),
 "FRI_ROYA": dict(tipo="dia", cond=lambda r: f"{rng('tmed', r['t_min'], r['t_max'])} && ( p > {f(r['lluvia_min_mm'])} || mojn >= {f(r['mojadura_min_h'])} )",
                  horaria=lambda r: f"{rng(T, r['t_min'], r['t_max'])} && ( {HR} > 95 || {MJ} > 4 )"),
 "FRI_ANTRACNOSIS": dict(tipo="dia", cond=lambda r: f"{rng('tmed', r['t_min'], r['t_max'])} && hr > {f(r['hr_min'])} && p >= {f(r['lluvia_min_mm'])}"),
 "FRI_MANCHA_ANGULAR": dict(tipo="semana", expr=lambda r:
     "VAR _lluv = CALCULATE(COUNTROWS(FILTER(Fact_Diaria_met, Fact_Diaria_met[Precip_Total] >= 1)))" + CRLF +
     "VAR _sec = CALCULATE(COUNTROWS(FILTER(Fact_Diaria_met, Fact_Diaria_met[Precip_Total] < 1)))" + CRLF +
     f"VAR _t = CALCULATE(COUNTROWS(FILTER(Fact_Diaria_met, Fact_Diaria_met[Temp_Media] >= {f(r['t_min'])} && Fact_Diaria_met[Temp_Media] <= {f(r['t_max'])})))" + CRLF +
     "RETURN IF(COALESCE(_lluv, 0) >= 2 && COALESCE(_sec, 0) >= 2, COALESCE(_t, 0), 0)"),
 "FRI_BACTERIOSIS": dict(tipo="dia", cond=lambda r: f"{rng('tmed', r['t_min'], r['t_max'])} && p > {f(r['lluvia_min_mm'])}"),
 "FRI_MOSAICO": dict(tipo="dia", cond=lambda r: f"{rng('tmed', r['t_min'], r['t_max'])} && p < {f(r['lluvia_max_mm'])}"),
 "FRI_CALOR_FLOR": dict(tipo="dia", cond=lambda r: f"tmax > {f(r['t_min'])}"),
 "GRA_SEQUIA": dict(tipo="dia", cond=lambda r: f"p < {f(r['lluvia_max_mm'])}"),
}

# Condiciones horarias: una hora sin dato en alguna variable usada no cuenta como favorable
# (en DAX un BLANK se compara como 0, p. ej. T < 30 sería verdadero).
def con_dato(fn):
    def g(r):
        c = fn(r)
        cols = [col for col in (T, HR, MJ, PP, RD, VT) if col in c]
        return " && ".join([f"NOT ISBLANK({col})" for col in cols] + [f"( {c} )"]) if cols else c
    return g
for _pl in PL.values():
    for _k in ("horaria", "hcond"):
        if _k in _pl: _pl[_k] = con_dato(_pl[_k])

def usadas(expr):
    import re
    return [v for v in V if re.search(r"\b%s\b" % v, expr)]

def filtro_estaciones(r, tabla):
    c = [f"NOT ISEMPTY(CALCULATETABLE({tabla}))"]
    if num(r["alt_min_m"]) is not None: c.append(f"CALCULATE(MAX(Estaciones_met[altitud])) >= {f(r['alt_min_m'])}")
    if num(r["alt_max_m"]) is not None: c.append(f"CALCULATE(MAX(Estaciones_met[altitud])) < {f(r['alt_max_m'])}")
    return ("VAR _Est =" + CRLF + "    FILTER(" + CRLF + "        VALUES(Estaciones_met[estacionid])," + CRLF +
            "        " + (CRLF + "            && ").join(c) + CRLF + "    )" + CRLF)

def filtro_fechas(r, pl):
    if pl.get("fechas"): return pl["fechas"]
    m = [x for x in str(r["meses"]).split(",") if x.strip()]
    return f"MONTH(Calendario[Fecha]) IN {{ {', '.join(m)} }}" if m else ""

def dax_riesgo(r):
    pl = PL[r["id"]]; t = pl["tipo"]
    if t == "dia":
        cond = pl["cond"](r); us = usadas(cond)
        fe = filtro_fechas(r, pl)
        fechas = f"FILTER(VALUES(Calendario[Fecha]), {fe})" if fe else "VALUES(Calendario[Fecha])"
        vs = [f"            VAR _d = Calendario[Fecha]"] if any(v in us for v in ("p30", "seco3")) else []
        vs += [f"            VAR {v} = {V[v]}" for v in us]
        guard = " && ".join(f"NOT ISBLANK({v})" for v in us if v in NOBLANK) or "TRUE()"
        return (filtro_estaciones(r, "Fact_Diaria_met") + "RETURN" + CRLF + "AVERAGEX(" + CRLF + "    _Est," + CRLF +
                "    SUMX(" + CRLF + f"        {fechas}," + CRLF + CRLF.join(vs) + CRLF +
                f"            RETURN IF({guard} && ( {cond} ), 1, 0)" + CRLF + "    )" + CRLF + ")")
    if t in ("hora", "horas_dia"):
        hc = pl["hcond"](r)
        fe = filtro_fechas(r, pl)
        base = f"CALCULATE(COUNTROWS(FILTER(Fact_Horaria_riesgo, {hc}))" + (f", FILTER(VALUES(Calendario[Fecha]), {fe})" if fe else "") + ")"
        val = f"COALESCE({base}, 0)" if t == "hora" else f"DIVIDE(COALESCE({base}, 0), CALCULATE(DISTINCTCOUNT(Fact_Horaria_riesgo[Fecha])))"
        return filtro_estaciones(r, "Fact_Horaria_riesgo") + "RETURN" + CRLF + f"AVERAGEX(_Est, {val})"
    if t == "semana":
        body = pl["expr"](r).replace(CRLF, CRLF + "        ")
        return filtro_estaciones(r, "Fact_Diaria_met") + "RETURN" + CRLF + "AVERAGEX(" + CRLF + "    _Est," + CRLF + "    CALCULATE(" + CRLF + "        " + body + CRLF + "    )" + CRLF + ")"
    if t == "max":
        return pl["expr"](r)
    raise ValueError(t)

# ───────────────────────── lectura del CSV ─────────────────────────
R = list(csv.DictReader(open(os.path.join(RAIZ, "config", "riesgos_cultivo.csv"), encoding="utf-8-sig"), delimiter=";"))
INC = [r for r in R if r["estado"] == "incluir"]
sin = [r["id"] for r in INC if r["id"] not in PL]
if sin: print("AVISO: riesgos 'incluir' sin plantilla (no se generan):", ", ".join(sin))
INC = [r for r in INC if r["id"] in PL]
ORD = {c: i for c, i, _, _ in CULTIVOS}

# ───────────────────────── TMDL helpers ─────────────────────────
def mstr(x): return '"' + str(x).replace('"', '""') + '"'
def mval(x, tipo):
    if tipo == "text": return mstr(x or "")
    if tipo == "logical": return "true" if x else "false"
    v = num(x); return "null" if v is None else ("%g" % v)

def tabla_m(nombre, columnas, filas, sort=None, ocultas=()):
    """columnas: [(nombre, tipoM, dataTypeTMDL, formato)]"""
    L = [f"table {nombre}", f"\tlineageTag: {tag(nombre)}", ""]
    for c, tm, dt, fmt in columnas:
        L += [f"\tcolumn {c if c.isidentifier() else repr(c)}", f"\t\tdataType: {dt}"]
        if fmt: L.append(f"\t\tformatString: {fmt}")
        if c in ocultas: L.append("\t\tisHidden")
        L += [f"\t\tlineageTag: {tag(nombre, c)}", "\t\tsummarizeBy: none", f"\t\tsourceColumn: {c}"]
        if sort and c in sort: L.append(f"\t\tsortByColumn: {sort[c]}")
        L += ["", "\t\tannotation SummarizationSetBy = User", ""]
    tipos = ", ".join(f"{c} = {tm}" for c, tm, _, _ in columnas)
    filas_m = ("," + CRLF + "\t\t\t\t\t").join("{" + ", ".join(mval(v, tm) for v, (_, tm, _, _) in zip(fila, columnas)) + "}" for fila in filas)
    L += [f"\tpartition {nombre} = m", "\t\tmode: import", "\t\tsource =", "\t\t\t\tlet",
          f"\t\t\t\t    // Generado por tools/generar_riesgos_modelo.py desde config/riesgos_cultivo.csv. No editar a mano.",
          f"\t\t\t\t    Tabla = #table(type table [{tipos}], {{" + CRLF + "\t\t\t\t\t" + filas_m + CRLF + "\t\t\t\t    })",
          "\t\t\t\tin", "\t\t\t\t    Tabla", "", "\tannotation PBI_ResultType = Table", ""]
    return CRLF.join(L)

def medida(nombre, expr, fmt=None, carpeta=None, desc=None, cat=None, fmtdef=None):
    L = []
    if desc: L.append(f"\t/// {desc}")
    L.append(f"\tmeasure {nombre} = ```")
    L += ["\t\t\t" + l for l in expr.replace(CRLF, "\n").split("\n")]
    L.append("\t\t\t```")
    if fmt: L.append(f"\t\tformatString: {fmt}")
    if cat: L.append(f"\t\tdataCategory: {cat}")
    if carpeta: L.append(f"\t\tdisplayFolder: {carpeta}")
    L.append(f"\t\tlineageTag: {tag('_Riesgos', nombre)}")
    # formatStringDefinition es un objeto hijo en TMDL: debe ir al final de la medida
    if fmtdef: L += ["", f"\t\tformatStringDefinition = {fmtdef}"]
    L.append("")
    return CRLF.join(L)

# ───────────────────────── Cultivos ─────────────────────────
cult_cols = [("Cultivo", "text", "string", None), ("Orden", "Int64.Type", "int64", "0"),
             ("GDD_Base", "number", "double", "0.0"), ("GDD_Tope", "number", "double", "0.0")]
open(os.path.join(DEF, "tables", "Cultivos.tmdl"), "w", encoding="utf-8", newline="").write(
    tabla_m("Cultivos", cult_cols, CULTIVOS, sort={"Cultivo": "Orden"}, ocultas=("Orden",)))

# ───────────────────────── Riesgos_Cultivo ─────────────────────────
filas = []
orden_nombre = {}
for i, r in enumerate(INC, 1):
    orden_nombre.setdefault(r["riesgo"], ORD.get(r["cultivo"], 9) * 100 + i)
def categoria(tipo):
    t = tipo.lower()
    if t.startswith("enfermedad"): return "Enfermedades", 1
    if t.startswith("plaga"): return "Plagas", 2
    if t.startswith("abi"): return "Clima (abióticos)", 3
    return "Manejo y producción", 4
for i, r in enumerate(INC, 1):
    am, ro = num(r["umbral_amarillo"]), num(r["umbral_rojo"])
    inv = am is not None and ro is not None and ro < am
    filas.append([r["id"], r["cultivo"], r["riesgo"], r["tipo"], r["escala"], r["semaforo_unidad"], am, ro, inv,
                  "horaria" in PL[r["id"]], r["condicion"], r["aplicacion"], r["fuente"], r["confianza"],
                  r["validado"] == "si", ORD.get(r["cultivo"], 9) * 100 + i, orden_nombre[r["riesgo"]], *categoria(r["tipo"])])
rc_cols = [("ID", "text", "string", None), ("Cultivo", "text", "string", None), ("Riesgo", "text", "string", None),
           ("Tipo", "text", "string", None), ("Escala", "text", "string", None), ("Unidad", "text", "string", None),
           ("Umbral_Amarillo", "number", "double", "0.##"), ("Umbral_Rojo", "number", "double", "0.##"),
           ("Invertido", "logical", "boolean", None), ("Tiene_Horaria", "logical", "boolean", None),
           ("Condicion", "text", "string", None), ("Aplicacion", "text", "string", None), ("Fuente", "text", "string", None),
           ("Confianza", "text", "string", None), ("Validado", "logical", "boolean", None), ("Orden", "Int64.Type", "int64", "0"),
           ("Orden_Nombre", "Int64.Type", "int64", "0"), ("Categoria", "text", "string", None), ("Orden_Categoria", "Int64.Type", "int64", "0")]
open(os.path.join(DEF, "tables", "Riesgos_Cultivo.tmdl"), "w", encoding="utf-8", newline="").write(
    tabla_m("Riesgos_Cultivo", rc_cols, filas, sort={"Riesgo": "Orden_Nombre", "Categoria": "Orden_Categoria"}, ocultas=("Orden", "Orden_Nombre", "Orden_Categoria")))

# ───────────────────────── Vistas_Mapa_Calor ─────────────────────────
# Vista, orden, unidad, formato, leyenda, cortes [(límite superior, color)...] y color final
VISTAS = [
    ("Riesgos", "% de horas-estación", "0%", "blanco 0 · amarillo < 25 % · naranja 25–50 % · rojo ≥ 50 %",
     [(0.0000001, "#FFFFFF"), (0.25, "#F9E79F"), (0.5, "#F39C12")], "#C0392B"),
    ("Temperatura", "°C", "0.0", "azul < 18 · celeste 18–24 · amarillo 24–30 · naranja 30–34 · rojo ≥ 34",
     [(18, "#4575B4"), (24, "#91BFDB"), (30, "#FFFFBF"), (34, "#FC8D59")], "#D73027"),
    ("Humedad relativa", "%", "0", "blanco < 60 · celeste 60–80 · azul 80–90 · azul oscuro ≥ 90",
     [(60, "#F7FBFF"), (80, "#C6DBEF"), (90, "#6BAED6")], "#2171B5"),
    ("Déficit de presión de vapor", "kPa", "0.00", "azul < 0.4 (muy húmedo) · verde 0.4–1.2 · amarillo 1.2–1.6 · rojo ≥ 1.6 (estrés)",
     [(0.4, "#6BAED6"), (1.2, "#A1D99B"), (1.6, "#FED976")], "#F03B20"),
    ("Sensación térmica", "°C", "0.0", "blanco < 27 · amarillo 27–32 (precaución) · naranja claro 32–41 (precaución extrema) · naranja 41–54 (peligro) · rojo ≥ 54",
     [(27, "#FFFFFF"), (32, "#FFFFB2"), (41, "#FECC5C"), (54, "#FD8D3C")], "#E31A1C"),
    ("Mojadura", "% de horas-estación mojadas", "0%", "blanco 0 · celeste < 50 % · azul ≥ 50 %",
     [(0.0000001, "#FFFFFF"), (0.5, "#9ECAE1")], "#3182BD"),
    ("Lluvia", "mm/h", "0.0", "blanco 0 · celeste < 1 · azul claro 1–5 · azul 5–10 · azul oscuro ≥ 10",
     [(0.0000001, "#FFFFFF"), (1, "#DEEBF7"), (5, "#9ECAE1"), (10, "#4292C6")], "#08519C"),
    ("Viento", "km/h", "0.0", "blanco calma < 1.8 · verde claro 1.8–10 · verde 10–20 · verde medio 20–30 · verde oscuro ≥ 30",
     [(1.8, "#FFFFFF"), (10, "#E5F5E0"), (20, "#A1D99B"), (30, "#41AB5D")], "#006D2C"),
    ("Radiación", "W/m²", "0", "gris ≤ 40 (sin luz) · amarillo claro 40–300 · amarillo 300–600 · naranja 600–800 · naranja oscuro ≥ 800",
     [(40.0000001, "#F0F0F0"), (300, "#FFF7BC"), (600, "#FEC44F"), (800, "#FE9929")], "#D95F0E"),
]
OSCUROS = ["#4575B4", "#D73027", "#2171B5", "#F03B20", "#E31A1C", "#3182BD", "#4292C6", "#08519C", "#41AB5D", "#006D2C", "#D95F0E", "#C0392B"]
vis_cols = [("Vista", "text", "string", None), ("Orden", "Int64.Type", "int64", "0"), ("Unidad", "text", "string", None), ("Leyenda", "text", "string", None)]
open(os.path.join(DEF, "tables", "Vistas_Mapa_Calor.tmdl"), "w", encoding="utf-8", newline="").write(
    tabla_m("Vistas_Mapa_Calor", vis_cols, [[v[0], i, v[1], v[3]] for i, v in enumerate(VISTAS, 1)], sort={"Vista": "Orden"}, ocultas=("Orden",)))

# ───────────────────────── _Riesgos (medidas) ─────────────────────────
M = ["table _Riesgos", f"\tlineageTag: {tag('_Riesgos')}", ""]
for r in INC:
    d = f"{r['riesgo']} ({r['cultivo']}). Unidad: {r['semaforo_unidad']}. {r['condicion']}".replace("\n", " ")
    M.append(medida(f"R_{r['id']}", dax_riesgo(r), "0.#", "Riesgos por ID", d[:400]))
sw = lambda nombre_fn: (CRLF + "    ").join(f'"{r["id"]}", {nombre_fn(r)},' for r in INC)
M.append(medida("_Riesgo_En_Cultivo",
    "NOT ISEMPTY(" + CRLF + "    CALCULATETABLE(" + CRLF + "        VALUES(Riesgos_Cultivo[ID])," + CRLF +
    "        TREATAS(VALUES(Cultivos[Cultivo]), Riesgos_Cultivo[Cultivo])" + CRLF + "    )" + CRLF + ")", None, "Genéricas",
    "TRUE si el riesgo en contexto pertenece al cultivo seleccionado (garantiza que no se muestren riesgos de otros cultivos)."))
M.append(medida("Riesgo_Valor",
    "VAR _id = SELECTEDVALUE(Riesgos_Cultivo[ID])" + CRLF + "RETURN" + CRLF + "IF(" + CRLF + "    [_Riesgo_En_Cultivo]," + CRLF + "SWITCH(" + CRLF + "    _id," + CRLF + "    " +
    sw(lambda r: f"[R_{r['id']}]") + CRLF + "    BLANK()" + CRLF + ")" + CRLF + ")", "0.#", "Genéricas",
    "Valor del riesgo seleccionado (días, horas o km/h según la unidad), promediado entre estaciones."))
M.append(medida("Riesgo_Semaforo",
    "VAR _v = [Riesgo_Valor]" + CRLF + "VAR _am = SELECTEDVALUE(Riesgos_Cultivo[Umbral_Amarillo])" + CRLF +
    "VAR _ro = SELECTEDVALUE(Riesgos_Cultivo[Umbral_Rojo])" + CRLF + "VAR _inv = SELECTEDVALUE(Riesgos_Cultivo[Invertido])" + CRLF +
    "RETURN" + CRLF + "IF(" + CRLF + "    ISBLANK(_v) || ISBLANK(_am), BLANK()," + CRLF +
    "    IF(_inv," + CRLF + "        SWITCH(TRUE(), _v <= _ro, 1, _v <= _am, 2, 3)," + CRLF +
    "        SWITCH(TRUE(), _v >= _ro, 1, _v >= _am, 2, 3)" + CRLF + "    )" + CRLF + ")", "0", "Genéricas",
    "1 = alerta, 2 = precaución, 3 = normal. En indicadores favorables (invertidos) menos valor es peor."))
M.append(medida("Riesgo_Color", 'SWITCH([Riesgo_Semaforo], 1, "#D64550", 2, "#F2B134", 3, "#3BA272", "#B0B0B0")', None, "Genéricas",
    "Color hexadecimal del semáforo para formato condicional."))
M.append(medida("Riesgo_Etiqueta",
    'VAR _v = [Riesgo_Valor]' + CRLF + 'RETURN IF(NOT [_Riesgo_En_Cultivo], BLANK(), IF(ISBLANK(_v), "Sin datos", FORMAT(_v, "0.#") & " " & SELECTEDVALUE(Riesgos_Cultivo[Unidad])))',
    None, "Genéricas", "Valor con su unidad para tarjetas."))
M.append(medida("Riesgos_En_Alerta",
    "COUNTROWS(FILTER(VALUES(Riesgos_Cultivo[ID]), [Riesgo_Semaforo] = 1))", "0", "Genéricas", "Número de riesgos del cultivo en alerta (rojo)."))
M.append(medida("Riesgos_En_Precaucion",
    "COUNTROWS(FILTER(VALUES(Riesgos_Cultivo[ID]), [Riesgo_Semaforo] = 2))", "0", "Genéricas", "Número de riesgos del cultivo en precaución (amarillo)."))
hor = [r for r in INC if "horaria" in PL[r["id"]]]
# Mapa de calor horario: riesgos elegidos (segmentador categoría → riesgo, o clic en el semáforo);
# sin selección válida, todos los riesgos horarios del cultivo que no son indicadores favorables.
IDS_HORA = ("VAR _cult = TREATAS(VALUES(Cultivos[Cultivo]), Riesgos_Cultivo[Cultivo])" + CRLF +
    "VAR _sel = CALCULATETABLE(VALUES(Riesgos_Cultivo[ID]), Riesgos_Cultivo[Tiene_Horaria] = TRUE(), _cult)" + CRLF +
    "VAR _todos = CALCULATETABLE(VALUES(Riesgos_Cultivo[ID]), REMOVEFILTERS(Riesgos_Cultivo), Riesgos_Cultivo[Tiene_Horaria] = TRUE(), Riesgos_Cultivo[Invertido] = FALSE(), _cult)" + CRLF +
    "VAR _usarSel = ( ISFILTERED(Riesgos_Cultivo[Categoria]) || ISFILTERED(Riesgos_Cultivo[Riesgo]) || ISFILTERED(Riesgos_Cultivo[ID]) ) && NOT ISEMPTY(_sel)" + CRLF +
    "VAR _ids = UNION(FILTER(_sel, _usarSel), FILTER(_todos, NOT _usarSel))" + CRLF)
M.append(medida("Riesgo_Hora",
    IDS_HORA + "VAR _n = COUNTROWS(Fact_Horaria_riesgo)" + CRLF +
    "VAR _fav =" + CRLF + "    COUNTROWS(" + CRLF + "        FILTER(" + CRLF + "            Fact_Horaria_riesgo," + CRLF + "            " +
    (CRLF + "            || ").join(f'( "{r["id"]}" IN _ids && {PL[r["id"]]["horaria"](r)} )' for r in hor) + CRLF +
    "        )" + CRLF + "    )" + CRLF +
    "RETURN IF(NOT ISEMPTY(_ids), DIVIDE(_fav + 0, _n))", "0%", "Genéricas",
    "Mapa de calor: fracción de horas-estación con al menos un riesgo elegido favorable (un riesgo, una categoría o todos los riesgos horarios del cultivo)."))
M.append(medida("Riesgo_Hora_N",
    IDS_HORA + "VAR _n = COUNTROWS(Fact_Horaria_riesgo)" + CRLF + "RETURN" + CRLF +
    "DIVIDE(" + CRLF + "    SUMX(" + CRLF + "        _ids," + CRLF + "        SWITCH(" + CRLF + "            Riesgos_Cultivo[ID]," + CRLF + "            " +
    (CRLF + "            ").join(f'"{r["id"]}", COUNTROWS(FILTER(Fact_Horaria_riesgo, {PL[r["id"]]["horaria"](r)})) + 0,' for r in hor) + CRLF +
    "            0" + CRLF + "        )" + CRLF + "    )," + CRLF + "    _n" + CRLF + ")", "0.0", "Genéricas",
    "Mapa de calor (tooltip): número promedio de riesgos elegidos favorables por hora-estación."))
M.append(medida("Riesgo_Hora_Titulo",
    IDS_HORA + "VAR _k = COUNTROWS(_ids)" + CRLF +
    "VAR _nom = CALCULATE(SELECTEDVALUE(Riesgos_Cultivo[Riesgo]), REMOVEFILTERS(Riesgos_Cultivo), TREATAS(_ids, Riesgos_Cultivo[ID]))" + CRLF +
    "VAR _grupo =" + CRLF + "    IF(" + CRLF + "        _usarSel," + CRLF +
    '        IF(ISFILTERED(Riesgos_Cultivo[Riesgo]) || ISFILTERED(Riesgos_Cultivo[ID]), "Riesgos seleccionados", CONCATENATEX(CALCULATETABLE(VALUES(Riesgos_Cultivo[Categoria]), TREATAS(_ids, Riesgos_Cultivo[ID])), Riesgos_Cultivo[Categoria], ", ")),' + CRLF +
    '        "Todos los riesgos"' + CRLF + "    )" + CRLF + "RETURN" + CRLF +
    "SWITCH(" + CRLF + "    TRUE()," + CRLF +
    '    _k = 0, "Sin riesgos con condición horaria para este cultivo",' + CRLF +
    '    _k = 1, "Horas favorables a " & LOWER(_nom) & " (% de horas-estación)",' + CRLF +
    '    _grupo & ": % de horas-estación con al menos uno de " & _k & " riesgos favorable"' + CRLF + ")",
    None, "Genéricas", "Título del mapa de calor horario según lo que se está mostrando."))
VSEL = 'VAR _v = SELECTEDVALUE(Vistas_Mapa_Calor[Vista], "Riesgos")' + CRLF
FH = lambda c: f"Fact_Horaria_riesgo[{c}]"
M.append(medida("Mapa_Calor_Valor",
    VSEL + "RETURN" + CRLF + "SWITCH(" + CRLF + "    _v," + CRLF +
    '    "Riesgos", [Riesgo_Hora],' + CRLF +
    f'    "Temperatura", AVERAGE({FH("Temp_Media")}),' + CRLF +
    f'    "Humedad relativa", AVERAGE({FH("HR_Media")}),' + CRLF +
    f'    "Déficit de presión de vapor", AVERAGEX(FILTER(Fact_Horaria_riesgo, NOT ISBLANK({FH("Temp_Media")}) && NOT ISBLANK({FH("HR_Media")})), 0.6108 * EXP(17.27 * {FH("Temp_Media")} / ({FH("Temp_Media")} + 237.3)) * (1 - {FH("HR_Media")} / 100)),' + CRLF +
    f'    "Sensación térmica", AVERAGE({FH("IC_Media")}),' + CRLF +
    f'    "Mojadura", DIVIDE(COUNTROWS(FILTER(Fact_Horaria_riesgo, NOT ISBLANK({FH("Mojadura_Max")}) && {FH("Mojadura_Max")} > 4)) + 0, COUNTROWS(FILTER(Fact_Horaria_riesgo, NOT ISBLANK({FH("Mojadura_Max")})))),' + CRLF +
    f'    "Lluvia", AVERAGE({FH("Precip_Total")}),' + CRLF +
    f'    "Viento", AVERAGE({FH("Viento_Media")}),' + CRLF +
    f'    "Radiación", AVERAGE({FH("Rad_Media")})' + CRLF + ")",
    None, "Mapa de calor", "Valor de cada casilla día × hora según la vista elegida (riesgos o una variable; promedio de las estaciones).",
    fmtdef='SWITCH(SELECTEDVALUE(Vistas_Mapa_Calor[Vista], "Riesgos"), ' + ", ".join(f'"{v[0]}", "{v[2]}"' for v in VISTAS) + ', "0.0")'))
def color_vista(v):
    casos = ", ".join(f'_x < {("%.10f" % lim).rstrip("0").rstrip(".")}, "{col}"' for lim, col in v[4])
    return f'"{v[0]}", SWITCH(TRUE(), {casos}, "{v[5]}")'
M.append(medida("Mapa_Calor_Color",
    VSEL + "VAR _x = [Mapa_Calor_Valor]" + CRLF + "RETURN" + CRLF + "IF(" + CRLF + "    ISBLANK(_x), BLANK()," + CRLF +
    "    SWITCH(" + CRLF + "        _v," + CRLF + "        " + ("," + CRLF + "        ").join(color_vista(v) for v in VISTAS) + CRLF + "    )" + CRLF + ")",
    None, "Mapa de calor", "Color de fondo de la casilla según los rangos fijos de cada vista (ver Vistas_Mapa_Calor[Leyenda])."))
M.append(medida("Mapa_Calor_Fuente",
    "VAR _c = [Mapa_Calor_Color]" + CRLF + 'RETURN IF(_c IN { ' + ", ".join(f'"{c}"' for c in OSCUROS) + ' }, "#FFFFFF", "#252525")',
    None, "Mapa de calor", "Color del texto: blanco sobre fondos oscuros."))
M.append(medida("Mapa_Calor_N", VSEL + 'RETURN IF(_v = "Riesgos", [Riesgo_Hora_N])', "0.0", "Mapa de calor",
    "Tooltip: riesgos favorables en promedio (solo en la vista Riesgos)."))
M.append(medida("Mapa_Calor_Titulo",
    VSEL + 'RETURN' + CRLF + 'IF(' + CRLF + '    _v = "Riesgos",' + CRLF + '    [Riesgo_Hora_Titulo],' + CRLF +
    '    _v & " (" & SELECTEDVALUE(Vistas_Mapa_Calor[Unidad]) & "), promedio horario de las estaciones · " & SELECTEDVALUE(Vistas_Mapa_Calor[Leyenda])' + CRLF + ')',
    None, "Mapa de calor", "Título del mapa de calor con la vista, la unidad y la leyenda de colores."))
M.append(medida("Titulo_Contexto",
    "VAR _ini = MIN(Calendario[Fecha])" + CRLF + "VAR _fin = MAX(Calendario[Fecha])" + CRLF +
    "VAR _est = FILTER(VALUES(Estaciones_met[estacionid]), NOT ISEMPTY(CALCULATETABLE(Fact_Diaria_met)))" + CRLF +
    "VAR _n = COUNTROWS(_est)" + CRLF +
    'VAR _txtEst =' + CRLF + '    SWITCH(' + CRLF + '        TRUE(),' + CRLF +
    '        NOT ISFILTERED(Estaciones_met), "Todas las estaciones (" & _n & ")",' + CRLF +
    '        _n = 1, "Estación " & CALCULATE(SELECTEDVALUE(Estaciones_met[finca]), _est),' + CRLF +
    '        ISFILTERED(Estaciones_met[estrato.nombre]) && NOT ISFILTERED(Estaciones_met[finca]) && NOT ISFILTERED(Estaciones_met[estacionid]),' + CRLF +
    '            "Estrato " & CONCATENATEX(VALUES(Estaciones_met[estrato.nombre]), Estaciones_met[estrato.nombre], ", ") & " (" & _n & " estaciones)",' + CRLF +
    '        _n & " estaciones seleccionadas"' + CRLF + '    )' + CRLF +
    'RETURN' + CRLF +
    'SELECTEDVALUE(Cultivos[Cultivo], "Sin cultivo") & "  ·  " & _txtEst & "  ·  " & FORMAT(_ini, "dd-mmm") & " al " & FORMAT(_fin, "dd-mmm-yyyy")',
    None, "Genéricas", "Título dinámico del Resumen Semanal: cultivo, estaciones o estrato y fechas del periodo."))
# Grados día por cultivo
gdd = ("VAR _b = SELECTEDVALUE(Cultivos[GDD_Base], 10)" + CRLF + "VAR _t = SELECTEDVALUE(Cultivos[GDD_Tope], 30)" + CRLF + "RETURN" + CRLF +
       "AVERAGEX(" + CRLF + "    VALUES(Estaciones_met[estacionid])," + CRLF + "    CALCULATE(" + CRLF + "        SUMX(" + CRLF +
       "            Fact_Diaria_met," + CRLF + "            VAR _x = Fact_Diaria_met[Temp_Media]" + CRLF +
       "            RETURN IF(ISBLANK(_x), BLANK(), MIN(MAX(_x - _b, 0), _t - _b))" + CRLF + "        )" + CRLF + "    )" + CRLF + ")")
M.append(medida("GDD_Cultivo", gdd, "0", "Grados día", "Grados día con tope del cultivo seleccionado en el periodo (por estación, promedio entre estaciones)."))
acum = lambda off: ("CALCULATE(" + CRLF + "    [GDD_Cultivo]," + CRLF + "    FILTER(" + CRLF + "        ALL(Calendario)," + CRLF +
       f"        Calendario[Año_Hidrologico] = MAX(Calendario[Año_Hidrologico]){off} &&" + CRLF +
       "        Calendario[Semana_Hidrologica] <= MAX(Calendario[Semana_Hidrologica])" + CRLF + "    )" + CRLF + ")")
M.append(medida("GDD_Cultivo_Acumulado", acum(""), "0", "Grados día", "Grados día acumulados del año hidrológico hasta la semana en contexto."))
M.append(medida("GDD_Cultivo_Acumulado_Anterior", acum(" - 1"), "0", "Grados día", "Ídem, año hidrológico anterior."))
graf = lambda off, corte: ("VAR _Anio = CALCULATE(MAX(Calendario[Año_Hidrologico]), ALLSELECTED(Calendario))" + CRLF +
       "VAR _SemMax = CALCULATE(MAX(Calendario[Semana_Hidrologica]), ALLSELECTED(Calendario))" + CRLF +
       "VAR _SemEje = MAX(Semanas_Anio[Semana_Num])" + CRLF + "RETURN" + CRLF +
       ("IF(_SemEje <= _SemMax, " if corte else "") + "CALCULATE([GDD_Cultivo], ALL(Calendario), Calendario[Año_Hidrologico] = _Anio" + off +
       ", Calendario[Semana_Hidrologica] <= _SemEje)" + (")" if corte else ""))
M.append(medida("GDD_Cultivo_Grafica", graf("", True), "0", "Grados día", "Para la gráfica de acumulados por semana (eje Semanas_Anio), año actual."))
M.append(medida("GDD_Cultivo_Anterior_Grafica", graf(" - 1", False), "0", "Grados día", "Para la gráfica de acumulados por semana, año anterior."))
# Indicadores complementarios
M.append(medida("Cogollero_Generaciones",
    "CALCULATE(" + CRLF + "    AVERAGEX(" + CRLF + "        VALUES(Estaciones_met[estacionid])," + CRLF +
    "        CALCULATE(SUMX(Fact_Diaria_met, MAX(Fact_Diaria_met[Temp_Media] - 10.9, 0)))" + CRLF + "    )," + CRLF +
    "    FILTER(ALL(Calendario), Calendario[Año_Hidrologico] = MAX(Calendario[Año_Hidrologico]) && Calendario[Semana_Hidrologica] <= MAX(Calendario[Semana_Hidrologica]))" + CRLF +
    ") / 559", "0.0", "Indicadores", "Generaciones potenciales de gusano cogollero en el año hidrológico (base 10.9 °C, 559 grados día por generación)."))
M.append(medida("Salivosa_Lluvia_Temporada",
    "VAR _fin = MAX(Calendario[Fecha])" + CRLF + "VAR _ini = DATE(YEAR(_fin), 4, 1)" + CRLF + "RETURN" + CRLF +
    "IF(_fin >= _ini," + CRLF + "    CALCULATE(" + CRLF + "        AVERAGEX(VALUES(Estaciones_met[estacionid]), CALCULATE(SUM(Fact_Diaria_met[Precip_Total])))," + CRLF +
    "        DATESBETWEEN(Calendario[Fecha], _ini, _fin)" + CRLF + "    )" + CRLF + ")", "0", "Indicadores",
    "Lluvia acumulada desde el 1 de abril (inicio de la temporada de salivosa)."))
M.append(medida("Salivosa_Alerta_Emergencia", "IF([Salivosa_Lluvia_Temporada] >= 50, 1, 0)", "0", "Indicadores",
    "1 cuando la lluvia acumulada de la temporada alcanza 50 mm (eclosión de la mayoría de los huevos)."))
M += ["\tcolumn Column", "\t\tformatString: 0", f"\t\tlineageTag: {tag('_Riesgos', 'Column')}", "\t\tsummarizeBy: none", "\t\tisHidden",
      "\t\tisNameInferred", "\t\tsourceColumn: [Column]", "", "\t\tannotation SummarizationSetBy = Automatic", "",
      "\tpartition _Riesgos = calculated", "\t\tmode: import", '\t\tsource = Row("Column", BLANK())', ""]
open(os.path.join(DEF, "tables", "_Riesgos.tmdl"), "w", encoding="utf-8", newline="").write(CRLF.join(M))

# ───────────────────────── model.tmdl y relaciones ─────────────────────────
mp = os.path.join(DEF, "model.tmdl"); s = open(mp, encoding="utf-8", newline="").read()
for t in ("Cultivos", "Riesgos_Cultivo", "Vistas_Mapa_Calor", "_Riesgos"):
    if f"ref table {t}\r\n" not in s and f"ref table {t}\n" not in s:
        i = s.index("ref cultureInfo") if "ref cultureInfo" in s else len(s)
        s = s[:i].rstrip("\r\n") + CRLF + f"ref table {t}" + CRLF + CRLF + s[i:]
open(mp, "w", encoding="utf-8", newline="").write(s)
rp = os.path.join(DEF, "relationships.tmdl"); s = open(rp, encoding="utf-8", newline="").read()
if "Riesgos_Cultivo.Cultivo" not in s:
    s = s.rstrip("\r\n") + CRLF + CRLF + f"relationship {tag('rel', 'Riesgos_Cultivo', 'Cultivos')}" + CRLF + \
        "\tfromColumn: Riesgos_Cultivo.Cultivo" + CRLF + "\ttoColumn: Cultivos.Cultivo" + CRLF + CRLF
    open(rp, "w", encoding="utf-8", newline="").write(s)
print(f"OK: {len(CULTIVOS)} cultivos, {len(INC)} riesgos, {len(INC) + 13} medidas en _Riesgos ({len(hor)} con condición horaria)")
