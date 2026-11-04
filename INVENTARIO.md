# Inventario de los cinco orígenes — Data School

Medición hecha el **2026-11-04** sobre la máquina de David. **Nada se ha dado por supuesto**: cada cifra sale de contar ficheros con un script reproducible, comparar hashes SHA-256 o leer los datos del propio portal (JSON de `web/datos/portal.js`, índice de `web/datos/busqueda.js`, base SQLite de la vista previa). Los cinco orígenes se han leído en **solo lectura**; no se ha escrito nada en ellos.

Reproducir la medición:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File tools/medir-origenes.ps1 -Salida INFORMES/medicion-origenes-2026-11-04.txt
```

El informe crudo de esta pasada está en [`INFORMES/medicion-origenes-2026-11-04.txt`](INFORMES/medicion-origenes-2026-11-04.txt).

## Resumen

| # | Origen | Ficheros | Tamaño | Conceptos | Fases | CSV | Figuras | Proyectos | Documentación |
|---|---|---|---:|---:|---:|---:|---|---|---|
| 1 | `F:\Proyectos\ProyectoServidor\aprender` — portal vivo | 7.478 | 271,41 MB | **459** | 13 (f00–f12) | **13** (10 de portal + 3 de proyectos) | 350 fuentes `.py`, 370 SVG, 370 recursos | **2 completos** + catálogo de **22** + 8 labs | 174 en `docs/` + 21 especificaciones |
| 2 | `...\aprender\docs\data-school-import` — importación | 13 | 0,07 MB | — | — | — | — | — | **32 fuentes** + 6 documentos + 5 de diseño + 2 herramientas |
| 3 | `E:\orca-workspaces-archivo-2026-11-03\aprender\equipo-ia` — archivo de Orca | 4.833 | 138,62 MB | **438** | 13 (f00–f12) | **6** | 350 fuentes `.py`, 369 SVG, 370 recursos | catálogo de **10** + 8 labs | 302 en `docs/` (168 exclusivos) |
| 4 | `C:\Users\David\orca\preview-data` — vista previa | 4 | 1,20 MB | **0** | — | **0** | — | — | 0 (base de datos vacía de contenido) |
| 5 | `F:\Proyectos\data-school` — esta carpeta | 18 versionados (25 en disco sin `.git`) | 0,20 MB | **0** | — | **0** | — | — | 8 documentos + sistema de diseño + comprobador |

> El origen 4 no es una copia del portal de datos: es la base SQLite de **otro** servicio (`opofuente`, una vista previa de oposiciones) con 76 tablas **sin filas de contenido**. Detalle en el apartado 4.

## 1. Portal vivo — `aprender`

**7.478 ficheros, 271,41 MB.** Es el origen más grande y el más completo. Incluye `node_modules` (182 ficheros), caché de bytecode, evidencias de verificación y entregas de sesiones anteriores; por eso el tamaño no es solo contenido.

### 1.1 Conceptos y fases

13 fases (`f00`–`f12`), **459 ficheros `.md`**, todos los que declara el propio portal: `web/datos/portal.js` dice `"total":459` y la suma de sus `porFase` da exactamente 459.

| Fase | Nombre | Conceptos |
|---|---|---:|
| f00 | Aprender a aprender | 14 |
| f01 | Fundamentos matemáticos | 41 |
| f02 | Inferencia y estadística | 26 |
| f03 | Python, SQL y herramientas | 42 |
| f04 | Ingeniería de datos | 61 |
| f05 | Exploración y series temporales | 29 |
| f06 | Machine learning clásico | 49 |
| f07 | Deep learning | 33 |
| f08 | LLMs e IA generativa | 22 |
| f09 | Finanzas cuantitativas | 61 |
| f10 | Algoritmos y estructuras | 32 |
| f11 | Ingeniería de software | 34 |
| f12 | Comunicación y carrera | 15 |
| **Total** | | **459** |

Comprobaciones adicionales:

- **459 de 459** conceptos llevan al menos un bloque de código (` ``` `).
- **349 bloques `:::figura`** repartidos por los conceptos; cada uno apunta a `figuras/<nombre>.py` y a un SVG generado.
- Cada `.md` empieza con frontmatter YAML: `id`, `titulo`, `fase`, `nivel`, `rutas`, `prerequisitos`, `tags`, `resumen`, `fuentes`.

### 1.2 Datasets

