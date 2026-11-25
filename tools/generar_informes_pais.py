"""Genera los informes por país (GT y SV) a partir del informe de trabajo Tablero-semanal-ICC.Report.

Esquema: un modelo semántico (Tablero-semanal-ICC) y tres informes:
  - Tablero-semanal-ICC.Report      informe de trabajo: diseño, validaciones, sin filtro de país.
                                    Es el único que se edita en Desktop y el que publica el modelo.
  - Tablero-semanal-ICC-GT.Report   generado: filtro Guatemala.
  - Tablero-semanal-ICC-SV.Report   generado: filtro El Salvador.
Los informes generados solo llevan las páginas públicas (se omiten Validaciones* y Pronóstico*),
filtro de país a nivel de informe (oculto y bloqueado) y mapas con ajuste automático.

Uso (con Power BI Desktop cerrado), después de cualquier cambio en el informe de trabajo:
      python tools/generar_informes_pais.py
Conexión: si existe config/conexion_servicio.json con {"connectionString": "..."} (copiada del definition.pbir de un
informe en blanco conectado al modelo publicado desde Desktop) o con {"workspace": "<nombre>", "semanticmodelid": "<id>"},
los informes por país se conectan al modelo publicado (informes ligeros: publicarlos NO reemplaza el modelo).
Sin ese archivo apuntan al modelo local, para revisarlos en Desktop.
"""
import json, os, shutil, uuid, datetime, glob
RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE = "Tablero-semanal-ICC"
PAISES = {"GT": "Guatemala", "SV": "El Salvador"}
PAGINAS_EXCLUIDAS = ("Validaciones", "Pronostico", "Pronóstico")
os.chdir(RAIZ)

def rj(p): return json.load(open(p, encoding="utf-8-sig"))
def wj(p, d): open(p, "w", encoding="utf-8", newline="").write(json.dumps(d, indent=2, ensure_ascii=False).replace("\n", "\r\n"))
lit = lambda v: {"expr": {"Literal": {"Value": v}}}

def filtro_pais(pais):
    col = lambda src: {"Column": {"Expression": {"SourceRef": src}, "Property": "pais.nombre"}}
    return {"filters": [{
        "name": "filtro_pais", "type": "Categorical",
        "field": col({"Entity": "Estaciones_met"}),
        "filter": {"Version": 2, "From": [{"Name": "e", "Entity": "Estaciones_met", "Type": 0}],
                   "Where": [{"Condition": {"In": {"Expressions": [col({"Source": "e"})],
                                                   "Values": [[{"Literal": {"Value": "'" + pais + "'"}}]]}}}]},
        "isHiddenInViewMode": True, "isLockedInViewMode": True}]}

def conexion():
    cfg = "config/conexion_servicio.json"
    if os.path.exists(cfg):
        c = rj(cfg)
        if c.get("connectionString"):  # copiada de un informe conectado creado por Desktop (necesario en Mi área de trabajo)
            return {"byConnection": {"connectionString": c["connectionString"]}}, "modelo publicado"
        cs = (f'Data Source="powerbi://api.powerbi.com/v1.0/myorg/{c["workspace"]}";initial catalog={BASE};'
              f'access mode=readonly;integrated security=ClaimsToken;semanticmodelid={c["semanticmodelid"]}')
        return {"byConnection": {"connectionString": cs}}, "modelo publicado"
    return {"byPath": {"path": f"../{BASE}.SemanticModel"}}, "modelo local"

ref, tipo_conexion = conexion()
_pag = f"{BASE}.Report/definition/pages"
OMITIDAS = [pid for pid in rj(f"{_pag}/pages.json")["pageOrder"]
            if rj(f"{_pag}/{pid}/page.json")["displayName"].startswith(PAGINAS_EXCLUIDAS)]
for cod, pais in PAISES.items():
    nombre = f"{BASE}-{cod}"; destino = f"{nombre}.Report"; plataforma = None
    # 1. respaldar la copia anterior (conserva su logicalId para no duplicar el informe en el servicio)
    if os.path.isdir(destino):
        if os.path.exists(f"{destino}/.platform"): plataforma = rj(f"{destino}/.platform")
        bk = f"_respaldo/informes_pais/{datetime.datetime.now():%Y%m%d_%H%M%S}_{cod}"
        os.makedirs(os.path.dirname(bk), exist_ok=True); shutil.move(destino, bk)
    def ignorar(carpeta, nombres):
        fuera = {".pbi"}
        if os.path.normpath(carpeta) == os.path.normpath(f"{BASE}.Report/definition/pages"):
            fuera |= set(OMITIDAS)
        return [n for n in nombres if n in fuera]
    shutil.copytree(f"{BASE}.Report", destino, ignore=ignorar)
    # 2. identidad propia
    if not plataforma:
        plataforma = rj(f"{destino}/.platform"); plataforma["config"]["logicalId"] = str(uuid.uuid4())
    plataforma["metadata"]["displayName"] = nombre
    wj(f"{destino}/.platform", plataforma)
    # 3. solo páginas públicas
    pj = f"{destino}/definition/pages/pages.json"; pages = rj(pj)
    orden = [pid for pid in pages["pageOrder"] if pid not in OMITIDAS]
    pages["pageOrder"] = orden
    if pages.get("activePageName") not in orden: pages["activePageName"] = orden[0]
    wj(pj, pages)
    # 4. filtro de país
    r = rj(f"{destino}/definition/report.json"); r["filterConfig"] = filtro_pais(pais)
    wj(f"{destino}/definition/report.json", r)
    # 5. mapas con ajuste automático a las estaciones del país
    for f in glob.glob(f"{destino}/definition/pages/*/visuals/*/visual.json"):
        v = rj(f)
        if v["visual"].get("visualType") == "azureMap":
            mc = v["visual"].setdefault("objects", {}).setdefault("mapControls", [{"properties": {}}])[0].setdefault("properties", {})
            for k in ("zoom", "centerLatitude", "centerLongitude"): mc.pop(k, None)
            mc["autoZoom"] = lit("true"); wj(f, v)
    # 6. conexión al modelo y archivo .pbip
    d = rj(f"{destino}/definition.pbir"); d["datasetReference"] = ref; wj(f"{destino}/definition.pbir", d)
    p = rj(f"{BASE}.pbip"); p["artifacts"] = [{"report": {"path": destino}}]; wj(f"{nombre}.pbip", p)
    print(f"OK {destino}: {pais}, {len(orden)} páginas, {tipo_conexion}")
