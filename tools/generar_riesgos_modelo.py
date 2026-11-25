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
DEF = os.path.join(RAIZ, "Tablero-semanal-ICC.SemanticModel", "definition")
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
    ("Temperatura del aire", "°C", "0.0", "azul < 18 · celeste 18–24 · amarillo 24–30 · naranja 30–34 · rojo ≥ 34",
     [(18, "#4575B4"), (24, "#91BFDB"), (30, "#FFFFBF"), (34, "#FC8D59")], "#D73027"),
    ("Humedad relativa", "%", "0", "blanco < 60 · celeste 60–80 · azul 80–90 · azul oscuro ≥ 90",
     [(60, "#F7FBFF"), (80, "#C6DBEF"), (90, "#6BAED6")], "#2171B5"),
    ("Déficit de presión de vapor", "kPa", "0.00", "azul < 0.4 (muy húmedo) · verde 0.4–1.2 · amarillo 1.2–1.6 · rojo ≥ 1.6 (estrés)",
     [(0.4, "#6BAED6"), (1.2, "#A1D99B"), (1.6, "#FED976")], "#F03B20"),
    ("Sensación térmica (índice de calor)", "°C", "0.0", "blanco < 27 · amarillo 27–32 (precaución) · naranja claro 32–41 (precaución extrema) · naranja 41–54 (peligro) · rojo ≥ 54",
     [(27, "#FFFFFF"), (32, "#FFFFB2"), (41, "#FECC5C"), (54, "#FD8D3C")], "#E31A1C"),
    ("Mojadura de la hoja", "% de registros horarios con la hoja mojada", "0%", "blanco seca · celeste mojadura parcial (< 50 %) · azul mojadura predominante (≥ 50 %)",
     [(0.0000001, "#FFFFFF"), (0.5, "#9ECAE1")], "#3182BD"),
    ("Lluvia", "mm/h", "0.0", "blanco 0 · celeste < 1 · azul claro 1–5 · azul 5–10 · azul oscuro ≥ 10",
     [(0.0000001, "#FFFFFF"), (1, "#DEEBF7"), (5, "#9ECAE1"), (10, "#4292C6")], "#08519C"),
    ("Velocidad del viento", "km/h", "0.0", "blanco calma < 1.8 · verde claro 1.8–10 · verde 10–20 · verde medio 20–30 · verde oscuro ≥ 30",
     [(1.8, "#FFFFFF"), (10, "#E5F5E0"), (20, "#A1D99B"), (30, "#41AB5D")], "#006D2C"),
    ("Irradiancia", "W/m²", "0", "gris ≤ 40 (sin luz) · amarillo claro 40–300 · amarillo 300–600 · naranja 600–800 · naranja oscuro ≥ 800",
     [(40.0000001, "#F0F0F0"), (300, "#FFF7BC"), (600, "#FEC44F"), (800, "#FE9929")], "#D95F0E"),
]
PAL_RIESGO = {"": ["#FFFFFF", "#F9E79F", "#F39C12", "#C0392B"]}  # paleta original del mapa de calor de riesgos
RANGOS_RIESGO = ["0 %", "< 25 %", "25 – 50 %", "≥ 50 %"]
ETIQ = {"Temperatura del aire": ["< 18", "18 – 24", "24 – 30", "30 – 34", "≥ 34"], "Humedad relativa": ["< 60", "60 – 80", "80 – 90", "≥ 90"],
        "Déficit de presión de vapor": ["< 0.4 · aire muy húmedo (riesgo de enfermedades)", "0.4 – 1.2 · favorable", "1.2 – 1.6 · inicio de estrés", "≥ 1.6 · estrés hídrico"],
        "Sensación térmica (índice de calor)": ["< 27", "27 – 32 precaución", "32 – 41 prec. extrema", "41 – 54 peligro", "≥ 54"],
        "Mojadura de la hoja": ["Seca", "Mojadura parcial (< 50 %)", "Mojadura predominante (≥ 50 %)"], "Lluvia": ["0", "< 1", "1 – 5", "5 – 10", "≥ 10"],
        "Velocidad del viento": ["< 1.8 calma", "1.8 – 10", "10 – 20", "20 – 30", "≥ 30"], "Irradiancia": ["≤ 40 sin luz", "40 – 300", "300 – 600", "600 – 800", "≥ 800"]}
OSCUROS = ["#54278F", "#A63603", "#A50F15", "#252525", "#969696", "#9E9AC8", "#FB6A4A", "#4575B4", "#D73027", "#2171B5", "#F03B20", "#E31A1C", "#3182BD", "#4292C6", "#08519C", "#41AB5D", "#006D2C", "#D95F0E", "#C0392B"]
vis_cols = [("Vista", "text", "string", None), ("Orden", "Int64.Type", "int64", "0"), ("Unidad", "text", "string", None), ("Leyenda", "text", "string", None)]
open(os.path.join(DEF, "tables", "Vistas_Mapa_Calor.tmdl"), "w", encoding="utf-8", newline="").write(
    tabla_m("Vistas_Mapa_Calor", vis_cols, [[v[0], i, v[1], v[3]] for i, v in enumerate(VISTAS, 1)], sort={"Vista": "Orden"}, ocultas=("Orden",)))