- **10 CSV** en `web/datos/datasets/`: `algoritmos-tiempos`, `cartera-acciones`, `clientes-churn`, `encuestas-satisfaccion`, `f1-clasificacion`, `futbol-partidos`, `precios-accion`, `sensores-planta`, `telemetria-f1`, `ventas-mensuales`.
- Metadatos en `web/datos/datasets.json`: **licencia `CC0-1.0` (datos sintéticos)**, filas, columnas, origen y **checksum SHA-256** de cada CSV.
- Generador de procedencia: `datos/generar-datasets.mjs` con semilla fija por conjunto.
- **3 CSV más** dentro de los proyectos: `pf-01-pulso-poblacion/data/poblacion.csv`, `pf-02-openf1/data/vueltas.csv` y `pf-02-openf1/data/degradacion.csv`.

### 1.3 Figuras y recursos

- **350 scripts de figura** en `figuras/*.py` (1,25 MB) — son la fuente de cada figura.
- **370 SVG** en `web/figuras/` (20,58 MB) — la figura ya renderizada que sirve el portal.
- **370 ficheros** en `recursos/` (369 SVG + 1 JSON) — mismo material que consume la web.
- 351 `.pyc` en `figuras/__pycache__/` — caché de bytecode, **no es fuente**.

### 1.4 Código ejecutado (evidencia)

`.verificacion/` guarda la prueba de que el código de los conceptos se ejecutó:

- **913 scripts `.py`** extraídos de los conceptos,
- **33 `.sql`**,
- **946 salidas `.txt`** en `.verificacion/salidas/` (resultado impreso de cada ejecución),
- 1 `.json`.

Total: **1.893 ficheros, 1,09 MB**.

**Cobertura medida: la evidencia del portal cubre 438 de los 459 conceptos.** Los 21 conceptos
añadidos después a la viva no están en `.verificacion/`: 16 de ellos sí tienen bloque
`python verificable` (ejecutable) y 5 no tienen código ejecutable (shell, YAML o metadatos). El
verificador del portal (`generar.mjs --ejemplos` + `verificar-ejemplos.ps1`) no se volvió a ejecutar
tras añadir esos conceptos. En la consolidación se ejecutaron los 16 que faltaban (16 scripts y 16
salidas, 0 fallos) con el Python del sistema: la carpeta importada queda con **1.925 ficheros**
(929 `.py`, 33 `.sql`, 1 `.json` y 962 salidas). Ver `conceptos/README.md` y
`tools/verificar-conceptos.ps1`.

### 1.5 Proyectos

- **2 proyectos completos** en `proyectos/`: `pf-01-pulso-poblacion` (16 ficheros: ingesta, dbt, panel, verificación, datos brutos) y `pf-02-openf1` (18 ficheros: telemetría, degradación, datos brutos). 34 ficheros, 2,86 MB.
- **Catálogo del portal**: 22 proyectos (`P01`–`P22`) y 8 laboratorios (`L01`–`L08`) con nivel, rutas y dataset asignado, leídos de `web/datos/busqueda.js` y `web/datos/portal.js`.

### 1.6 Documentación

`docs/` tiene 174 ficheros: 16 en la raíz (6 documentos y 8 capturas), **122 en `docs/entregas/`** (informes de entrega de sesiones anteriores), **23 en `docs/integracion/`** (investigación: NotebookLM, proyectos, fuentes, plan, trazabilidad, cobertura, certificaciones, proyectos del mundo, APIs gratuitas, F1, leer código y 3 anexos) y **13 en `docs/data-school-import/`** (el origen 2, que vive dentro del portal). Además, 21 ficheros en `especificaciones/`.

## 2. Importación de Data School — `docs/data-school-import`

**13 ficheros, 0,07 MB.** Es el material que se importó a Data School y que ya está copiado en esta carpeta (mismos hashes que `designs/`, `tools/`, `FUENTES.md`…).

| Fichero | Bytes |
|---|---:|
| `FUENTES.md` | 16.282 |
| `INVESTIGACION.md` | 9.507 |
| `ESPECIFICACION.md` | 7.323 |
| `BACKLOG.md` | 7.058 |
| `DECISIONES.md` | 4.090 |
| `README.md` | 1.899 |
| `designs/` (5 ficheros: `tokens.json` 8.581, `README.md` 5.730, `preview.html` 3.128, `design-system.json` 595, `.gitignore` 198) | 18.232 |
| `tools/` (2 ficheros: `check-links.mjs` 10.182, `check-links.test.mjs` 3.681) | 13.863 |

### 2.1 Las 32 fuentes, medidas

Del propio `FUENTES.md` (comprobadas el 2026-11-04): **32 filas = 31 vivas + 1 muerta** (Papers with Code, redirige a Hugging Face Papers y queda fuera del catálogo).

