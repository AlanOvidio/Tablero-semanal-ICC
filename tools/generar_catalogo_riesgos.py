#!/usr/bin/env python3
"""
Genera docs/10_catalogo_riesgos.md a partir de:
  config/riesgos_cultivo.csv  (un riesgo por fila; editable en Excel, separador ';')
  config/fuentes_riesgos.csv  (referencias bibliográficas; clave usada en la columna 'fuente')

Uso:  python tools/generar_catalogo_riesgos.py
Ejecutar después de editar cualquiera de los dos CSV.
"""
import csv, os, datetime
RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
leer = lambda p: list(csv.DictReader(open(os.path.join(RAIZ, p), encoding="utf-8-sig"), delimiter=";"))
R = leer("config/riesgos_cultivo.csv")
F = {f["clave"]: f for f in leer("config/fuentes_riesgos.csv")}
claves = lambda d: [k.strip() for k in d["fuente"].split(";") if k.strip() in F]
CULT = []
for d in R:
    if d["cultivo"] not in CULT: CULT.append(d["cultivo"])
inc = sum(d["estado"] == "incluir" for d in R); pen = sum(d["estado"] == "pendiente" for d in R); val = sum(d["validado"] == "si" for d in R)
L = ["# Catálogo de riesgos por cultivo\n",
     f"> Generado por `tools/generar_catalogo_riesgos.py` el {datetime.date.today().isoformat()} desde [`config/riesgos_cultivo.csv`](../config/riesgos_cultivo.csv). "
     f"**{len(R)} riesgos**: {inc} a incluir, {pen} pendientes; {val} validados. No editar a mano: editar el CSV y regenerar.\n",
     "## Cómo leer este catálogo\n",
     "- **Escala:** H = horaria (va al mapa de calor), D = diaria (días favorables por semana), A = acumulada (ventana de días o grados día).",
     "- **Confianza de la fuente:** **A** = fuente de Guatemala, El Salvador o Centroamérica con valores numéricos · **B** = fuente revisada pero cualitativa o de otra latitud · **C** = criterio vigente del modelo, operativo o fuente no verificada.",
     "- **Estado:** *incluir* = se implementa · *pendiente* = sin umbral climático documentado (propuesta: excluir, salvo nuevo criterio).",
     "- **Aplicación:** restricciones de altitud y meses que el modelo aplica automáticamente, y etapas fenológicas sensibles. El modelo no conoce la fecha de siembra ni la etapa del cultivo: los riesgos ligados a una etapa se muestran siempre y deben interpretarse según el calendario de siembra de cada zona.",
     "- **Semáforo:** 🟡 precaución / 🔴 alerta; ✔️ = umbral validado por el responsable.",
     "- **Estratos altitudinales** (CENGICAÑA, Villatoro y Pérez 2012): litoral 0–40, bajo 40–100, medio 100–300 y alto > 300 msnm. Cada estación trae su estrato desde la API (`Estaciones_met[estrato.nombre]`); la columna `estratos` del CSV indica dónde aplica o es más relevante cada riesgo.",
     "- **Estudios técnicos regionales de CENGICAÑA:** documentos internos no publicados; se citan como estudio técnico regional con su año.\n"]
for c in CULT:
    L += [f"## {c}\n", "| Riesgo | Escala | Condición | Aplicación | 🟡 / 🔴 | Fuente (zona) | Conf. | Estado |", "|---|---|---|---|---|---|---|---|"]
    for d in R:
        if d["cultivo"] != c: continue
        fu = "; ".join(f"[{k}](#{k.lower()})" + (f" ({F[k]['zona']})" if F[k]["zona"] not in ("", "—") else "") for k in claves(d)) or "—"
        sem = f"{d['umbral_amarillo']} / {d['umbral_rojo']} {d['semaforo_unidad']}" if d["umbral_amarillo"] else "—"
        nota = f"<br>*{d['notas']}*" if d["notas"] else ""
        est = "✅ incluir" if d["estado"] == "incluir" else "⏸️ pendiente"
        v = " ✔️" if d["validado"] == "si" else ""
        L.append(f"| **{d['riesgo']}**{v} | {d['escala']} | {d['condicion']}{nota} | {d['aplicacion']} | {sem} | {fu} | {d['confianza']} | {est} |")
    L.append("")
L += ["## Referencias\n", "Cada criterio cita su fuente; **Usada en** indica qué riesgos toman valores de cada referencia.\n"]
for k, f in F.items():
    usos = [f"{d['riesgo']} ({d['cultivo']})" for d in R if k in claves(d)]
    enlace = f" [Enlace]({f['enlace']})" if f["enlace"] else ""
    zona = f" Zona: {f['zona']}." if f["zona"] not in ("", "—") else ""
    L.append(f"- <a id='{k.lower()}'></a>**{k}** — {f['referencia']}{zona}{enlace}<br>Usada en: {'; '.join(usos) if usos else '— (referencia de apoyo)'}")
pend = [d for d in R if d["estado"] == "pendiente" or d["confianza"].startswith("C")]
L += ["", "## Pendientes de revisión\n", "Riesgos sin fuente verificada (confianza C) o pendientes de criterio:\n"]
for d in pend:
    L.append(f"- **{d['riesgo']}** ({d['cultivo']}): {d['notas'] or 'sin fuente verificada.'}")
open(os.path.join(RAIZ, "docs", "10_catalogo_riesgos.md"), "w", encoding="utf-8", newline="\n").write("\n".join(L) + "\n")
print("OK docs/10_catalogo_riesgos.md —", len(R), "riesgos")