ley = []
for v in VISTAS:
    if v[0] == "Riesgos":
        for g, c in PAL_RIESGO.items():
            ley += [["Riesgos", g, i, r, col] for i, (r, col) in enumerate(zip(RANGOS_RIESGO, c), 1)]
    else:
        cols_v = [col for _, col in v[4]] + [v[5]]
        u = "" if v[0].startswith("Mojadura") else " " + v[1]
        ley += [[v[0], "", i, r + u, col] for i, (r, col) in enumerate(zip(ETIQ[v[0]], cols_v), 1)]
ley_cols = [("Vista", "text", "string", None), ("Grupo", "text", "string", None), ("Orden", "Int64.Type", "int64", "0"),
            ("Rango", "text", "string", None), ("Color", "text", "string", None)]
open(os.path.join(DEF, "tables", "Leyenda_Mapa_Calor.tmdl"), "w", encoding="utf-8", newline="").write(
    tabla_m("Leyenda_Mapa_Calor", ley_cols, ley, sort={"Rango": "Orden"}, ocultas=("Orden",)))

# ───────────────────────── Día / noche ─────────────────────────
DN = [  # ID, gráfica, periodo (Día / Noche / 24 h), serie, medida, eje secundario requerido
    ("DPV_MED_D", "Estrés atmosférico", "Día", "DPV medio diurno", "VPD_Media_Diurna", None),
    ("DPV_MAX_D", "Estrés atmosférico", "Día", "DPV máx. diurno", "VPD_Max_Diurna", None),
    ("DPV_MED_N", "Estrés atmosférico", "Noche", "DPV medio nocturno", "VPD_Media_Nocturna", None),
    ("HR_MIN", "Estrés atmosférico", "24 h", "HR mínima", "HR_Min", "Humedad relativa"),
    ("HR_MED", "Estrés atmosférico", "24 h", "HR media", "HR_Media", "Humedad relativa"),
    ("T_NOC", "Estrés atmosférico", "Noche", "T media nocturna", "Temp_Nocturna_Media", "Temperatura nocturna"),
    ("T_MIN_NOC", "Estrés atmosférico", "Noche", "T mínima nocturna", "Temp_Min_Nocturna", "Temperatura nocturna"),
    ("MOJ_D", "Estrés vegetal", "Día", "Mojadura diurna", "Mojadura_Horas_Semanal", None),
    ("MOJ_N", "Estrés vegetal", "Noche", "Mojadura nocturna", "Mojadura_Horas_Nocturna_Semanal", None),
    ("LUZ_D", "Estrés vegetal", "Día", "Horas con luz", "Horas_Luz", None),
    ("ESTRES_D", "Estrés vegetal", "Día", "Horas de estrés térmico", "Horas_Estres_Termico_Semanal", None),
    ("IRR_MAX", "Estrés vegetal", "Día", "Irradiancia máx. diurna", "Rad_Max_Diurna", None),
    ("IRR_LUZ", "Estrés vegetal", "Día", "Irradiancia media de luz", "Rad_Media_Luz", None),
    ("V_MAX_D", "Viento", "Día", "Viento máx. diurno", "Viento_Max_Diurno", None),
    ("V_MAX_N", "Viento", "Noche", "Viento máx. nocturno", "Viento_Max_Nocturno", None),
    ("V_MED_D", "Viento", "Día", "Viento medio diurno", "Viento_Media_Diurna", None),
    ("V_MED_N", "Viento", "Noche", "Viento medio nocturno", "Viento_Media_Nocturna", None),
]
dn_cols = [("ID", "text", "string", None), ("Grafica", "text", "string", None), ("Periodo", "text", "string", None),
           ("Serie", "text", "string", None), ("Orden", "Int64.Type", "int64", "0")]
open(os.path.join(DEF, "tables", "Series_DiaNoche.tmdl"), "w", encoding="utf-8", newline="").write(
    tabla_m("Series_DiaNoche", dn_cols, [[d[0], d[1], d[2], d[3], i] for i, d in enumerate(DN, 1)],
            sort={"Serie": "Orden"}, ocultas=("Orden", "ID")))
open(os.path.join(DEF, "tables", "Periodo_Vista.tmdl"), "w", encoding="utf-8", newline="").write(
    tabla_m("Periodo_Vista", [("Vista", "text", "string", None), ("Orden", "Int64.Type", "int64", "0")],
            [["Día", 1], ["Noche", 2], ["Ambos", 3]], sort={"Vista": "Orden"}, ocultas=("Orden",)))