Clasificación por licencia, contada fila a fila:

| Clase | Cuántas | Cuáles |
|---|---:|---|
| **Solo enlace + resumen propio** (no se puede copiar su contenido) | **15** | roadmap.sh, DataTalksClub, Kaggle Learn, dbt Learn, Google Skills, Coursera, edX, DeepLearning.AI, fast.ai, YouTube, docs de dbt, Python Data Science Handbook, ISLR, Mathematics for Machine Learning, IMDb |
| **Licencia por ítem** (hay que comprobar cada recurso) | **7** | Kaggle Datasets, Hugging Face Datasets, data.gov, datos.gob.es, UCI ML Repository, arXiv, Hugging Face Papers |
| **Reutilizable con atribución** | **9** | MIT OCW, freeCodeCamp (solo su código BSD-3; el currículo no), Docs de Python, Docs de PostgreSQL, Docs de SQLite, Docs de Spark, Docs de Airflow, Docs de DuckDB, Dive into Deep Learning |
| **Muerta** | **1** | Papers with Code |
| **Total** | **32** | |

**Discrepancia corregida:** `FUENTES.md` dice en su recuento «11 fuentes con licencia restrictiva o sin licencia explícita», pero la lista que acompaña enumera **14**. Medida fila a fila con el criterio «no se puede copiar su contenido», la clase *solo enlace* son **15** (las 14 enumeradas más Google Skills). El número correcto es **15**; queda anotado en `DECISIONES.md` y corregido en `fuentes/README.md`.

### 2.2 Comprobador de enlaces

Ejecutado sobre el catálogo ya ordenado (`fuentes/FUENTES.md`, `fuentes/POR-TRAMO.md` e
`investigacion/INVESTIGACION.md`): `INFORMES/enlaces-2026-11-04.md` — **82 enlaces comprobados:
79 vivos, 3 redirigen** (`datos.gob.es` → `/es/`, `paperswithcode.com` → `huggingface.co/papers/trending`
y `mode.com/sql-tutorial` → `thoughtspot.com/sql-tutorial`), **0 caídos, 0 bloqueados, 0 errores**.
La comprobación anterior del origen dio 60 enlaces (58 vivos, 2 redirigen); esta cubre además el
nuevo `POR-TRAMO.md`. Se vuelve a ejecutar con `npm run check:links`.

## 3. Archivo de Orca — `equipo-ia`

**4.833 ficheros, 138,62 MB.** Es una foto anterior del mismo portal. Comparado fichero a fichero con la viva (por nombre **y** por SHA-256):

| Métrica | Viva | Orca | Diferencia |
|---|---:|---:|---|
| Conceptos `.md` | 459 | 438 | **+21 en la viva** |
| Fases | 13 | 13 | 0 |
| CSV de portal | 10 | 6 | **+4 en la viva** |
| CSV de proyectos | 3 | 0 | +3 en la viva |
| Scripts de figura `.py` | 350 | 350 | 0 |
| SVG servidos | 370 | 369 | +1 en la viva (`_probe_escalado.svg`) |
| Recursos | 370 | 370 | 0 |
| Proyectos en el catálogo | 22 | 10 | **+12 en la viva** |
| Labs en el catálogo | 8 | 8 | 0 |
| Evidencias de ejecución (`.txt`) | 946 | **0** | la viva sí tiene salidas |
| Ficheros de verificación | 1.893 | 947 | +946 en la viva |
| Documentación (`docs/`) | 174 | 302 | **168 exclusivos de Orca** |

### 3.1 Qué hay dentro de Orca que no esté en la viva

- **Contenido: nada.** Los 438 conceptos de Orca son **idénticos** a 438 de la viva (0 distintos, 0 solo-en-Orca); los 6 CSV son idénticos (6/6); los 350 scripts de figura, idénticos (350/350); los 370 recursos, idénticos (370/370).
- **Sí hay material exclusivo, pero no es contenido de datos e IA:**
  - `docs/diseno/` — **168 ficheros, 16,08 MB**: registro del rediseño del portal Muestra (`REDISENO.json` 67.349 B, `REDISENO.base.json` 14.438 B, `.rediseno-aplicado`, 3 `.diff` de origen, 3 recorridos JSON, 3 manifiestos y **156 capturas PNG = 15,9 MB**).
  - `actividades.js` (8.774 B), módulo del portal que la viva no tiene, presente en `web/assets/` y en `sitio/`.
- La viva añade además 4 CSV, 1 SVG de sonda y 21 conceptos, y tiene las **946 salidas de ejecución** que a Orca le faltan.

### 3.2 Consecuencia

