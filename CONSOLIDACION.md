# Consolidación — qué se trae, de dónde y qué se descarta

Fecha: **2026-11-04**. Esta sesión consolida en `F:\Proyectos\data-school` el material de datos e IA de los cinco orígenes medidos en `INVENTARIO.md`.

## La regla que manda

1. **Los cinco orígenes son de solo lectura.** No se ha escrito nada en `F:\Proyectos\ProyectoServidor\aprender` ni en el archivo de Orca. Se lee y se trae aquí.
2. **Se enlaza y se resume, no se copia.** El material de terceros (temarios, PDFs, vídeos, figuras ajenas) no entra: 15 de las 32 fuentes del catálogo solo admiten enlace + resumen propio (la cifra «11» del documento anterior era errónea; ver `INVENTARIO.md` §2.1). Lo que sí se copia es **material propio del proyecto**: conceptos, figuras, datasets sintéticos.
3. **La viva es la fuente de verdad del contenido.** No hay dos versiones que elegir: la viva contiene el 100 % del contenido de Orca —438/438 conceptos, 350/350 figuras y 370/370 recursos con hash idéntico— y 21 conceptos, 12 proyectos y 4 CSV más. Orca es una foto anterior.
4. **Todo concepto lleva código ejecutado** y todo dataset lleva licencia y procedencia. No entra nada sin esas dos condiciones.

## Qué se trae

| # | Qué | De dónde | Destino | Volumen | Por qué |
|---|---|---|---|---:|---|
| 1 | **459 conceptos** en 13 fases (f00–f12) | Portal vivo `contenido/` | `conceptos/f00..f12/` | 459 `.md`, 7,11 MB | Es el núcleo del producto. La viva es superconjunto exacto de Orca (438 iguales + 21 nuevos) y los 459/459 llevan código. |
| 2 | **Figuras renderizadas** | Portal vivo `web/figuras/*.svg` | `conceptos/figuras/` | 370 SVG, 20,58 MB | Las referencian 349 bloques `:::figura`; sin ellas los conceptos quedan ciegos. Son material propio generado. |
| 3 | **Fuentes de las figuras** | Portal vivo `figuras/*.py` | `conceptos/figuras-fuente/` | 350 `.py`, 1,25 MB | Permiten regenerar cada SVG y auditar qué se dibuja. |
| 4 | **Evidencia de ejecución** | Portal vivo `.verificacion/` + ejecución propia de los 16 huecos | `conceptos/verificacion/` | 1.925 ficheros (929 `.py`, 33 `.sql`, 962 salidas `.txt`), ~1,15 MB | Es la prueba de que el código de los conceptos se ejecutó. La evidencia del portal cubría 438 conceptos y estaba desfasada; los 16 conceptos nuevos con `python verificable` se ejecutaron aquí (0 fallos). Orca no tiene las salidas. |
| 5 | **Catálogo de fuentes** | Origen 2 (`data-school-import/FUENTES.md`, ya en esta carpeta) | `fuentes/FUENTES.md` | 32 fuentes, 16.282 B | 31 vivas + 1 muerta, con licencia, coste, idioma y estado comprobados. |
| 6 | **Catálogo por tramos** | Elaboración propia sobre `FUENTES.md` | `fuentes/POR-TRAMO.md` | 4 tramos × (1 principal + 2 alternativas) | Cierra la tarea 7 del backlog: el catálogo pasa de lista a decisión. |
| 7 | **10 datasets sintéticos + metadatos + generador** | Portal vivo `web/datos/datasets/`, `datasets.json` y `datos/generar-datasets.mjs` | `datasets/csv/`, `datasets/datasets.json`, `datasets/generar-datasets.mjs` | 10 CSV (89 KB) + metadata + generador | Licencia **CC0-1.0**, origen sintético y checksum SHA-256 por conjunto: licencia y procedencia cumplidas. |
| 8 | **2 proyectos completos** | Portal vivo `proyectos/pf-01-pulso-poblacion` y `pf-02-openf1` | `proyectos/` | 34 ficheros; se excluyen caché, `.duckdb` y `.log` | Son los dos únicos proyectos con código, datos brutos, verificación y criterio de terminado reales. |
| 9 | **Catálogo de 22 proyectos y 8 laboratorios** | Portal vivo `web/datos/busqueda.js` + `portal.js` | `proyectos/CATALOGO.md` | 22 proyectos (P01–P22) + 8 labs (L01–L08) | Da el mapa completo de práctica; cada proyecto con nivel, rutas y dataset asignado. |
| 10 | **Investigación de producto** | Origen 2 (`INVESTIGACION.md`) | `investigacion/INVESTIGACION.md` | 60 líneas | Cómo presentan su catálogo seis plataformas y qué se adopta. |
| 11 | **Investigación del portal** | Portal vivo `docs/integracion/` | `investigacion/integracion/` | 23 ficheros (15 `.md` + 8 capturas), 1,32 MB | NotebookLM, proyectos del mundo, APIs gratuitas, certificaciones, trazabilidad, cobertura y anexos de fuentes. |
| 12 | **Registro del rediseño del portal (solo Orca)** | Archivo de Orca `docs/diseno/` (10 ficheros) | `investigacion/rediseno-muestra-orca/` | ~90 KB | Es lo único exclusivo de Orca que no es contenido de datos; las 156 capturas (15,9 MB) se quedan fuera. |
| 13 | **Comprobador de enlaces y medición** | Origen 2 + elaboración propia | `tools/` | `check-links.mjs`, su test y `medir-origenes.ps1` | Verificable: cualquier cifra de `INVENTARIO.md` se puede reproducir. |