open(os.path.join(DEF, "tables", "Leyenda_Mapa_Riesgo.tmdl"), "w", encoding="utf-8", newline="").write(
    tabla_m("Leyenda_Mapa_Riesgo", [("Modo", "text", "string", None), ("Orden", "Int64.Type", "int64", "0"), ("Rango", "text", "string", None), ("Color", "text", "string", None)],
            [["Conteo", 1, "Sin riesgos en alerta", "#C6DBEF"], ["Conteo", 2, "1 riesgo en alerta", "#6BAED6"], ["Conteo", 3, "2 a 3 riesgos en alerta", "#2171B5"],
             ["Conteo", 4, "4 o más riesgos en alerta", "#08306B"], ["Conteo", 5, "Sin datos", "#FFFFFF"],
             ["Riesgo", 6, "Alerta", "#D64550"], ["Riesgo", 7, "Precaución", "#F2B134"], ["Riesgo", 8, "Normal", "#3BA272"], ["Riesgo", 9, "Sin datos\u200b", "#B0B0B0"]],
            sort={"Rango": "Orden"}, ocultas=("Orden",)))
open(os.path.join(DEF, "tables", "Ventana_Semanas.tmdl"), "w", encoding="utf-8", newline="").write(
    tabla_m("Ventana_Semanas", [("Ventana", "text", "string", None), ("Semanas", "Int64.Type", "int64", "0")],
            [["4 semanas", 4], ["8 semanas", 8], ["12 semanas", 12], ["Desde el inicio del año", 0]], sort={"Ventana": "Semanas"}, ocultas=("Semanas",)))
open(os.path.join(DEF, "tables", "Eje_Secundario.tmdl"), "w", encoding="utf-8", newline="").write(
    tabla_m("Eje_Secundario", [("Opcion", "text", "string", None), ("Orden", "Int64.Type", "int64", "0")],
            [["Humedad relativa", 1], ["Temperatura nocturna", 2]], sort={"Opcion": "Orden"}, ocultas=("Orden",)))

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
    f'    "Temperatura del aire", AVERAGE({FH("Temp_Media")}),' + CRLF +
    f'    "Humedad relativa", AVERAGE({FH("HR_Media")}),' + CRLF +
    f'    "Déficit de presión de vapor", AVERAGEX(FILTER(Fact_Horaria_riesgo, NOT ISBLANK({FH("Temp_Media")}) && NOT ISBLANK({FH("HR_Media")})), 0.6108 * EXP(17.27 * {FH("Temp_Media")} / ({FH("Temp_Media")} + 237.3)) * (1 - {FH("HR_Media")} / 100)),' + CRLF +
    f'    "Sensación térmica (índice de calor)", AVERAGE({FH("IC_Media")}),' + CRLF +
    f'    "Mojadura de la hoja", DIVIDE(COUNTROWS(FILTER(Fact_Horaria_riesgo, NOT ISBLANK({FH("Mojadura_Max")}) && {FH("Mojadura_Max")} > 4)) + 0, COUNTROWS(FILTER(Fact_Horaria_riesgo, NOT ISBLANK({FH("Mojadura_Max")})))),' + CRLF +
    f'    "Lluvia", AVERAGE({FH("Precip_Total")}),' + CRLF +
    f'    "Velocidad del viento", AVERAGE({FH("Viento_Media")}),' + CRLF +
    f'    "Irradiancia", AVERAGE({FH("Rad_Media")})' + CRLF + ")",
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
    '    _v & " (" & SELECTEDVALUE(Vistas_Mapa_Calor[Unidad]) & "), promedio horario de las estaciones"' + CRLF + ')',
    None, "Mapa de calor", "Título del mapa de calor con la vista y la unidad."))
M.append(medida("Leyenda_Mostrar",
    VSEL + "RETURN IF(SELECTEDVALUE(Leyenda_Mapa_Calor[Vista]) = _v, 1)",
    "0", "Mapa de calor", "Filtro de la tabla de leyenda: 1 en los rangos de la vista (y categoría de riesgo) que se muestra."))
M.append(medida("Leyenda_Color", "SELECTEDVALUE(Leyenda_Mapa_Calor[Color])", None, "Mapa de calor", "Color de la fila de leyenda."))
M.append(medida("Leyenda_Fuente", 'IF([Leyenda_Color] IN { ' + ", ".join(f'"{c}"' for c in OSCUROS) + ' }, "#FFFFFF", "#252525")',
    None, "Mapa de calor", "Color del texto de la leyenda."))

