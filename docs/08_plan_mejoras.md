# Plan de mejoras: tablero multicultivo y pronóstico semanal

> Estado: **aprobado** (2026-11-03). Marcar cada tarea al completarla y registrar el detalle en [06 · Decisiones y cambios](06_decisiones_y_cambios.md).

## Objetivo

1. Una sola página **Resumen Semanal** que sirva para todos los cultivos mediante un **selector de cultivo**, sustituyendo la página específica de caña.
2. Una página contraparte **Pronóstico Semanal** con la misma estructura, alimentada con pronósticos de Open-Meteo.
3. Criterios de riesgo **parametrizados en tablas** (umbrales, fuente, validación), de modo que agregar o ajustar un cultivo o un riesgo no requiera programar.

## Decisiones tomadas

| Tema | Decisión |
|---|---|
| Página por cultivo | **No.** Una página con selector de cultivo; se integra lo relevante de la página de Caña y luego se elimina. |
| Cultivos | Caña de azúcar, Banano, Aguacate, Palma de aceite, **Granos básicos** (maíz y frijol en un mismo selector, riesgos rotulados "Maíz – …" / "Frijol – …"). |
| Riesgos de balance hídrico (déficit de palma, estrés hídrico de banano) | **Se excluyen**: el balance es un proceso diario/acumulado y ya se muestra en otros visuales. |
| Escala de cada riesgo | **H** horaria (también en el mapa de calor), **D** diaria (días/semana), **A** acumulada (ventana de días o grados día). Solo los riesgos que dependen de la duración de humedad/mojadura y temperatura van al mapa de calor. |
| Umbrales | En la tabla `Riesgos_Cultivo`, con **fuente**, **zona de origen** y estado **validado** (inicia en *no*). |
| Prioridad de fuentes | 1) Guatemala / El Salvador · 2) Centroamérica y sur de México · 3) otras zonas tropicales de baja latitud. |
| Grados día granos básicos | **Una sola serie** (maíz y frijol comparten base 10 °C). Tope a definir con la bibliografía. |
| Época de zafra | **Noviembre – mayo** (para "interrupción de zafra"). |
| Comparación estación vs. promedio | **Descartada.** |
| Selección de estaciones | **Segmentador de Estación** persistente; los clics en visuales **filtran** (no resaltan). |
| Pronóstico | Open-Meteo, **7 días**, API gratuita en primera instancia. Desde el día 5 los indicadores horarios se marcan **baja confianza**. Mojadura estimada con proxy. En lugar de "semanas anteriores": **anomalía vs. climatología**. |
| Repositorio | Se trabaja en `Tablero-semanal-ICC`; los commits los hace el responsable con GitHub Desktop. |
| Estratos altitudinales | Se usan los de CENGICAÑA (litoral, bajo, medio, alto) que ya trae cada estación desde la API, como criterio de aplicación y de contexto. |
| Fuentes no publicadas | Los estudios internos de CENGICAÑA se usan y se citan como **estudio técnico regional de CENGICAÑA (año)**; los libros y capítulos publicados se citan normalmente. |
| Umbrales de estrés térmico | Por cultivo (Chaves-Barrantes y Gutiérrez-Soto 2017), no un valor genérico. |

## Fases

### Fase 1a · Revisión bibliográfica de riesgos
- [x] Primera revisión entregada: [10 · Catálogo de riesgos](10_catalogo_riesgos.md), datos en `config/riesgos_cultivo.csv` y `config/fuentes_riesgos.csv`.
- [x] Segunda revisión con documentos aportados (`referencias/`) y bibliografía local de caña (libro CENGICAÑA 2012 y estudios técnicos regionales).
- [ ] Para cada riesgo del catálogo: condición favorable, umbrales (amarillo/rojo), escala, variables, fuente y zona.
- [ ] Entrega como tabla para validación del responsable.

### Fase 1b · Modelo multicultivo (sin cambios visuales)
- [x] Tabla `Cultivos` (cultivo, temperatura base y tope de GDD, orden).
- [x] Tabla `Riesgos_Cultivo` (cultivo, riesgo, tipo, escala, umbral amarillo, umbral rojo, unidad, descripción, fuente, zona, validado).
- [x] Medidas genéricas: `Dias_Riesgo_Sel`, `Semaforo_Riesgo_Sel` (umbrales desde la tabla), `GDD_Cultivo_Acumulado` y año anterior (base/tope desde la tabla).
- [x] Condiciones diarias y horarias de los riesgos como medidas DAX generadas desde el CSV; generaciones de cogollero y alerta de emergencia de salivosa. (Índice acumulado de sigatoka: pendiente.)
- [x] Mapa de calor por cultivo con `Riesgo_Hora` (la tabla `Plagas` se retira en la Fase 2).

### Fase 2 · Resumen Semanal multicultivo
Diseño acordado (2026-11-03): clima arriba (secciones actuales) y debajo un bloque *Riesgos del cultivo*; riesgos en **matriz semáforo** (fila por riesgo: valor, unidad, umbrales, color); **matriz finca × riesgo** agrupada por estrato con celdas coloreadas; segmentador de **Estación** desplegable en la fila de segmentadores.