## Qué se descarta y por qué

| Qué | De dónde | Por qué se descarta |
|---|---|---|
| `node_modules/` (182 ficheros) | Portal vivo | Dependencias instaladas; no es material de contenido. |
| `figuras/__pycache__/` (351 `.pyc`) | Portal vivo | Caché de bytecode, no fuente. |
| La aplicación web completa (`web/`: 441 ficheros, incluido `todo.html` de 9,8 MB, `assets/`, `datos/*.js`, `index.html`) | Portal vivo | Es el producto **Muestra**, no contenido. Aquí solo se trae su contenido: los datasets, el catálogo de proyectos y las figuras. Tocar el portal es de la otra sesión. |
| `sitio/`, `plataforma/`, `android/`, `ios/` | Portal vivo | Código y datos operativos del portal; `plataforma/` incluye bases (`academia.db`, `analitica.db`, `cobro.db`), `clave-ip` y `legal/titular.json`. No es contenido y no debe viajar a un repositorio de contenido. |
| `docs/` raíz (bundles JS del sitio + capturas), `docs/entregas/` (122 ficheros), `especificaciones/` (21 ficheros de producto v2) | Portal vivo | Son artefactos de construcción del portal y evidencia de sesiones anteriores; no son material de datos e IA. La investigación sí se trae (`docs/integracion/`). |
| Carpetas de trabajo `_plan*`, `_olor/`, `_mirar/`, `_revision/`, `_rev_tmp/`, `_verify_out/`, `_determinismo/`, `_fixture/`, `.capturas-t16/`, `.github/` | Portal vivo | Andamiaje de sesiones y CI (y aquí no se usa GitHub Actions). |
| 156 capturas PNG del rediseño (15,9 MB) | Orca | Son capturas de interfaz del portal, no contenido; el archivo es de solo lectura y las decisiones de diseño ya están en el registro importado. |
| `actividades.js` (8.774 B, en `web/assets/` y `sitio/`) | Orca | Módulo JS del portal que la viva no tiene; es código de producto, no contenido. Se anota para la otra sesión (ver abajo), no se copia. |
| Base SQLite y log de `opofuente` | `preview-data` | **0 filas de contenido** en 76 tablas; no es el portal de datos. Nada que traer. |
| Material de las 15 fuentes «solo enlace» (temarios, PDFs, vídeos, figuras) | Origen 2 / internet | Sus licencias prohíben copiar; se enlazan y se resumen con palabras propias, nunca se copia el contenido. |
| Datasets externos (Kaggle, Hugging Face, data.gov, datos.gob.es, UCI, IMDb) | Origen 2 | Se enlazan; cada uno tiene su licencia y no se aloja. Solo entran los 10 sintéticos propios (CC0). |