M.append(medida("Titulo_Semana",
    "VAR _ini = MIN(Calendario[Fecha])" + CRLF + "VAR _fin = MAX(Calendario[Fecha])" + CRLF +
    "VAR _est = FILTER(VALUES(Estaciones_met[estacionid]), NOT ISEMPTY(CALCULATETABLE(Fact_Diaria_met)))" + CRLF +
    "VAR _n = COUNTROWS(_est)" + CRLF +
    'VAR _txtEst =' + CRLF + '    SWITCH(' + CRLF + '        TRUE(),' + CRLF +
    '        NOT ISFILTERED(Estaciones_met[estrato.nombre]) && NOT ISFILTERED(Estaciones_met[finca]) && NOT ISFILTERED(Estaciones_met[estacionid]),' + CRLF +
    '            "Todas las estaciones (" & _n & ")",' + CRLF +
    '        _n = 1, "Estación " & CALCULATE(SELECTEDVALUE(Estaciones_met[finca]), _est),' + CRLF +
    '        ISFILTERED(Estaciones_met[estrato.nombre]) && NOT ISFILTERED(Estaciones_met[finca]) && NOT ISFILTERED(Estaciones_met[estacionid]),' + CRLF +
    '            "Estrato " & CONCATENATEX(VALUES(Estaciones_met[estrato.nombre]), Estaciones_met[estrato.nombre], ", ") & " (" & _n & " estaciones)",' + CRLF +
    '        _n & " estaciones seleccionadas"' + CRLF + '    )' + CRLF +
    "VAR _ult = CALCULATE(MAX(Fact_Diaria_met[Fecha]), REMOVEFILTERS())" + CRLF +
    "VAR _dias = COUNTROWS(FILTER(VALUES(Calendario[Fecha]), Calendario[Fecha] <= _ult))" + CRLF +
    "VAR _tot = COUNTROWS(VALUES(Calendario[Fecha]))" + CRLF +
    'VAR _pais = IF(HASONEVALUE(Estaciones_met[pais.nombre]), VALUES(Estaciones_met[pais.nombre]) & "  ·  ")' + CRLF +
    'RETURN' + CRLF +
    '_pais & _txtEst & "  ·  " & FORMAT(_ini, "dd-mmm") & " al " & FORMAT(_fin, "dd-mmm-yyyy") & IF(_dias < _tot, "  ·  " & _dias & " de " & _tot & " días con datos")',
    None, "Contexto", "Indicador de la semana: país (si hay uno solo), estaciones o estrato, fechas y, si la semana está incompleta, días con datos."))
M.append(medida("Titulo_Contexto",
    'SELECTEDVALUE(Cultivos[Cultivo], "Sin cultivo") & "  ·  " & [Titulo_Semana]',
    None, "Genéricas", "Indicador de la página de riesgos: cultivo + Titulo_Semana."))
# ───── Contexto, semana a semana y resumen (Fase 2b) ─────
EST = "FILTER(VALUES(Estaciones_met[estacionid]), NOT ISEMPTY(CALCULATETABLE(Fact_Diaria_met)))"
GDDX = "VAR _b = SELECTEDVALUE(Cultivos[GDD_Base], 10)" + CRLF + "VAR _t = SELECTEDVALUE(Cultivos[GDD_Tope], 30)" + CRLF
M.append(medida("Datos_Al_Diaria", 'VAR _f = CALCULATE(MAX(Fact_Diaria_met[Fecha]), REMOVEFILTERS())' + CRLF + 'RETURN "Datos al " & FORMAT(_f, "dd/mm/yyyy")',
    None, "Contexto", "Última fecha con datos diarios (tarjeta «Datos al…»)."))
M.append(medida("Datos_Al_Horaria", 'VAR _f = CALCULATE(MAX(Fact_Horaria_riesgo[Fecha]), REMOVEFILTERS())' + CRLF +
    'VAR _h = CALCULATE(MAX(Fact_Horaria_riesgo[Hora]), REMOVEFILTERS(), Fact_Horaria_riesgo[Fecha] = _f)' + CRLF +
    'RETURN "Datos al " & FORMAT(_f, "dd/mm/yyyy") & " " & FORMAT(_h, "00") & ":00 h"',
    None, "Contexto", "Última fecha y hora con datos horarios (tarjeta «Datos al…» de la página horaria)."))
M.append(medida("Horas_Luz_Diaria", f"AVERAGEX({EST}, CALCULATE(AVERAGE(Fact_Subdiaria_met_aux[Duracion_Luz_h])))", "0.0", "Semana a semana",
    "Duración media diaria del periodo de luz (h)."))
M.append(medida("Mapa_Balance_Color",
    "VAR _b = [Balance_Semanal]" + CRLF + "RETURN" + CRLF +
    'IF(ISBLANK(_b), "#BDBDBD", SWITCH(TRUE(), _b <= -30, "#8C510A", _b <= -10, "#D8B365", _b < 10, "#F5F5F5", _b < 30, "#5AB4AC", "#01665E"))',
    None, "Contexto", "Color del mapa de la página 1 por balance hídrico de la semana (café = déficit, verde azulado = excedente)."))
M.append(medida("Rad_Diaria_Media", f"AVERAGEX({EST}, CALCULATE(AVERAGE(Fact_Diaria_met[Rad_MJ])))", "0.0", "Semana a semana",
    "Radiación media diaria (MJ/m²/día): promedio por estación y luego entre estaciones."))