- [ ] Selector de **Cultivo** junto a Año, Semana y Estrato; segmentador de **Estación**.
- [ ] Secciones comunes: mapa, lluvia/ETo/balance, temperaturas, VPD, viento, radiación, rosa de vientos.
- [ ] Secciones por cultivo (desde la página de Caña): tarjetas de alerta (una por riesgo), contexto productivo (GDD vs. año anterior, horas de luz, mojadura), tabla estaciones × riesgos, mapa con riesgos, mapa de calor horario.
- [ ] Configuración de reporte: **filtrado cruzado por defecto**; revisión de interacciones de la página.
- [ ] Título dinámico con el contexto (estación/estrato y fechas).
- [ ] Eliminar la página *Resumen Semanal – Caña Azúcar*.

### Fase 3 · Pronóstico Semanal (Open-Meteo)
- [ ] Ingesta: una llamada con las coordenadas de todas las estaciones; datos horarios, zona horaria de Guatemala; parámetro de horizonte (7 días por defecto); actualización completa diaria.
- [ ] Tablas `Fact_Pron_Horaria`, `Fact_Pron_Diaria`, `Fact_Pron_Subdiaria` con las mismas columnas que las observadas.
- [ ] Variables directas (T, HR, lluvia, viento km/h y dirección, ráfagas, radiación de onda corta, ETo FAO, VPD, punto de rocío) y calculadas (índice de calor, periodo de luz, horas de estrés, GDD, banderas). **Mojadura** por proxy (HR ≥ 90 % o T − Td ≤ 2 °C), rotulada como estimada.
- [ ] Tabla `Escenario` (Observado / Pronóstico): las medidas base cambian de fuente según la página; las derivadas se reutilizan. Requiere que los días de riesgo evalúen medidas en lugar de filtrar columnas de `Fact_Diaria_met`.
- [ ] `Calendario` extendido hasta hoy + 16 días.
- [ ] Página *Pronóstico Semanal*: fecha de emisión, próximos 7 días, marca de baja confianza desde el día 5, anomalía vs. climatología.
- [ ] Atribución visible: "Datos de pronóstico: Open-Meteo.com (CC BY 4.0)".
- [ ] (Opcional, Fase 5) Corrección de sesgo comparando pronóstico vs. observado.

### Fase 4 · Documentación y validación
- [ ] Guía de usuario (selector de cultivo, pronóstico, indicadores estimados), arquitectura, bitácora; regenerar documentos automáticos.

## Catálogo de riesgos (propuesta para la Fase 1a)

Escala: **H** horaria · **D** diaria · **A** acumulada. Condiciones **referenciales**, a precisar y validar en la Fase 1a. *(actual)* = ya existe en el modelo.

### Caña de azúcar
| Riesgo | Tipo | Condición referencial | Escala |
|---|---|---|---|
| Roya café *(actual)* | Enfermedad | 15–25 °C, HR > 80 %, mojadura prolongada | H |
| Roya naranja | Enfermedad | ~22–30 °C, rocío/mojadura prolongada | H |
| Carbón *(actual)* | Enfermedad | 25–30 °C, días secos | D |
| Salivosa *(actual)* | Plaga | 22–28 °C, HR > 80 %, lluvia | H/D |
| Barrenador *(actual)* | Plaga | > 24 °C, HR 60–80 %, seco; generaciones por grados día | D/A |
| Estrés térmico *(actual)* | Abiótico | T > 35 °C y radiación > 800 W/m² | H |
| Interrupción de zafra | Operativo | Lluvia > umbral, noviembre – mayo | D |
| Riesgo de quema / incendio | Operativo | HR baja + viento fuerte + días secos consecutivos | D |
| Condiciones de maduración | Productivo | Amplitud térmica alta, noches frescas | D |

### Banano
| Riesgo | Tipo | Condición referencial | Escala |
|---|---|---|---|
| Sigatoka negra *(actual, mejorar)* | Enfermedad | 25–28 °C, HR > 90 %, mojadura nocturna + índice acumulado 7–14 días | H/A |
| Sigatoka amarilla | Enfermedad | Más fresca que la negra, HR alta, mojadura | H |
| Moko *(actual)* | Enfermedad | Lluvia abundante (dispersión) | D |
| Punta de cigarro | Enfermedad | HR alta y lluvia frecuente | D |
| Pudrición acuosa (*Erwinia*) | Enfermedad | Cálido y muy húmedo | D |
| Picudo negro (*Cosmopolites*) | Plaga | Periodos lluviosos y húmedos | A |
| Thrips de la mancha roja | Plaga | Periodos cálidos y secos | A |
| Volcamiento *(actual)* | Abiótico | Viento máximo > 40 / 60 km/h | D |