El archivo de Orca **no aporta ningún concepto, dataset ni figura que no esté ya en la viva**. Aporta el registro de decisión del rediseño del portal (material de diseño, no de datos) y un módulo JS del portal. Ver la decisión en `CONSOLIDACION.md`.

## 4. Vista previa de Orca — `preview-data`

**4 ficheros, 1,20 MB.** No es una copia del portal de datos:

| Fichero | Bytes | Qué es |
|---|---:|---|
| `opofuente/opofuente.sqlite3` | 1.220.608 | Base SQLite del servicio **opofuente** (vista previa de una app de oposiciones) |
| `opofuente/opofuente.sqlite3-shm` | 32.768 | Memoria compartida de SQLite |
| `opofuente/opofuente.sqlite3-wal` | 0 | WAL vacío |
| `opofuente/logs/opofuente.log` | 2.190 | Arranques del servicio: 2026-10-31 y 2026-11-01, host 127.0.0.1:8766, `plataforma=apagada` |

Lectura de la base con SQLite en modo solo lectura:

- **76 tablas**.
- **0 filas de contenido**: todas las tablas de datos están a 0. Solo hay 3 filas en `app_metadata` (`schema_initialized_at` = 2026-10-31T21:49:57Z, `instance_id`, `schema_origin` = `S00`), 1 en `alembic_version` (`0048_motivo_de_borrador`) y las tablas internas de FTS (config 1, data 2).
- No hay conceptos, datasets, figuras ni material de datos e IA.

**Aportación a esta carpeta: 0.** Se documenta para que no se confunda con una copia del portal.

## 5. Esta carpeta — `F:\Proyectos\data-school` (estado antes de la consolidación)

**18 ficheros versionados** (25 en disco sin contar `.git`), 0,20 MB, rama `main`, 3 commits. Cinco carpetas **vacías** (`fuentes/`, `conceptos/`, `proyectos/`, `datasets/`, `investigacion/`). Lo que ya había:

- 8 documentos: `AGENTE.md`, `README.md`, `ESPECIFICACION.md`, `ESTADO-AGENTE.md`, `BACKLOG.md`, `DECISIONES.md`, `FUENTES.md`, `INVESTIGACION.md`.
- `designs/data-school/` — sistema de diseño con `tokens.json`, `design-system.json`, README y una preview de componente.
- `tools/check-links.mjs` (10.182 B) + `tools/check-links.test.mjs` (3.681 B), sin dependencias.
- `INFORMES/enlaces-2026-11-04.md` (60 enlaces: 58 vivos, 2 redirigen, 0 caídos).
- `package.json` sin dependencias, `.gitignore`.

**Aportación:** la estructura, el catálogo de 32 fuentes ya verificado, el sistema de diseño, el comprobador de enlaces con sus pruebas y la especificación de producto.

## 6. El dato de coordinación: confirmado o desmentido

La coordinación decía: *«la versión viva va por delante del archivo de Orca (fases más grandes) y los 6 CSV de Orca ya están en la viva»*.

| Afirmación | Veredicto | Números |
|---|---|---|
| La viva va por delante | **CONFIRMADO** | 459 conceptos vs 438 (**+21**); 22 proyectos vs 10 (+12); 946 salidas de ejecución vs 0; 10 CSV de portal vs 6; 1.893 ficheros de verificación vs 947. |
| «Fases más grandes» | **CONFIRMADO, con matiz** | Crecen 6 de 13 fases: f00 +3, f01 +2, f03 +1, f04 +7, f09 +7, f12 +1. Las otras 7 (f02, f05, f06, f07, f08, f10, f11) están **iguales**. Ninguna fase de la viva es más pequeña. |
| Los 6 CSV de Orca ya están en la viva | **CONFIRMADO** | 6 de 6 con SHA-256 idéntico. La viva añade 4 CSV de portal (`cartera-acciones`, `f1-clasificacion`, `futbol-partidos`, `telemetria-f1`) y 3 de proyectos. |
| (implícito) Orca aporta contenido propio | **DESMENTIDO** | 438/438 conceptos idénticos, 350/350 figuras idénticas, 370/370 recursos idénticos, 0 conceptos solo-en-Orca. Lo único exclusivo es el registro de diseño del portal (168 ficheros, 16,08 MB) y `actividades.js` (8.774 B). |

**Conclusión:** el archivo de Orca es una foto anterior del mismo trabajo; no se pierde nada al no importarlo como contenido. Lo que sí se trae de Orca es el registro de decisión de su rediseño, y solo eso (ver `CONSOLIDACION.md`).