M.append(medida("GDD_Diario_Medio", GDDX + "RETURN" + CRLF + f"AVERAGEX({EST}, CALCULATE(AVERAGEX(FILTER(Fact_Diaria_met, NOT ISBLANK(Fact_Diaria_met[Temp_Media])), MIN(MAX(Fact_Diaria_met[Temp_Media] - _b, 0), _t - _b))))",
    "0.0", "Semana a semana", "Grados día medios por día (base y tope del cultivo elegido; sin cultivo, base 10 °C y tope 30 °C)."))
VENT = ("VAR _sel = CALCULATE(MAX(Calendario[Inicio_Semana]), ALLSELECTED(Calendario))" + CRLF +
        "VAR _eje = MAX(Semanas_Grafica[Inicio_Semana])" + CRLF)
for base, nom in (("Rad_Diaria_Media", "Rad"), ("GDD_Diario_Medio", "GDD")):
    M.append(medida(f"{nom}_Sem_Grafica", VENT + "RETURN" + CRLF +
        f"IF(_eje <= _sel && _eje > _sel - 84, CALCULATE([{base}], ALL(Calendario), Calendario[Inicio_Semana] = _eje))",
        "0.0", "Semana a semana", f"Gráfica semana a semana (eje Semanas_Grafica): {base} de cada una de las últimas 12 semanas hasta la elegida."))
    M.append(medida(f"{nom}_Sem_Anterior_Grafica", VENT + "VAR _a = MAX(Semanas_Grafica[Año_Hidrologico])" + CRLF +
        "VAR _s = MAX(Semanas_Grafica[Semana_Hidrologica])" + CRLF + "RETURN" + CRLF +
        f"IF(_eje <= _sel && _eje > _sel - 84, CALCULATE([{base}], ALL(Calendario), Calendario[Año_Hidrologico] = _a - 1, Calendario[Semana_Hidrologica] = _s))",
        "0.0", "Semana a semana", f"Misma semana hidrológica del año anterior ({base})."))
def acum(expr, prev):
    v = ("VAR _anio = CALCULATE(MAX(Calendario[Año_Hidrologico]), ALLSELECTED(Calendario))" + CRLF +
         "VAR _ult = CALCULATE(MAX(Fact_Diaria_met[Fecha]), REMOVEFILTERS())" + CRLF +
         "VAR _fin = MIN(CALCULATE(MAX(Calendario[Fecha]), ALLSELECTED(Calendario)), _ult)" + CRLF +
         "VAR _ini = CALCULATE(MIN(Calendario[Fecha]), ALL(Calendario), Calendario[Año_Hidrologico] = _anio)" + CRLF)
    if prev:
        v += ("VAR _ini2 = CALCULATE(MIN(Calendario[Fecha]), ALL(Calendario), Calendario[Año_Hidrologico] = _anio - 1)" + CRLF +
              "VAR _fin2 = _ini2 + (_fin - _ini)" + CRLF)
    a, b = ("_ini2", "_fin2") if prev else ("_ini", "_fin")
    return v + "RETURN" + CRLF + f"CALCULATE(AVERAGEX(VALUES(Estaciones_met[estacionid]), CALCULATE({expr})), ALL(Calendario), DATESBETWEEN(Calendario[Fecha], {a}, {b}))"
GDDSUM = "SUMX(FILTER(Fact_Diaria_met, NOT ISBLANK(Fact_Diaria_met[Temp_Media])), MIN(MAX(Fact_Diaria_met[Temp_Media] - _b, 0), _t - _b))"
for nom, expr, pre, unidad in (("Rad", "SUM(Fact_Diaria_met[Rad_MJ])", "", "MJ/m²"), ("GDD", GDDSUM, GDDX, "°C día")):
    M.append(medida(f"{nom}_Acum_Hidro", pre + acum(expr, False), "#,0", "Semana a semana",
        f"Acumulado del año hidrológico hasta el último día con datos de la semana elegida ({unidad})."))
    M.append(medida(f"{nom}_Acum_Hidro_Ant", pre + acum(expr, True), "#,0", "Semana a semana",
        f"Acumulado del año hidrológico anterior con el mismo número de días ({unidad})."))
    M.append(medida(f"{nom}_Acum_Dif_Pct", f"DIVIDE([{nom}_Acum_Hidro] - [{nom}_Acum_Hidro_Ant], [{nom}_Acum_Hidro_Ant])", "+0%;-0%;0%", "Semana a semana",
        "Diferencia del acumulado frente al año anterior."))
M.append(medida("Rad_Titulo",
    '"Radiación media diaria (MJ/m²) · acumulado del año: " & FORMAT([Rad_Acum_Hidro], "#,0") & " MJ/m² (" & FORMAT([Rad_Acum_Dif_Pct], "+0%;-0%;0%") & " vs. año anterior)"',
    None, "Semana a semana", "Título de la gráfica de radiación semana a semana con el acumulado del año."))