### Anexo A — Descartes con rutas y tamaños (medido el 2026-11-04)

Para que «se descarta» no sea una palabra vacía, esto es lo que se queda fuera y cuánto pesa. Los
tamaños son del origen, no de esta carpeta; ninguno se ha copiado.

| Material descartado | Origen | Ficheros | Tamaño | Motivo |
|---|---|---:|---:|---|
| `.git/` | portal vivo | 740 | 61,07 MB | Historial del repositorio del portal; viaja con su proyecto, no con el catálogo. |
| `_revision/` | portal vivo | 471 | 56,56 MB | Revisiones y capturas de sesiones anteriores; no es contenido. |
| `web/` (app Muestra: `index.html`, `todo.html`, `assets/`, bundles `datos/*.js`) | portal vivo | 441 | 44,62 MB | Es el producto **Muestra**; de `web/` solo se importan las figuras (20,58 MB) y los datasets (0,09 MB). |
| `_mirar/` | portal vivo | 152 | 24,33 MB | Material de revisión visual de sesiones; no es contenido. |
| `node_modules/` | portal vivo | 182 | 17,83 MB | Dependencias instaladas. |
| `_olor/` | portal vivo | 575 | 12,39 MB | Pruebas de estilo y detección de texto generado; andamiaje. |
| `docs/` raíz (bundles del sitio y capturas) | portal vivo | 16 | ~1,3 MB | Artefactos de construcción y capturas; de `docs/` solo se importa `integracion/` (23 ficheros). |
| `docs/entregas/` | portal vivo | 122 | 5,19 MB | Evidencia de entregas de sesiones anteriores del portal. |
| `sitio/` | portal vivo | 32 | 0,97 MB | Código de la web. |
| `plataforma/` | portal vivo | 38 | 3,34 MB | Backend del portal, con bases (`academia.db`, `analitica.db`, `cobro.db`), `clave-ip` y `legal/titular.json`: datos operativos que no deben viajar. |
| `android/` + `ios/` | portal vivo | 18 | 0,06 MB | Apps del portal. |
| `especificaciones/` | portal vivo | 21 | 0,45 MB | Especificación del producto v2 (Muestra), no del catálogo de contenido. |
| `figuras/__pycache__/` | portal vivo | 351 | 1,76 MB | Caché de bytecode (`.pyc`), no fuente. |
| `_plan/`, `_plan2/`, `_plan3/`, `_plan4/` | portal vivo | 172 | 0,33 MB | Planes de trabajo de sesiones anteriores. |
| `_verify_out/`, `_rev_tmp/`, `_verif_tmp/` | portal vivo | 225 | 0,30 MB | Salidas temporales de verificación. |
| `_determinismo/`, `_fixture/` | portal vivo | 7 | 0,42 MB | Utilidades de prueba. |
| `.capturas-t16/` | portal vivo | 12 | 1,86 MB | Capturas de una tanda concreta. |
| `.github/` | portal vivo | 1 | 0,00 MB | CI del portal; aquí no se usa GitHub Actions. |
| `docs/diseno/capturas/` (156 PNG del rediseño) | archivo de Orca | 156 | 15,88 MB | Capturas de interfaz del portal Muestra; el registro de decisión sí se importa (10 ficheros, ~90 KB). |
| `actividades.js` (en `web/assets/` y `sitio/`) | archivo de Orca | 2 | 0,02 MB | Módulo JS del portal que la viva no tiene; es producto, no contenido. Anotado para la otra sesión. |
| Base SQLite y log de `opofuente` | `preview-data` | 4 | 1,20 MB | 76 tablas y **0 filas de contenido**; no es el portal de datos. |

