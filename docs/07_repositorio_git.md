# Versionar el proyecto con Git y GitHub

El formato `.pbip` guarda el modelo (TMDL) y el reporte (JSON) como texto. Con Git cada cambio queda registrado y se puede comparar o revertir. Además se reemplazan los respaldos manuales (`_respaldo_*`) y se evitan los conflictos de OneDrive.

## Recomendación

| Opción | Ventajas | Notas |
|---|---|---|
| **GitHub, repositorio privado** (recomendada) | Gratis, fácil con GitHub Desktop, muestra Markdown y diagramas | Cuenta personal o de la organización ICC |
| Azure DevOps (Repos) | Integración con el ecosistema Microsoft | Útil si el ICC ya lo usa |

Con licencia **Pro** se trabaja en modo local: Desktop guarda en la carpeta y Git versiona esa carpeta. La sincronización automática entre un área de trabajo del servicio y Git (*Git integration* de Fabric) requiere capacidad Premium/Fabric; no es necesaria para este flujo.

## Paso a paso (primera vez)

### 1. Mover el proyecto fuera de OneDrive (recomendado)
OneDrive y Git sincronizando la misma carpeta generan conflictos. Copiar la carpeta `Tablero` a una ruta local, por ejemplo `C:\Proyectos\Tablero-ICC\`, y trabajar desde ahí. GitHub se convierte en el respaldo en la nube.

### 2. Instalar herramientas
- [GitHub Desktop](https://desktop.github.com) (incluye Git).
- Opcional: [Visual Studio Code](https://code.visualstudio.com) para ver diferencias en TMDL con resaltado.

### 3. Crear el repositorio
1. GitHub Desktop → *File → Add local repository* → elegir `C:\Proyectos\Tablero-ICC`.
2. Aceptar *create a repository here*. Nombre: `tablero-agroclimatico-icc`. **Git ignore: None** (el proyecto ya trae su `.gitignore`).
3. Verificar en la lista de cambios que **no** aparezcan `cache.abf`, `localSettings.json` ni carpetas `_respaldo_*`.
4. Resumen del primer commit: `Versión inicial del tablero y documentación` → **Commit to main**.
5. **Publish repository** → marcar **Keep this code private** → Publish.

## Flujo de trabajo diario

1. **Antes de abrir Power BI:** en GitHub Desktop, *Fetch origin / Pull* (si trabaja más de una persona o equipo).
2. Hacer los cambios en Power BI Desktop y **guardar**.
3. **Cerrar Power BI Desktop.**
4. Regenerar la documentación: `python tools/generar_docs_modelo.py`.
5. Registrar el cambio en `docs/06_decisiones_y_cambios.md`.
6. GitHub Desktop: revisar los archivos modificados (los `.tmdl` muestran exactamente qué medida o consulta cambió), escribir un resumen claro y **Commit** → **Push origin**.

### Buenas prácticas
- Un commit por cambio lógico ("Balance semanal por estación", no "cambios varios").
- Cambios grandes o experimentales en una **rama** (*Branch → New branch*), y fusionar a `main` cuando estén validados.
- Para volver a una versión anterior: *History* → clic derecho en el commit → *Revert changes in commit*.
- Etiquetar versiones publicadas (`v2026.11`) para saber qué versión está en el servicio.
- No subir credenciales. La API se autentica desde Power BI; ninguna contraseña queda en los archivos TMDL.

## Qué se versiona y qué no

| Se versiona | No se versiona (`.gitignore`) |
|---|---|
| `*.pbip`, `*.SemanticModel/definition/**` (TMDL), `*.Report/definition/**` (JSON), `diagramLayout.json`, `docs/`, `tools/`, `README.md` | `.pbi/cache.abf` (datos), `.pbi/localSettings.json`, `_respaldo_*`, copias de conflicto de OneDrive |

Después de clonar el repositorio en otro equipo, abrir el `.pbip` y **Actualizar**: los datos se descargan de la API (no viajan en el repositorio).
