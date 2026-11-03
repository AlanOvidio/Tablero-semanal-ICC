# Tablero agroclimático ICC — Boletines semanales en Power BI

Modelo semántico y reporte de Power BI que reemplazan los boletines meteorológicos semanales en PDF con un tablero interactivo para agrónomos y técnicos de campo. Los datos provienen de la **Red Meteorológica del ICC** (API REDMET, 35 estaciones en la costa sur de Guatemala, datos desde 2008).

- **Responsable:** Alan — equipo CeH, Instituto Privado de Investigación sobre Cambio Climático (ICC)
- **Formato:** Power BI Project (`.pbip`): modelo en TMDL y reporte en PBIR, legibles y versionables con Git
- **Licencia de Power BI:** Pro

## Contenido de la carpeta

```
Tablero/
├── 2026_dashboard_exp1.pbip            ← abrir este archivo en Power BI Desktop
├── 2026_dashboard_exp1.SemanticModel/  ← modelo: tablas, Power Query (M), medidas DAX (TMDL)
│   └── definition/
│       ├── tables/*.tmdl               ← una tabla por archivo; _Medidas.tmdl tiene todas las medidas
│       ├── relationships.tmdl
│       └── expressions.tmdl            ← parámetros (RangeStart, RangeEnd…) y funciones de la API
├── 2026_dashboard_exp1.Report/         ← reporte: páginas y visuales (JSON)
├── docs/                               ← documentación
├── config/                             ← catálogo de riesgos y fuentes (CSV editables en Excel)
├── referencias/                        ← PDFs de las fuentes (no se suben al repositorio)
├── tools/                              ← generadores de documentación
├── .gitignore
└── README.md
```

## Documentación

| Documento | Para quién | Contenido |
|---|---|---|
| [01 · Arquitectura](docs/01_arquitectura.md) | Mantenimiento | Fuentes, flujo de datos, tablas de hechos, calendario hidrológico, reglas de agregación |
| [02 · Diccionario de datos](docs/02_diccionario_datos.md) ⚙️ | Mantenimiento | Parámetros, actualización incremental, relaciones, columnas y consultas M |
| [03 · Catálogo de medidas](docs/03_catalogo_medidas.md) ⚙️ | Mantenimiento | Las medidas DAX por tema, con descripción y código |
| [04 · Guía de usuario](docs/04_guia_usuario.md) | Agrónomos / técnicos | Cómo leer cada página, indicadores, semáforos y umbrales |
| [05 · Operación](docs/05_operacion.md) | Mantenimiento | Actualizar, publicar, agregar estaciones, solución de problemas |
| [06 · Decisiones y cambios](docs/06_decisiones_y_cambios.md) | Mantenimiento | Por qué el modelo funciona como funciona, y bitácora de cambios |
| [07 · Repositorio Git/GitHub](docs/07_repositorio_git.md) | Mantenimiento | Cómo versionar el proyecto paso a paso |
| [08 · Plan de mejoras](docs/08_plan_mejoras.md) | Mantenimiento | Tablero multicultivo, pronóstico semanal, catálogo de riesgos y decisiones |
| [09 · Inventario de visuales](docs/09_inventario_visuales.md) ⚙️ | Mantenimiento | Páginas, visuales y campos que usa cada uno |
| [10 · Catálogo de riesgos](docs/10_catalogo_riesgos.md) | Mantenimiento / agronomía | Riesgos por cultivo con condiciones, umbrales, fuentes y estado de validación ([CSV editable](config/riesgos_cultivo.csv)) |

⚙️ = se genera automáticamente; no editar a mano.

## Inicio rápido

1. Abrir `2026_dashboard_exp1.pbip` con Power BI Desktop (cerrar OneDrive o esperar a que termine de sincronizar).
2. En Power Query → **Administrar parámetros**: `RangeEnd` = las **00:00 del día siguiente** al último día del boletín (p. ej., boletín al domingo 25-oct → `26-oct 00:00`).
3. **Inicio → Actualizar**.
4. En la página **Resumen Semanal**, elegir *Año hidrológico* y *Semana*.
5. Para publicar: **Publicar** al área de trabajo; la primera vez hacer una actualización completa en el servicio (ver [Operación](docs/05_operacion.md)).

## Mantener la documentación al día

Después de cualquier cambio al modelo o al reporte, y antes de hacer *commit*:

```
python tools/generar_docs_modelo.py
python tools/generar_catalogo_riesgos.py   # si se editaron config/riesgos_cultivo.csv o config/fuentes_riesgos.csv
python tools/generar_riesgos_modelo.py     # aplica el CSV de riesgos al modelo (con Power BI Desktop cerrado)
```

Y registrar el cambio en [06 · Decisiones y cambios](docs/06_decisiones_y_cambios.md).