Comprobación: el origen del portal suma 271,41 MB; estos descartes explican los 171,2 MB que no
viajan, más el historial de `.git` (61,07 MB) y lo que sí se importó (~34 MB de contenido).

### Anexo B — Se queda en el origen, pero documentado aquí

- **21 SVG sin bloque `:::figura`** y **3 módulos `.py` que no son figuras** (`comun.py`,
  `_medir.py`, `_tanteo.py`) del portal: se conservan en `conceptos/figuras/` y
  `conceptos/figuras-fuente/` como material de apoyo, explicados en `conceptos/figuras/LEEME.md`.
  No se borran: son fuente de variantes y utilidades compartidas, y su coste es pequeño.
- **Fichas de proyecto:** 4 fichas que cubren los **12 proyectos** de los 4 CSV nuevos (P11–P22).
  Quedan pendientes las **10 fichas de P01–P10** (el encargo hablaba de 18, pero la cuenta real es
  10: las 4 fichas agrupan 12 proyectos). No se descartan: están en `BACKLOG.md`.
- **Contenido del portal que no se duplica:** los conceptos, figuras y datasets existen en el
  portal y en esta carpeta con hash idéntico; la copia canónica es esta y el portal es quien publica.

## Notas para la otra sesión (portal Muestra) — **no se toca el portal**

La consolidación no requiere ningún cambio en el portal. Observaciones medidas que la otra sesión puede revisar cuando quiera:

1. **El contenido de la viva está completo y por delante de Orca:** 459 conceptos (portal.js `total: 459`, suma por fases = 459), 10 CSV de portal, 3 CSV de proyectos, 22 proyectos y 8 laboratorios. Nada que reponer desde Orca.
2. **Posible pérdida en la viva:** el archivo de Orca tiene `actividades.js` (8.774 B) en `web/assets/` y en `sitio/`, y la viva **no** lo tiene. Si el módulo de actividades sigue en uso en el portal, revisar si se retiró a propósito. No se ha tocado nada.
3. **Cifra de fuentes:** `FUENTES.md` (y su copia en `aprender/docs/data-school-import/`) dice «11 fuentes» pero enumera 14; la medición da **15**. Aquí se corrige en `fuentes/README.md`; si el portal lee ese número, actualizarlo allí (nivel 2 de la otra sesión).
4. **Duplicación deliberada:** `docs/data-school-import/` del portal y esta carpeta comparten los mismos ficheros (hash idéntico). La copia canónica pasa a ser la de esta carpeta; la del portal es histórica.
5. **Última entrega del portal:** `docs/entregas/RECORRIDO-UNICO-2026-11-04/` (4 ficheros) no se importa; es evidencia del trabajo del portal.
6. **La verificación del portal está desfasada:** `.verificacion/` cubre 438 de los 459 conceptos. Hay **16 conceptos con bloque `python verificable` sin script ni salida** (`cadenas-de-markov`, `correccion-point-in-time`, `ecuaciones-diferenciales-estocasticas`, `enmascarado-y-retencion`, `eventos-push-y-webhooks`, `expansion-karhunen-loeve`, `flink-y-procesamiento-de-eventos`, `griegas-y-cobertura`, `indicadores-tecnicos`, `lema-de-ito`, `medir-tu-progreso`, `movimiento-browniano`, `problema-de-ficheros-pequenos`, `registro-de-esquemas`, `valoracion-de-opciones`, `volatility-drag`) y 5 sin código ejecutable (`fuentes-y-canales`, `rutas-de-aprendizaje`, `terminal-y-shell`, `iam-y-permisos-cloud`, `certificaciones-de-datos`). Aquí se ejecutaron los 16 y se guardó su salida; **en el portal conviene volver a lanzar `generar.mjs --ejemplos` + `verificar-ejemplos.ps1`** para que su `.verificacion` y su `manifiesto.json` queden al día. No se ha tocado el portal.
7. **`ventas-mensuales` no es un panel tienda × día:** el CSV tiene una fila por día con la tienda rotando (cada tienda 60 días alternos), así que no se pueden comparar tiendas del mismo día. Si el portal lo describe como panel, la descripción hay que corregirla allí; aquí queda advertido en `datasets/FICHAS.md` y `datasets/VERIFICACION.md`.
8. **Figuras duplicadas por tilde:** 20 de los 370 SVG son variantes con tilde de una figura ya referenciada (el script guarda con el nombre acentuado y el bloque `:::figura` enlaza el no acentuado). Se conservan y se explican en `conceptos/figuras/LEEME.md`; en el portal se podría dejar una sola variante por figura si se quiere ahorrar peso.