M.append(medida("GDD_Titulo",
    '"Grados día por día (base " & SELECTEDVALUE(Cultivos[GDD_Base], 10) & " °C, tope " & SELECTEDVALUE(Cultivos[GDD_Tope], 30) & " °C) · acumulado del año: " & FORMAT([GDD_Acum_Hidro], "#,0") & " (" & FORMAT([GDD_Acum_Dif_Pct], "+0%;-0%;0%") & " vs. año anterior)"',
    None, "Semana a semana", "Título de la gráfica de grados día semana a semana con el acumulado del año."))
VINI = ("VAR _w = SELECTEDVALUE(Ventana_Semanas[Semanas], 8)" + CRLF +
        "VAR _anioVent = CALCULATE(MAX(Calendario[Año_Hidrologico]), ALLSELECTED(Calendario))" + CRLF +
        "VAR _iniAnio = CALCULATE(MIN(Calendario[Inicio_Semana]), ALL(Calendario), Calendario[Año_Hidrologico] = _anioVent)" + CRLF +
        "VAR _ini = IF(_w = 0, _iniAnio, _sel - 7 * (_w - 1))" + CRLF)
VENT8 = ("VAR _sel = CALCULATE(MAX(Calendario[Inicio_Semana]), ALLSELECTED(Calendario))" + CRLF +
         "VAR _eje = MAX(Semanas_Grafica[Inicio_Semana])" + CRLF +
         "VAR _ult = CALCULATE(MAX(Fact_Diaria_met[Fecha]), REMOVEFILTERS())" + CRLF) + VINI
def semanas8(base, hasta_eje=True):
    lim = "_eje" if hasta_eje else "_sel"
    return ("VAR _t =" + CRLF + "    ADDCOLUMNS(" + CRLF +
            f"        FILTER(ALL(Semanas_Grafica[Inicio_Semana]), Semanas_Grafica[Inicio_Semana] >= _ini && Semanas_Grafica[Inicio_Semana] <= {lim})," + CRLF +
            f'        "@x", VAR _i = Semanas_Grafica[Inicio_Semana] RETURN CALCULATE([{base}], ALL(Calendario), Calendario[Inicio_Semana] = _i),' + CRLF +
            '        "@n", MAX(0, MIN(7, INT(_ult - Semanas_Grafica[Inicio_Semana]) + 1)),' + CRLF +
            f'        "@ant", VAR _i = Semanas_Grafica[Inicio_Semana] RETURN CALCULATE(CALCULATE([{base}], DATEADD(Calendario[Fecha], -1, YEAR)), ALL(Calendario), Calendario[Inicio_Semana] = _i),' + CRLF +
            f'        "@clim", VAR _i = Semanas_Grafica[Inicio_Semana] RETURN CALCULATE(AVERAGEX(GENERATESERIES(1, 18), VAR _k = [Value] RETURN CALCULATE([{base}], DATEADD(Calendario[Fecha], -_k, YEAR))), ALL(Calendario), Calendario[Inicio_Semana] = _i)' + CRLF +
            "    )" + CRLF)
EXPR = {"Acum8": "SUMX(_t, [@x] * [@n])", "Acum8_Ant": "SUMX(_t, [@ant] * 7)", "Acum8_Media": "SUMX(_t, [@clim] * [@n])",
        "Desv_Acum": "SUMX(FILTER(_t, NOT ISBLANK([@x]) && NOT ISBLANK([@clim])), ([@x] - [@clim]) * [@n])",
        "Desv_Acum_Ant": "SUMX(FILTER(_t, NOT ISBLANK([@ant]) && NOT ISBLANK([@clim])), ([@ant] - [@clim]) * 7)"}
DESC = {"Acum8": "Acumulado del año actual desde el inicio de la ventana (4, 8, 12 semanas o inicio del año) hasta la semana del eje",
        "Acum8_Ant": "Acumulado de los mismos días del año anterior", "Acum8_Media": "Acumulado de la media de los mismos días en años anteriores (hasta 18)",
        "Desv_Acum": "Desviación acumulada del año actual frente a la media (mismos días de años anteriores)",
        "Desv_Acum_Ant": "Desviación acumulada del año anterior frente a la misma media"}
