# proyectos · los proyectos completos y el catálogo del portal

**Qué es esta carpeta.** El taller práctico de Data School: aquí viven los proyectos que se
ejecutan de principio a fin, con código, datos, verificaciones y criterio de terminado — no
enunciados para leer. Se importó el **2026-11-04** desde el portal vivo (`aprender`).

- `pf-01-pulso-poblacion/` y `pf-02-openf1/`: los **2 proyectos completos**, copiados enteros
  (código, modelos, datos y README propio).
- `CATALOGO.md`: el **catálogo de 22 proyectos (P01–P22) y 8 laboratorios (L01–L08)** del portal,
  con nivel, rutas y dataset asignado.
- `fichas/`: las **4 fichas de proyecto** de los datasets nuevos — telemetría de F1, cartera de
  acciones, clasificación de F1 y fútbol —, que agrupan los **12 proyectos P11–P22** que usan esos
  CSV. Ver [`fichas/`](fichas/).

---

## 1. Los dos proyectos completos

Los dos están terminados y verificados con **datos reales**, y cada uno trae su README con el
detalle de decisiones, límites y criterio de terminado. Aquí va el resumen; el enlace lleva al
original.

### PF-01 · El pulso de dos economías con datos públicos → [`pf-01-pulso-poblacion/README.md`](pf-01-pulso-poblacion/README.md)

La cadena entera: **ingesta → dbt → panel**. Baja población y PIB per cápita de cinco economías
europeas (ESP, FRA, DEU, ITA, PRT, 2000–2023) de la API abierta del Banco Mundial, guarda el bruto
inmutable con fecha, lo deja en tabla larga y lo modela con un proyecto dbt de verdad
(`dbt_project.yml`, `staging`, `marts` en estrella `dim_pais` + `f_poblacion`, `schema.yml` con
pruebas). El panel es un HTML con SVG que se abre con doble clic, sin servidor ni dependencias.

**Criterio de terminado** (resumido de su README): `ingerir.py` deja el bruto y las 240 filas del
CSV; `modelar.py` construye los tres modelos con sus **7 pruebas dbt en verde**; `verificar.py`
pasa sus **11 comprobaciones de la ingesta**; y `panel.py` escribe `panel.html` que se abre sin
servidor. Nada queda «a medias»: o los cuatro comandos se ejecutan sobre datos reales y las pruebas
pasan, o el proyecto no está terminado.

**15 ficheros** (incluye `data/raw/*.json` y `data/poblacion.csv`).

### PF-02 · De la API de F1 a una tabla que no se duplica → [`pf-02-openf1/README.md`](pf-02-openf1/README.md)

La cadena de **ingesta de telemetría** con el matiz que la hace difícil: idempotencia. Descarga
sesiones, pilotos, stints y vueltas de tres carreras de 2024 (Sakhir, Jeddah, Melbourne) de OpenF1
—API gratuita y sin clave—, guarda el bruto fechado y deja una tabla de vueltas cuya clave es
`(sesión, piloto, vuelta)`: reejecutar la ingesta no duplica ni pierde nada. `degradacion.py`
cruza stints y vueltas y calcula la pendiente de cada tramo, incluido el detalle incómodo: las
pendientes salen negativas porque el coche se aligera de combustible más rápido de lo que el
neumático se degrada.

**Criterio de terminado** (resumido de su README): **8 comprobaciones** en `verificar.py` en verde,
**3.029 vueltas únicas**, 59 pares sesión-piloto, **cero duplicados** al reejecutar, y el bruto
guardado. El proyecto declara además lo que le falta para portfolio (orquestación diaria, cruce con
`pit`, panel de posiciones).

Es el proyecto **P17** del catálogo del portal, hecho de verdad.

**16 ficheros** (incluye `data/raw/*.json`, `data/vueltas.csv` y `data/degradacion.csv`).

---

## 2. El catálogo: 22 proyectos y 8 laboratorios → [`CATALOGO.md`](CATALOGO.md)

`CATALOGO.md` tabula los **22 proyectos (P01–P22)** y los **8 laboratorios (L01–L08)** del portal
vivo, con id, título, resumen, nivel (básico 7 · intermedio 16 · avanzado 7), rutas de estudio
(NUC/DE/DS/QT/ALG) y el dataset asignado a cada uno, más los 10 conjuntos sintéticos con sus filas
y licencia.

**Qué es y qué no es.** Es el **catálogo del portal vivo**: el mapa de qué practicar y con qué
datos. De los 30 recursos, solo los **2 proyectos completos** de esta carpeta traen código, datos y
**criterios verificables**; los otros 28 son la referencia de qué cubre el temario, no enunciados
importados. Un laboratorio es una pieza corta sobre un dataset; un proyecto cruza varias capas y
cierra con un criterio explícito.

---

## 3. Procedencia, fecha y regla de contenido

- **Procedencia.** `F:\Proyectos\ProyectoServidor\aprender` (portal vivo), leído en **solo
  lectura** el **2026-11-04**: `proyectos/pf-01-pulso-poblacion`, `proyectos/pf-02-openf1` y el
  catálogo extraído con Node de `web/datos/portal.js` (`window.PORTAL.recursos`) y contrastado con
  el índice de búsqueda `web/datos/busqueda.js`.
- **Exclusiones de la copia.** No se copian `__pycache__`, `*.pyc`, `*.duckdb` ni `*.log`: son
  artefactos de ejecución, no material del proyecto. Los CSV y el bruto JSON sí, porque sin datos no
  se puede verificar nada.
- **Regla.** **No se copian enunciados ni textos de terceros.** Los resúmenes del catálogo y los
  READMEs son contenido propio del proyecto; las fuentes externas se enlazan y se resumen en
  palabras propias. Se puede aprender del modelo de otros catálogos; no redistribuir su contenido.
- **Sin git.** Esta importación no hace commits ni toca el historial; de eso se encarga el Lead.