## Decisiones tomadas en esta consolidación (nivel 2)

Están desarrolladas en `DECISIONES.md` con sus IDs:

- **D-010** — La carpeta se organiza en `fuentes/`, `conceptos/`, `proyectos/`, `datasets/` e `investigacion/`; los documentos de producto se quedan en la raíz. Motivo: la ficha del agente ya define esa estructura.
- **D-011** — Se importan los 459 conceptos de la viva, no los 438 de Orca. Motivo: superconjunto verificado por hash (+21), y los 459 llevan código.
- **D-012** — Se versionan las 370 figuras SVG (20,58 MB) además de sus 350 fuentes. Motivo: 349 referencias `:::figura`; sin SVG el archivo queda ciego. Reversible (`git rm`).
- **D-013** — Se importa la evidencia de ejecución completa (1.893 ficheros). Motivo: es la prueba de «código ejecutado, no de ejemplo».
- **D-014** — Los 10 datasets sintéticos se alojan (CC0-1.0); los externos se enlazan. Motivo: licencia y procedencia verificables; los ajenos no se copian.
- **D-015** — De Orca se trae solo el registro de decisión del rediseño (10 ficheros, ~90 KB), no las 156 capturas. Motivo: es lo único exclusivo y no es contenido de datos.
- **D-016** — Se corrige de 11 a 15 el número de fuentes que solo admiten enlace. Motivo: conteo fila a fila; el propio documento enumeraba 14.
- **D-017** — Una fuente «solo enlace» **puede** ser principal de un tramo; la licencia decide qué se puede copiar, no qué se puede recomendar. Motivo: el producto enlaza; el criterio antiguo («ninguna restringida como principal») confundía recomendación con copia.
- **D-018** — `preview-data` no aporta nada (0 filas de contenido) y no se importa. Motivo: medido.
- **D-019** — Se ejecutan los 16 bloques de código que el verificador del portal no cubría y se guarda su salida. Motivo: la evidencia del portal cubría 438 de 459.
- **D-020** — Comprobación de enlaces periódica en local: puerta (`comprobar-enlaces.ps1`) y tarea semanal opcional (`programar-enlaces.ps1`), sin GitHub Actions.
- **D-021** — Plantilla de resumen obligatoria para altas, con 10 fuentes reescritas como muestra.
- **D-022** — Ficha homogénea y verificación ejecutada de los 10 datasets (`data_profile`), sin tocar el manifiesto del portal.
- **D-023** — 4 fichas de proyecto para los CSV nuevos (cubren P11–P22); las 10 fichas de P01–P10 quedan en backlog.
- **D-024** — Se conservan y documentan los 21 SVG sin `:::figura` y los 3 módulos de apoyo; criterio de uso = tener bloque `:::figura`.
- **D-025** — El orden de lectura por fase es una recomendación derivada de los `prerequisitos`, no una regla.

### Bloque de mejora cerrado en esta sesión (backlog)

- **Comprobador periódico:** `tools/comprobar-enlaces.ps1` (sale 1 si hay caídos) y
  `tools/programar-enlaces.ps1` (registra la tarea semanal; no se ejecuta aquí porque cambia el
  sistema). Sin GitHub Actions.