### Aguacate
| Riesgo | Tipo | Condición referencial | Escala |
|---|---|---|---|
| Phytophthora *(actual)* | Enfermedad | 20–30 °C con exceso de agua | D |
| Antracnosis | Enfermedad | 20–30 °C, lluvia, HR alta/mojadura | H |
| Roña (*Sphaceloma*) | Enfermedad | Lluvia y humedad en floración y cuajado | H/D |
| Frío *(actual)* | Abiótico | Tmín < 12 °C | D |
| Golpe de calor / quemadura de fruto | Abiótico | T > 35 °C y radiación alta | H |

### Palma de aceite
| Riesgo | Tipo | Condición referencial | Escala |
|---|---|---|---|
| Pudrición del cogollo (*P. palmivora*) *(actual, mejorar)* | Enfermedad | Lluvia frecuente, HR > 90 % prolongada, 20–30 °C | H/A |
| Picudo (*R. palmarum*) / anillo rojo | Plaga / vector | Mayor actividad en temporada lluviosa y cálida | A |
| Complejo *Leptopharsa* – *Pestalotiopsis* | Plaga + enfermedad | Periodo seco y cálido seguido de humedad | A |
| Estrés térmico | Abiótico | T > 35 °C y radiación alta | H |

Excluidos por depender de vectores o suelo más que del clima: marchitez letal y sorpresiva, *Ganoderma*.

### Granos básicos (maíz y frijol)
| Riesgo | Tipo | Condición referencial | Escala |
|---|---|---|---|
| Maíz – Mancha de asfalto *(actual)* | Enfermedad | Temperatura moderada, HR > 75 %, mojadura nocturna prolongada | H |
| Maíz – Roya común | Enfermedad | ~16–23 °C, HR alta | H |
| Maíz – Tizón foliar | Enfermedad | ~18–27 °C, rocío/mojadura | H |
| Maíz – Mancha gris | Enfermedad | HR > 90 % prolongada, cálido | H |
| Maíz – Gusano cogollero | Plaga | Generaciones por grados día; calor y sequía | A |
| Maíz – Estrés térmico en floración | Abiótico | T > 35 °C | D |
| Frijol – Mustia hilachosa | Enfermedad | ~25–30 °C, HR alta, lluvia | H |
| Frijol – Roya | Enfermedad | ~17–27 °C, HR > 95 %, 10–18 h de mojadura | H |
| Frijol – Antracnosis | Enfermedad | ~13–26 °C, lluvia | H |
| Frijol – Mancha angular | Enfermedad | ~16–28 °C, alternancia húmedo/seco | H |
| Frijol – Bacteriosis común | Enfermedad | ~28–32 °C con lluvia y viento | D |
| Frijol – Mosca blanca (vector de virus) | Plaga | Periodos cálidos y secos | A |
| Frijol – Estrés por calor en floración | Abiótico | Tmáx > 30–32 °C o noches > 20 °C | D |
| Granos – Sequía *(actual)* | Abiótico | Días secos consecutivos | D |

## Fuentes de partida para la Fase 1a

| Cultivo | Guatemala / El Salvador | Región / latitudes similares |
|---|---|---|
| Caña | Universidad del Valle de Guatemala (tesis de plagas); Universidad de El Salvador (salivosa, barrenador) | IMN Costa Rica; Colombia |
| Granos básicos | ICTA (boletines y memorias); USAC (CyTES); complejo de mancha de asfalto en el altiplano de Guatemala; UES (frijol) | Zamorano (Honduras); INTA y UNA (Nicaragua); MAG y UCR (Costa Rica); CIAT |
| Banano | — | TEC y MAG (Costa Rica); sistemas de alerta de sigatoka (Venezuela, Colombia, Ecuador) |
| Palma | Universidad del Valle de Guatemala | Femexpalma (sur de México); Fedepalma e ICA (Colombia); CATIE |
| Aguacate | — | MAG Costa Rica; INIFAP (México); República Dominicana |

## Open-Meteo: condiciones de uso (consultadas el 2026-11-03)

- La API gratuita es para **uso no comercial**: incluye sitios o aplicaciones sin fines de lucro **sin suscripciones ni publicidad**, contenido educativo e **investigación pública en instituciones públicas**. Se considera comercial: suscripciones, publicidad, productos comerciales y la investigación no divulgada en entidades comerciales.
- No hay un plan académico separado; el uso educativo/de investigación pública entra en el nivel gratuito.
- Límites: < 10 000 llamadas/día, 5 000/hora, 600/minuto. Este tablero necesita **1–2 llamadas por actualización** (todas las estaciones en una sola consulta).
- Licencia de datos CC BY 4.0: incluir la atribución en la página de pronóstico.
- **Pendiente:** el ICC es una institución privada. Si el tablero se distribuye sin costo, sin publicidad y sin suscripción, el uso es compatible con el nivel gratuito en espíritu, pero conviene **confirmarlo con Open-Meteo** (contacto en su sitio) antes de publicarlo de forma abierta. Si no aplica, la alternativa es una suscripción (API comercial).