for nom, base, uni in (("Rad", "Rad_Diaria_Media", "MJ/m²"), ("GDD", "GDD_Diario_Medio", "°C día")):
    for k, e in EXPR.items():
        M.append(medida(f"{nom}_{k}", VENT8 + semanas8(base) + "RETURN" + CRLF + f"IF(_eje <= _sel && _eje >= _ini, {e})",
            "+0;-0;0" if "Desv" in k else "#,0", "Semana a semana", f"{DESC[k]} ({uni}). Eje: Semanas_Grafica."))
    tot = {k: f"CALCULATE([{nom}_{k}], TREATAS({{_sel}}, Semanas_Grafica[Inicio_Semana]))" for k in ("Acum8", "Acum8_Ant", "Acum8_Media", "Desv_Acum", "Desv_Acum_Ant")}
    etiqueta = "Radiación" if nom == "Rad" else "Grados día (base 10 °C, tope 30 °C)"
    M.append(medida(f"{nom}_Titulo_Desv",
        "VAR _sel = CALCULATE(MAX(Calendario[Inicio_Semana]), ALLSELECTED(Calendario))" + CRLF +
        'VAR _v = SELECTEDVALUE(Ventana_Semanas[Ventana], "8 semanas")' + CRLF + "RETURN" + CRLF +
        f'"{etiqueta} ({uni}) · " & _v & ": acumulado " & FORMAT({tot["Acum8"]}, "#,0") & " (" & FORMAT({tot["Desv_Acum"]}, "+0;-0;0") & " vs. media) · año anterior " & FORMAT({tot["Acum8_Ant"]}, "#,0") & " (" & FORMAT({tot["Desv_Acum_Ant"]}, "+0;-0;0") & ") · media " & FORMAT({tot["Acum8_Media"]}, "#,0")',
        None, "Semana a semana", "Título: acumulado de la ventana con la desviación frente a la media entre paréntesis (año actual y anterior) y acumulado de la media."))
    M.append(medida(f"{nom}_Texto_Actual", f'FORMAT([{nom}_Acum8], "#,0") & " (" & FORMAT([{nom}_Desv_Acum], "+0;-0;0") & ")"', None, "Semana a semana",
        "Información sobre herramientas: acumulado del año actual (desviación frente a la media)."))
    M.append(medida(f"{nom}_Texto_Anterior", f'FORMAT([{nom}_Acum8_Ant], "#,0") & " (" & FORMAT([{nom}_Desv_Acum_Ant], "+0;-0;0") & ")"', None, "Semana a semana",
        "Información sobre herramientas: acumulado del año anterior (desviación frente a la media)."))
M.append(medida("Desv_Media_Linea",
    "VAR _sel = CALCULATE(MAX(Calendario[Inicio_Semana]), ALLSELECTED(Calendario))" + CRLF + "VAR _eje = MAX(Semanas_Grafica[Inicio_Semana])" + CRLF +
    VINI + "RETURN IF(_eje <= _sel && _eje >= _ini, 0)", "0", "Semana a semana", "Línea de la media (desviación 0) en las gráficas de desviación acumulada."))
M.append(medida("Mapa_DPV_Color",
    "VAR _x = [VPD_Max_Diurna]" + CRLF + 'RETURN IF(ISBLANK(_x), "#BDBDBD", SWITCH(TRUE(), _x < 0.4, "#6BAED6", _x < 1.2, "#A1D99B", _x < 1.6, "#FED976", "#F03B20"))',
    None, "Contexto", "Color del mapa de la página de estrés: DPV máximo diurno con la paleta del mapa de calor."))
M.append(medida("Mapa_Riesgo_Color",
    "VAR _uno = ISFILTERED(Riesgos_Cultivo[Riesgo]) && HASONEVALUE(Riesgos_Cultivo[ID])" + CRLF +
    "VAR _n = [Riesgos_En_Alerta]" + CRLF + "RETURN" + CRLF +
    'IF(_uno, [Riesgo_Color], SWITCH(TRUE(), ISBLANK([Riesgo_Valor_Max_Estacion]), "#FFFFFF", COALESCE(_n, 0) = 0, "#C6DBEF", _n = 1, "#6BAED6", _n <= 3, "#2171B5", "#08306B"))',
    None, "Contexto", "Color del mapa de riesgos: número de riesgos en alerta (azules: 0, 1, 2–3, ≥ 4; blanco sin datos); con un riesgo elegido en el semáforo, su color de semáforo."))
M.append(medida("Leyenda_Riesgo_Mostrar",
    "VAR _uno = ISFILTERED(Riesgos_Cultivo[Riesgo]) && HASONEVALUE(Riesgos_Cultivo[ID])" + CRLF +
    'RETURN IF(SELECTEDVALUE(Leyenda_Mapa_Riesgo[Modo]) = IF(_uno, "Riesgo", "Conteo"), 1)',
    "0", "Contexto", "Filtro de la leyenda del mapa de riesgos: número de alertas, o semáforo si hay un riesgo elegido."))
M.append(medida("Leyenda_Riesgo_Color", "SELECTEDVALUE(Leyenda_Mapa_Riesgo[Color])", None, "Contexto", "Color de la fila de la leyenda del mapa de riesgos."))
M.append(medida("Leyenda_Riesgo_Fuente", 'IF([Leyenda_Riesgo_Color] IN {"#2171B5", "#08306B", "#D64550", "#3BA272"}, "#FFFFFF", "#252525")', None, "Contexto", "Color del texto de la leyenda del mapa de riesgos."))
M.append(medida("Leyenda_Riesgo_Titulo",
    "VAR _uno = ISFILTERED(Riesgos_Cultivo[Riesgo]) && HASONEVALUE(Riesgos_Cultivo[ID])" + CRLF +
    'RETURN IF(_uno, "Semáforo de " & LOWER(SELECTEDVALUE(Riesgos_Cultivo[Riesgo])), "Riesgos en alerta por estación")',
    None, "Contexto", "Título del mapa de riesgos y de su leyenda."))