- **Plantilla de fuentes:** `fuentes/PLANTILLA-RESUMEN.md` + `fuentes/RESUMENES-EJEMPLO.md` con 10
  fuentes reescritas con sus campos y su puerta.
- **Fichas de datasets:** `datasets/FICHAS.md` (10 fichas homogéneas) y `datasets/VERIFICACION.md`
  con `data_profile` real; comprobador reproducible `datasets/_verificar-fichas.ps1` (85 criterios,
  verde). Medido: 10/10 cargan, 63/63 columnas y tipos, 0 nulos, 0 duplicados.
- **Fichas de proyecto:** `proyectos/fichas/` con 4 fichas que cubren los 12 proyectos de los 4 CSV
  nuevos (P11–P22), con criterios de terminado y rúbrica.
- **Orden de lectura:** `conceptos/INDICE-LECTURA.md` (459 filas, 0 ciclos) y
  `conceptos/figuras/LEEME.md` (349 figuras en uso, 21 variantes/sonda, 3 módulos de apoyo).

## Dudas de nivel 3 (anotadas, no decididas aquí)

1. **Sincronización archivo ↔ portal.** ¿El portal (Muestra) consume esta carpeta como fuente, o se sigue copiando a mano? Es una decisión de producto y de flujo entre dos proyectos; afecta a la otra sesión. Anotada en `DECISIONES.md`.
2. **Publicación del catálogo.** ¿Esta carpeta se publica tal cual (conceptos completos) o el portal es el único que publica? Toca alcance, no contenido. Anotada.
3. **Las 4 decisiones de producto abiertas de `ESPECIFICACION.md`** (progreso, apuntes, datasets enlazados o locales, catálogo público o privado) siguen abiertas; la primera (un tronco y tres salidas) ya la cerró David el 2026-11-04. El archivo las resuelve **solo para sí mismo** (datasets propios locales; contenido público/privado no aplica a un repositorio). No se cierran desde aquí.

## Resultado y verificación (cierre de la sesión 2)

Resultado medido al cerrar (sin contar `.git`): **3.235 ficheros, 33,84 MB**.

| Puerta | Comprobación | Resultado |
|---|---|---|
| Contenido | 459 `.md` en `conceptos/f00`…`f12`, idénticos byte a byte al origen | **459/459**, 0 distintos |
| Código ejecutado | 454 de 459 conceptos con script y salida (los otros 5 no tienen bloque ejecutable) | 929 `.py` + 33 `.sql` + 962 salidas = **1.925 ficheros**, 16 ejecutados aquí, **0 fallos** |
| Figuras | Las 349 referencias `:::figura` resuelven a un SVG | **349/349**, 0 ausencias |
| Índices | Filas de `conceptos/INDICE.md` y de `conceptos/INDICE-LECTURA.md` | **459 y 459**, 0 ciclos topológicos |
| Datasets | `data_profile` de los 10 CSV + `datasets/_verificar-fichas.ps1` | **10/10 cargan**, 63/63 columnas y tipos, 0 nulos, 0 duplicados, **85/85 criterios** |
| Proyectos | 2 completos + catálogo + 4 fichas | **22 proyectos + 8 laboratorios**, 12 con ficha |
| Fuentes | Catálogo + plantilla + resúmenes de ejemplo | **32 fuentes**, 15 solo enlace, 10 reescritas |
| Enlaces | `npm run check:links` sobre `FUENTES.md`, `POR-TRAMO.md` e `INVESTIGACION.md` | **82 comprobados: 79 vivos, 3 redirigen, 0 caídos, 0 bloqueados** |
| Pruebas | `npm test` + puerta de enlaces | **8/8 en verde** y puerta en 0 caídos |
| Orígenes | Sin escrituras en el portal ni en el archivo de Orca | **solo lectura** |

- Sin GitHub Actions: todo se ejecuta en local. Commit local y push al final de la sesión.
- El detalle de la medición previa está en `INFORMES/medicion-origenes-2026-11-04.txt`; el informe
  de enlaces, en `INFORMES/enlaces-2026-11-04.md`.