M.append(medida("Riesgo_Valor_Max_Estacion", "MAXX(VALUES(Riesgos_Cultivo[ID]), [Riesgo_Valor])", "0.#", "Contexto",
    "Indica si la estación tiene algún valor de riesgo calculado (para distinguir «sin datos» en el mapa)."))
for d in DN:
    cond = ['"' + d[3] + '" IN VALUES(Series_DiaNoche[Serie])']
    if d[2] != "24 h": cond.append('(_vis = "Ambos" || _vis = "' + d[2] + '")')
    if d[5]: cond.append('SELECTEDVALUE(Eje_Secundario[Opcion], "Humedad relativa") = "' + d[5] + '"')
    M.append(medida("DN_" + d[0],
        'VAR _vis = SELECTEDVALUE(Periodo_Vista[Vista], "Ambos")' + CRLF + "RETURN IF(" + " && ".join(cond) + ", [" + d[4] + "])",
        "0.0", "Día y noche", f"{d[3]} ({d[1]}): se muestra según los botones Día / Noche / Ambos, la lista de series y, si aplica, el eje secundario."))
# Resumen de la semana (tabla Resumen_Variables)
RES = [("Lluvia", "mm", "0.0", "[Precip_Semanal]"), ("Evapotranspiración (ETo)", "mm", "0.0", "[ETO_Semanal]"),
       ("Balance hídrico", "mm", "+0.0;-0.0;0.0", "[Balance_Semanal]"), ("Temperatura media", "°C", "0.0", "[Temp_Media]"),
       ("Temperatura máxima", "°C", "0.0", "[Temp_Max]"), ("Temperatura mínima", "°C", "0.0", "[Temp_Min]"),
       ("Radiación (media diaria)", "MJ/m²/día", "0.0", "[Rad_Diaria_Media]"), ("Horas con luz (media diaria)", "h", "0.0", "[Horas_Luz_Diaria]"),
       ("Grados día (media diaria)", "°C día", "0.0", "[GDD_Diario_Medio]")]
M.append(medida("Resumen_Actual",
    'VAR _v = SELECTEDVALUE(Resumen_Variables[Variable])' + CRLF + "RETURN" + CRLF + "SWITCH(" + CRLF + "    _v," + CRLF + "    " +
    ("," + CRLF + "    ").join(f'"{v}", {m}' for v, _, _, m in RES) + CRLF + ")",
    "0.0", "Resumen", "Valor de la semana elegida para la variable de la fila (solo días con datos).",
    ))
DESF = ("VAR _ult = CALCULATE(MAX(Fact_Diaria_met[Fecha]), REMOVEFILTERS())" + CRLF +
        "VAR _f = FILTER(VALUES(Calendario[Fecha]), Calendario[Fecha] <= _ult)" + CRLF)
M.append(medida("Resumen_Semana_Anterior", DESF + 'VAR _d = SELECTCOLUMNS(_f, "F", Calendario[Fecha] - 7)' + CRLF + "RETURN" + CRLF +
    "CALCULATE([Resumen_Actual], ALL(Calendario), TREATAS(_d, Calendario[Fecha]))", "0.0", "Resumen",
    "Los mismos días de la semana anterior (si la semana va incompleta, compara solo esos días).",
    ))
M.append(medida("Resumen_Anio_Anterior", DESF + 'VAR _d = SELECTCOLUMNS(_f, "F", Calendario[Fecha] - 364)' + CRLF + "RETURN" + CRLF +
    "CALCULATE([Resumen_Actual], ALL(Calendario), TREATAS(_d, Calendario[Fecha]))", "0.0", "Resumen",
    "Los mismos días 52 semanas antes (mismo día de la semana).",
    ))
res_cols = [("Variable", "text", "string", None), ("Orden", "Int64.Type", "int64", "0"), ("Unidad", "text", "string", None), ("Formato", "text", "string", None)]
open(os.path.join(DEF, "tables", "Resumen_Variables.tmdl"), "w", encoding="utf-8", newline="").write(
    tabla_m("Resumen_Variables", res_cols, [[v, i, u, f] for i, (v, u, f, _) in enumerate(RES, 1)], sort={"Variable": "Orden"}, ocultas=("Orden", "Formato")))
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
for t in ("Cultivos", "Riesgos_Cultivo", "Vistas_Mapa_Calor", "Leyenda_Mapa_Calor", "Resumen_Variables", "Series_DiaNoche", "Periodo_Vista", "Eje_Secundario", "Ventana_Semanas", "Leyenda_Mapa_Riesgo", "_Riesgos"):
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
